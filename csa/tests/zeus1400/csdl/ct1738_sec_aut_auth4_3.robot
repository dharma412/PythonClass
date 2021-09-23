# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/ct1738_sec_aut_auth4_3.txt#1 $
# $Date: 2020/10/29 $
# $Author: nthallap $

*** Settings ***
Resource     esa/backdoor_snippets.txt
Resource     esa/global.txt
Resource     esa/injector.txt
Resource     esa/logs_parsing_snippets.txt
Resource     esa/message_tracking.txt
Resource     regression.txt
Resource     sma/csdlresource.txt
Resource     sma/global_sma.txt
Resource     sma/esasma.txt
Resource     sma/config_masters.txt
Resource     ../build_acceptance_tests/sma_esa_interop/email_interop_resource.txt

Suite Setup  Initialize Suite
Suite Teardown  SuiteTeardown


*** Variables ***
${SPAM_FILE}=               %{SARF_HOME}/tests/testdata/esa/antispam/spam.mbox
${SPAM_NOTIF_SUBJ}=         Spam Quarantine Notification
${URL_TRACKING_SUBJ}=       Test With Mail Body
${BAD_RPT_URL}=             www.ihaveabadreputation.com
${DLP_TRACKING_SUBJ}=       DLP test for CC
${CREDITCARD_FILE}=         %{SARF_HOME}/tests/testdata/esa/dlp/credit_card.mbox
${EUQ_LOGS_PATH}=           /data/pub/euq_logs/euq.current
${MAIL_LOGS_PATH}=          /data/pub/mail_logs/mail.current
${SHOW_DETAILS_XPATH}=      //tr[@id='result_1']//a[normalize-space()='Show Details']@href


*** Keywords ***
Initialize Suite
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup
    ...  should_revert_to_initial=${False}
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    ${ESA_PR_LISTENER_IP}=  Get ESA Private IP
    Set Suite Variable  ${ESA_PR_LISTENER_IP}
    EsaCliLibrary.Smtp Routes New
    ...  domain=.${NETWORK}
    ...  dest_hosts=${CLIENT}
    Commit
    Quarantines Spam Disable
    Commit Changes
    Clean System Quarantines
    Message Tracking Enable  tracking=centralized
    Commit Changes
    Centralized Email Reporting Enable
    Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    Commit Changes
    ${ESA_ORIG_CONF}=  Save Config
    Set Suite Variable  ${ESA_ORIG_CONF}
    Selenium Close

    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup
    ${SMA_BASIC_CONF}=  Configuration File Save Config
    Set Suite Variable  ${SMA_BASIC_CONF}
    Initialize Users
    Add Users
    ${ISQ_URL}=  Catenate  SEPARATOR=  https://  ${SMA}  :83
    Set Suite Variable  ${ISQ_URL}
    Smtp Routes Add  .${NETWORK}  ${CLIENT}
    Commit Changes
    Diagnostic Tracking Delete DB
    Diagnostic Reporting Delete DB
    Clean System Quarantines
    Enable Centralized Services
    Add ESA To SMA
    Enable Euq

    ${SMA_ORIG_CONF}=  Configuration File Save Config
    Set Suite Variable  ${SMA_ORIG_CONF}

    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp(dir="%{SARF_HOME}/tmp")  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}

SuiteTeardown
    ${cli_result}=  Load Config From File   ${SMA_BASIC_CONF}
    Log  ${cli_result}
    Commit
    OperatingSystem.Empty Directory  ${SUITE_TMP_DIR}
    OperatingSystem.Remove Directory  ${SUITE_TMP_DIR}
    DefaultTestSuiteTeardown

Enable Centralized Services
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    Commit Changes

