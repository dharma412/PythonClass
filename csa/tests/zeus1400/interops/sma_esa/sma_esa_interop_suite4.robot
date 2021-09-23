# $Id: $ $DateTime: $ $Author: $

*** Settings ***
Resource     esa/injector.txt
Resource     regression.txt
Resource     sma/esasma.txt
Resource     email_interop_resource.txt

Suite Setup  Do Suite Setup
Suite Teardown  Finalize Suite

*** Variables ***
${SESSION_TIMEOUT}         1440
${DATA_UPDATE_TIMEOUT}=  30m
${RETRY_TIME}=  30s
${SENDER1}=  abc@ironport.com
${SENDER2}=  def@ironport.com
${expected_count}  0
${TESTs_ID}  Tvh123456
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${PROFILE_NAME} =  smaesa_interop
${SPAM_NOTIF_SUBJ}=  Spam Quarantine Notification
${SLBL spam negative}=  SLBL spam negative
${SLBL spam positive}=  SLBL spam positive
${ldap_user}  ldapinteropuser
${PASSWORD}  ironport

*** Keywords ***

Do Suite Setup
    Library Order ESA
    DefaultRegressionSuiteSetup
    ${ESA_PUBLIC_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUBLIC_LISTENER_IP}
    Smtp Routes New  domain=ALL  dest_hosts=/dev/null
    Message Tracking Enable  tracking=centralized
    Centralized Email Reporting Enable
    ${local_spam_quarantine_enabled}=  Quarantines Spam Is Enabled
    Run Keyword If  ${local_spam_quarantine_enabled}  Quarantines Spam Disable
    EUQ Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    Antispam Enable  IronPort
    ${settings}=  Create Dictionary  Positive Spam Apply Action  Spam Quarantine
    Mail Policies Edit Antispam  incoming  default  ${settings}
    Commit Changes
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes
    ${dut_hostname}  ${domain}=  Split String  ${DUT}  .
    Set Suite Variable  ${RECIPIENT_ADDRESS}  xyz@ironport.${domain}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Run Keyword And Ignore Error  Null Smtpd Stop
      Null Smtpd Start
      Roll Over Now  mail_logs
    END
    Library Order SMA
    Selenium Login
    Network Access Edit Settings  ${SESSION_TIMEOUT}
    Clean System Quarantines
    Spam Quarantine Enable
    Spam Quarantine Edit
    ...  interface=Management
    ...  port=6025
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_fname=${TESTs_ID}@${CLIENT}
    ...  spam_notif_freq=daily
    ...  spam_notif_week_day=${None}
    ...  spam_notif_days=Mon, Tue, Wed, Thu, Fri, Sat, Sun
    ...  spam_notif_hours=03,15,21
    ...  spam_notif_baddr=test@${CLIENT}
    Spam Quarantine SlBl Enable
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    ${ISQ_URL}=  Catenate  SEPARATOR=  https://  ${DUT}  :83
    Set Suite Variable  ${ISQ_URL}
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp()  tempfile
    Set Suite Variable  ${MAIL}  ${ldap_user}@${CLIENT}
    Set Suite Variable  ${MAIL_LOCAL_ADDRESS}  ldapinterop@${CLIENT}

    LDAP Client Connect  ${LDAP_AUTH_SERVER}
    ...  ldap_server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  basedn=${LDAP_BASEDN}
    ...  binddn=${LDAP_BINDDN}
    ...  password=${LDAP_PASSWORD}
    LDAP Client Create User  uid=${ldap_user}  password=${PASSWORD}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}  mail=${MAIL}
    ...  mail_local_address=${MAIL_LOCAL_ADDRESS}

    @{addrs}=  Create List  ${MAIL_LOCAL_ADDRESS}
    ${addrs_file}=  Join Path  ${SUITE_TMP_DIR}  addr.txt
    Set Suite Variable  ${addrs_file}
    OperatingSystem.Create File  ${addrs_file}
    FOR  ${addr}  IN  @{addrs}
        OperatingSystem.Append to File  ${addrs_file}  ${addr}\n
    END
    Set Suite Variable  ${SUITE_TMP_DIR}
    IP Interfaces Edit  Management  isq_https_service=83  isq_default=https://${DUT}:83/  hostname=${DUT}
    Ldap Add Server Profile
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}
    ...  base_dn=${LDAP_BASEDN}
    ...  auth_method=anonymous
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    Ldap Edit Isq End User Authentication Query
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}.isq_auth
    ...  (uid={u})
    ...  mail
    ...  ${True}
    Ldap Edit Isq Alias Consolidation Query
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}.isq_consolidate
    ...  (mailLocalAddress={a})
    ...  mail
    ...  ${True}
    Spam Quarantine Edit EndUser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=None
    Commit Changes
    Spam Quarantine Delete Message
    ${esa_cnt}=  Get Length  ${esa_appliances}
    Set Suite Variable  ${esa_cnt}

