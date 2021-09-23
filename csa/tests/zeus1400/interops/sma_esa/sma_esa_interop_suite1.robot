# $Id: //prod/main/sarf_centos/tests/zeus1350/build_acceptance_tests/sma_esa_interop/sma_esa_interop_suite1.txt#2 $ $DateTime: 2020/02/27 21:23:41 $ $Author: vsugumar $

*** Settings ***
Resource     esa/injector.txt
Resource     regression.txt
Resource     sma/esasma.txt
Suite Setup  Run Keywords
...  Initialize Suite
Suite Teardown  DefaultRegressionSuiteTeardown

*** Variables ***
${DATA_UPDATE_TIMEOUT}=  30m
${RETRY_TIME}=  30s
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${TRACKERD_LOGS}  /data/pub/trackerd_logs/trackerd.current
${Message_Tracking}  //table[@class='cols']/tbody/tr/td[2]/div/a
${Message_Details}  //tbody[@id='resultTable']/tr/td[5]/a[contains(text(), 'Show Details')]
${expected_count}  4
${Tvh1165328c_DLP_POLICY} =   PCI-DSS (Payment Card Industry Data Security Standard)

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
    @{ESA_NAMES}=    Create List
    Library Order SMA
    Selenium Login
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    Commit Changes
    FOR  ${appliance}  IN  @{esa_appliances}
      Wait Until Keyword Succeeds  1m  10s
      ...  Security Appliances Add Email Appliance
      ...  ${appliance}
      ...  ${${appliance}_IP}
      ...  tracking=${True}
      ...  reporting=${True}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
      Commit Changes
      Append To List    ${ESA_NAMES}  ${appliance}
    END
    ${expected_count}=  Convert To Integer  ${expected_count}
    ${esa_cnt}=  Get Length  ${esa_appliances}
    ${expected_count}=  Evaluate    ${esa_cnt} * ${expected_count}
    Set Suite Variable  ${expected_count}
    Set Suite Variable  ${esa_cnt}
    Set Suite Variable  @{ESA_NAMES}


Clear Email Tracking Reporting Data
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Roll Over Now
      Commit
      Diagnostic Reporting Delete Db  confirm=yes
      Wait Until Ready
      Diagnostic Tracking Delete Db   confirm=yes
      Wait Until Ready
    END
    Library Order Sma
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready

General Test Case Setup
    FOR  ${dut_type}  IN  @{appliances}
      Run Keyword  Library Order ${dut_type}
      DefaultTestCaseSetup
    END
    Sync Appliances Datetime  ${SMA}  @{ESA_NAMES}

General Test Case Teardown
    FOR  ${dut_type}  IN  @{appliances}
      Run Keyword  Library Order ${dut_type}
      DefaultTestCaseTeardown
    END

Email Tracking Search and Return
    [Arguments]  ${mesg_received}=  ${start_date}=  ${start_time}=  ${end_date}=  ${end_time}=  ${message_event}=
    ...  ${sender_ip}=  ${exp_count}=
    ${messages}=  Email Message Tracking Search
    ...  mesg_received=${mesg_received}
    ...  start_date=${start_date}  start_time=${start_time}
    ...  end_date=${end_date}  end_time=${end_time}
    ...  message_event=${message_event}  sender_ip=${sender_ip}

    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Run Keyword If  ${tracking_message_count} != ${exp_count}  Fail
    [Return]  ${tracking_message_count}

Amp Email Count
    [Arguments]  ${mesg_count}=  ${col_value}=  ${table_param}=
    ${reporting_data}=  Email Report Table Get Data  Incoming Mail Summary  table_parameters=${table_param}
    @{col_values} =  Get From Dictionary  ${reporting_data}
    ...  Messages
    ${value} =  Get From List  ${col_values}  ${col_value}
    ${value} =  Convert To Integer  ${value}
    ${mesg_count}=  Convert To Integer  ${mesg_count}
    Log  values is received ${value}
    Log  values is Expected ${mesg_count}
    Run Keyword If  ${value} != ${mesg_count}  Fail
    [Return]  ${value}

Dlp Email Count
    [Arguments]  ${mail_count}=
    ${table_data}=  Email Report Table Get Data  DLP Incident Details
    Log  ${table_data}
    @{col_values} =  Get From Dictionary  ${table_data}
    ...  Medium
    @{total}=  Get From Dictionary  ${table_data}  Total
    ${value} =  Get From List  ${col_values}  0
    ${tot_value} =  Get From List  ${total}  0
    Run Keyword If  ${value} != ${mail_count} and ${tot_value} != ${mail_count}  Fail
    [Return]  ${tot_value}