Add Users
    @{USERS_DETAILS}  Create List  ${TEST_USER15}   ${sma_user_roles.EMAIL_ADMIN}
                            ...  ${TEST_USER16}   ${sma_user_roles.WEB_ADMIN}
                            ...  ${TEST_USER17}   ${sma_user_roles.WEB_POLICY_ADMIN}
                            ...  ${TEST_USER18}   ${sma_user_roles.OPERATOR}
                            ...  ${TEST_USER19}   ${sma_user_roles.RO_OPERATOR}
                            ...  ${TEST_USER20}   ${sma_user_roles.HELP_DESK}
    FOR    ${user}    ${user_role}  IN   @{USERS_DETAILS}
        User Config New  ${user}   ${user}   ${TEST_USER_PSW}  ${user_role}
    END
    Commit

Common SMA Test Teardown
    Set Appliance Under Test to SMA
    Restart CLI Session
    ${cli_result}=  Load Config From File   ${SMA_ORIG_CONF}
    Log  ${cli_result}
    Commit
    Close Browser
    Selenium Login
    DefaultTestCaseTeardown

Common Admin Test Teardown
    Set Appliance Under Test to ESA
    Restart CLI Session
    Load Config From File  ${ESA_ORIG_CONF}
    Commit
    Common SMA Test Teardown

Add ESA To SMA
    ${res}=  Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  isq=${True}
    ...  reporting=${True}
    ...  tracking=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Log  ${res}
    Commit Changes

Check Show Details Message
	[Arguments]  ${mid}  ${subject_data}=${None}
    ${message}=  Email Message Tracking Search
    ...  subject_data=${subject_data}
    ...  subject_comparator=Contains
    ...  ironport_mid=${mid}
    Log  ${message}
    Page Should Contain  Show Details

Check Message Tracking Details
    [Arguments]  ${mid}  ${tracking_sub}  ${link_name}
    Wait Until Keyword Succeeds
    ...  16 min
    ...  5 sec
    ...  Check Show Details Message  ${mid}  ${tracking_sub}

    ${show_details_href}=  Get Element Attribute
    ...  //tr[@id='result_1']//a[normalize-space()='Show Details']@href
    ${show_details_link}=  Evaluate
    ...  re.search(r"'(https://.*)'", """${show_details_href}""").groups()[0]  re

    Go To  ${show_details_link}
    Page Should Contain  ${link_name}
    Click Link  ${link_name}

Verify DLP
    [Arguments]  ${mid}
    @{credit_cards}  Create List  Credit Card Numbers  5297087928927803  53 31598027912692
    Check Message Tracking Details  ${mid}  ${DLP_TRACKING_SUBJ}  DLP Matched Content
    FOR  ${credit_card}  IN  @{credit_cards}
        Page Should Contain  ${credit_card}
    END

Verify URL Tracking
    [Arguments]  ${mid}
    @{urls}  Create List  ${BAD_RPT_URL}
    Check Message Tracking Details  ${mid}  ${URL_TRACKING_SUBJ}  URL Details
    FOR  ${url}  IN  @{urls}
      Page Should Contain  ${url}
    END

Verify Spam Quarantine Messages Count
    @{search_result}=  Spam Quarantine Advanced Search
    ...  date_range=today
    ...  header_name=Subject
    ...  header_cmp=Contains
    ...  header_value=Spam
    ${search_result_length} =  Get Length  ${search_result}
    Should Be True  ${search_result_length} > 0

Enable Euq
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=None

    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_username=${DUT_ADMIN}
    ...  spam_notif_domain=${CLIENT}
    ...  spam_notif_consolidate=${True}
    ...  spam_notif_baddr=${DUT_ADMIN}@${CLIENT}
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
    Commit Changes

