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
${mbox.SPAM}=    %{SARF_HOME}/tests/testdata/esa/antispam/spam.mbox
${SPAM_NOTIF_SUBJ}=  Spam Quarantine Notification


*** Keywords ***
Initialize Suite
    global_sma.DefaultTestSuiteSetup
    ${SMA_ORIG_CONF}=  Save Config
    Set Suite Variable  ${SMA_ORIG_CONF}
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

    Ldap Add Server Profile
    ...  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_AUTH_SERVER}
    ...  base_dn=${LDAP_BASEDN}
    ...  auth_method=anonymous
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}

    Ldap Edit Isq Alias Consolidation Query
    ...  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_AUTH_SERVER}.isq_consolidate
    ...  (mailLocalAddress={a})
    ...  mail
    ...  ${True}

    ${res}=  Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  isq=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Log  ${res}
    Commit Changes

    Clean System Quarantines
    Roll Over Now  mail_logs

    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup
    ...  should_revert_to_initial=${False}
    ${ESA_ORIG_CONF}=  Save Config
    Set Suite Variable  ${ESA_ORIG_CONF}

    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    ${ESA_PUB_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${ESA_PUB_LISTENER}
    Clean System Quarantines
    Quarantines Spam Disable
    Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    Commit Changes
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp(dir="%{SARF_HOME}/tmp")  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}

Finalize Suite
    Run Keyword And Ignore Error  Remove Directory  ${SUITE_TMP_DIR}  recursive=${True}

    Set Appliance Under Test To ESA
    Restore Config From ${ESA_ORIG_CONF}
    DefaultTestSuiteTeardown

    Set Appliance Under Test To SMA
    Restore Config From ${SMA_ORIG_CONF}
    DefaultTestSuiteTeardown

Create File With Recipients List
    [Arguments]  @{addrs}
    ${rnd}=  String.Generate Random String
    ${addr_file}=  Join Path  ${SUITE_TMP_DIR}  ${rnd}.txt
    OperatingSystem.Create File  ${addr_file}
    :FOR  ${addr}  IN  @{addrs}
    \  OperatingSystem.Append to File  ${addr_file}  ${addr}\n
    [Return]  ${addr_file}

Login To WebUI
    [Arguments]  ${dut}
    Set Appliance Under Test to ${dut}
    Selenium Close
    Selenium Login

Restore Config From ${file}
    ${res}=  Load Config From File  ${file}
    Commit  Loaded configuration from file: ${file}
    [Return]  ${res}

Initialize Tvh1344782c
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=None

    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_username=testuser
    ...  spam_notif_domain=cisco.com
    ...  spam_notif_enable_login=${False}
    ...  spam_notif_consolidate=${True}
    ...  spam_notif_baddr=mybounceaddress@${CLIENT}

Initialize Tvh1344781c
    Login To WebUI  SMA
    DefaultTestCaseSetup

Rollover Logs
    [Arguments]  ${logs}
    Roll Over Now  ${logs}
    Sleep  10s  msg=Wait for log rollover

Fetch Mail Content Using Drain
    ${MAIL_CONTENT}=  Wait Until Keyword Succeeds
    ...  3 min
    ...  0 sec
    ...  Verify And Wait For Mail In Drain  test_euq@${CLIENT}
         ...  Subject  ${SPAM_NOTIF_SUBJ}
    Log   ${MAIL_CONTENT}
    [Return]  ${MAIL_CONTENT}

Verify URL Auto Login Validation
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

Verify URL Force Login Validation
    [Arguments]  ${url}
    @{original_url}=  Split String    ${url}  '
    Log  @{original_url}[1]
    Go To  @{original_url}[1]
    ${current_url}=  Get Location
    Run Keyword And Ignore Error  Capture Screenshot
    Log  ${current_url}
    Should Contain  ${url}  ${current_url}
    Should Contain  ${current_url}  ${CLIENT_HOSTNAME}

*** Test Cases ***
Tvh1344781c
    [Documentation]  To verify that euq notification is generated with SAML\n
    ...  from Backend logs with enable login option in spam quarantine\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344781
    [Tags]  Tvh1344781c  srts
    [Setup]   Initialize Tvh1344781c
    [Teardown]    DefaultTestCaseTearDown
    Login To WebUI  ESA
    Rollover Logs  mail_logs

    Inject Messages
    ...  mbox-filename=${mbox.SPAM}
    ...  num-msgs=2
    ...  inject-host=${ESA_PUB_LISTENER_IP}
	...  rcpt-host-list=test_euq@${CLIENT}

    Verify Log Contains Records
      ...  interim verdict using engine: CASE spam positive >= 1

    Login To WebUI  SMA
    Rollover Logs  mail_logs
    Rollover Logs  euq_logs

    Null Smtpd Start
    Force ISQ Notifications
    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}

    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCOED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{LIST_OF_URLS}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    :FOR  ${url}  IN  @{LIST_OF_URLS}
    \  Run Keyword If  'Release' in "${url}"
    \  ...  Verify URL Auto Login Validation  ${url}
    Login To WebUI  SMA

    Message Unload
    NUll Smtpd Stop

    Verify Log Contains Records
    ...  search_path=/data/pub/euq_logs/euq.current
    ...  Notification sent: #recipients >= 1

    Verify Log Contains Records
    ...  search_path=/data/pub/mail_logs/mail.current
    ...  Start MID .*ICID .*ISQ Notification >= 1
    ...  MID .*ICID .*From: .*test@cisco.com >= 1
    ...  MID .*ICID .*RID .* To.*test_euq@${CLIENT} >= 1
    ...  Subject 'Spam Quarantine Notification' >= 1

Tvh1344782c
    [Documentation]  To verify that euq notification is generated with SAML Backend\n
    ...  logs without enable login option in spam quarantine.\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344782
    [Tags]  Tvh1344782c  srts
    [Setup]     Run Keywords
    ...  DefaultTestCaseSetup
    ...  Initialize Tvh1344782c
    [Teardown]    DefaultTestCaseTearDown
    Login To WebUI  ESA
    Rollover Logs  mail_logs

    Inject Messages
    ...  mbox-filename=${mbox.SPAM}
    ...  num-msgs=2
    ...  inject-host=${ESA_PUB_LISTENER_IP}
	...  rcpt-host-list=test_euq@${CLIENT}

    Verify Log Contains Records
      ...  interim verdict using engine: CASE spam positive >= 1

    Login To WebUI  SMA
    Rollover Logs  mail_logs
    Rollover Logs  euq_logs

    Null Smtpd Start
    Force ISQ Notifications
    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}

    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCOED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{LIST_OF_URLS}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    :FOR  ${url}  IN  @{LIST_OF_URLS}
    \  Run Keyword If  'Release' in "${url}"
    \  ...  Verify URL Force Login Validation  ${url}
    Login To WebUI  SMA

    Message Unload
    NUll Smtpd Stop

    Verify Log Contains Records
    ...  search_path=/data/pub/euq_logs/euq.current
    ...  Notification sent: #recipients >= 1

    Verify Log Contains Records
    ...  search_path=/data/pub/mail_logs/mail.current
    ...  Start MID .*ICID .*ISQ Notification >= 1
    ...  MID .*ICID .*From: .*test@cisco.com >= 1
    ...  MID .*ICID .*RID .* To.*test_euq@${CLIENT} >= 1
    ...  Subject 'Spam Quarantine Notification' >= 1