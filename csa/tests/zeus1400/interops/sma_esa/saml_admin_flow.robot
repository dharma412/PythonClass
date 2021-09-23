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
${SPAM_NOTIF_SUBJ}=  Spam Quarantine Notification
${TEST_EUQ_SP_PROFILE}=  euq_sp_profile
${TEST_EUQ_IDP_PROFILE}=   euq_idp_profile
${SENDER1}=  abc@ironport.com
${SENDER2}=  def@ironport.com
${CONFIG_PATH}     /data/pub/configuration
${DATA_UPDATE_TIMEOUT}=  30m
${RETRY_TIME}=  30s
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${PROFILE_NAME} =  smaesa_interop
${SLBL spam negative}=  SLBL spam negative
${SLBL spam positive}=  SLBL spam positive
${Outbreak_xpath}=  //*[@id='content']/form/dl/dd/table/tbody/tr[3]/td[3]/a
${Policy_xpath}=  //*[@id='content']/form/dl/dd/table/tbody/tr[4]/td[3]/a
${Virus_xpath}=   //*[@id='content']/form/dl/dd/table/tbody/tr[6]/td[3]/a
${Subject_xpath}=  //tbody[@class='yui-dt-data']/tr[1]/td[4]//div[@class='yui-dt-liner']//div[@class='trim-container']/span//a
${Tracking_xpath}=  //*[@id='form']/table/tbody/tr[2]/td[7]/a
${spam_qxpath}=  //a[@title='Spam Quarantine (open in new window)']
${expected_count}=  2
${user_name1}  user1
${full_user_name1}  User1
${user_name2}  user2
${full_user_name2}  User2

*** Keywords ***
Initialize Suite
    global_sma.DefaultTestSuiteSetup
    Run Keyword And Ignore Error  Log Out of DUT
    Log Into DUT
    Add Customer/Devops SAML Config Azure  ${USER_ROLE}
    Enable Externalauth Customer
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
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

    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure

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

    Ldap Add Server Profile
    ...  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_AUTH_SERVER}
    ...  base_dn=${LDAP_BASEDN}
    ...  auth_method=anonymous
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}

    Ldap Edit Isq End User Authentication Query
    ...  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_AUTH_SERVER}.isq_auth
    ...  (uid={u})
    ...  mail
    ...  ${True}

    Ldap Edit Isq Alias Consolidation Query
    ...  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_AUTH_SERVER}.isq_consolidate
    ...  (mailLocalAddress={a})
    ...  mail
    ...  ${True}
    Commit Changes
    Selenium Close
    ${dut_hostname}  ${domain}=  Split String  ${DUT}  .
    Set Suite Variable  ${RECIPIENT_ADDRESS}  xyz@ironport.${domain}

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
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
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
    Set Suite Variable  @{ESA_NAMES}

    Clean System Quarantines
    Start Cli Session If Not Open
    Roll Over Now  mail_logs
    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Wait Until Keyword Succeeds  5m  1m  Pvo Quarantines Enable
      Run Keyword And Ignore Error  Commit Changes
    END

Finalize Suite
    Run Keyword And Ignore Error  Remove Directory  ${SUITE_TMP_DIR}  recursive=${True}
    Set Appliance Under Test To ESA
    FOR  ${appliance}  IN  @{esa_appliances}
      Clear Email Tracking Reporting Data
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
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

Do Tvh1165329c Setup
    Set Appliance Under Test to SMA
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    DefaultTestCaseSetup
    Go To Spam Quarantine
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week

Go To Spam Quarantine
    Navigate To  Email  Message Quarantine  Spam Quarantine
    Click Element  ${spam_qxpath}  don't wait
    Go To  https://${DUT}:83

Do Tvh1165329c Teardown
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week
    Selenium Close

General Test Case Setup
    @{appliances}=  Split String  ${DUT_IDS}  ,
    FOR  ${dut_type}  IN  @{appliances}
      Run Keyword  Library Order ${dut_type}
      DefaultTestCaseSetup
    END
    Library Order ESA
    Start Cli Session If Not Open
    Sync Appliances Datetime  ${SMA}  @{ESA_NAMES}