Spam Quarntine Search
    [Arguments]  ${date_range}=today  ${recipient_cmp}=contains  ${recipient_value}=recipient@${CLIENT}  ${expected}=
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  date_range=${date_range}  recipient_cmp=${recipient_cmp}  recipient_value=${recipient_value}
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} != ${expected}  Fail
    [Return]  ${actual_spam_count}

Filter Message Tracking Log Check
    [Documentation]  This keyword checks trackerd log for correct entry.
    [Arguments]  ${baseline}  ${pattern}=.*FlashPla_exe.mbox.*  ${no_entry}=1  ${timeout}=60  ${log_count_check}=True
    ${trackerd_log}  ${trackerd_count}=  Filter Log  ${TRACKERD_LOGS}
    ...  baseline=${baseline}  timeout=${timeout}
    ...  match_patterns=-E '${pattern}'
    Log  ${trackerd_log}

    [Return]  ${trackerd_log}

Filter Message Tracking Log Create Baseline
  [Documentation]    Creates baseline for trackerd_log\n
  ${_baseline_trackerdlog}=    Filter Log Create Baseline    ${TRACKERD_LOGS}
  Set Test Variable    ${baseline_trackerdlog}    ${_baseline_trackerdlog}

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

Do Tvh1171788c Teardown
    Time Zone Edit  America  United States  Los_Angeles
    Commit Changes
    Email Archived Reports Delete All Reports
    Email Scheduled Reports Delete All Reports
    Commit Changes
    General Test Case Teardown

Do Tvh1165321c Setup
    General Test Case Setup
    Clear Email Tracking Reporting Data
    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/unscannable.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/FlashPla_exe.mbox  ${PUBLIC_LISTENER.ipv4}
    END

Get Archive Report
    ${reports}=  Email Archived Reports Get Reports
    Log  ${reports}
    ${length}=  Get Length  ${reports}
    Run Keyword If  ${length}==0  Fail
    [Return]  ${reports}

Add AMP Feature Key
     ${amp_file_rep_fkey}=  Generate DUT Feature Key  amp_file_rep
     ${amp_file_analysis_fkey}=  Generate DUT Feature Key  amp_file_analysis
     Start Cli Session If Not Open
     Feature Key Activate  ${amp_file_rep_fkey}
     Restart CLI Session
     Feature Key Activate  ${amp_file_analysis_fkey}
     Restart CLI Session


*** Test Cases ***

Tvh1173623c
    [Tags]  interop  Tvh1173623c
    [Documentation]  Add custom Email role and provide privileges in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1173623
    ...  1. Navigate to Management Appliance->System Administration-> User Roles
    ...  2. Click on "Add Email User Role"
    ...  3. Enter name for the role (eg. emailrole).
    ...  4. Provide access privileges.
    ...  5. Submit and commit changes
    [Setup]  General Test Case Setup


    User Roles Email Role Add  emailrole  tracking_access=${True}
    Commit Changes


Tvh1171788c
    [Tags]  interop  Tvh1171788c  Tvh1161584c
    [Documentation]  After scheduled time is over , verify the presence of Archived reports in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1171788
    ...  1. Schedule a report with specific time.
    ...  2. Wait until schedule time has passed.
    ...  3. Navigate to Archived report and check whether the scheduled report is present.
    [Setup]  General Test Case Setup
    [Teardown]  Do Tvh1171788c Teardown

    Time Zone Edit  Asia  India  Kolkata
    Commit Changes
    ${dateandtime}=  Run On DUT  date -v+0M "+%m/%d/%Y %H:%M"
    ${time}=  Fetch From Right  ${dateandtime}  ${SPACE}
    ${time}=  Split String  ${time}  :
    ${int_hour}=  Get From List  ${time}  0
    ${hour}=  Convert to integer  ${int_hour}
    ${incrementhour}=  Evaluate  ${hour}+1
    ${catenate}=  Catenate  SEPARATOR=  0  ${incrementhour}
    Run Keyword If  ${incrementhour}<10  Set Test Variable  ${incrementhour}  ${catenate}
    ${min}=  Get From List  ${time}  1
    ${min}=  Convert To Integer  ${min}
    Run Keyword If  ${min}<=14  Set Test Variable  ${minute}  15
    Run Keyword If  ${min}>=15  Set Test Variable  ${minute}  30
    Run Keyword If  ${min}>=30  Set Test Variable  ${minute}  45
    Run Keyword If  ${min}>=45  Set Test Variable  ${minute}  00
    Run Keyword If  ${min}>=45  Set Test Variable  ${hour}  ${incrementhour}
    Email Scheduled Reports Add Report    ${sma_email_reports.FILTERS}
    ...  title=ContentFiltersReport
    ...  report_format=csv
    ...  time_range=last day
    ...  schedule=daily:${hour}:${minute}
    ...  email_to=test_email@${CLIENT_HOSTNAME}
    Commit Changes
    ${reports}=  Wait Until Keyword Succeeds  14m  1m  Get Archive Report
    ${item} =  Get From List  ${reports}  0
    Should Contain  ${item}  Report Title: ContentFiltersReport

