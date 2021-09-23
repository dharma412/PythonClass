*** Settings ***
Suite Setup        Initialize Suite
Suite Teardown     Finalize Suite
Test Setup         General Test Case Setup
Resource           regression.txt
Resource           sma/esasma.txt

*** Variables ***
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${DATA_UPDATE_TIMEOUT}  20m
${RETRY_TIME}        30s
${expected_count}  15000

*** Keywords ***

Initialize Suite
    DefaultRegressionSuiteSetup
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Smtp Routes New  domain=ALL  dest_hosts=/dev/null
      Commit
      Selenium Login
      Message Tracking Enable  tracking=centralized
      Centralized Email Reporting Enable
      Commit Changes
    END
    Library Order SMA
    Selenium Login
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    Commit Changes

Clear Email Tracking Reporting Data
    Library Order ESA
    Start Cli Session If Not Open
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready
    Library Order Sma
    Start Cli Session If Not Open
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    FOR  ${index}  IN RANGE  20
      Inject Messages  inject-host=${inject-host}  num-msgs=500
      ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
      ...  mbox-filename=${MAIL_MBOX}  max-msgs-per-conn=1
      Sleep  10s
    END

Get Expected Mail Count
    [Arguments]   ${table}=DLP Incident Details  ${column}=Messages  ${col_index}=0   ${count}=${expected_count}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  ${table}
    Log  ${reporting_data}
    @{col_values} =  Get From Dictionary  ${reporting_data}  ${column}
    ${mail_value} =  Get From List  ${col_values}  ${col_index}
    ${mail_value} =  Replace String  ${mail_value}  .  ${EMPTY}
    ${mail_value} =  Replace String  ${mail_value}  k  00
    Run Keyword If  ${mail_value} < ${count}  Fail
    [Return]  ${mail_value}

Check Outbreak Message Count
    ${msg_count}=  Outbreak Messages Count
    Should Be Equal  ${msg_count}  0

Get Time
    [Arguments]  ${line}
    ${timestmp1}  ${day}  ${tmpstmp1}  ${tmpstmp2}  ${tmpstmp3}=
    ...  Should Match Regexp  ${line}  \\w{3}\\s+\\w{3}\\s+(\\d+)\\s+([0-9]+):([0-9]+):([0-9]+)
    ${tmpstmp1}=  Convert To Integer  ${tmpstmp1}
    ${tmpstmp2}=  Convert To Integer  ${tmpstmp2}
    ${tmpstmp3}=  Convert To Integer  ${tmpstmp3}
    ${time}=  Evaluate  ${tmpstmp1}*60*60+${tmpstmp2}*60+${tmpstmp3}
    [Return]  ${day}  ${time}

General Test Case Setup
    FOR  ${dut_type}  IN  @{appliances}
      Run Keyword  Library Order ${dut_type}
      DefaultTestCaseSetup
    END

Finalize Suite
    FOR  ${appliance}  IN  @{esa_appliances}
      Clear Email Tracking Reporting Data
      Library Order ${appliance}
      Run Keyword And Ignore Error  Log Out Of DUT
      Log Into DUT
      PVO Quarantines Disable
      Commit Changes
    END
    DefaultRegressionSuiteTeardown

***Test Cases***

CSCvp84172
    [Tags]  srts  teacat  CSCvp84172  CSCvp84162
    [Documentation]  To verify the PVO quarantine messages are release at optimum speed

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    PVO Quarantines Enable
    Commit Changes
    FOR  ${appliance}  IN  @{esa_appliances}
      Wait Until Keyword Succeeds  5m  1m  Security Appliances Add Email Appliance
      ...  ${${appliance}}
      ...  ${${appliance}_IP}
      ...  tracking=${True}
      ...  reporting=${True}
      ...  pvo=${true}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    END
    Commit Changes
    Library Order ESA
    Start Cli Session If Not Open
    Policyconfig Edit Antispam Disable  Incoming  DEFAULT
    Commit
    Library Order SMA
    Selenium Login
    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Wait Until Keyword Succeeds  5m  1m  Pvo Quarantines Enable
      Run Keyword And Ignore Error  Commit Changes
    END
    Clear Email Tracking Reporting Data
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${settings}=  Create Dictionary
      ...  Outbreak Filters  Enable Outbreak Filtering (Customize settings)
      ...  Enable Message Modification  ${True}
      Mail Policies Edit Outbreak Filters  incoming  default  ${settings}
      Commit Changes
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  outbreak/vof-phishurl.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  outbreak/vof_multi_phishurl.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    ${mail_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Threat Details  column=Total Messages  col_index=0  count=${expected_count}
    Log  ${mail_count}
    ${msg_count}=  Outbreak Messages Count
    Should Be True  ${msg_count}>15000
    FOR  ${esa}  IN  @{esa_appliances}
      ${settings}=  Create Dictionary
      ...  Outbreak Filters  Enable Outbreak Filtering (Customize settings)
      ...  Quarantine Threat Level  5
      Library Order ESA
      Run Keyword And Ignore Error  Log Out Of DUT
      Log Into DUT
      Mail Policies Edit Outbreak Filters  incoming  default  ${settings}
      Commit Changes
      Start Cli Session If Not Open
      Update Config Dynamichost  dynamic_host=${STAGE_UPDATER}
      Update Config Validate Certificates  validate_certificates=no
      Commit
      Outbreak Flush  confirm=yes
      ${update_msg}=  Outbreak Filters Update Now
      Log  ${update_msg}
      ${status}=  Outbreak Status
      Log  ${status}
      Outbreak Update  force=yes
    END
    Library Order SMA
    Run Keyword And Ignore Error  Log Out Of DUT
    Log Into DUT
    Wait Until Keyword Succeeds  60m  1m
    ...  Check Outbreak Message Count
    Import Library  UtilsLibrary  ${SMA}  WITH NAME  UtilsLibrarySMA
    Start Cli Session If Not Open
    ${matches}  ${found}=  UtilsLibrarySMA.Log Search  .*MID .*released from quarantine.*Outbreak  search_path=mail  timeout= 60
    ${line}=  Get From List  ${found}  0
    ${start_day}  ${start_tm}=  Get Time  ${line}
    ${last_index}=  Evaluate  ${matches} - 1
    ${line}=  Get From List  ${found}  ${last_index}
    ${end_day}  ${end_tm}=  Get Time  ${line}
    ${diff_day}=  Evaluate  ${end_day} - ${start_day}
    ${end_tm}=  Evaluate  ${end_tm} + ${diff_day}*24*60*60
    ${mail_per_sec}=  Evaluate  ${matches}/(${end_tm}-${start_tm})
    Should Be True  ${mail_per_sec}>=1
