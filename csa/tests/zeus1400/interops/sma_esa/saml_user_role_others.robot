# $ Id: $
# $ DateTime:  $
# $ Author: $

*** Settings ***
Resource     sma/global_sma.txt
Resource     esa/injector.txt
Resource     esa/global.txt
Resource     regression.txt
Resource     esa/logs_parsing_snippets.txt
Resource     esa/backdoor_snippets.txt
Resource     sma/esasma.txt
Resource     sma/saml.txt
Library      OperatingSystem

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Set Appliance Under Test to SMA
...  Initialize Suite

Suite Teardown  Finalize Suite

*** Variables ***
${DATA_UPDATE_TIMEOUT}=  30m
${RETRY_TIME}=  30s
${CONFIG_PATH}     /data/pub/configuration
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/

*** Keywords ***
Initialize Suite
    global_sma.DefaultTestSuiteSetup

    Run Keyword And Ignore Error  Log Out of DUT
    Log Into DUT
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    PVO Quarantines Enable
    Commit Changes

    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=SAML 2.0

    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_fname=testuser@cisco.com
    ...  spam_notif_username=testuser
    ...  spam_notif_domain=cisco.com
    ...  spam_notif_enable_login=${True}
    ...  spam_notif_consolidate=${True}
    ...  spam_notif_baddr=test@cisco.com

    Spam Quarantine SlBl Enable
    Commit Changes
    IP Interfaces Edit  Management  isq_https_service=83  isq_default=https://${DUT}:83/  hostname=${DUT}
    Commit Changes
    Selenium Close

    ${esa_duts}=  Set Variable  ${ESA_IDS}
    @{esa_appliances}=  Split String  ${esa_duts}  ,
    Set Suite Variable  @{esa_appliances}
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup
    ...  should_revert_to_initial=${False}
    ${ESA_ORIG_CONF}=  Save Config
    Set Suite Variable  ${ESA_ORIG_CONF}
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    ${ESA_PUB_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${ESA_PUB_LISTENER}
    Message Tracking Enable  tracking=centralized
    Centralized Email Reporting Enable
    Clean System Quarantines
    Quarantines Spam Disable
    Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    Commit Changes
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp(dir="%{SARF_HOME}/tmp")  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}

    @{ESA_NAMES}=    Create List
    Library Order SMA
    Selenium Login
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    FOR  ${appliance}  IN  @{esa_appliances}
      Wait Until Keyword Succeeds  1m  10s
      ...  Security Appliances Add Email Appliance
      ...  ${${appliance}}
      ...  ${${appliance}_IP}
      ...  tracking=${True}
      ...  reporting=${True}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
      Commit Changes
      Append To List    ${ESA_NAMES}  ${${appliance}}
    END

    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Wait Until Keyword Succeeds  5m  1m  Pvo Quarantines Enable
      Run Keyword And Ignore Error  Commit Changes
      Selenium Close
    END
    Library Order SMA
    Clean System Quarantines
    Start Cli Session If Not Open
    Roll Over Now  mail_logs
    Add Customer/Devops SAML Config Azure  ${USER_ROLE}
    Add Policy Quarantine  name=upq  retention_period=20  retention_unit=Hours  default_action=delete
    Commit Changes
    Selenium Close
    Start Cli Session If Not Open
    ${current_date}  Get SMA Date
    ...  "+%m/%d/%Y %H:%M:%S"
    Set Suite Variable  ${current_date}
    Configure ESA Appliance

SMA Reporting Data
    ${table_params}=  Email Report Table Create Parameters
    ...  Incoming Mail Details
    ...  period=Day
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  10 sec
    ...  Email Report Table Get Data
    ...  Incoming Mail Details
    ...  ${table_params}