Tvh1473833c Setup
    Selenium Close
    Set Appliance Under Test to SMA
    Selenium Login
    DefaultTestCaseSetup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Users Edit DLP Tracking Privileges
    ...  admin=${True}
    ...  operators=${False}
    ...  readonly=${True}
    ...  helpdesk=${False}
    Commit Changes

    Selenium Close
    Set Appliance Under Test to ESA
    Selenium Login
    DLP Enable
    Commit Changes
    DLP Edit Settings  enable_matched_content_logging=${True}
    Commit Changes
    DLP Policy New  Privacy Protection  Credit Card Numbers
    ...  change_policy_name=${TEST_ID}  submit=${True}

    ${settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  Enable All  ${True}
    Mail Policies Edit Dlp
    ...  outgoing
    ...  default
    ...  ${settings}
    Commit Changes

Tvh1473831c Setup
    Set Appliance Under Test to SMA
    DefaultTestCaseSetup

    Roll Over Now  mail_logs
    Sleep  10s  msg=Wait for log rollover
    Roll Over Now  euq_logs
    Sleep  10s  msg=Wait for log rollover

    Selenium Close
    Set Appliance Under Test to ESA
    Selenium Login

Tvh1473832c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Appliance Under Test to SMA
    DefaultTestCaseSetup
    Users Edit URL Tracking Privileges
    ...  admin=${True}
    ...  operators=${False}
    ...  readonly=${True}
    ...  helpdesk=${False}
    Commit Changes

    Selenium Close
    Set Appliance Under Test to ESA
    Selenium Login
    Url Filtering Enable
    Commit Changes

    ${action_value}  Create Dictionary
    ...  Scan Type  All
    ${condition}  Content Filter Create Conditions
    ...  URL Reputation Condition  ${action_value}

    ${quarantine_action}=  Create Dictionary
    ...  Send message to quarantine   Policy
    ${actions}=  Content Filter Create Actions
    ...  Quarantine     ${quarantine_action}

    Content Filter Add  outgoing   ${TEST_ID}
    ...  Super filter  ${actions}  ${condition}
    Commit Changes

    ${settings}=  Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  Enable All  ${True}
    Mail Policies Edit Content Filters  outgoing  default  ${settings}
    Commit Changes

    ${settings}=  Create Dictionary
    ...  Outbreak Filters  Enable Outbreak Filtering (Customize settings)
    Mail Policies Edit Outbreak Filters  outgoing  default  ${settings}
    Commit Changes
    Restart CLI Session
    Outbreak Config Setup  log_urls=yes
    Commit

Tvh1468359c Setup
    Set Test Variable  ${range}  Yesterday (00:00 to 23:59)
    Selenium Close
    Set Appliance Under Test to SMA
    DefaultTestCaseSetup
    Selenium Login

    ${table_params}=  Email Report Table Create Parameters
    ...  Incoming Mail Details
    ...  period=${range}

    Selenium Close
    Set Appliance Under Test to ESA
    Selenium Login


*** Test Cases ***
Tvh1472435c
    [Documentation]  Verify Web admin user's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472435 \n
    [Tags]   Tvh1472435c  csdl  SEC-AUT-AUTH-4
    [Setup]  Run Keywords  Selenium Close
    ...  Set Appliance Under Test to SMA
    ...  DefaultTestCaseSetup
    ...  Selenium Login
    ...  Set CMs
    ...  Centralized Web Configuration Manager Enable
    ...  Commit Changes
    [Teardown]  Common SMA Test Teardown
    Log Out Of Dut
    Log Into Dut  ${TEST_USER16}  ${TEST_USER_PSW}
    ${results} =  Web Tracking Search
    Configuration Masters Initialize  ${sma_config_masters.${CM}}  ${True}
    Commit Changes
    Run Keyword And Expect Error  *   Configuration File Save Config
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Run Keyword And Expect Error  *   Email Message Tracking Search
    Close Cli Session
    Start Cli Session   ${TEST_USER16}  ${TEST_USER_PSW}
    Run Keyword And Expect Error  *   Reset Config

Tvh1472436c
    [Documentation]  Verify Email admin user's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472436 \n
    [Tags]   Tvh1472436c  csdl  SEC-AUT-AUTH-4
    [Setup]  Run Keywords  Selenium Close
    ...  Set Appliance Under Test to SMA
    ...  DefaultTestCaseSetup
    ...  Selenium Login
    [Teardown]  Common SMA Test Teardown
    Log Out Of Dut
    Log Into Dut  ${TEST_USER15}  ${TEST_USER_PSW}
    ${messages}=   Email Message Tracking Search
    Run Keyword And Expect Error  *   Configuration File Save Config
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Run Keyword And Expect Error  *   Web Tracking Search
    Close Cli Session
    Start Cli Session   ${TEST_USER15}  ${TEST_USER_PSW}
    Run Keyword And Expect Error  *   Reset Config

Tvh1473831c
    [Documentation]  Verify logging in as user via spam notification alert mail and make sure User A \n
    ...  can see only their messages and not other Users \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1473831c \n
    [Tags]  Tvh1473831c   csdl  SEC-AUT-AUTH-4
    [Setup]  Tvh1473831c Setup
    [Teardown]  Run Keywords
    ...  Message Unload
    ...  NUll Smtpd Stop
    ...  Common Admin Test Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Restart CLI Session
    Roll Over Now  logname=mail_logs
    Sleep  10  waiting to mail_logs up

    Inject Messages
    ...  mbox-filename=${SPAM_FILE}
    ...  num-msgs=2
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  rcpt-host-list=${TEST_ID}@${CLIENT}

    Verify And Wait For Log Records
    ...  search_path=mail
    ...  interim verdict using engine: CASE spam positive >= 1

    Selenium Close
    Set Appliance Under Test to SMA
    Selenium Login
    Null Smtpd Start
    Force ISQ Notifications
    ${ENCODED_MAIL_CONTENT}=  Wait Until Keyword Succeeds
    ...  3 min
    ...  0 sec
    ...  Verify And Wait For Mail In Drain  ${DUT_ADMIN}@${CLIENT}
    ...  Subject  ${SPAM_NOTIF_SUBJ}
    Log  ${ENCODED_MAIL_CONTENT}
    Message Load  ${ENCODED_MAIL_CONTENT}

    Verify Log Contains Records
    ...  search_path=${EUQ_LOGS_PATH}
    ...  Notification sent: #recipients >= 1

    Verify Log Contains Records
    ...  search_path=${MAIL_LOGS_PATH}
    ...  Start MID .*ICID .*ISQ Notification >= 1
    ...  Subject 'Spam Quarantine Notification' >= 1

    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCODED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{LIST_OF_URLS}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    FOR  ${url}  IN  @{LIST_OF_URLS}
      Run Keyword If  'Release' in "${url}"
      ...  Release Message Through Email Links  ${url}
    END

Tvh1468359c
    [Documentation]  Verify SMA can communicate to ESA (Tracking, Reporting and Quarantine) \n
	...  only after authentication \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468359 \n
    [Tags]  Tvh1468359c   csdl  SEC-AUT-AUTH-4
    [Setup]  Tvh1468359c Setup
    [Teardown]  Common Admin Test Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${recipient}=  Join Path  ${SUITE_TMP_DIR}  ${TEST_ID}_recipients.txt
    OperatingSystem.Create File  ${recipient}
    OperatingSystem.Append to File  ${recipient}  ${TEST_ID}@${CLIENT}
    Set Test Variable  ${recipient}
    Restart CLI Session
    Roll Over Now  logname=mail_logs
    Sleep  10  waiting to mail_logs up

    Inject Messages
    ...  mbox-filename=${SPAM_FILE}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}
    ...  address-list=${recipient}:.${CLIENT}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  addr-per-msg=2

    ${mid}=  Get Mid Value  From: <${TEST_ID}@${CLIENT}>
    Verify And Wait For Log Records
    ...  search_path=mail
    ...  interim verdict using engine: CASE spam positive >= 1
    ...  MID ${mid} to RID .* to offbox IronPort Spam Quarantine >= 1

    Selenium Close
    Set Appliance Under Test to SMA
    Selenium Login

    Wait Until Keyword Succeeds
    ...  16 min
    ...  5 sec
    ...  Check Show Details Message  ${mid}

	Page Should Contain  Show Details
    Spam Quarantine Search Page Open  user=${DUT_ADMIN}  password=${DUT_ADMIN_SSW_PASSWORD}
    Wait Until Keyword Succeeds  16 minutes  20 seconds
    ...  Verify Spam Quarantine Messages Count
    Selenium Close
    Selenium Login
    ${table_params}=  Email Report Table Create Parameters
    ...  Incoming Mail Summary  period=Day

    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  16 min
    ...  10 sec
    ...  Email Report Table Get Data
    ...  Incoming Mail Details
    ...  ${table_params}
	Log  ${reporting_data}

Tvh1473832c
    [Documentation]  Verify enabling URL tracking privileges and corresponding users alone can see url \n
    ...  details tab in tracking page \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1473832c \n
    [Tags]  Tvh1473832c   csdl  SEC-AUT-AUTH-4
    [Setup]  Tvh1473832c Setup
    [Teardown]  Common Admin Test Teardown
    Roll Over Now  logname=mail_logs

    Inject Messages
    ...  inject-host=${ESA_PR_LISTENER_IP}
    ...  num-msgs=1
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  rcpt-host-list=${CLIENT}
    ...  subject="${URL_TRACKING_SUBJ}"
    ...  msg-body="${BAD_RPT_URL}"

    ${mid}=  Get Mid Value  From: <${TEST_ID}@${CLIENT}>
    Log  ${mid}
    Selenium Close
    Set Appliance Under Test to SMA
    Selenium Login
    Verify URL Tracking  ${mid}
    Close All Browsers
    Launch Dut Browser
    Log Into Dut  ${TEST_USER19}   ${TEST_USER_PSW}
    Verify URL Tracking  ${mid}
    Close All Browsers
    Launch Dut Browser
    Log Into Dut  ${TEST_USER18}   ${TEST_USER_PSW}
    Run Keyword And Expect Error  Page should have contained text*  Verify URL Tracking  ${mid}
    Close All Browsers
    Launch Dut Browser
    Log Into Dut  ${TEST_USER20}   ${TEST_USER_PSW}
    Run Keyword And Expect Error  Page should have contained text*  Verify URL Tracking  ${mid}

Tvh1473833c
    [Documentation]  Verify enabling DLP tracking previleges and corresponding users alone can see dlp \n
    ...  details tab in tracking page\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1472699c \n
    [Tags]  Tvh1473833c   csdl  SEC-AUT-AUTH-4
    [Setup]  Tvh1473833c Setup
    [Teardown]  Common Admin Test Teardown
    Roll Over Now  logname=mail_logs
    Inject Messages
    ...  inject-host=${ESA_PR_LISTENER_IP}
    ...  num-msgs=1
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  rcpt-host-list=${CLIENT}
    ...  subject="${DLP_TRACKING_SUBJ}"
    ...  mbox-filename=${CREDITCARD_FILE}

    ${mid}=  Get Mid Value  From: <${TEST_ID}@${CLIENT}>
    Log  ${mid}
    Selenium Close
    Set Appliance Under Test to SMA
    Selenium Login
    Verify DLP  ${mid}
    Close All Browsers
    Launch Dut Browser
    Log Into Dut  ${TEST_USER19}   ${TEST_USER_PSW}
    Verify DLP  ${mid}
    Close All Browsers
    Launch Dut Browser
    Log Into Dut  ${TEST_USER18}   ${TEST_USER_PSW}
    Run Keyword And Expect Error  Page should have contained text*  Verify DLP  ${mid}
    Close All Browsers
    Launch Dut Browser
    Log Into Dut  ${TEST_USER20}   ${TEST_USER_PSW}
    Run Keyword And Expect Error  Page should have contained text*  Verify DLP  ${mid}