Finalize Suite
    Ldap Client Delete User  ${ldap_user}
    Ldap Client Disconnect
    Run Keyword And Ignore Error  Remove Directory  ${SUITE_TMP_DIR}  recursive=${True}
    DefaultRegressionSuiteTeardown

Clear Email Tracking Reporting Data
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Start CLI Session If Not Open
      Roll Over Now
      Commit
      Diagnostic Reporting Delete Db  confirm=yes
      Wait Until Ready
      Diagnostic Tracking Delete Db   confirm=yes
      Wait Until Ready
    END
    Library Order Sma
    Start CLI Session If Not Open
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}  ${num_msgs}=1
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  address-list=${addrs_file}:${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

Spam Quarntine Search
    [Arguments]  ${date_range}=today  ${count}=${expected_count}
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  is_admin=${False}  date_range=${date_range}
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} == ${count}  Fail
    [Return]  ${actual_spam_count}

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

Spam Quarantine Delete Message
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To  https://${DUT}:83
    Run Keyword And Ignore Error
    ...  Log Into DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week
    Commit Changes

Edit Ldap Server Profile
    [Arguments]  ${server_type}  ${end_user_auth}
    Ldap Edit Server Profile
    ...  ${PROFILE_NAME}
    ...  hostname=${LDAP_AUTH_SERVER}
    ...  auth_method=anonymous
    ...  server_type=${server_type}
    ...  port=${LDAP_AUTH_PORT}
    Spam Quarantine Edit EndUser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=${end_user_auth}
    Commit Changes

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

Login To ISQ
    [Arguments]  ${user}
    ...  ${password}
    Selenium Close
    Set Appliance Under Test to SMA
    Set Up Selenium Environment
    Launch DUT Browser  url=${ISQ_URL}
    Log Into DUT  ${user}  ${password}

Database Sync for Safelist Or Blocklist
    [Arguments]  ${listtype}  ${address}  ${senders}
    Login To ISQ
    ...  ${DUT_ADMIN}
    ...  ${DUT_ADMIN_SSW_PASSWORD}

    Add SLBL admin and Verify
    ...  ${listtype}
    ...  ${address}
    ...  ${senders}

    Set Appliance Under Test to ESA
    Roll Over Now  mail_logs
    Sleep  5s  msg=Wait for logs roll over

    Set Appliance Under Test to SMA
    Selenium Login
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

Inject Message And Verify Log
    [Arguments]  ${mbox-filename}  ${mail-from}  ${spam_negative}
    Inject Messages
    ...  mbox-filename=${mbox-filename}
    ...  mail-from=${mail-from}
    ...  address-list=${rcpts}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    Verify And Wait For Log Records
    ...  MID .* ICID .* From: .*${mail-from}.* >= 1
    ...  MID .* using engine.* ${spam_negative} >= 1