Tvh1165321c
    [Tags]  interop  Tvh1165321c
    [Documentation]  Check the message tracking functionality in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165321
    ...  1. Send spam and virus mails to ESA.
    ...  2. Naviage to Message Tracking in SMA and click search, messages must be visible.
    ...  3. Click on show details.
    ...  4. Check trackerd logs in cli whether tracking mails is present.
    [Setup]  Do Tvh1165321c Setup

    Library Order SMA
    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  exp_count=${expected_count}
    Should Be Equal As Integers  ${tracking_messages_count}  ${expected_count}
    Click Element  ${Message_Details}  don't wait
    Filter Message Tracking Log Create Baseline
    Filter Message Tracking Log Check  ${baseline_trackerdlog}  .*FlashPla_exe.mbox.*
    Filter Message Tracking Log Check  ${baseline_trackerdlog}  .*spam.mbox.*
    Filter Message Tracking Log Check  ${baseline_trackerdlog}  .*spam_url.mbox.*
    Filter Message Tracking Log Check  ${baseline_trackerdlog}  .*unscannable.mbox.*

Tvh1175818c
    [Tags]  interop  Tvh1175818c
    [Documentation]  Create a custom Email user in SMA and verify the provided privileges.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1175818
    ...  1. Navigate to Users in SMA.
    ...  2. Add users with userrole 'emailrole'.
    ...  3. Submit and commit changes.
    ...  4. Login to SMA with created user credentials.
    ...  5. Click Message Tracking, messages should be visible.
    [Setup]  General Test Case Setup

    Library Order SMA
    Selenium Login
    Users Add User  testemail  testemail  ${DUT_ADMIN_SSW_PASSWORD}  user_role=emailrole
    Commit Changes
    Log Out of Dut
    Log Into Dut  testemail  ${DUT_ADMIN_SSW_PASSWORD}
    Click Element  ${Message_Tracking}
    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  exp_count=${expected_count}
    Should Be Equal As Integers  ${tracking_messages_count}  ${expected_count}

Tvh1174480c
    [Tags]  interop  Tvh1174480c
    [Documentation]  Verify Message Tracking data  for various time ranges.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1174480
    ...  1. Incoming mail policy is enabled for spam, virus.
    ...  2. Send Spam/Virus mails to ESA.
    ...  3. Via cli change the date of both SMA and ESA to week before the current date.
    ...  4. Send Spam/Virus mails to ESA.
    ...  5. Go To SMA,Navigate to Email>Message Tracking.
    ...  6. Select last day, last week and custom range and check the results.
    [Setup]  General Test Case Setup

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    ${day_count}=  Evaluate    ${esa_cnt} * 2
    ${week_count}=  Evaluate    ${esa_cnt} * 4

    Clear Email Tracking Reporting Data
    Sync Appliances Datetime  ${SMA}  @{ESA_NAMES}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/unscannable.mbox  ${PUBLIC_LISTENER.ipv4}
      ${current_time}=  Run On DUT
      ...  date "+%m/%d/%Y %H:%M:%S"
      Sleep  10s
      ${current_date}=  Fetch From Left  ${current_time}  ${SPACE}
      ${cur_time} =  Set Time
      ${six_days_var}=  Set Variable  6
      ${week_ago_var}=  Calculate Shifted Datetime  ${six_days_var}  cur_time=${cur_time}
      Set Time  ${week_ago_var}
      Inject Custom Message  antispam/spam.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/unscannable.mbox  ${PUBLIC_LISTENER.ipv4}
      Sleep  10s
      ${custom_date}=  Fetch From Left  ${week_ago_var}  ${SPACE}
     END
    Sync Appliances Datetime  ${SMA}  @{ESA_NAMES}
    ${last_day}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  mesg_received=last day  exp_count=${day_count}
    ${last_week}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  mesg_received=last week  exp_count=${week_count}
    ${custom_range}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  mesg_received=custom range  exp_count=${week_count}
    ...  start_date=${custom_date}  end_date=${current_date}