Configure ESA Appliance
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      Selenium Login
      ${text} =  Set Variable  ppt
      ${msg_body_or_attachment_cond}=  Create Dictionary
      ...  Contains text  ${text}
      ${conditions}=  Content Filter Create Conditions
      ...  Message Body or Attachment  ${msg_body_or_attachment_cond}
      ${quarantine_action}=  Create Dictionary
      ...  Send message to quarantine   Policy
      ...  Duplicate message   ${False}
      ${actions}=  Content Filter Create Actions
      ...  Quarantine  ${quarantine_action}
      Content Filter Add  Incoming  Test_Role  Test_Role
      ...  ${actions}  ${conditions}
      Commit Changes
      ${settings}=  Create Dictionary
      ...  Content Filters  Enable Content Filters (Customize settings)
      ...  Test_Role  ${True}
      Mail Policies Edit Content Filters  Incoming  default
      ...  ${settings}
      ${settings} =  Create Dictionary
      ...  Anti-Virus Scanning  Yes
      ...  Virus Infected Messages Apply Action  Quarantine
      Mail Policies Edit Antivirus
      ...  Incoming
      ...  default
      ...  ${settings}
      ${settings}=  Create Dictionary
      ...  Outbreak Filters  Enable Outbreak Filtering (Customize settings)
      ...  Enable Message Modification  ${True}
      Mail Policies Edit Outbreak Filters  incoming  default  ${settings}
      Commit Changes
      Selenium Close
    END

Send Email Data
    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    Set Suite Variable  ${first_day_of_curr_month_to_set}
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Start Cli Session If Not Open
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Start Cli Session If Not Open
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    @{time_periods}=  Create List  300  20  7  1
    FOR  ${period}  IN  @{time_periods}
      ${datetime_to_set}=  Calculate Shifted Datetime
      ...  ${period}  cur_time=${first_day_of_curr_month}
      SmaCliLibrary.Start Cli Session If Not Open
      SmaCliLibrary.Set Time Set  ${datetime_to_set}
      Library Order Esa
      Start Cli Session If Not Open
      Library Order Sma
      Sync Appliances Datetime  ${SMA}  ${ESA}
      Inject Custom Message  antispam/spam.mbox  ${ESA_PUB_LISTENER_IP}
      Sleep  1m
      Library Order Sma
      SMA Reporting Data
    END

Send PVO Data
    Library Order Sma
    Start Cli Session If Not Open
    SmaCliLibrary.Set Time Set  ${current_date}
    EsaCliLibrary.Start Cli Session If Not Open
    Library Order Sma
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Run keyword And Ignore Error  Pvo Release Policy Message  Outbreak  week
    Run keyword And Ignore Error  Pvo Release Policy Message  Policy  week
    Run keyword And Ignore Error  Pvo Release Policy Message  Virus  week

    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${ESA_PUB_LISTENER_IP}
      Inject Custom Message  antivirus/testvirus.mbox  ${ESA_PUB_LISTENER_IP}
      Inject Custom Message  outbreak/vofmanual.mbox  ${ESA_PUB_LISTENER_IP}
    END

Finalize Suite
    Clear Email Tracking Reporting Data
    Set Appliance Under Test To ESA
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Run Keyword And Ignore Error  Run On DUT  rm -rf ${CONFIG_PATH}/default_config.xml
      Selenium Close
    END
    DefaultTestSuiteTeardown

    Set Appliance Under Test To SMA
    DefaultTestSuiteTeardown

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=Test_Role@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

Enable Externalauth Customer
    [Arguments]  ${user_role}
    Users Edit External Authentication  SAML
    ...  extauth_attribute_name_map=
    ...  group_mapping=${SAML_GROUP_Azure}:${user_role}
    Commit Changes

Add Customer/Devops SAML Config Azure
    [Arguments]  ${user_role}
    ${settings}=  Create Dictionary
    ...  User Role                          ${user_role}
    ...  SP Entity ID                       ${SP_ENTITY_ID_Azure}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP  ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes

Clear Email Tracking Reporting Data
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ESA
      Start Cli Session If Not Open
      Roll Over Now
      Commit
      Diagnostic Reporting Delete Db  confirm=yes
      Wait Until Ready
      Diagnostic Tracking Delete Db   confirm=yes
      Wait Until Ready
    END
    Library Order Sma
    Start Cli Session If Not Open
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready

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

PVO Message Count
    FOR  ${type}  IN  Policy  Virus  Outbreak
      ${count}=  Run Keyword  ${type} Messages Count
      ${count}=  Convert To Integer  ${count}
      Should be Equal As Integers  ${count}  1
    END

