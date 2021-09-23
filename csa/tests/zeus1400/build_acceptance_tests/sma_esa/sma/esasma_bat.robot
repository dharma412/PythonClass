# $Id: //prod/main/sarf_centos/tests/zeus1350/build_acceptance_tests/esasma_bat.txt#2 $
# $DateTime: 2020/02/25 21:38:06 $
# $Author: vsugumar $

*** Settings ***
Resource     esa/global.txt
Resource     sma/global_sma.txt
Resource     sma/esasma.txt
Resource     esa/injector.txt
Resource     regression.txt
Resource     esa/logs_parsing_snippets.txt
Variables    sma/constants.py

Suite Setup  Do Suite Setup
Suite Teardown  Do Suite Teardown

*** Variables ***
${DATA_UPDATE_TIMEOUT}=  5m
${RETRY_TIME}=  20s
${SLAVE_ESA_NAME} =  Slave ESA
${GROUP_NAME} =  Test Group
${SESSION_TIMEOUT}                   1440
${PROFILE_NAME} =  esasma_bat
${SPAM_NOTIF_SUBJ}=  Spam Quarantine Notification
${Tvh544823c_DLP_POLICY_NAME}=      Test-HIPPA-and-HITECH-Match
${Tvh544821c_DLP_POLICY_NAME}=      Test-HIPPA-and-HITECH-Match

*** Keywords ***
Do Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup  should_revert_to_initial=${False}
    global.Configure RAT to Allow Sending to Client

    ${PUBLIC_LISTENER}=  Get ESA Listener
    ${PRIVATE_LISTENER} =  Get ESA Listener  scope=Private
    Set Suite Variable  ${PUBLIC_LISTENER}
    Set Suite Variable  ${PRIVATE_LISTENER}
    ${ESA_PUBLIC_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUBLIC_LISTENER_IP}
    ${ESA_PRIVATE_LISTENER_IP}=  Get ESA Private IP
    Set Suite Variable  ${ESA_PRIVATE_LISTENER_IP}
    ${settings}=  Create Dictionary  Web UI Inactivity Timeout  60
    Network Access Edit  ${settings}
    Commit Changes
    Message Tracking Enable  tracking=centralized
#    Message Tracking Edit Settings  tracking=centralized
    Commit Changes
    Admin Access Config Timeout   timeout_webui=1440  timeout_cli=1440
    Commit
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes
    Reporting Config Setup  enable=yes
    Commit

    Set Appliance Under Test To SMA
    global_sma.DefaultTestSuiteSetup
    Init BAT Common Variables
    Add LDAP Users
    Selenium Login
    ${FAKE_DOMAIN_NAME} =  Catenate  SEPARATOR=  mail.  ${LDAP_AUTH_SERVER}  .${NETWORK}
    Set Suite Variable  ${FAKE_DOMAIN_NAME}
    ${NOTIFICATION_RCPT} =  Set Variable  dev_null@${CLIENT_HOSTNAME}
    Set Suite Variable  ${NOTIFICATION_RCPT}
    @{MAIL_ADDRS} =  Create List
    ...  ${isq_user}@mail.${CLIENT_HOSTNAME}
    ...  ${isq_user}@${CLIENT_HOSTNAME}
    ...  dev_null@${CLIENT_HOSTNAME}
    Set Suite Variable  @{MAIL_ADDRS}

    #global_sma.DefaultTestSuiteSetup
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  c_rep_processing  duration=2592000
    Commit Changes
    Admin Access Config Timeout   timeout_webui=1440  timeout_cli=1440
    Commit
    Diagnostic Reporting Delete DB  confirm=yes
    Diagnostic Tracking Delete DB  confirm=yes
    Commit
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  ${SESSION_TIMEOUT}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes

    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp(dir="%{SARF_HOME}/tmp")  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}

Do Suite Teardown
    Run keyword and ignore error  Remove LDAP Users
    Remove Directory  ${SUITE_TMP_DIR}  recursive=${True}
    Switch To ESA
    Diagnostic Reporting Delete DB  confirm=yes
    Reporting Config Setup  enable=no
    Diagnostic Tracking Delete DB  confirm=yes
    Commit
    global.DefaultTestSuiteTeardown

    Switch To SMA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Diagnostic Reporting Delete DB  confirm=yes
    Diagnostic Tracking Delete DB  confirm=yes
    Commit
    Security Appliances Delete Email Appliance  ${ESA}
    Centralized Email Reporting Disable
    Centralized Email Message Tracking Disable
    Network Access Edit Settings  60
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    global_sma.DefaultTestSuiteTeardown