Enable Externalauth Customer
    Users Edit External Authentication  SAML
    ...  extauth_attribute_name_map=
    ...  group_mapping=${SAML_GROUP_Azure}:Administrator
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

Search and Delete Message Through Email links
    [Arguments]  ${search_url}
    @{original_url}=  Split String  ${search_url}  '
    Log  @{original_url}[1]
    Go To  @{original_url}[1]
    ${current_url}=  Get Location
    Run Keyword And Ignore Error  Capture Screenshot
    Log  ${current_url}
    ${sub_string}=  Set Variable   https://${SMA}:83/Search
    Should Contain  ${current_url}  ${sub_string}
    Should Contain  ${current_url}  ${CLIENT_HOSTNAME}
    Spam Quarantine Delete Messages  is_admin=${False}
    Run Keyword And Ignore Error  Capture Screenshot
    Page Should Contain  Success

Spam Quarntine Search
    [Arguments]  ${date_range}=today  ${recipient_cmp}=  ${recipient_value}=  ${expected}=
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  date_range=${date_range}  recipient_cmp=${recipient_cmp}  recipient_value=${recipient_value}
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} != ${expected}  Fail
    [Return]  ${actual_spam_count}

Check Spam Count
    [Arguments]  ${expected}=${expected_count}
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  date_range=week
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} != ${expected}  Fail
    [Return]  ${actual_spam_count}

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

Euq Spam Quarantine Search
    [Arguments]  ${expected}=1
    Go To Spam Quarantine
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Check Spam Count  ${expected}
    Log  ${spam_count}

Get Expected Mail Count
    [Arguments]   ${table}=DLP Incident Details  ${column}=Messages  ${col_index}=0   ${count}=0
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  ${table}
    Log  ${reporting_data}
    @{col_values} =  Get From Dictionary  ${reporting_data}  ${column}
    ${mail_value} =  Get From List  ${col_values}  ${col_index}
    Run Keyword If  ${mail_value} != ${count}  Fail
    [Return]  ${mail_value}

Add SLBL admin and Verify
    [Arguments]  ${listtype}  ${address}  ${senders}
    ${slbl_admin_added}=   SLBL Admin Is Recipient Exist
    ...  ${listtype}  ${address}
    Run Keyword If  ${slbl_admin_added}
    ...  SLBL Admin Delete Recipient  ${listtype}  ${address}

    SLBL Admin Add Recipient
    ...  ${listtype}
    ...  ${address}
    ...  ${senders}
    ${slbl_admin_added}=   SLBL Admin Is Recipient Exist
    ...  ${listtype}  ${address}
    Should Be True  ${slbl_admin_added}

Database Sync for Safelist Or Blocklist
    [Arguments]  ${listtype}  ${address}  ${senders}
    Add SLBL admin and Verify
    ...  ${listtype}
    ...  ${address}
    ...  ${senders}

    Set Appliance Under Test to ESA
    Roll Over Now  mail_logs
    Sleep  5s  msg=Wait for logs roll over

    Set Appliance Under Test to SMA
    Go To  https://${DUT}
    ${synced}=  Spam Quarantine Sync Appliances
    Log  "Database Synchronisation is ${synced}"

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  wait_time=3 minutes
    ...  retry_time=1 minute
    ...  SLBL: Database watcher updated from snapshot >= 1

Create Recipients List File
    [Arguments]  ${recepients}
    ${rcpts}=  Join Path  ${SUITE_TMP_DIR}  ${TEST_ID}_rcpts.txt
    OperatingSystem.Create File  ${rcpts}
    OperatingSystem.Append To File  ${rcpts}  ${recepients}
    [Return]  ${rcpts}

Database Slbl Sync
    [Arguments]  ${LIST_TYPE}  ${LIST_TYPE_SENDER}
    Database Sync for Safelist Or Blocklist
    ...  ${LIST_TYPE}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${LIST_TYPE_SENDER}
    ${rcpts}=  Create Recipients List File   ${RECIPIENT_ADDRESS}
    [Return]  ${rcpts}