Tvh1173628c
    [Tags]  interop  Tvh1173628c
    [Documentation]  Verify message tracking with advanced search option.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1173628
    ...  1. Send spam mails to ESA.
    ...  2. Go To SMA, Navigate to Email>Message Tracking.
    ...  3. Click on advanced, select message action as spam positive and check results.
    ...  4. Click on advanced, enter sender ip in the Sender Ip feild and check result.
    [Setup]  Do Tvh1165321c Setup

    @{checkbox}=  Create List  spam positive
    ${spam_count}=  Evaluate    ${esa_cnt} * 2
    ${sender_count}=  Evaluate    ${esa_cnt} * 4
    ${message_event}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  message_event=${checkbox}  exp_count=${spam_count}
    Should Be Equal As Integers  ${message_event}  ${spam_count}
    ${CLIENT_DATA_IP}=  Get Host IP By Name  d1.${CLIENT}
    ${sender}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  sender_ip=${CLIENT_DATA_IP}  exp_count=${sender_count}
    Should Be Equal As Integers  ${sender}  ${sender_count}

Tvh1165324c
    [Tags]  interop  Tvh1165324c
    [Documentation]  Configure  AMP in ESA and verify presence of  AMP mails in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165324
    ...  1. In ESA, Enable feature keys for File Reputation and File Analysis.
    ...  2. Navigate to Incoming mail policy-> enable Advanced malware protection. Set action as Quarantine.
    ...  3. Send Amp positive mail to ESA .
    ...  4. Check the Email Reporting in SMA-> Email
    [Setup]  General Test Case Setup

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    ${amp_count}=  Evaluate    ${esa_cnt} * 2
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Run Keyword If  ${USE_SMART_LICENSE} == 0  Add AMP Feature Key
      Sync Appliances Datetime  ${SMA}  ${${appliance}}
      Selenium Login
      ${settings_antispam}=  Create Dictionary
      ...  Anti-Spam Scanning  Disabled
      ${settings_antivirus}=  Create Dictionary
      ...  Anti-Virus Scanning  No
      Mail Policies Edit Antispam
      ...  Incoming
      ...  Default
      ...  ${settings_antispam}
      Mail Policies Edit Antivirus
      ...  Incoming
      ...  Default
      ...  ${settings_antivirus}
      Commit Changes
      ${settings}=  Create Dictionary
      ...  Advanced Malware Protection  Yes
      ...  Enable File Analysis  ${True}
      ...  Messages with File Analysis Pending Apply Action  Quarantine
      Advancedmalware Enable
      Mail Policies Edit Advanced Malware Protection
      ...  Incoming
      ...  default
      ...  ${settings}
      Commit Changes
      Inject Custom Message  advancedmalware/malware.tar.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  advancedmalware/malware.tar.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    ${amp}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  exp_count=${amp_count}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Amp Email Count  mesg_count=${amp_count}  col_value=5