Create File With Recipients List
    [Arguments]  @{addrs}
    ${rnd}=  String.Generate Random String
    ${addr_file}=  Join Path  ${SUITE_TMP_DIR}  ${rnd}.txt
    OperatingSystem.Create File  ${addr_file}
    FOR  ${addr}  IN  @{addrs}
    OperatingSystem.Append to File  ${addr_file}  ${addr}\n
    END
    [Return]  ${addr_file}

Switch To ${dut}
    Set Appliance Under Test To ${dut}
    Execute JavaScript  window.focus()
    Run Keyword And Ignore Error  Log Into DUT

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

Verify Table Column Value
    [Documentation]  Veirfies that particular column value\n
    ...  from given table is equal to ${expected_val}
    [Arguments]  ${table_name}  ${col_name}  ${expected_val}
    ...  ${table_params}=${None}  ${should_navigate_to_table}=${True}
    ${table_data} =  Email Report Table Get Data  ${table_name}
    ...  table_parameters=${table_params}
    ...  should_navigate_to_table=${should_navigate_to_table}
    Check Table Column Value  ${table_data}  ${col_name}  ${expected_val}

Get Date With Offset
    [Documentation]  Calculates resulting date plus day offset\n
    ...  datetime format should look like "Wed Jul 11 07:03:12 2012 PDT"
    [Arguments]  ${current_datetime}  ${day_offset}
    ${result_dt} =  Evaluate
    ...  datetime.datetime.strptime('${current_datetime}'[:-4], '%a %b %d %H:%M:%S %Y') + datetime.timedelta(days=${day_offset})
    ...  datetime
    ${result_date_str} =  Evaluate
    ...  datetime.datetime.strptime('${result_dt}', '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
    ...  datetime
    [Return]  ${result_date_str}

Verify Tracking Messages Count
    [Documentation]  Verifies count of tracking messages\n
    ...  on SMA appliance is equal to ${expected_cnt}\n
    ...  Next arguments are passed to Email Message Tracking Search\n
    ...  keyword
    [Arguments]  ${expected_cnt}  ${mesg_received}=${None}
    ...  ${attachment_name}=${None}   ${sender_data}=${None}
    @{msgs} =  SmaGuiLibrary.Email Message Tracking Search  mesg_received=${mesg_received}
    ...  attachment_name=${attachment_name}   sender_data=${sender_data}
    Length Should Be  ${msgs}  ${expected_cnt}

Do Tvh544821c Setup
    General Test Case Setup

    Switch To SMA
    SmaGuiLibrary.Centralized Email Reporting Group Add
    ...  ${GROUP_NAME}  ${ESA}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes

    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  Yes
    ...  Use Sophos Anti-Virus  ${True}
    Mail Policies Edit Antivirus  incoming  default  ${settings}
    Commit Changes

    FOR  ${mbox}  IN  ${CLEAN}  ${EICAR_COM_ZIP}  ${SPAM}
    Inject Messages
    ...  mbox-filename=${mbox}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    END

Do Tvh544821c Teardown
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  DLP Policies  Disable DLP
    ...  Enable All  ${False}
    Mail Policies Edit Dlp
    ...  outgoing
    ...  default
    ...  ${settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${${TEST_NAME}_DLP_POLICY_NAME}
    Commit Changes

    Switch To SMA
    SmaGuiLibrary.Centralized Email Reporting Group Delete
    ...  ${GROUP_NAME}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    General Test Case Teardown

Do Tvh544830c Setup
    DefaultTestCaseSetup
    Null Smtpd Start

Do Tvh544830c Teardown
    Null Smtpd Stop
    DefaultTestCaseTeardown

Generate RAW Email Data
    ${pub_listener} =  Get ESA Listener
    ${listener} =   Set Variable   ${pub_listener.ipv4}
    FOR  ${mail_addr}  IN  @{MAIL_ADDRS}
    ${payload} =  Catenate  SEPARATOR=
    ...  From: ${mail_addr}\r\n
    ...  To: ${mail_addr}\r\nSubject: Deadly\ \ \ v 1 a g r a\r\n
    ...  X-Advertisement: spam
    ...  \r\nIt is said that vi4gra can fsck(8)'n' kill a person
    ...  \ with weak heart.\r\n
    Inject Raw Msg
    ...  listener=${listener}
    ...  payload=${payload}
    ...  rcpt_to=${mail_addr}
    ...  mail_from=dev_null@${CLIENT_HOSTNAME}
    END
    Sleep  10 seconds

Enable EUQ On ESA
    [Arguments]  ${commit}=${True}
    Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${False}
    Run Keyword If  ${commit}  Commit Changes

Enable Spam Quarantine On SMA
    [Arguments]  ${commit}=${True}
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Run Keyword If  ${commit}  Commit Changes

Do Tvh544817c Setup
    General Test Case Setup
    Switch To ESA
    Clean System Quarantines
    Quarantines Spam Disable
    Enable EUQ On ESA
    Roll Over Now  mail_logs

    Switch To SMA
    DefaultTestCaseSetup
    Clean System Quarantines
    Roll Over Now  mail_logs
    Enable Spam Quarantine On SMA  commit=${False}
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_format=Text
    ...  spam_notif_consolidate=${True}
    ...  spam_notif_baddr=mybounceaddress@${CLIENT}
    Security Appliances Edit Email Appliance
    ...  ${ESA}
    ...  address=${ESA_IP}
    ...  isq=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    IP Interfaces Edit  Management  isq_https_service=83  isq_default=https://${DUT}:83/  hostname=${DUT}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
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
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    Spam Quarantine Edit EndUser Access
    ...  end_user_access_enable=${True}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    Go To Euq Gui  ${isq_user}@${CLIENT}  ${DUT_ADMIN_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To  https://${DUT}:83

Do Tvh544817c Teardown
    Switch To ESA
    EUQ Disable
    Quarantines Spam Enable
    Commit Changes

    Switch To SMA
    Go To Main Gui
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${False}
    Wait Until Keyword Succeeds  1 minutes  10 seconds
    ...  Security Appliances Edit Email Appliance
    ...  ${ESA}
    ...  address=${ESA_IP}
    ...  isq=${False}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Spam Quarantine Edit EndUser Access
    ...  end_user_access_enable=${False}
    LDAP Delete Server Profile  ${PROFILE_NAME}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    General Test Case Teardown

Do Tvh544818c Setup
    General Test Case Setup
    Ldap Client Create User
    ...  uid=${TEST_NAME}
    ...  password=${TEST_NAME}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}
    ...  mail=${TEST_NAME}@${CLIENT}
    ...  mail_local_address=${TEST_NAME}_local1@${CLIENT}, ${TEST_NAME}_local2@${CLIENT}

    Switch To ESA
    Clean System Quarantines
    Quarantines Spam Disable
    Enable EUQ On ESA
    Roll Over Now  mail_logs

    Switch To SMA
    DefaultTestCaseSetup
    Null SMTPd Start

    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit
    Clean System Quarantines
    Roll Over Now  mail_logs
    Enable Spam Quarantine On SMA  commit=${False}
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_format=Text
    ...  spam_notif_consolidate=${True}
    ...  spam_notif_baddr=mybounceaddress@${CLIENT}
    Security Appliances Edit Email Appliance
    ...  ${ESA}
    ...  address=${ESA_IP}
    ...  isq=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Ldap Add Server Profile
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}
    ...  base_dn=${LDAP_BASEDN}
    ...  auth_method=anonymous
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    Ldap Edit Isq Alias Consolidation Query
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}.isq_consolidate
    ...  (mailLocalAddress={a})
    ...  mail
    ...  ${True}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes

Do Tvh544818c Teardown
    LDAP Client Delete User  ${TEST_NAME}
    Switch To ESA
    EUQ Disable
    Quarantines Spam Enable
    Commit Changes

    Switch To SMA
    Null SMTPd Stop

    Smtp Routes Delete  .${NETWORK}
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${False}
    Security Appliances Edit Email Appliance
    ...  ${ESA}
    ...  address=${ESA_IP}
    ...  isq=${False}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    LDAP Delete Server Profile  ${PROFILE_NAME}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    General Test Case Teardown

Do Tvh544846c Setup
    General Test Case Setup
    Switch To ESA
    Clean System Quarantines
    Quarantines Spam Disable
    Enable EUQ On ESA
    Roll Over Now  mail_logs

    Switch To SMA
    DefaultTestCaseSetup
    Clean System Quarantines
    Roll Over Now  mail_logs
    Enable Spam Quarantine On SMA  commit=${False}
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_format=Text
    ...  spam_notif_consolidate=${True}
    ...  spam_notif_baddr=mybounceaddress@${CLIENT}
    Security Appliances Edit Email Appliance
    ...  ${ESA}
    ...  address=${ESA_IP}
    ...  isq=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    ${pub_listener} =  Get ESA Listener
    ${listener_addr} =   Set Variable   ${pub_listener.ipv4}

    Inject Messages
    ...  rcpt-host-list=[ipv6:${CLIENT_IPV6}]
    ...  mail-from=dev_null@[ipv6:${CLIENT_IPV6}]
    ...  mbox-filename=${SPAM}  num-msgs=1
    ...  inject-host=${listener_addr}

    Spam Quarantine Search Page Open