Add AMP Feature Key
    ${amp_file_rep_fkey}=  Generate DUT Feature Key  amp_file_rep
    ${amp_file_analysis_fkey}=  Generate DUT Feature Key  amp_file_analysis
    Start Cli Session If Not Open
    Feature Key Activate  ${amp_file_rep_fkey}
    Restart CLI Session
    Feature Key Activate  ${amp_file_analysis_fkey}
    Restart CLI Session

Inject Message And Verify Log
    [Arguments]  ${mbox-filename}  ${mail-from}  ${spam_negative}
    Inject Messages
    ...  mbox-filename=${mbox-filename}
    ...  mail-from=${mail-from}
    ...  address-list=${rcpts}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    Verify And Wait For Log Records
    ...  MID .* ICID .* From: .*${mail-from}.* >= 1
    ...  MID .* using engine.* ${spam_negative} >= 1

Fetch Mail Content Using Drain
    ${MAIL_CONTENT}=  Wait Until Keyword Succeeds
    ...  3 min
    ...  0 sec
    ...  Verify And Wait For Mail In Drain  ${CLIENT}
         ...  Subject  ${SPAM_NOTIF_SUBJ}
    Log   ${MAIL_CONTENT}
    [Return]  ${MAIL_CONTENT}

Release Message Through Email Links
    [Arguments]  ${url}
    @{original_url}=  Split String    ${url}  '
    Log  @{original_url}[1]
    Go To  @{original_url}[1]
    ${current_url}=  Get Location
    Run Keyword And Ignore Error  Capture Screenshot
    Log  ${current_url}
    ${sub_string}=  Set Variable   https://${SMA}:83/Message?action=Release
    Should Contain  ${current_url}  ${sub_string}
    Should Contain  ${current_url}  ${CLIENT_HOSTNAME}

*** Test Cases ***

Tvh1165329c
    [Tags]  interop  Tvh1165329c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165329
    ...  1. Navigate to Management Appliance ->Centralised Services -> Spam Quarantine.
    ...  2. Click on "Edit Settings".
    ...  3. In Edit Spam Quarantine page
    ...  a. Enable End-User Quarantine Access (eg . using LDAP/ SAML)
    ...  b. Enable Spam Notification
    ...  4. In Spam Notification Section -> enter the below settings
    ...  a. enter the from address
    ...  b. Enter email address in 'Deliver Bounce Message To' section.
    ...  c. select the Notification schedule
    ...  5. Click on submit, and Enable End user safe list / block list,Commit changes
    ...  6. Go to Network tab -> IP interfaces -> click on management interface
    ...  7. Enter the spam quarantine port for 'HTTPS'.
    ...  8. Enter the end user spam quarantine URL
    ...  9. Click on submit and commit changes
    [Setup]  Do Tvh1165329c Setup
    [Teardown]  Do Tvh1165329c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Check Spam Count
    Null Smtpd Start
    Force ISQ Notifications
    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}
    ${subj}=  Message Get  Subject
    Should Contain  ${subj}  ${SPAM_NOTIF_SUBJ}
    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCOED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{LIST_OF_URLS}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Release' in "${url}"
      ...  Release Message Through Email Links  ${url}
    END
    Message Unload
    NUll Smtpd Stop
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${esa_cnt}
    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@cisco.com.* >= ${esa_cnt}

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
    Selenium Close