Tvh1174739c
    [Tags]  interop  Tvh1174739c
    [Documentation]  Verify Message Reporting data  for various time ranges in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1174739
    ...  1. Send different kinds of mails to ESA.
    ...  2. Check the incoming mail summary table has recieved complete mails for different time ranges.
    [Setup]  General Test Case Setup

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    ${spam_messages_count}=  Set Variable  0
    ${virus_messages_count}=  Set Variable  0
    ${total__messages_count}=  Set Variable  0
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      ${settings}=  Create Dictionary
      ...  Anti-Spam Scanning  Use IronPort Anti-Spam service
      ...  Use IronPort Anti-Spam  ${True}
      Selenium Login
      Mail Policies Edit Antispam   incoming  default  ${settings}
      ${settings} =  Create Dictionary
      ...  Anti-Virus Scanning  Yes
      ...  Use Sophos Anti-Virus  ${True}
      Mail Policies Edit Antivirus  incoming  default  ${settings}
      Commit Changes
      ${current_time}=  Run On DUT
      ...  date "+%m/%d/%Y %H:%M:%S"
      ${current_date}=  Fetch From Left  ${current_time}  ${SPACE}
      ${cur_time} =  Set Time
      ${year_days_var}=  Set Variable  45
      ${year_ago_var}=  Calculate Shifted Datetime  ${year_days_var}  cur_time=${cur_time}
      Set Time  ${year_ago_var}
      Inject Custom Message  antispam/spam.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/FlashPla_exe.mbox  ${PUBLIC_LISTENER.ipv4}
      Sleep  1m
      ${six_days_var}=  Set Variable  6
      ${week_ago_var}=  Calculate Shifted Datetime  ${six_days_var}  cur_time=${cur_time}
      Set Time  ${week_ago_var}
      Inject Custom Message  antispam/spam.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/FlashPla_exe.mbox  ${PUBLIC_LISTENER.ipv4}
      Sleep  1m
      Library Order SMA
      ${current_time}=  Run On DUT
      ...  date "+%m/%d/%Y %H:%M:%S"
      Library Order ${esa}
      Set Time  ${current_time}
      Inject Custom Message  antispam/spam.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/FlashPla_exe.mbox  ${PUBLIC_LISTENER.ipv4}
      Sleep  1m
    END
    Library Order SMA
    Selenium Login
    FOR  ${time_period}  IN
    ...  Day
    ...  Week
    ...  Year
      ${virus_messages_count}=  Evaluate  ${virus_messages_count} + ${esa_cnt}
      ${spam_messages_count}=  Evaluate  ${spam_messages_count} + ${esa_cnt}
      ${total_messages_count}=  Evaluate  ${virus_messages_count} + ${spam_messages_count}
      ${expected_columns}=  Create List
      ...  Spam Detected    ${spam_messages_count}
      ...  Virus Detected   ${virus_messages_count}
      ...  Total Attempted Messages  ${total_messages_count}
      ${table_params}=  Email Report Table Create Parameters
      ...  Incoming Mail Summary  period=${time_period}
      ${reporting_data}=  Wait Until Keyword Succeeds
      ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
      ...  Amp Email Count  mesg_count=${total_messages_count}  col_value=17  table_param=${table_params}
      ${reporting_data}=  Wait Until Keyword Succeeds
      ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
      ...  Email Report Table Get Data  Incoming Mail Summary  table_parameters=${table_params}
      @{col_values} =  Get From Dictionary  ${reporting_data}
      ...  Messages
      ${virus_value} =  Get From List  ${col_values}  4
      ${spam_value} =  Get From List  ${col_values}  3
      ${total_value}=  Get From List  ${col_values}  17
      Should Be Equal As Integers  ${virus_value}  ${virus_messages_count}
      Should Be Equal As Integers  ${spam_value}  ${spam_messages_count}
      Should Be Equal As Integers  ${total_value}  ${total_messages_count}
    END