Do Tvh544846c Teardown
    Spam Quarantine Delete Messages  date_range=week
    ...  recipient_cmp=contains  recipient_value=${CLIENT_IPV6}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    Close Window
    Select Window
    Security Appliances Edit Email Appliance
    ...  ${ESA}
    ...  address=${ESA_IP}
    ...  isq=${False}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes

    Switch To ESA
    EUQ Disable
    Quarantines Spam Enable
    Commit Changes
    Switch To SMA
    General Test Case Teardown

Do Tvh544828c Setup
    DefaultTestCaseSetup
    Spam Quarantine Enable  interface=Management  port=6025
    Spam Quarantine Edit EndUser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=LDAP
    Spam Quarantine SLBL Enable
    Ldap Add Server Profile
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}
    ...  base_dn=${LDAP_BASEDN}
    ...  auth_method=anonymous
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    Ldap Edit Isq End User Authentication Query
    ...  ${PROFILE_NAME}
    ...  query_name=${PROFILE_NAME}.isq_auth
    ...  query_string=(uid={u})
    ...  email_attrs=mail
    ...  activate=${True}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes  ${SMA} configured.

    Go To Euq Gui  ${isq_user}@${CLIENT}  ${RTESTER_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete

Do Tvh544828c Teardown
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To Main Gui
    Spam Quarantine Disable
    LDAP Delete Server Profile  ${PROFILE_NAME}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    DefaultTestCaseTeardown

Enable Reporting on ESA
    Reporting Config Setup  enable=yes
    Commit

Enable Reporting on SMA
    Centralized Email Reporting Enable
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes

General Test Case Setup
    FOR  ${dut_type}  IN  ESA  SMA
    Switch To ${dut_type}
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Diagnostic Reporting Delete DB  confirm=yes
    Run Keyword If  '${dut_type}' == 'ESA'
    ...  Enable Reporting on ESA
    Run Keyword If  '${dut_type}' == 'SMA'
    ...  Enable Reporting on SMA
    DefaultTestCaseSetup
    END

General Test Case Teardown
    OperatingSystem.Empty Directory  ${SUITE_TMP_DIR}
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Sync Appliances Datetime  ${SMA}  ${ESA}
    FOR  ${dut_type}  IN  SMA  ESA
    Switch To ${dut_type}
    DefaultTestCaseTeardown
    END

Do Tvh544838c Setup
    General Test Case Setup
    Switch To ESA
    Inject Messages
    ...  mbox-filename=${CLEAN}
    ...  num-msgs=2
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}

Do Tvh544838c Teardown
    General Test Case Teardown

Do Tvh544823c Setup
    General Test Case Setup
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  Yes
    ...  Use Sophos Anti-Virus  ${True}
    Mail Policies Edit Antivirus  incoming  default  ${settings}
    Commit Changes

    ${spam_dict}=  Spam Params Get  action_spam=IRONPORT QUARANTINE
    ${suspected_spam_dict}=  Suspected Spam Params Get  action_spam_suspected=IRONPORT QUARANTINE
    Policyconfig Edit Antispam Edit  Incoming
    ...  DEFAULT
    ...  ${spam_dict}
    ...  ${suspected_spam_dict}
    Commit

    FOR  ${mbox}  IN  ${CLEAN}  ${EICAR_COM_ZIP}  ${SPAM}
    Inject Messages
    ...  mbox-filename=${mbox}
    ...  num-msgs=2
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    END