Euq Spam Quarantine Search
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Go To  https://${DUT}:83
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week
    Log  ${spam_count}
    [Return]  ${spam_count}

Verify Headers In Message
    [Arguments]  @{varargs}
    [Documentation]  Accepts multiple named arguments.\n
    ...  Argument is header name to get value from.\
    ...  Value is expected header's value.
    ...  This keyword gets drained message, gets headers and compares values.
    Message Unload
    ${msg}=  Null Smtpd Next Message  timeout=60
    Message Load  ${msg}
    ${headers}=  Message Items
    Log Dictionary  ${headers}
    FOR  ${arg}  IN  @{varargs}
      ${k}  ${v}=  Split String  ${arg}  =  1
      ${header_value}=  Message Get  ${k}
      Should Be Equal As Strings  ${header_value}  ${v}
    END

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

*** Test Cases ***

Tvh1235450c
    [Tags]  interop  Tvh1235450c  Tvh1235451c  Tvh1330304c
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
    Set Appliance Under Test To ESA
    Start Cli Session If Not Open
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Set Test Variable   ${LIST_TYPE1}  Safelist
    Library Order SMA
    Selenium Login
    ${rcpts}=  Database Slbl Sync  ${LIST_TYPE1}  ${LIST_TYPE1}_1_${SENDER1}
    Set Test Variable   ${rcpts}

    Inject Message And Verify Log
    ...  ${SPAM}
    ...  ${LIST_TYPE1}_1_${SENDER1}
    ...  ${SLBL spam negative}

    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Incoming Mail Details  column=Spam Detected  col_index=0  count=0

    ${messages}=  Email Message Tracking Search
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Strings  ${tracking_message_count}  1

    Set Test Variable   ${LIST_TYPE2}  Blocklist
    ${rcpts}=  Database Slbl Sync  ${LIST_TYPE2}  ${LIST_TYPE2}_2_${SENDER2}

    Inject Message And Verify Log
    ...  ${CLEAN}
    ...  ${LIST_TYPE2}_2_${SENDER2}
    ...  ${SLBL spam positive}

    Library Order SMA
    Selenium Login
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Incoming Mail Details  column=Spam Detected  col_index=0  count=1

    ${spam_count}=  Euq Spam Quarantine Search
    Should Be Equal As Strings  ${spam_count}  1

    Login To ISQ
    ...  ${DUT_ADMIN}
    ...  ${DUT_ADMIN_SSW_PASSWORD}
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
    ...  MID ${mid} .* .*test@${CLIENT}.* >= ${esa_cnt}

    ${msg}=  Null Smtpd Next Message  timeout=60
    Message Load  ${msg}
    ${subj}=  Message Get  Subject
    Should Contain  ${subj}  ${SPAM_NOTIF_SUBJ}

    Selenium Login
    ${spam_count}=  Euq Spam Quarantine Search
    Should Be Equal As Strings  ${spam_count}  3

    Message Delete And Release

Tvh1337865c
    [Tags]  interop  Tvh1337865c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA - Using LDAP as
    ...  authentication method with Active Directory as authentication server
    ...  check release and delete functionality when..
    ...  "Enable login without credentials for quarantine access" is  Unchecked
    ...  Log in to SMA appliance with admin credential.
    ...  Navigate to Management Appliance ->Centralised Services -> Spam Quarantine.
    ...  Click on "Edit Settings".
    ...  In Edit Spam Quarantine page
    ...  a. Enable End-User Quarantine Access and configure it to use LDAP
    ...  b. Enable Spam Notification
    ...  In Spam Notification Section -> enter the below settings
    ...  a. enter the from address
    ...  b. Enter email address in 'Deliver Bounce Message To' section.
    ...  c. select the Notification schedule
    ...  Click on submit.
    ...  Navigate to System Administration -> LDAP and add a server profile with Active Directory as Server Type.
    ...  Enable "Spam Quarantine End-User Authentication Query" and check the box "Designate as the active query".
    ...  Click on submit.
    ...  Commit changes
    ...  Go to Network tab -> IP interfaces -> click on management interface
    ...  Enter the spam quarantine port for 'HTTPS' .
    ...  Enter the end user spam quarantine URL
    ...  Click on submit and commit changes
    ...  Click on the "your email quarantine" link in the Spam Notification mail.
    ...  Click on any of the mail
    ...  Spam quarantine settings will be enbled and configured successfully.
    ...  And spam quarantine page should open in the defined url.
    ...  Spam quarantine mails should get delivered to the mentioned email id in Spam Notification section.
    ...  End user should be able to view all Spam quarantine mails.
    ...  Mail details should be displayed.

    Set Test Variable   ${TEST_ID}  ${TEST_NAME}
    Set Appliance Under Test To ESA
    Start Cli Session If Not Open
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Library Order SMA
    Selenium Login
    Edit Ldap Server Profile  Active Directory  LDAP
    Spam Quarantine Delete Message
    Library Order ESA
    Start CLI Session If Not Open
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
    Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    Library Order SMA
    Force ISQ Notifications
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${esa_cnt}

    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@${CLIENT}.* >= ${esa_cnt}

    Wait Until Keyword Succeeds
    ...  5 min
    ...  0 sec
    ...  Verify Headers In Message
    ...  Subject=${SPAM_NOTIF_SUBJ}

    Selenium Login
    ${spam_count}=  Euq Spam Quarantine Search
    Should Be Equal As Strings  ${spam_count}  2
    Go To  https://${DUT}:83
    Log out of DUT
    Log Into DUT  ${ldap_user}  ${PASSWORD}

Tvh1339959c
    [Tags]  interop  Tvh1339959c  Tvh1340029c  Tvh1340110c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA - Using LDAP as
    ...  authentication method with Active Directory as authentication server when "Enable
    ...  login without credentials for quarantine access" is checked and check release
    ...  and delete functionality
    ...  Log in to SMA appliance with admin credential.
    ...  Navigate to Management Appliance ->Centralised Services -> Spam Quarantine.
    ...  Click on ""Edit Settings"".
    ...  In Edit Spam Quarantine page
    ...    a. Enable End-User Quarantine Access and configure it to use LDAP
    ...    d. Enable Spam Notification
    ...  in Spam Notification Section -> enter the below settings
    ...     a. enter the from address
    ...     b. Enter email address in 'Deliver Bounce Message To' section.
    ...     c. select the Notification schedule
    ...  Click on submit.
    ...  Navigate to System Administration -> LDAP and add a server profile with Active Directory as Server Type.
    ...  Enable ""Spam Quarantine End-User Authentication Query"" and
    ...  check the box ""Designate as the active query"".
    ...  Click on submit.
    ...  Go to Network tab -> IP interfaces -> click on management interface
    ...  Enter the spam quarantine port for 'HTTPS' .
    ...  Enter the end user spam quarantine URL
    ...  Click on submit and commit changes
    ...  Click on the legacy spam quarantine link in the Spam Notification mail
    ...  Expected Result :
    ...  Spam quarantine settings will be enbled and configured successfully.
    ...  And spam quarantine page should open in the defined url.
    ...  Spam quarantine mails should get delivered to the mentioned email id in Spam Notification section.
    ...  End user should be able to view all Spam quarantine mails.

    Set Test Variable   ${TEST_ID}  ${TEST_NAME}
    Set Appliance Under Test To ESA
    Start Cli Session If Not Open
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Library Order SMA
    Selenium Login
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_fname=${ALERT_RCPT}
    ...  spam_notif_freq=daily
    ...  spam_notif_week_day=${None}
    ...  spam_notif_days=Mon, Tue, Wed, Thu, Fri, Sat, Sun
    ...  spam_notif_hours=03,15,21
    ...  spam_notif_baddr=test@${CLIENT}
    ...  spam_notif_enable_login=${True}
    Commit Changes

    Edit Ldap Server Profile  Active Directory  LDAP
    Spam Quarantine Delete Message
    Library Order ESA
    Run Keyword And Ignore Error  Null Smtpd Stop
    Null Smtpd Start
    Roll Over Now  mail_logs
    Start CLI Session If Not Open
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
    Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    ${addr_from}=  Set Variable  me@${CLIENT}
    ${TMP_DIR}=  Evaluate  tempfile.mkdtemp()  tempfile
    Set Test Variable  ${TMP_DIR}
    ${main_message}=  Message Builder Create MIMEMultipart  subtype=related
    Message Builder Add Headers  ${main_message}
    ...  From=${addr_from}
    ...  Sender=${addr_from}
    ...  To=user@${CLIENT}
    ...  Reply-To=${addr_from}
    ...  Subject=For user
    ...  X-Advertisement=spam
    ${mbox_path}=  Join Path  ${TMP_DIR}  user_spam.mbox
    Create MBOX Containing Message  ${mbox_path}  ${main_message}
    Inject Custom Message  ${mbox_path}  ${PUBLIC_LISTENER.ipv4}  3
    Library Order SMA
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week
    Log  ${spam_count}
    Force ISQ Notifications
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${esa_cnt}

    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@${CLIENT}.* >= ${esa_cnt}

    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}
    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCOED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{LIST_OF_URLS}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Search' in "${url}"
      ...  Exit For Loop
    END
    Search Action Message Through Email links  ${url}  Release
    Search Action Message Through Email links  ${url}  Delete
    Search Action Message Through Email links  ${url}  Release Safelist
    ...  LDAP  ${MAIL}  ${PASSWORD}
    Message Unload

Tvh1340099c
    [Tags]  interop  Tvh1340099c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA - Using LDAP as
    ...  authentication method with Active Directory as authentication server when "Enable
    ...  login without credentials for quarantine access" is Unchecked and check release
    ...  and delete functionality
    ...  Log in to SMA appliance with admin credential.
    ...  Navigate to Management Appliance ->Centralised Services -> Spam Quarantine.
    ...  Click on ""Edit Settings"".
    ...  In Edit Spam Quarantine page
    ...    a. Enable End-User Quarantine Access and configure it to use LDAP
    ...    d. Enable Spam Notification
    ...  in Spam Notification Section -> enter the below settings
    ...     a. enter the from address
    ...     b. Enter email address in 'Deliver Bounce Message To' section.
    ...     c. select the Notification schedule
    ...  Click on submit.
    ...  Navigate to System Administration -> LDAP and add a server profile with Active Directory as Server Type.
    ...  Enable ""Spam Quarantine End-User Authentication Query"" and check the box ""Designate as the active query""
    ...  and checked "Spam Quarantine Alias Consolidation Query'
    ...  Click on submit.
    ...  Go to Network tab -> IP interfaces -> click on management interface
    ...  Enter the spam quarantine port for 'HTTPS' .
    ...  Enter the end user spam quarantine URL
    ...  Click on submit and commit changes
    ...  Click on the legacy spam quarantine link in the Spam Notification mail and
    ...  provide valid credentials to log in
    ...  Select 1 mail and perform release functionality
    ...  Select 1 mail and perform delete functionality
    ...  Expected Result :
    ...  1. Spam quarantine settings will be enbled and configured successfully.
    ...  And spam quarantine page should open in the defined url.
    ...  2. Spam quarantine mails should get delivered to the mentioned email id in Spam Notification section.
    ...  3. End user should be able to view all Spam quarantine mails.
    ...  4. After step 17, 1 mail should get released from spam quarantine
    ...  5. After step 18, 1 mail should get deleted from spam quarantine

    Set Test Variable   ${TEST_ID}  ${TEST_NAME}
    Set Appliance Under Test To ESA
    Start Cli Session If Not Open
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Library Order SMA
    Selenium Login
    Spam Quarantine Edit Notification
    ...  spam_notif_enable_login=${False}
    Edit Ldap Server Profile  Active Directory  LDAP
    Spam Quarantine Delete Message
    Library Order ESA
    Start CLI Session If Not Open
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
    Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}

    Library Order SMA
    Force ISQ Notifications
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${esa_cnt}

    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@${CLIENT}.* >= ${esa_cnt}

    Selenium Login
    ${spam_count}=  Euq Spam Quarantine Search
    Should Be Equal As Strings  ${spam_count}  2

    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}
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

Tvh1339886c
    [Tags]  interop  Tvh1339886c  Tvh1339883c  Tvh1339888c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA
    ...  Using LDAP as authentication method with LDAP as authentication server
    ...  and check release and delete functionality when "Enable login without
    ...  credentials for quarantine access"  is  checked
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1339886
    ...  Preconditions:
    ...  1.ESA and SMA have been netinstalled with the latest version .
    ...  2.Load license has been done via CLI .
    ...  3.SPAM Quarantine has been enabled on SMA .
    ...  4.ESA is added to SMA.
    ...  5."Enable login without credentials for quarantine access" is checked
    ...  Steps :
    ...  1.Log in to SMA appliance with admin credential.
    ...  2.Navigate to Management Appliance ->Centralised Services -> Spam Quarantine.
    ...  3.Click on ""Edit Settings"".
    ...  4.In Edit Spam Quarantine page
    ...  a.Enable End-User Quarantine Access and configure it to use LDAP
    ...  b.Enable Spam Notification
    ...  6.in Spam Notification Section -> enter the below settings
    ...  a.enter the from address
    ...  b.Enter email address in 'Deliver Bounce Message To' section.
    ...  c.select the Notification schedule
    ...  7.Click on submit.
    ...  8.Navigate to System Administration -> LDAP and add a server profile
    ...   with openLDAP as Server Type.
    ...  9.Enable ""Spam Quarantine End-User Authentication Query""
    ...   and check the box ""Designate as the active query"".
    ...  10.Click on submit.
    ...  11.Commit changes
    ...  12.Go to Network tab -> IP interfaces -> click on management interface
    ...  13.Enter the spam quarantine port for 'HTTPS' .
    ...  14.Enter the end user spam quarantine URL
    ...  15.Click on submit and commit changes
    ...  16.Click on the legacy spam quarantine link in the Spam Notification mail
    ...  17.Select 1 mail and do release
    ...  18.Select 1 mail and perform delete
    ...  Expected Result :
    ...  1.Spam quarantine settings will be enbled and configured successfully.
    ...  And spam quarantine page should open in the defined url.
    ...  2.Spam quarantine mails should get delivered to the mentioned email id
    ...  in Spam Notification section.
    ...  3.End user should be able to view all Spam quarantine mails.
    ...  4.After step 17, 1 mail should get released from spam quarantine
    ...  5.After step 18, 1 mail should get deleted from spam quarantine

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Library Order SMA
    Selenium Login
    Spam Quarantine Delete Message
    Library Order ESA
    Run Keyword And Ignore Error  Null Smtpd Stop
    Null Smtpd Start
    Clean System Quarantines
    Roll Over Now  mail_logs
    Start CLI Session If Not Open
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
    Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    ${addr_from}=  Set Variable  me@${CLIENT}
    ${TMP_DIR}=  Evaluate  tempfile.mkdtemp()  tempfile
    Set Test Variable  ${TMP_DIR}
    ${main_message}=  Message Builder Create MIMEMultipart  subtype=related
    Message Builder Add Headers  ${main_message}
    ...  From=${addr_from}
    ...  Sender=${addr_from}
    ...  To=user@${CLIENT}
    ...  Reply-To=${addr_from}
    ...  Subject=For user
    ...  X-Advertisement=spam
    ${mbox_path}=  Join Path  ${TMP_DIR}  user_spam.mbox
    Create MBOX Containing Message  ${mbox_path}  ${main_message}
    Inject Custom Message  ${mbox_path}  ${PUBLIC_LISTENER.ipv4}  3
    Library Order SMA
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week
    Force ISQ Notifications
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${expected_count}

    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@${CLIENT}.* >= ${expected_count}

    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}
    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCOED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{LIST_OF_URLS}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Search' in "${url}"
      ...  Exit For Loop
    END
    Search Action Message Through Email links  ${url}  Release
    Search Action Message Through Email links  ${url}  Delete
    Search Action Message Through Email links  ${url}  Release Safelist
    ...  LDAP  ${MAIL}  ${PASSWORD}
    Message Unload