Tvh1165148c
    [Tags]  interop  Tvh1165148c  Tvh1174742c
    [Documentation]  Verify the functionality of Spam Quarantine search result with search criteria in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165148
    ...  1. Send different spam mails to ESA.
    ...  2. Navigate to Email>Messgae Quarantine>Spam Quarantine in SMA, click link for spam quarantine.
    ...  3. Search with advanced criteria such as Envelope Recipient and verify the mail count.
    ...  4. Search the result for different time ranges and verify the mail count.
    [Setup]  General Test Case Setup


    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    ${quarant_count} =  Evaluate    2 * ${esa_cnt}
    Clear Email Tracking Reporting Data
    Library Order SMA
    Selenium Login
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    Spam Quarantine Edit EndUser Access  end_user_access_enable=${True}  end_user_auth=None
    Spam Quarantine Edit Notification  spam_notif_enable=${True}  spam_notif_baddr=${TEST_ID}@${CLIENT}
    Commit Changes
    Spam Quarantine Search Page Open  user=${DUT_ADMIN}  password=${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week
    Library Order SMA
    Selenium Login
    FOR  ${esa_name}  IN  @{ESA_NAMES}
      Wait Until Keyword Succeeds  5m  1m  Security Appliances Edit Email Appliance
      ...  ${esa_name}
      ...  isq=${true}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
      Commit Changes
    END
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Quarantines Spam Disable
      Commit Changes
      EUQ Enable  ${SMA}  ${SMA_IP}  enable_slbl=${False}
      ${settings}=  Create Dictionary  Positive Spam Apply Action  Spam Quarantine
      Mail Policies Edit Antispam  incoming  default  ${settings}
      Commit Changes
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    Spam Quarantine Search Page Open  user=${DUT_ADMIN}  password=${DUT_ADMIN_SSW_PASSWORD}
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=today  recipient_cmp=contains  recipient_value=${CLIENT}  expected=${quarant_count}
    Should Be Equal As Integers  ${spam_count}  ${quarant_count}
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week  recipient_cmp=contains  recipient_value=${CLIENT}  expected=${quarant_count}
    Should Be Equal As Integers  ${spam_count}  ${quarant_count}
    ${current_time}=  Run On DUT
    ...  date "+%m/%d/%Y %H:%M:%S"
    ${current_date}=  Fetch From Left  ${current_time}  ${SPACE}
    ${Shift_time}=  Run On DUT  date -v-3d "+%m/%d/%Y 00:00:00"
    ${Shift_date}=  Fetch From Left  ${Shift_time}  ${SPACE}
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=${Shift_date},${current_date}  recipient_cmp=contains  recipient_value=${CLIENT}  expected=${quarant_count}
    Should Be Equal As Integers  ${spam_count}  ${quarant_count}

Tvh1165338c
    [Tags]  interop  Tvh1165338c
    [Documentation]  Verify functionality of release and delete actions in SPAM Quarantine search result.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165338
    ...  1. Send different spam mails to ESA.
    ...  2. Navigate to Email>Messgae Quarantine>Spam Quarantine in SMA, click link for spam quarantine.
    ...  3. Select a mail and click on release .
    ...  4. Select another mail from the list and click on delete .
    [Setup]  General Test Case Setup

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    ${quarant_count} =  Evaluate    2 * ${esa_cnt}
    Spam Quarantine Search Page Open  user=${DUT_ADMIN}  password=${DUT_ADMIN_SSW_PASSWORD}
    Spam Quarantine Delete Messages  date_range=week  recipient_cmp=contains  recipient_value=${CLIENT}
    ${spam_count}=  Spam Quarantine Advanced Search  date_range=week  recipient_cmp=contains  recipient_value=${CLIENT}
    ${spam_count}=  Get Length  ${spam_count}
    Should Be Equal As Integers  ${spam_count}  0
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam.mbox  ${PUBLIC_LISTENER.ipv4}
      Sleep  1m
    END
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week  recipient_cmp=contains  recipient_value=${CLIENT}  expected=${quarant_count}
    Spam Quarantine Release Messages  date_range=week  recipient_cmp=contains  recipient_value=${CLIENT}
    ${spam_count}=  Spam Quarantine Advanced Search  date_range=week  recipient_cmp=contains  recipient_value=${CLIENT}
    ${spam_count}=  Get Length  ${spam_count}
    Should be equal as integers  ${spam_count}  0

Tvh1165328c
    [Tags]  interop  Tvh1165328c
    [Documentation]  Verify outgoing mail report(DLP) in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165328
    ...  1. In ESA, Navigate to security services, enable data loss prevention with match content logging.
    ...  2. Add DLP Policy Manager and Add DLP Policy Customization with message action quarantine.
    ...  3. Enable DLP in outgoing mail policy.
    ...  4. Send mails according to DLP Policy.
    ...  5. Navigate to Email>Reporting>DLP Incidents in SMA, and check whether mails are visible.
    [Setup]  General Test Case Setup

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    ${dlp_count}=  Evaluate    2 * ${esa_cnt}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      ${PRIVATE_LISTENER_IP} =  Get ESA Private IP
      Dlp Enable
      Dlp Edit Settings  enable_matched_content_logging=${True}
      Dlp Message Action Add
      ...  name=quarantine
      ...  description=quarantines messages
      ...  msg_action=Quarantine
      Dlp Policy New
      ...  Regulatory Compliance
      ...  ${Tvh1165328c_DLP_POLICY}
      ...  submit=${False}
      Dlp Policy Configure Severity Settings
      ...  critical=quarantine
      ...  high=quarantine
      ...  medium=quarantine
      ...  low=quarantine
      ...  submit=${True}
      ${settings}=  Create Dictionary
      ...  DLP Policies  Enable DLP (Customize settings)
      ...  ${Tvh1165328c_DLP_POLICY}  ${True}
      ...  Enable All  ${True}
      Mail Policies Edit DLP  outgoing  default  ${settings}
      Commit Changes
      Sleep  1m
      Inject Custom Message  dlp/credit_card.mbox  ${PRIVATE_LISTENER_IP}
      Inject Custom Message  dlp/credit_card.mbox  ${PRIVATE_LISTENER_IP}
    END
    Library Order SMA
    Selenium Login
    ${table_data}=   Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  ${RETRY_TIME}
    ...  Dlp Email Count  mail_count=${dlp_count}
    Log  ${table_data}