Do Tvh544823c Teardown
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  DLP Policies  Disable DLP
    ...  Enable All  ${False}
    Mail Policies Edit Dlp
    ...  outgoing
    ...  default
    ...  ${settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${${TEST_NAME}_DLP_POLICY_NAME}
    Commit Changes
    General Test Case Teardown

Verify DLP Data In Group
    ${table_params} =  SmaGuiLibrary.Email Report Table Create Parameters
    ...  DLP Incident Details  view_data_for=Group: ${GROUP_NAME}
    ...  period=Week
    ${table_data} =  SmaGuiLibrary.Email Report Table Get Data  DLP Incident Details
    ...  table_parameters=${table_params}
    Check Table Column Value  ${table_data}  High  1


Do Tvh544825c Setup
    DefaultTestCaseSetup

Do Tvh544825c Teardown
    DefaultTestCaseTeardown

Verify Spam Quarantine Messages Count
    [Arguments]  ${is_admin}  ${header_name}
    ...  ${header_cmp}  ${header_value}
    ...  ${exp_length}
    @{search_result} =  Spam Quarantine Advanced Search
    ...  is_admin=${is_admin}  date_range=week  header_name=${header_name}
    ...  header_cmp=${header_cmp}  header_value=${header_value}
    ${search_result_length} =  Get Length  ${search_result}
    Should Be Equal As Integers  ${search_result_length}  ${exp_length}

Do Tvh544848c Setup
    DefaultTestCaseSetup
    Set Appliance Under Test to Esa
    DefaultTestCaseSetup
    ${hat_dict}  Create Dictionary  enable_mrpes  Yes  mrpes  1
    ListenerConfig Edit HostAccess Edit Policy  InboundMail  ACCEPTED  ${Empty}
    ...  hat_params=${hat_dict}  hat_change_bool=yes
    Commit  comment=Rate Per Envelope Sender Enabled.

    Diagnostic Tracking Delete DB   confirm=yes
    Set Appliance Under Test to Sma
    Diagnostic Tracking Delete DB   confirm=yes
    Generate Email Data

Do Tvh544848c Teardown
    Set Appliance Under Test to Esa
    ${hat_dict}  Create Dictionary  enable_mrpes  No
    ListenerConfig Edit Hostaccess Edit Policy  InboundMail  ACCEPTED  ${Empty}
    ...  hat_params=${hat_dict}  hat_change_bool=yes
    Commit  comment=Rate Per Envelope Sender Disabled.
    DefaultTestCaseTeardown
    Set Appliance Under Test to Sma
    DefaultTestCaseTeardown

Do Tvh544829c Setup
    FOR  ${dut_type}  IN  ESA  SMA
    Switch To ${dut_type}
    DefaultTestCaseSetup
    END
    Null Smtpd Start

Do Tvh544829c Teardown
    Null Smtpd Stop
    Sync Appliances Datetime  ${SMA}  ${ESA}
    FOR  ${dut_type}  IN  ESA  SMA
    Switch To ${dut_type}
    DefaultTestCaseTeardown
    END

Verify Rate Limits Reporting Data
    [Documentation]  Succeeds if there is any data about Rate Limits\n
    Navigate To  Email  Reporting  Rate Limits
    Select From List  //select[@id="date_range"]  Week
    ${text} =  Get Text
    ...  //div[@id='container_mga_rate_limit_sender_top_senders_by_incidents']
    Should Not Be Equal As Strings  ${text}
    ...  No data was found in the selected time range

Verify IPv6 Spam Count
   @{search_result} =  Spam Quarantine Advanced Search
         ...  date_range=week  recipient_cmp=contains  recipient_value=${CLIENT_IPV6}
    Log  ${search_result}
    Should Not Be Empty  ${search_result}


*** Test Cases ***
Tvh544828c
    [Documentation]  Verify SLBL entries are retained and new entries\n
    ...  can be added/deleted\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544828c\n
    [Tags]  autobat  Tvh544828c
    [Setup]     Do Tvh544828c Setup
    [Teardown]  Do Tvh544828c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544828c

    Turn SLBL Entries  Add
    @{blocklist_entries} =  BlockList Get
    Length Should Be  ${blocklist_entries}  3
    Turn SLBL Entries  Delete
    @{blocklist_entries} =  BlockList Get
    Length Should Be  ${blocklist_entries}  0

Tvh544838c
    [Documentation]  Verify that time ranges, hide/show columns\n
    ...  and sort columns works for email reports\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544838c\n
    [Tags]  autobat  Tvh544838c
    [Setup]     Do Tvh544838c Setup
    [Teardown]  Do Tvh544838c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544838c

    ${TARGET_TABLE} =  Set Variable  Incoming Mail Details

    Switch To SMA
    ${table_params}=  SmaGuiLibrary.Email Report Table Create Parameters  ${TARGET_TABLE}  period=Week
    Wait Until Keyword Succeeds  30 minutes  30 seconds
    ...  Verify Table Column Value  ${TARGET_TABLE}  Clean  2  ${table_params}

    # Check different time periods
    @{periods} =  Create List  30 days  Week  Year
    FOR  ${period}  IN  @{periods}
    ${table_params} =  SmaGuiLibrary.Email Report Table Create Parameters  ${TARGET_TABLE}   period=${period}
    Verify Table Column Value  ${TARGET_TABLE}  Clean  2  ${table_params}
    END
    # Check sorting
    SmaGuiLibrary.Email Report Table Sort Column  ${TARGET_TABLE}  Virus Detected
    ...  should_navigate_to_table=${False}
    ${cnt} =  Get Matching Xpath Count
    ...  //table[@summary]/thead/tr/th[starts-with(.//text(), "Virus Detected")]//span[@class="dt-sort-disabled"]
    Should Be True  ${cnt} > 0

    # Check show/hide columns
    ${cols_to_leave} =  Create List  Spam Detected  Clean
    SmaGuiLibrary.Email Report Table Show Columns  ${TARGET_TABLE}  columns=${cols_to_leave}
    ${cnt} =  Get Matching Xpath Count
    ...  //table[@summary]/thead/tr/th[starts-with(.//text(), "Virus Detected") and contains(@class, "yui-dt-hidden")]
    SmaGuiLibrary.Email Report Table Show Columns  ${TARGET_TABLE}  columns=all
    Should Be True  ${cnt} > 0

Tvh544823c
    [Tags]  Tvh544823c  autobat
    [Documentation]  Verify presence of email reporting data \n
    ...  generated after upgrade\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544823c\n
    [Setup]     Do Tvh544823c Setup
    [Teardown]  Do Tvh544823c Teardown
    Set Test Variable  ${TEST_ID}          Tvh544823c

    ${TARGET_TABLE} =  Set Variable  Incoming Mail Details

    Switch To SMA
    ${table_params}=  SmaGuiLibrary.Email Report Table Create Parameters  ${TARGET_TABLE}  period=Week
    Wait Until Keyword Succeeds  25 minutes  30 seconds
    ...  Verify Table Column Value  ${TARGET_TABLE}  Clean  2  ${table_params}
    ${table_data} =  SmaGuiLibrary.Email Report Table Get Data  Incoming Mail Details
    ...  should_navigate_to_table=${False}
    Check Table Column Value  ${table_data}  Spam Detected  2
    Check Table Column Value  ${table_data}  Virus Detected  2
    Check Table Column Value  ${table_data}  Clean  2

    Switch To ESA
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable
    Commit Changes

    DLP Policy New  Regulatory Compliance  HIPAA and HITECH
    ...  change_policy_name=${${TEST_NAME}_DLP_POLICY_NAME}  submit=${True}
    Dlp Message Action Edit  Default Action  msg_action=Deliver
    ...  description=delivers messages
    ...  cust_header_name=X-DLP-Policy-violated
    ...  cust_header_value=Policy $DLPPolicy
    Mailpolicy Edit DLP  Outgoing  Default Policy  custom  enable_all_dlp_policies=${True}
    Commit Changes

    Inject Messages  inject-host=${ESA_PRIVATE_LISTENER_IP}  num-msgs=2
    ...  rcpt-host-list=${CLIENT}  mail-from=test@${CLIENT}
    ...  mbox-filename=${HIPAA_HITECH_MEDIUM}

    ${table_data}=  Wait Until Keyword Succeeds  25 minutes  30 seconds
    ...  SmaGuiLibrary.Email Report Table Get Data  DLP Incident Details
    Check Table Column Value  ${table_data}  High  2

Tvh544825c
    [Tags]  Tvh544825c  skip_autobat
    [Documentation]  Verifies that email tracking reports can\n
    ...  be generated\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544825c\n
    [Setup]     Do Tvh544825c Setup
    [Teardown]  Do Tvh544825c Teardown
    Set Test Variable  ${TEST_ID}          Tvh544825c

    Wait Until Keyword Succeeds  30 minutes  30 seconds
    ...  Verify Tracking Messages Count  10  mesg_received=last week

    Verify Tracking Messages Count  10  mesg_received=last week
    Verify Tracking Messages Count  4  mesg_received=last week
    ...  attachment_name=Clean

Tvh544821c
    [Tags]  Tvh544821c  autobat
    [Documentation]  Verifies that reports based on groups can\n
    ...  be generated\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544821c\n
    [Setup]     Do Tvh544821c Setup
    [Teardown]  Do Tvh544821c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544821c

    Switch To SMA
    ${table_params} =  SmaGuiLibrary.Email Report Table Create Parameters
    ...  Incoming Mail Details  view_data_for=Group: ${GROUP_NAME}
    ...  period=Week
    Wait Until Keyword Succeeds  25 minutes  30 seconds
    ...  SmaGuiLibrary.Email Report Table Get Data
    ...  Incoming Mail Details  table_parameters=${table_params}
    ${table_data} =  SmaGuiLibrary.Email Report Table Get Data  Incoming Mail Details
    ...  table_parameters=${table_params}  should_navigate_to_table=${False}
    Check Table Column Value  ${table_data}  Spam Detected   1
    Check Table Column Value  ${table_data}  Virus Detected  1
    Check Table Column Value  ${table_data}  Clean           1

    Switch To ESA
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable
    Commit Changes

    DLP Policy New  Regulatory Compliance  HIPAA and HITECH
    ...  change_policy_name=${${TEST_NAME}_DLP_POLICY_NAME}  submit=${True}
    Dlp Message Action Edit  Default Action  msg_action=Deliver
    ...  description=delivers messages
    ...  cust_header_name=X-DLP-Policy-violated
    ...  cust_header_value=Policy $DLPPolicy
    Mailpolicy Edit DLP  Outgoing  Default Policy  custom  enable_all_dlp_policies=${True}
    Commit Changes

    Inject Messages  inject-host=${ESA_PRIVATE_LISTENER_IP}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=test@${CLIENT}
    ...  mbox-filename=${HIPAA_HITECH_MEDIUM}

    Wait Until Keyword Succeeds  25 minutes  30 seconds
    ...  Verify DLP Data In Group

Tvh544830c
    [Documentation]  Verify archived reports are available and
    ...  can be delivered and archived after upgrade\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544830c\n
    [Tags]  autobat  Tvh544830c
    [Setup]     Do Tvh544830c Setup
    [Teardown]  Do Tvh544830c Teardown
    Set Test Variable  ${TEST_ID}          Tvh544830c

    Null Smtpd Local Rollover
    SmaGuiLibrary.Email Archived Reports Add Report   ${sma_email_reports.IN_MAIL}
    ...  title=CSVIncomingMailReport
    ...  report_format=csv
    ...  time_range=last week
    ...  archive=yes
    ...  email_to=test@${CLIENT_HOSTNAME}
    Null Smtpd Next Message  timeout=60
    SmaGuiLibrary.Email Archived Reports Add Report   ${sma_email_reports.IN_MAIL}
    ...  title=PDFIncomingMailReport
    ...  report_format=pdf
    ...  time_range=last week
    ...  archive=yes
    ...  email_to=test@${CLIENT_HOSTNAME}

Tvh544817c
    [Documentation]  ISQ User Release/Delete\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544817c\n
    [Tags]  skip_autobat  Tvh544817c
    [Setup]     Do Tvh544817c Setup
    [Teardown]  Do Tvh544817c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544817c

    Click Link  Advanced Search
    Spam Quarantine Delete Messages
    ...  is_admin=${False}  date_range=week
    Generate RAW Email Data
    Wait Until Keyword Succeeds  10 minutes  20 seconds
    ...  Verify Spam Quarantine Messages Count
    ...  ${False}  Subject  contains  Deadly  3

    @{delete_msgs} =  Create List  @{MAIL_ADDRS}[0]  @{MAIL_ADDRS}[1]
    FOR  ${mail_addr}  IN  @{delete_msgs}
    Spam Quarantine Delete Messages
    ...  is_admin=${False}  date_range=week  header_name=From
    ...  header_cmp=contains  header_value=${mail_addr}
    END
    @{search_result} =  Spam Quarantine Advanced Search
    ...   is_admin=${False}  date_range=week  header_name=Subject
    ...   header_cmp=contains  header_value=Deadly
    ${search_result_length} =  Get Length  ${search_result}
    Should Be Equal As Integers  ${search_result_length}  1

    Spam Quarantine Release Messages
    ...   is_admin=${False}  date_range=week  header_name=From
    ...   header_cmp=contains  header_value=@{MAIL_ADDRS}[2]
    @{search_result} =  Spam Quarantine Advanced Search
    ...   is_admin=${False}  date_range=week  header_name=Subject
    ...   header_cmp=contains  header_value=Deadly
    Length Should Be  ${search_result}  0

Tvh544818c
    [Documentation]  ISQ Notification\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544818c\n
    [Tags]  skip_autobat   Tvh544818c
    [Setup]     Do Tvh544818c Setup
    [Teardown]  Do Tvh544818c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544818c

    @{addrs}=  Create List  ${TEST_NAME}_local1@${CLIENT}  ${TEST_NAME}_local2@${CLIENT}
    ${addr_file}=  Create File With Recipients List  @{addrs}

    Inject Messages
    ...  mbox-filename=${SPAM}
    ...  num-msgs=2
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    ...  address-list=${addr_file}

    FOR  ${my_addr}  IN  @{addrs}
    ${mid}=  Get Mid Value  MID .* ICID .* To: .*${my_addr}.*
    Verify Log Contains Records
    ...  ISQ: Quarantined MID ${mid} >= 1
    END

    Roll Over Now  mail_logs
    Sleep  5s  Wait for log roll over

    Force ISQ Notifications

    FOR  ${my_addr}  IN  @{addrs}
    ${matches}  ${found}=  Log Search  .*${my_addr}.*  search_path=mail  timeout=15
    Should Be True  ${matches} == 0
    END

    ${msg}=  Wait Until Keyword Succeeds
    ...  3 min
    ...  0 sec
    ...  Verify And Wait For Mail In Drain  mybounceaddress@${CLIENT}
         ...  Subject  ${SPAM_NOTIF_SUBJ}

    Message Load  ${msg}
    Message Unload

Tvh544846c
    [Documentation]  ISQ Search by IPv6 Literal\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544846c\n
    Set Test Variable  ${TEST_ID}          Tvh544846c
    [Tags]  skip_autobat   Tvh544846c
    [Setup]     Do Tvh544846c Setup
    [Teardown]  Do Tvh544846c Teardown

    Wait Until Keyword Succeeds   5 minutes  20 seconds
    ...  Verify IPv6 Spam Count

Tvh544848c
    [Documentation]  Rate Limit per Envelope Sender\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544848c\n
    [Tags]  skip_autobat   Tvh544848c
    [Setup]     Do Tvh544848c Setup
    [Teardown]  Do Tvh544848c Teardown
    Set Test Variable  ${TEST_ID}   Tvh544848c

    Wait Until Keyword Succeeds  4 minutes  19 seconds
    ...  Verify Tracking Messages Count  6  mesg_received=last week
    ...  sender_data=dev_null@[${CLIENT_IP}]

    Wait Until Keyword Succeeds  25 minutes  15 seconds
    ...  Verify Rate Limits Reporting Data

Tvh544829c
    [Documentation]  Verify that domain-based scheduled email\n
    ...  report can generated
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544829c\n
    [Tags]  autobat   Tvh544829c
    [Setup]     Do Tvh544829c Setup
    [Teardown]  Do Tvh544829c Teardown
    Set Test Variable  ${TEST_ID}          Tvh544829c

    ${datetime_now} =  SmaCliLibrary.Set Time Get
    ${date_plus_one_day} =  Get Date With Offset  ${datetime_now}  1
    SmaCliLibrary.Set Time Set  ${date_plus_one_day} 12:26:00

    Null Smtpd Local Rollover
    SMAGuiLibrary.Email Scheduled Reports Add Domain Based Report
    ...  title=PDFDomainBasedReport
    ...  report_format=pdf
    ...  time_range=last week
    ...  report_generation=individual
    ...  schedule=daily:12:30
    ...  domains=${FAKE_DOMAIN_NAME}
    ...  email_to=test@${CLIENT_HOSTNAME}
    Sleep  10 seconds
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes

