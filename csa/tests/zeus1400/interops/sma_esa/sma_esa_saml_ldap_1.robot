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
Resource     email_interop_resource.txt
Resource     sma/esasma.txt
Resource     sma/saml.txt
Library      OperatingSystem
Library      SeleniumLibrary

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Set Appliance Under Test to SMA
...  Initialize Suite

Suite Teardown  Finalize Suite

*** Variables ***
${SPAM_NOTIF_SUBJ}=  Spam Quarantine Notification
${TEST_EUQ_SP_PROFILE}=  euq_sp_profile
${TEST_EUQ_IDP_PROFILE}=   euq_idp_profile
${DATA_UPDATE_TIMEOUT}=  20m
${RETRY_TIME}=  15s
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${spam_qxpath}=  //a[@title='Spam Quarantine (open in new window)']
${expected_count}=  2
${spam_select}  //tbody[@class="yui-dt-data"]/tr[1]/td[1]/div/input
${MAIL}  newuser@${CLIENT}
${MAIL_LOCAL_ADDRESS}  newuser1@${CLIENT}

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

    LDAP Client Connect  ${LDAP_AUTH_SERVER}
    ...  ldap_server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  basedn=${LDAP_BASEDN}
    ...  binddn=${LDAP_BINDDN}
    ...  password=${LDAP_PASSWORD}
    LDAP Client Create User  uid=newuser  password=${PASSWORD}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}  mail=${MAIL}
    ...  mail_local_address=${MAIL_LOCAL_ADDRESS}

    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure

    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
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
    ...  spam_notif_enable_login=${True}

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

    ${test_result} =  LDAP Run ISQ Alias Consolidation Query Test
    ...   ${LDAP_AUTH_SERVER}  ${MAIL_LOCAL_ADDRESS}
    Log  ${test_result}
    Should Contain  ${test_result}  ${MAIL}
    ${dut_hostname}  ${domain}=  Split String  ${DUT}  .

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
    Log Out of DUT
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
    Commit Changes
    @{addrs}=  Create List  ${MAIL_LOCAL_ADDRESS}
    ${addrs_file}=  Join Path  ${SUITE_TMP_DIR}  addr.txt
    Set Suite Variable  ${addrs_file}
    OperatingSystem.Create File  ${addrs_file}
    FOR  ${addr}  IN  @{addrs}
      OperatingSystem.Append to File  ${addrs_file}  ${addr}\n
    END

Finalize Suite
    Ldap Client Delete User  newuser
    Ldap Client Disconnect
    Run Keyword And Ignore Error  Remove Directory  ${SUITE_TMP_DIR}  recursive=${True}
    Set Appliance Under Test To ESA
    FOR  ${appliance}  IN  @{esa_appliances}
      Clear Email Tracking Reporting Data
      Library Order ${appliance}
      Selenium Close
    END
    DefaultTestSuiteTeardown

    Set Appliance Under Test To SMA
    DefaultTestSuiteTeardown

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  address-list=${addrs_file}:${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

Do Tvh1337864c Setup
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
    Run Keyword And Ignore Error  Capture Page Screenshot
    ${title_var}        Get Window Titles
    Select Window       title=@{title_var}[1]

Do Tvh1337864c Teardown
    Close Window
    Selenium Close
    DefaultTestCaseTeardown

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
    Click Element  ${spam_select}
    ${res}=  Quarantines Spam Message Delete
    Log  ${res}
    Should Contain  ${res}  Success
    Capture Page Screenshot

    Click Element  ${spam_select}
    ${res}=  Quarantines Spam Message Release
    Log  ${res}
    Should Contain  ${res}  Success
    Capture Page Screenshot

Check Spam Count
    [Arguments]  ${expected}=${expected_count}
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  date_range=week
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} != ${expected}  Fail
    [Return]  ${actual_spam_count}

*** Test Cases ***

Tvh1339871c
    [Tags]  interop  Tvh1339871c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA.
    ...  link:https://tims.cisco.com/view-entity.cmd?ent=1339871
    ...  1.Log in to SMA appliance with admin credential.
    ...  2. Navigate to Management Appliance ->Centralised Services -> Spam Quarantine.
    ...  4. Click on "Edit Settings".
    ...  5.In Edit Spam Quarantine page
    ...  a. Enable End-User Quarantine Access and configure it to use SAML2.0
    ...  d. Enable Spam Notification
    ...  6. in Spam Notification Section -> enter the below settings
    ...  a. enter the from address
    ...  b. Enter email address in 'Deliver Bounce Message To' section.
    ...  c. select the Notification schedule
    ...  7. Click on submit.
    ...  8. Navigate to System Administration -> LDAP and add a server profile with OpenLDAP as Server Type.
    ...  9. Enable "Spam Quarantine End-User Authentication Query" and check the box "Designate as the active query".
    ...  10. Click on submit.
    ...  11. Navigate to System Administration -> SAML.
    ...  a. Add Service Provider with proper SP Certificate, Private Key and passphrase.
    ...  b. Add Identity Provider with IDP metadata.
    ...  12. Commit changes
    ...  13. Go to Network tab -> IP interfaces -> click on management interface
    ...  14. Enter the spam quarantine port for 'HTTPS' .
    ...  15. Enter the end user spam quarantine URL
    ...  16. Click on submit and commit changes
    ...  17. Click on the "your email quarantine" link in the Spam Notification mail.
    ...  18. Click on any of the mail
    ...  Verify
    ...  1. Spam quarantine settings will be enbled and configured successfully. And spam quarantine page should open in the defined url.
    ...  2. Spam quarantine mails should get delivered to the mentioned email id in Spam Notification section.
    ...  3. End user should be able to view all Spam quarantine mails.
    ...  4. Mail details should be displayed.
    [Setup]  Do Tvh1337864c Setup
    [Teardown]  Do Tvh1337864c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    @{rcpt_header}=  Create List  To  ${MAIL}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_test1.mbox  ${PUBLIC_LISTENER.ipv4}
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
    Verify Message Headers  ${ENCOED_MAIL_CONTENT}  @{rcpt_header}
    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCOED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{LIST_OF_URLS}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    ${cnt}=  Get Length  ${LIST_OF_URLS}
    Log  ${cnt}
    Should Be Equal As Numbers  ${cnt}  5
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Detail' in "${url}"
      ...  Check Detail Message Through Email Links  ${url}
    END
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Search' in "${url}"
      ...  Exit For Loop
    END
    Search Action Message Through Email links  ${url}  Release
    Search Action Message Through Email links  ${url}  Delete
    Message Unload
    NUll Smtpd Stop
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${expected_count}
    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@cisco.com.* >= ${expected_count}

Tvh1339873c
    [Tags]  interop  Tvh1339873c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA
    ... link:https://tims.cisco.com/view-entity.cmd?ent=1339873
    ... 1. Go to Network tab -> IP interfaces -> click on management interface
    ... 2. Enter the spam quarantine port for 'HTTPS' .
    ... 3. Enter the end user spam quarantine URL
    ... 4. Click on submit and commit changes
    ... 5. Send spam mails through ESA to have them at SMA
    ... 6. Click on the Legacy spam quarantine link from spam notification mail
    ... 7. Perform Release and Delete action
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    Go To Spam Quarantine
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
    ${cnt}=  Get Length  ${LIST_OF_URLS}
    Log  ${cnt}
    Should Be Equal As Numbers  ${cnt}  5
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Detail' in "${url}"
      ...  Check Detail Message Through Email Links  ${url}
    END
    Message Unload
    NUll Smtpd Stop

    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${expected_count}
    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@${CLIENT}.* >= ${expected_count}
    Message Delete And Release
