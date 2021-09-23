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
${expected_count}=  2
${CONFIG_PATH}     /data/pub/configuration
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${spam_qxpath}=  //a[@title='Spam Quarantine (open in new window)']
${TEST_EUQ_SP_PROFILE}=  euq_sp_profile
${TEST_EUQ_IDP_PROFILE}=   euq_idp_profile

*** Keywords ***
Initialize Suite
    global_sma.DefaultTestSuiteSetup

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
    ${expected_count}=  Convert To Integer  ${expected_count}
    ${esa_cnt}=  Get Length  ${esa_appliances}
    ${expected_count}=  Evaluate    ${esa_cnt} * ${expected_count}
    Set Suite Variable  ${expected_count}
    Set Suite Variable  ${esa_cnt}

    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Wait Until Keyword Succeeds  5m  1m  Pvo Quarantines Enable
      Run Keyword And Ignore Error  Commit Changes
    END
    Library Order SMA
    Clean System Quarantines
    Start Cli Session If Not Open
    Roll Over Now  mail_logs
    Add Customer/Devops SAML Config Azure  ${USER_ROLE}
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID_Azure}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP FOR EUQ  ${TEST_EUQ_SP_PROFILE}  ${TEST_EUQ_IDP_PROFILE}  ${settings}
    Commit Changes

Send Spam And PVO Data
    Library Order Sma
    Start Cli Session If Not Open
    Go To Spam Quarantine
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week
    Close Window
    ${title_var}        Get Window Titles
    Select Window       title=@{title_var}[0]
    Run Keyword And Ignore Error  Log Into DUT
    Run keyword And Ignore Error  Pvo Release Policy Message  Outbreak  week
    Run keyword And Ignore Error  Pvo Release Policy Message  Policy  week
    Run keyword And Ignore Error  Pvo Release Policy Message  Virus  week

    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      Selenium Login
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${ESA_PUB_LISTENER_IP}
      Inject Custom Message  antispam/spam_url.mbox  ${ESA_PUB_LISTENER_IP}
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
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${ESA_PUB_LISTENER_IP}
      Inject Custom Message  antivirus/testvirus.mbox  ${ESA_PUB_LISTENER_IP}
      Inject Custom Message  outbreak/vofmanual.mbox  ${ESA_PUB_LISTENER_IP}
    END

Send Email Time Data
    Clear Email Tracking Reporting Data
    ${spam_messages_count}=  Set Variable  0
    ${virus_messages_count}=  Set Variable  0
    ${total__messages_count}=  Set Variable  0
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
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
      Inject Custom Message  antispam/spam.mbox  ${ESA_PUB_LISTENER_IP}
      Inject Custom Message  antivirus/FlashPla_exe.mbox  ${ESA_PUB_LISTENER_IP}
      Sleep  1m
      ${six_days_var}=  Set Variable  6
      ${week_ago_var}=  Calculate Shifted Datetime  ${six_days_var}  cur_time=${cur_time}
      Set Time  ${week_ago_var}
      Inject Custom Message  antispam/spam.mbox  ${ESA_PUB_LISTENER_IP}
      Inject Custom Message  antivirus/FlashPla_exe.mbox  ${ESA_PUB_LISTENER_IP}
      Sleep  1m
      Library Order SMA
      ${current_time}=  Run On DUT
      ...  date "+%m/%d/%Y %H:%M:%S"
      Library Order ${esa}
      Set Time  ${current_time}
      Inject Custom Message  antispam/spam.mbox  ${ESA_PUB_LISTENER_IP}
      Inject Custom Message  antivirus/FlashPla_exe.mbox  ${ESA_PUB_LISTENER_IP}
      Sleep  1m
      Selenium Close
    END
    Library Order SMA
    Selenium Login
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
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

Go To Spam Quarantine
    Run Keyword And Ignore Error  Capture Page Screenshot
    Navigate To  Email  Message Quarantine  Spam Quarantine
    Click Element  ${spam_qxpath}  don't wait
    ${title_var}        Get Window Titles
    Select Window       title=@{title_var}[1]
    Run Keyword And Ignore Error  Log Into DUT
    Run Keyword And Ignore Error  Capture Page Screenshot

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

Check Spam Count
    [Arguments]  ${expected}=${expected_count}
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  date_range=week
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} != ${expected}  Fail
    [Return]  ${actual_spam_count}

Message Delete And Release
    Spam Quarantine Delete Messages
    ...  date_range=today
    ...  header_cmp=contains
    ...  header_value=danel
    Page Should Contain  Success

    Spam Quarantine Release Messages
    ...  date_range=today
    ...  header_cmp=contains
    ...  header_value=test
    Page Should Contain  Success

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

*** Test Cases ***

Tvh1437038c
    [Tags]  Tvh1437038c  saml  interop
    [Documentation]
    ...  TIMS link:https://tims.cisco.com/view-entity.cmd?ent=1437038
    ...  1. Login as admin and create SAML profile with SP and IDP.
    ...  2. Enable external authenticateion under "users" -> system administrator page.
    ...  3. Provide SAML group name and User Role as "email administrator". (save the changes)
    ...  4. Send Live traffic into reporting, tracking, spam and PVO from ESA to SMA.
    ...  5. Now logout.
    ...  6. Login again as saml "email administrator" by clicking on SSO button.
    ...  7. check the reporting, tracking, quarnatine and pvo messages count are same.
    ...  8. Check when saml email administrator clicks on quarantine then he is able to release and delete the spam messages.
    ...  9. Check 2-3 reports that loading properly with different time ranges, able to see the data and count is proper.
    ...  10. Check tracking advanced search with some filters, showing proper data. When user click on any tracking message more details, he is able to see full details.
    ...  11. Check pvo search and validate all the actions release, delete, sendcopy, move and delay. Also click on more deatils of any message and validate the details of the message.
    ...  12. check it has only access to Email tab. other tabs he will not able to see like " network", "system administrators".
    ...  13. He should not able to see web tab

    Library Order Sma
    Selenium Login
    Enable Externalauth Customer  Email Administrator
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Run Keyword And Expect Error
    ...   *  Navigate To  Web  Reporting

    Send Email Time Data

    Wait Until Keyword Succeeds  25m  1m
    ...  Email Tracking Search and Return  mesg_received=last week  exp_count=4
    Click Link  Show Details
    Select Window  Message Details
    Page Should Contain  Test_Role
    Close Window
    ${title_var}        Get Window Titles
    Select Window       title=@{title_var}[0]
    Send Spam And PVO Data
    Library Order Sma
    Go To Spam Quarantine
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Check Spam Count
    Message Delete And Release
    ${title_var}        Get Window Titles
    Select Window       title=@{title_var}[0]
    Run Keyword And Ignore Error  Log Into DUT
    FOR  ${type}  IN  Policy  Virus  Outbreak
       ${count}=  Run Keyword  ${type} Messages Count
       ${count}=  Convert To Integer  ${count}
       Should be Equal As Integers  ${count}  1
    END
    Add Policy Quarantine  name=upq  retention_period=20  retention_unit=Hours  default_action=delete
    Commit Changes
    Run keyword And Ignore Error  Pvo Delete Policy Message  Virus  week
    Run keyword And Ignore Error  Pvo Release Policy Message  Policy  week
    Run keyword And Ignore Error  Pvo Release Policy Message  Outbreak  week
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
    ...   *  Navigate To  Management Appliance  Centralized Services  Security Appliances
    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  System Administration
    Run Keyword And Expect Error
    ...   *  Navigate To  Management Appliance  Network
    Selenium Close