Tvh1173628c
    [Tags]  interop  Tvh1173628c
    [Documentation]  Verify message tracking with advanced search option.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1173628
    ...  1. Send spam mails to ESA.
    ...  2. Go To SMA, Navigate to Email>Message Tracking.
    ...  3. Click on advanced, select message action as spam positive and check results.
    ...  4. Click on advanced, enter sender ip in the Sender Ip feild and check result.
    [Setup]  Do Tvh1165321c Setup

    Library Order SMA
    Selenium Login
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    @{checkbox}=  Create List  spam positive
    ${spam_count}=  Evaluate    ${esa_cnt} * 2
    ${sender_count}=  Evaluate    ${esa_cnt} * 4
    ${message_event}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  message_event=${checkbox}  exp_count=${spam_count}
    Should Be Equal As Integers  ${message_event}  ${spam_count}
    ${CLIENT_DATA_IP}=  Get Host IP By Name  ${CLIENT}
    Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  exp_count=${sender_count}
    ${d1_ip}=  Catenate  SEPARATOR=.  d1  ${CLIENT}
    ${status}  ${CLIENT_DATA_IP1}=  Run Keyword And Ignore Error  global_sma.Get Host IP By Name  ${d1_ip}
    Run Keyword If  '${status}' == 'FAIL'
    ...  Email Tracking Search and Return  sender_ip=${CLIENT_DATA_IP}  exp_count=${sender_count}
    ...  ELSE  Email Tracking Search and Return  sender_ip=${CLIENT_DATA_IP1}  exp_count=${sender_count}
    Selenium Close

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
    Library Order SMA
    Selenium Login
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Go To Spam Quarantine
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
    Should Be Equal As Integers  ${spam_count}  0
    Selenium Close

Tvh1165325c
    [Tags]  interop  Tvh1165325c  Tvh1231742c
    [Documentation]  Configure Anti spam in ESA and verify presence of Spam mails in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165325
    ...  1. In ESA, navigate to security services>centralized services>spam quarantine, and edit the details.
    ...  2. Navigate to Monitor-> Spam quarantine . Disable Spam Quarantine locally.
    ...  3. Go to Security Services -> Enable Ironport Anti Spam.
    ...  4. Navigate to Mail Policies-> Incoming mail Policies.
    ...  5. Go to Anti Spam option and enable it by selecting the radio button "Use IronPort Anti-Spam service".
    ...  6. Send Spam positive mail to ESA.
    ...  7. Check the Email Reporting in SMA-> Email.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Set Test Variable  ${spam_messages_count}  2
    Clear Email Tracking Reporting Data
    Sync Appliances Datetime  ${SMA}  @{ESA_NAMES}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      AntiSpam Enable  IronPort
      ${settings}=  Create Dictionary  Positive Spam Apply Action  Spam Quarantine
      Mail Policies Edit Antispam  incoming  default  ${settings}
      Commit Changes
    END
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Incoming Mail Summary  column=Messages  col_index=3  count=${expected_count}
    Selenium Close

Tvh1174799c
    [Tags]  interop  Tvh1174799c
    [Documentation]  Configure OutBreakFilter quarantine in ESA and verify presence of OF quarantined mails in SMA
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1174799
    ...  1. Navigate to Incoming mail policy-> Outbreak Filters.
    ...  2. Enable Outbreak Filtering.
    ...  3. Enable message modification and submit the changes.
    ...  4. Send mails (for eg. containing phising url ) to ESA.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
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
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Threat Details  column=Total Messages  col_index=0  count=${expected_count}
    Log  ${reporting_data}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Threat Details
    Log  ${reporting_data}
    @{col_values} =  Get From Dictionary  ${reporting_data}  Threat Name
    ${value} =  Get From List  ${col_values}  0
    Selenium Close