Tvh1339885c
    [Tags]  interop  Tvh1339885c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA.
    ...  Using LDAP as authentication method with LDAP as authentication server
    ...  and check release and delete functionality when "Enable login without
    ...  credentials for quarantine access" is  unchecked
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1339885
    ...  Preconditions:
    ...  1.ESA and SMA have been netinstalled with the latest version .
    ...  2.Load license has been done via CLI .
    ...  3.SPAM Quarantine has been enabled on SMA .
    ...  4.ESA is added to SMA.
    ...  5."Enable login without credentials for quarantine access" is Unchecked
    ...  Steps :
    ...  1.Log in to SMA appliance with admin credential.
    ...  2.Navigate to Management Appliance ->Centralised Services -> Spam Quarantine.
    ...  3.Click on ""Edit Settings"".
    ...  4.In Edit Spam Quarantine page
    ...  a.Enable End-User Quarantine Access and configure it to use LDAP
    ...  d.Enable Spam Notification
    ...  5.in Spam Notification Section -> enter the below settings
    ...  a.enter the from address
    ...  b.Enter email address in 'Deliver Bounce Message To' section.
    ...  c.select the Notification schedule
    ...  6.Click on submit.
    ...  7.Navigate to System Administration -> LDAP and add a server profile with
    ...   openLDAP as Server Type.
    ...  8.Enable ""Spam Quarantine End-User Authentication Query"" and check the box
    ...   ""Designate as the active query""and checked "Spam Quarantine Alias Consolidation Query"
    ...  9.Click on submit.
    ...  10.Commit changes
    ...  11.Go to Network tab -> IP interfaces -> click on management interface
    ...  12.Enter the spam quarantine port for 'HTTPS' .
    ...  13.Enter the end user spam quarantine URL
    ...  14.Click on submit and commit changes
    ...  15.Click on the legacy spam quarantine link in the Spam Notification mail
    ...   and pro
    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Library Order SMA
    Start Cli Session If Not Open
    Roll Over Now  mail_logs
    Selenium Login
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_fname=${ALERT_RCPT}
    ...  spam_notif_freq=daily
    ...  spam_notif_week_day=${None}
    ...  spam_notif_days=Mon, Tue, Wed, Thu, Fri, Sat, Sun
    ...  spam_notif_hours=03,15,21
    ...  spam_notif_baddr=test@${CLIENT}
    ...  spam_notif_enable_login=${False}
    Commit Changes
    Spam Quarantine Delete Message
    Clear Email Tracking Reporting Data
    Library Order ESA
    Run Keyword And Ignore Error  Null Smtpd Stop
    Null Smtpd Start
    Clean System Quarantines
    Roll Over Now  mail_logs
    Start CLI Session If Not Open
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
    Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    Library Order SMA
    Force ISQ Notifications
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${expected_count}
    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@${CLIENT}.* >= ${expected_count}
    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}
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
    :FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Search' in "${url}"
      ...  Exit For Loop
    END
    ${search_url}=  Set Variable  ${url}
    Search and Delete Message Through Email links  ${search_url}
    Message Unload
    Run Keyword And Ignore Error  Null Smtpd Stop
    Spam Quarantine Delete Message