Get SMA Date
    [Arguments]  ${args}
    Library Order SMA
    ${return_val}  Run On Dut   date ${args}
    [Return]  ${return_val}

Check Table Column Value
    [Documentation]  Extracts particular column value\n
    ...  from given table data and verifies it is equal\n
    ...  to ${expected_val}
    [Arguments]  ${table_data}  ${col_name}  ${expected_val}
    @{col_values} =  Get From Dictionary  ${table_data}
    ...  ${col_name}
    ${value} =  Get From List  ${col_values}  0
    ${value} =  Convert To Integer  ${value}
    Should Be Equal As Integers  ${value}  ${expected_val}

*** Test Cases ***

Tvh1437037c
    [Tags]  saml  interop  Tvh1437037c
    [Documentation]
    ...  TIMS Link:https://tims.cisco.com/view-entity.cmd?ent=1437037
    ...  1. Login as admin and create SAML profile with SP and IDP.
    ...  2. Enable external authenticateion under "users" -> system administrator page.
    ...  3. Provide SAML group name and User Role as "guest user". (save the changes)
    ...  4. Send Live traffic into reporting, tracking, spam and PVO from ESA to SMA.
    ...  5. Now logout.
    ...  6. Login again as saml user by clicking on SSO button.
    ...  7. check the reporting and pvo that count are same.
    ...  8. saml user behvaing like guestuser so he should not able to see "spam quarantine tab" or tracking.
    ...  9. Check 2-3 reports that loading properly with different time ranges, able to see the data and count is proper.
    ...  10. Check pvo search with all the actions.
    ...  11. he should not have access for system administration tab.
    [Teardown]  Clear Email Tracking Reporting Data

    Library Order Sma
    Selenium Login
    Enable Externalauth Customer  ${sma_user_roles.GUEST}
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Send Email Data
    FOR  ${time_period}  ${cnt}  IN
    ...  Day  1
    ...  Week  2
    ...  30 days  3
    ...  Year  4
      ${table_params}=  Email Report Table Create Parameters
      ...  Incoming Mail Details
      ...  period=${time_period}
      ${reporting_data}=  Email Report Table Get Data
      ...  Incoming Mail Details
      ...  ${table_params}
      Log  ${reporting_data}
      Check Table Column Value  ${reporting_data}  Total Attempted  ${cnt}
    END
    Log Out of DUT
    Log Into DUT
    Quarantines Edit
    ...  name=upq
    ...  ext_auth_groups=guest
    Quarantines Edit
    ...  name=Policy
    ...  ext_auth_groups=guest
    Quarantines Edit
    ...  name=Virus
    ...  ext_auth_groups=guest
    Quarantines Edit
    ...  name=Outbreak
    ...  ext_auth_groups=guest
    Commit Changes

    Log Out of DUT
    Send PVO Data
    Library Order Sma
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  PVO Message Count
    Pvo Delete Policy Message  Virus  week
    Pvo Release Policy Message  Policy  week
    Pvo Release Policy Message  Outbreak  week
    @{esa_appliances}  Create List  ESA
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${ESA_PUB_LISTENER_IP}
    END
    Library Order Sma
    ${res}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value1}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value1}
    Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Schedule Exit By  -- by 24 Hours
    Log  ${res}
    Should Match Regexp  ${res}  .*1 Message delayed by 1 day.*
    ${res}=  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value2}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value2}
    Should Not Be Equal As Strings  ${value1}  ${value2}
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Send Copy To  testuser@${CLIENT}
    Log  ${res}
    Should Match Regexp  ${res}  .*Messages are successfully sent.*
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Move To  upq
    Log  ${res}
    Should Match Regexp  ${res}  .*Message moved to upq quarantine.*

    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Spam Quarantine
    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  System Administration
    Selenium Close
    Clear Email Tracking Reporting Data