Tvh1231741c
    [Tags]  interop  Tvh1231741c
    [Documentation]  Check for PVO Quarantine to Tracking Drilldown for PVO messages
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1231739
    ...  1. All the Centralised services for Email in SMA are enabled.
    ...  2. All the Centralised services in ESA are enabled.
    ...  3. ESA is attached to SMA.
    ...  4. Mails have been Quarantined in SMA under PVO
    ...  5. In SMA navigate to Email ->PVO Quarantine and click on the no. of messages for Virus.
    ...  6. Click on "View" under "Tracking" column for an email.
    ...  7. Navigate to Email ->PVO Quarantine ,click on the no. of messages for Outbreak.
    ...  8. Click on "View" under "Tracking" column for an email.
    ...  9. navigate to Email ->PVO Quarantine and click on the no. of messages for Policy.
    ...  10. Click on "View" under "Tracking" column for an email.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Library Order SMA
    Selenium Login
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
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
      Content Filter Add  Incoming  ${TEST_ID}  ${TEST_ID}
      ...  ${actions}  ${conditions}
      Commit Changes
      ${settings}=  Create Dictionary
      ...  Content Filters  Enable Content Filters (Customize settings)
      ...  ${TEST_ID}   ${True}
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
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/testvirus.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  outbreak/vofmanual.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    FOR  ${type}  IN  Policy  Virus  Outbreak
      ${count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  ${type} Messages Count
      ${count}=  Convert To Integer  ${count}
      Should be Equal As Integers  ${count}  ${esa_cnt}
    END
    Library Order SMA
    FOR  ${path}  IN  ${Policy_xpath}  ${Virus_xpath}  ${Outbreak_xpath}
      Navigate To  Email  Message Quarantine  Policy, Virus and Outbreak Quarantines
      Click Element  ${path}  don't wait
      Sleep  25s
      Wait Until Keyword Succeeds      5x     10s
      ...   Press Keys  ${Subject_xpath}  RETURN
      Sleep  25s
      Wait Until Page Contains  Message Details  60s
      Click Element  ${Tracking_xpath}  don't wait
      Sleep  25s
      Page Should Contain  Message Tracking
    END
    Selenium Close

Tvh1232385c
    [Tags]  interop  Tvh1232385c  Tvh1232354c  Tvh1174601c
    [Documentation]  Verify functionality of Delay Scheduled Exit in PVO quarantine search result.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1232385
    ...  1. Centralised PVO is configured in both SMA and ESA.
    ...  2. SMA has received emails under Policy quarantine category.
    ...  3. Create quarantine for eg. "upq"
    ...  4. In the SMA , navigate to Email->Message Quarantine-> Policy, Virus and Outbreak.
    ...  5. Click on the no. of messages under Policy section
    ...  6. Select a mail and click on More Actions ->Delay Schedule Exit by 24 hrs and confirms the changes.
    ...  7. Verify that in the "Scheduled Exit" column delayed time should be shown.
    ...  8. Select a mail and click on More Actions -> Move .
    ...  9. Select the folder to which the mail will be moved (eg. "upq") and click on "Move.
    ...  10. Select another mail from the list and click on More Actions -> Send Copy
    ...  11. Enter the mail id (eg. test@cisco.com)to which the mail has to be sent and click on "Send".

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Library Order Sma
    Selenium Login
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Add Policy Quarantine  name=upq  retention_period=20  retention_unit=Hours  default_action=delete
    Commit Changes
    Run keyword And Ignore Error  Pvo Delete Policy Message  Virus  week
    Run keyword And Ignore Error  Pvo Release Policy Message  Policy  week
    Run keyword And Ignore Error  Pvo Release Policy Message  Outbreak  week
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/testvirus.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  outbreak/vofmanual.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    FOR  ${type}  IN  Policy  Virus  Outbreak
      ${count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  ${type} Messages Count
      ${count}=  Convert To Integer  ${count}
      Should be Equal As Integers  ${count}  ${esa_cnt}
    END
    Library Order Sma
    ${res}=  Quarantines Search Get All Messages  name=Policy
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
    Clear Email Tracking Reporting Data
    Selenium Close

Tvh1330304c
    [Tags]  interop  Tvh1330304c  Tvh1330303c  Tvh1436948c
    [Documentation]  verify the functionality of Blocklist.
    ...  SPAM quarantine has been enabled in SMA.
    ...  1. Navigate to Email -> Message Quarantine -> Spam Quarantine
    ...  2. Click on Spam Quarantine link.
    ...  3. Navigate to Options -> Safelist Blocklist.
    ...  4. Click on Add.
    ...  5. In 'Recipient Address', enter the address of the envelope recipient.
    ...  6. In 'Sender List', enter the value of 'From' from the mbox file.
    ...  7. Navigate to Management Appliance -> Centralized Services -> Spam Quarantine
    ...  and click on 'Synchronize All Appliances' under End-User Safelist/Blocklist.
    ...  8. Wait for some time for synchronization to complete.
    ...  9. Inject a single clean mail and in the address list only
    ...  keep the address of the recipient you have added in the Blocklist.
    ...  10.verify in message tracking as message should be captured and
    ...  verify in spam quarentine page in which the mail should not be captured.

    Set Test Variable   ${TEST_ID}  ${TEST_NAME}
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Set Test Variable   ${LIST_TYPE1}  Safelist
    Set Suite Variable  ${RECIPIENT_ADDRESS}  xyz@ironport.cs27
    Library Order SMA
    Selenium Login
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Go To Spam Quarantine
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week
    ${rcpts}=  Database Slbl Sync  ${LIST_TYPE1}  ${LIST_TYPE1}_1_${SENDER1}
    Set Test Variable  ${rcpts}

    Inject Message And Verify Log
    ...  ${SPAM}
    ...  ${LIST_TYPE1}_1_${SENDER1}
    ...  ${SLBL spam negative}

    Library Order SMA
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Incoming Mail Details  column=Spam Detected  col_index=0  count=0

    ${messages}=  Email Message Tracking Search
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Strings  ${tracking_message_count}  1

    Set Test Variable   ${LIST_TYPE2}  Blocklist
    Go To Spam Quarantine
    ${rcpts}=  Database Slbl Sync  ${LIST_TYPE2}  ${LIST_TYPE2}_2_${SENDER2}

    Inject Message And Verify Log
    ...  ${CLEAN}
    ...  ${LIST_TYPE2}_2_${SENDER2}
    ...  ${SLBL spam positive}

    Library Order SMA
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Incoming Mail Details  column=Spam Detected  col_index=0  count=1

    Euq Spam Quarantine Search

    FOR  ${LIST_TYPE}  IN  ${LIST_TYPE1}  ${LIST_TYPE2}
      ${slbl_admin_added}=   SLBL Admin Is Recipient Exist
      ...  ${LIST_TYPE}  ${RECIPIENT_ADDRESS}
      Run Keyword If  ${slbl_admin_added}
      ...  SLBL Admin Delete Recipient  ${LIST_TYPE}  ${RECIPIENT_ADDRESS}
    END
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Force ISQ Notifications
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${esa_cnt}

    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@cisco.com.* >= ${esa_cnt}

    Null Smtpd Start
    Force ISQ Notifications
    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}
    ${subj}=  Message Get  Subject
    Should Contain  ${subj}  ${SPAM_NOTIF_SUBJ}
    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCOED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{LIST_OF_URLS}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Release' in "${url}"
      ...  Exit For Loop
    END
    ${release_url}=  Set Variable  ${url}
    Release Message Through Email Links  ${release_url}
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Search' in "${url}"
      ...  Exit For Loop
    END
    ${search_url}=  Set Variable  ${url}
    Search and Delete Message Through Email links  ${search_url}
    Message Unload
    NUll Smtpd Stop

    Go To  https://${DUT}
    #Set Test Variable   ${expected}  3
    #Euq Spam Quarantine Search  ${expected}
    Euq Spam Quarantine Search

    #Message Delete And Release
    Selenium Close

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
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    ${amp}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  exp_count=${amp_count}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Amp Email Count  mesg_count=${amp_count}  col_value=5
    Selenium Close

Tvh1437033c
    [Tags]  interop  Tvh1437033c
    [Documentation]  Create some users under "users" page with saml admin.
    ...  link:https://tims.cisco.com/view-entity.cmd?ent=1437033
    ...  create some users unders "users" page
    ...  and validate that saml admin able to create the users.
    [Setup]  General Test Case Setup

    Library Order SMA
    Selenium Login
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    FOR  ${user}  ${full_name}  ${role}  IN
    ...   ${user_name1}  ${full_user_name1}  OPERATOR
    ...   ${user_name2}  ${full_user_name2}  GUEST
      Users Add User  ${user}  ${full_name}  ${DUT_ADMIN_SSW_PASSWORD}  user_role=${sma_user_roles.${role}}
    END
    Commit Changes
    Selenium Close