Tvh1437039c
    [Tags]  saml  interop  Tvh1437039c
    [Documentation]
    ...  TIMS Link:https://tims.cisco.com/view-entity.cmd?ent=1437039
    ...  1. Login as admin and create SAML profile with SP and IDP.
    ...  2. Enable external authenticateion under "users" -> system administrator page.
    ...  3. Provide SAML group name and User Role as "helpdesk user". (save the changes)
    ...  4. Send Live traffic into reporting, tracking, spam and PVO from ESA to SMA.
    ...  5. Now logout.
    ...  6. Login again as saml "helpdesk user" by clicking on SSO button.
    ...  7. check tracking and pvo that he has access and showing proper message.
    ...  8. he should not have access to spam and reporting tabs.
    ...  9. Check tracking advanced search with some filters, showing proper data. When user click on any tracking message more details, he is able to see full details.
    ...  10. Check pvo search and validate all the actions release, delete, sendcopy, move and delay. Also click on more deatils of any message and validate the details of the message.
    ...  11. check it has only access to Email tab. other tabs he will not able to see like " network", "system administrators".
    ...  12. He should not able to see web tab
    [Teardown]  Clear Email Tracking Reporting Data

    Library Order Sma
    Selenium Login
    Enable Externalauth Customer  ${sma_user_roles.HELP_DESK}
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Inject Custom Message  antispam/clean.mbox  ${ESA_PUB_LISTENER_IP}
    END
    Library Order Sma
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  exp_count=1
    Click Link  Show Details
    Select Window  Message Details
    Page Should Contain  Test_Role
    Close Window
    Selenium Close
    Selenium Login
    Quarantines Edit
    ...  name=upq
    ...  ext_auth_groups=helpdesk
    Quarantines Edit
    ...  name=Policy
    ...  ext_auth_groups=helpdesk
    Quarantines Edit
    ...  name=Virus
    ...  ext_auth_groups=helpdesk
    Quarantines Edit
    ...  name=Outbreak
    ...  ext_auth_groups=helpdesk
    Commit Changes
    Log Out of DUT
    Send PVO Data
    Library Order Sma
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  PVO Message Count
    Pvo Delete Policy Message  Virus  week
    Pvo Release Policy Message  Policy  week
    Pvo Release Policy Message  Outbreak  week
    @{esa_appliances}  Create List  ESA
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${ESA_PUB_LISTENER_IP}
    END
    Library Order Sma
    ${res}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value1}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value1}
    Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Schedule Exit By  -- by 24 Hours
    Log  ${res}
    Should Match Regexp  ${res}  .*1 Message delayed by 1 day.*
    ${res}=  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value2}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value2}
    Should Not Be Equal As Strings  ${value1}  ${value2}
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Send Copy To  testuser@${CLIENT}
    Log  ${res}
    Should Match Regexp  ${res}  .*Messages are successfully sent.*
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Move To  upq
    Log  ${res}
    Should Match Regexp  ${res}  .*Message moved to upq quarantine.*

    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Spam Quarantine
    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  System Administration
    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  Network
    Run Keyword And Expect Error
    ...   *  Navigate To  Web  Reporting
    Selenium Close

Tvh1437034c
    [Tags]  interop  saml  Tvh1437034c
    [Documentation]
    ...  TIMS Link:https://tims.cisco.com/view-entity.cmd?ent=1437034
    ...  1. Login as admin and create SAML profile with SP and IDP.
    ...  2. Enable external authenticateion under "users" -> system administrator page.
    ...  3. Provide SAML group name and User Role as "operator role". (save the changes)
    ...  4. Send Live traffic into reporting, tracking, spam and PVO from ESA to SMA.
    ...  5. Now logout.
    ...  6. Login again as saml user by clicking on SSO button.
    ...  7. check the reporting, tracking and pvo messages count are same.
    ...  8. saml user behvaing like opertaor so he should not able to see "spam quarantine tab" or messages.
    ...  9. Check 2-3 reports that loading properly with different time ranges, able to see the data and count is proper.
    ...  10. Check tracking advanced search with some filters, showing proper data. When user click on any tracking message more details, he is able to see full details.
    ...  11. Check pvo search and validate all the actions release, delete, sendcopy, move and delay. Also click on more deatils of any message and validate the details of the message.
    ...  12. he will not able to configure user under users page as he does not have pemission.
    [Teardown]  Clear Email Tracking Reporting Data

    Library Order Sma
    Selenium Login
    Enable Externalauth Customer  ${sma_user_roles.OPERATOR}
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Send Email Data
    FOR  ${time_period}  ${cnt}  IN
    ...  Day  1
    ...  Week  2
    ...  30 days  3
    ...  Year  4
      ${table_params}=  Email Report Table Create Parameters
      ...  Incoming Mail Details
      ...  period=${time_period}
      ${reporting_data}=  Email Report Table Get Data
      ...  Incoming Mail Details
      ...  ${table_params}
      Check Table Column Value  ${reporting_data}  Total Attempted  ${cnt}
    END
    @{checkbox}=  Create List  spam positive
    Email Tracking Search and Return  message_event=${checkbox}  exp_count=1
    Click Link  Show Details
    Select Window  Message Details
    Page Should Contain  Test_Role
    Close Window
    Selenium Close
    Selenium Login
    Quarantines Edit
    ...  name=upq
    ...  ext_auth_groups=operators
    Quarantines Edit
    ...  name=Policy
    ...  ext_auth_groups=operators
    Quarantines Edit
    ...  name=Virus
    ...  ext_auth_groups=operators
    Quarantines Edit
    ...  name=Outbreak
    ...  ext_auth_groups=operators
    Commit Changes
    Log Out of DUT
    Send PVO Data
    Library Order Sma
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  PVO Message Count
    Pvo Delete Policy Message  Virus  week
    Pvo Release Policy Message  Policy  week
    Pvo Release Policy Message  Outbreak  week
    @{esa_appliances}  Create List  ESA
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${ESA_PUB_LISTENER_IP}
    END
    Library Order Sma
    ${res}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value1}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value1}
    Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Schedule Exit By  -- by 24 Hours
    Log  ${res}
    Should Match Regexp  ${res}  .*1 Message delayed by 1 day.*
    ${res}=  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value2}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value2}
    Should Not Be Equal As Strings  ${value1}  ${value2}
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Send Copy To  testuser@${CLIENT}
    Log  ${res}
    Should Match Regexp  ${res}  .*Messages are successfully sent.*
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Move To  upq
    Log  ${res}
    Should Match Regexp  ${res}  .*Message moved to upq quarantine.*

    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Spam Quarantine
    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  System Administration  Users
    Selenium Close

Tvh1437036c
    [Tags]  saml  interop  Tvh1437036c
    [Documentation]
    ...  TIMS Link:https://tims.cisco.com/view-entity.cmd?ent=1437036
    ...  1. Login as admin and create SAML profile with SP and IDP.
    ...  2. Enable external authenticateion under "users" -> system administrator page.
    ...  3. Provide SAML group name and User Role as "readonlyuser". (save the changes)
    ...  4. Send Live traffic into reporting, tracking, spam and PVO from ESA to SMA.
    ...  5. Now logout.
    ...  6. Login again as saml user by clicking on SSO button.
    ...  7. check the reporting, tracking and pvo messages count are same.
    ...  8. saml user behvaing like readonlyuser so he should not able to see "spam quarantine tab" or messages.
    ...  9. Check 2-3 reports that loading properly with different time ranges, able to see the data and count is proper.
    ...  10. Check tracking advanced search with some filters, showing proper data. When user click on any tracking message more details, he is able to see full details.
    ...  11. Check pvo search , if user click on pvo then he should not have access.
    ...  12. he will not able to configure user under users page as he does not have pemission.
    [Teardown]  Clear Email Tracking Reporting Data

    Library Order Sma
    Selenium Login
    Enable Externalauth Customer  ${sma_user_roles.RO_OPERATOR}
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Send Email Data
    FOR  ${time_period}  ${cnt}  IN
    ...  Day  1
    ...  Week  2
    ...  30 days  3
    ...  Year  4
      ${table_params}=  Email Report Table Create Parameters
      ...  Incoming Mail Details
      ...  period=${time_period}
      ${reporting_data}=  Email Report Table Get Data
      ...  Incoming Mail Details
      ...  ${table_params}
      Check Table Column Value  ${reporting_data}  Total Attempted  ${cnt}
    END
    @{checkbox}=  Create List  spam positive
    Email Tracking Search and Return  message_event=${checkbox}  exp_count=1
    Click Link  Show Details
    Select Window  Message Details
    Page Should Contain  Test_Role
    Close Window
    Selenium Close
    Selenium Login
    Quarantines Edit
    ...  name=upq
    ...  ext_auth_groups=readonly
    Quarantines Edit
    ...  name=Policy
    ...  ext_auth_groups=readonly
    Quarantines Edit
    ...  name=Virus
    ...  ext_auth_groups=readonly
    Quarantines Edit
    ...  name=Outbreak
    ...  ext_auth_groups=readonly
    Commit Changes
    Log Out of DUT
    Send PVO Data
    Library Order Sma
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  PVO Message Count
    Pvo Delete Policy Message  Virus  week
    Pvo Release Policy Message  Policy  week
    Pvo Release Policy Message  Outbreak  week
    @{esa_appliances}  Create List  ESA
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${ESA_PUB_LISTENER_IP}
    END
    Library Order Sma
    ${res}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value1}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value1}
    Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Schedule Exit By  -- by 24 Hours
    Log  ${res}
    Should Match Regexp  ${res}  .*1 Message delayed by 1 day.*
    ${res}=  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value2}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value2}
    Should Not Be Equal As Strings  ${value1}  ${value2}
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Send Copy To  testuser@${CLIENT}
    Log  ${res}
    Should Match Regexp  ${res}  .*Messages are successfully sent.*
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Move To  upq
    Log  ${res}
    Should Match Regexp  ${res}  .*Message moved to upq quarantine.*

    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Spam Quarantine
    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  System Administration  Users
    Selenium Close

Tvh1437035c
    [Tags]  saml  interop  Tvh1437035c
    [Documentation]
    ...  TIMS Link:https://tims.cisco.com/view-entity.cmd?ent=1437035
    ...  1. Login as admin and create SAML profile with SP and IDP.
    ...  2. Enable external authenticateion under "users" -> system administrator page.
    ...  3. Provide SAML group name and User Role as "technician role". (save the changes)
    ...  4. Send Live traffic into reporting, tracking, spam and PVO from ESA to SMA.
    ...  5. Now logout.
    ...  6. Login again as saml user by clicking on SSO button.
    ...  7. check the reporting, tracking and pvo messages count are same.
    ...  8. saml user behvaing like technician so he should able to see only system status page under reporitng.
    ...  9. This user does not have access for tracking, spam and pvo.
    ...  10. He is having very limited access.

    Library Order Sma
    Selenium Login
    Enable Externalauth Customer  ${sma_user_roles.TECHNICIAN}
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure

    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  Centralized Services  Security Appliances
    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  Network
    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Message Tracking
    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Message Quarantine  Spam Quarantine
    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Message Quarantine  Policy, Virus and Outbreak Quarantines
    Selenium Close

Tvh1437040c
    [Tags]  saml  interop  Tvh1437040c
    [Documentation]
    ...  TIMS Link:https://tims.cisco.com/view-entity.cmd?ent=1437040
    ...  1. Login as admin and create SAML profile with SP and IDP.
    ...  2. Enable external authenticateion under "users" -> system administrator page.
    ...  3. Provide SAML group name and User Role as "webadmin user". (save the changes)
    ...  4. Send Live traffic into reporting, tracking, spam and PVO from ESA to SMA.
    ...  5. Now logout.
    ...  6. Login again as saml "webadmin user" by clicking on SSO button.
    ...  7. he should able to see only web tab, reporting and utilities tabs.
    ...  8. he should not able to see Email admin tab.

    Library Order Sma
    Start Cli Session If Not Open
    Selenium Login
    Enable Externalauth Customer  ${sma_user_roles.WEB_ADMIN}
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Run Keyword And Ignore Error  Capture Page Screenshot
    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Reporting
    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Message Tracking
    Run Keyword And Expect Error
    ...   *  Navigate To  Email  Message Quarantine  Spam Quarantine
    Navigate To  Web  Reporting  Overview
    Navigate To  Web  Utilities  Web Appliance Status
    Selenium Close
