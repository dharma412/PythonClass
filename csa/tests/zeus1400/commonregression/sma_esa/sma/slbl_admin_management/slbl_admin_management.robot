# $Id: //prod/main/sarf_centos/tests/zeus1350/feature_acceptance_tests/slbl_admin_management/slbl_admin_management.txt#2 $ $DateTime: 2020/03/02 21:31:03 $ $Author: vsugumar $

*** Settings ***
Resource          sma/global_sma.txt
Resource          esa/injector.txt
Resource          esa/global.txt
Resource          esa/logs_parsing_snippets.txt
Resource          esa/backdoor_snippets.txt
Resource          regression.txt

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Set Appliance Under Test to SMA
...  Do Suite Setup
Suite Teardown  Run Keywords
...  Do Suite Teardown
...  Selenium Close

*** Variables ***
${RECIPIENT_ADDRESS}=       xyz@ironport.ibqa
${SENDER1}=                 abc@ironport.com
${SENDER2}=                 def@ironport.com

*** Keywords ***
Do Suite Setup
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    Spam Quarantine Slbl Enable
    Commit Changes

    ${ISQ_URL}=  Catenate  SEPARATOR=  https://  ${DUT}  :83
    Set Suite Variable  ${ISQ_URL}
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup
    ...  should_revert_to_initial=${False}
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp()  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    ${ESA_PUB_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${ESA_PUB_LISTENER}

Do Suite Teardown
    Set Appliance Under Test to SMA
    Login To WebUI  SMA
    Spam Quarantine Slbl Disable
    Spam Quarantine Disable
    Commit Changes

    global_sma.DefaultTestSuiteTeardown
    Set Appliance Under Test to ESA
    Empty Directory  ${SUITE_TMP_DIR}
    Remove Directory  ${SUITE_TMP_DIR}

Get Recipient Address
    [Arguments]  ${DUT}
    ${dut_hostname}  ${domain}=  Split String  ${DUT}  .
    ${RECIPIENT_ADDRESS}=  Set Variable
    ...  xyz@ironport.${domain}
    [Return]  ${RECIPIENT_ADDRESS}

Recipients List Should Contain Address
    [Arguments]  ${rcpt_list}  ${rcpt_address}
    ${is_address_found}=  Evaluate
    ...  bool(filter(lambda x: x['Address'] == '${rcpt_address}', ${rcpt_list}))
    Should Be True  ${is_address_found}

Login To ISQ
    [Arguments]  ${user}
    ...  ${password}
    Close Browser
    Selenium Close
    Set Appliance Under Test to SMA
    Set Up Selenium Environment
    Launch DUT Browser  url=${ISQ_URL}
    Log Into DUT  ${user}  ${password}

Login To WebUI
    [Arguments]  ${dut}
    Selenium Close
    Selenium Login

Add SLBL admin and Verify
    [Arguments]  ${listtype}  ${address}  ${senders}
    SLBL Admin Add Recipient
    ...  ${listtype}
    ...  ${address}
    ...  ${senders}
    ${slbl_admin_added}=  SLBL Admin Is Recipient Exist
    ...  ${listtype}  ${address}
    Should Be True  ${slbl_admin_added}

Remove SLBL admin and Verify
    [Arguments]  ${listtype}  ${address}
    ${link}=  SLBL Admin Delete Recipient
    ...  ${listtype}
    ...  ${address}
    ${slbl_admin_removed}=  SLBL Admin Is Recipient Exist
    ...  ${listtype}  ${address}
    Should Not Be True  ${slbl_admin_removed}

Edit SLBL Recipient
    [Arguments]  ${listtype}  ${address}  ${senders}
    ${new_settings}=  Create Dictionary
     ...  Address         ${address}
     ...  Sender List     ${senders}
     SLBL Admin Edit Recipient  ${list_type}
     ...  ${address}  ${new_settings}

Verify SLBL Edit Recipient
     [Arguments]  ${listtype}  ${address}  ${senders}
     @{found_recipients}=   SLBL Admin Search  ${listtype}
     ...  Recipient  ${address}
     Log List  ${found_recipients}
     Recipients List Should Contain Address  ${found_recipients}  ${address}
     ${recipient_info}=   SLBL Admin Get Recipient  ${listtype}  ${address}
     Log Dictionary  ${recipient_info}
     ${senders_new}=   Get From Dictionary  ${recipient_info}  Sender List
     @{senders_list}=  Split String  ${senders}  ,
     Should Be True  all(map(lambda x: """${senders_new}""".find(x) >= 0, ${senders_list}))

Handle Failed Test
     Run Keyword If Test Failed
     ...  SLBL Admin Delete Recipient  ${list_type}  ${RECIPIENT_ADDRESS}

Check For SLBL DB Update
    ${matches}  ${found}=  Log Search  SLBL: Database watcher updated from snapshot .*-slbl.db
    ...  search_path=mail  timeout=60
    Should Be True  ${matches} >= 1

Wait For SLBL DB Update
    [Arguments]  ${minutes}
    Heimdall Restart  slbld
    Wait Until Keyword Succeeds
    ...  ${minutes} min
    ...  5 sec
    ...  Check For SLBL DB Update

Create Recipients List File
    [Arguments]  ${recepients}
    ${rcpts}=  Join Path  ${SUITE_TMP_DIR}  ${TEST_ID}_rcpts.txt
    OperatingSystem.Create File  ${rcpts}
    OperatingSystem.Append To File  ${rcpts}  ${recepients}
    [Return]  ${rcpts}

Configure LDAP Server
   [Arguments]  ${username}  ${password}  ${ldapclass}
   LDAP Client Connect  ${LDAP_AUTH_SERVER}
   ...  ldap_server_type=${LDAP_SERVER_TYPE}
   ...  port=${LDAP_AUTH_PORT}
   ...  basedn=${LDAP_BASEDN}
   ...  binddn=${LDAP_BINDDN}
   ...  password=${password}
   Ldap Client Add User
   ...  uid=${username}
   ...  password=${password}
   ...  objectclass=inetOrgPerson,inetLocalMailRecipient
   ...  posixAccount=${True}
   ...  mail=${username}@${CLIENT}

   Ldap Client Add Group
   ...  ${ldapclass}
   ...  members=${username}
   ...  basedn=${LDAP_BASEDN}

Create ISQ Auth Profile
   [Arguments]   ${ldapprofilename}   ${ladpisqquery}
    LDAP Add Server Profile
    ...  ${ldapprofilename}
    ...  ${LDAP_AUTH_SERVER}
    ...  anonymous
    ...  OpenLDAP
    ...  ${LDAP_AUTH_PORT}
    ...  ${LDAP_BASE_DN}

    Ldap Edit Isq End User Authentication Query
    ...  ${ldapprofilename}
    ...  ${ldapisqquery}
    ...  query_string=(uid={u})
    ...  email_attrs=mail
    ...  activate=${True}

Delete LDAP Config
   [Arguments]  ${ldapclass}   ${username}
   Login To WebUI  SMA
   Ldap Client Delete Group   ${ldapclass}
   Ldap Client Delete User   ${username}
   Ldap Client Disconnect

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
   Login To WebUI  SMA
   ${synced}=  Spam Quarantine Sync Appliances
   Log  "Database Synchronisation is ${synced}"

   Set Appliance Under Test to ESA
   Verify And Wait For Log Records
   ...  wait_time=3 minutes
   ...  retry_time=1 minute
   ...  SLBL: Database watcher updated from snapshot >= 1

Initialize Tvh703627c
   Set Appliance Under Test to SMA
   DefaultTestCaseSetup
   Login To ISQ
   ...  ${DUT_ADMIN}
   ...  ${DUT_ADMIN_SSW_PASSWORD}

Initialize Tvh703630c
   Set Appliance Under Test to SMA
   Login To WebUI  SMA
   Set Test Variable   ${LIST_TYPE}    blocklist
   Set Test Variable   ${ENTRY}    ${LIST_TYPE}_x_${SENDER1}
   Set Test Variable   ${NEW_ENTRY}   ${LIST_TYPE}_${SENDER1}
   Set Test Variable   ${LDAP_USER_NAME}  ldap_user
   Set Test Variable   ${LDAP_PASSWORD}   ironport
   LDAP Client Connect  ${LDAP_AUTH_SERVER}
   ...  ldap_server_type=${LDAP_SERVER_TYPE}
   ...  port=${LDAP_AUTH_PORT}
   ...  basedn=${LDAP_BASEDN}
   ...  binddn=${LDAP_BINDDN}
   ...  password=${LDAP_PASSWORD}
   Ldap Client Add User
   ...  uid=${LDAP_USER_NAME}
   ...  password=${LDAP_PASSWORD}
   ...  objectclass=inetOrgPerson,inetLocalMailRecipient
   ...  posixAccount=${True}
   ...  mail=${LDAP_USER_NAME}@${CLIENT}

    Set Test Variable   ${LDAP_CLASS}  ldap_admin_group
    Ldap Client Add Group
    ...  ${LDAP_CLASS}
    ...  members=${LDAP_USER_NAME}
    ...  basedn=${LDAP_BASEDN}

    Set Test Variable   ${LDAP_PROFILE_NAME}   main_ldap_profile
    Set Test Variable   ${LDAP_ISQ_QUERY}   isqauth
    LDAP Add Server Profile
    ...  ${LDAP_PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}
    ...  anonymous
    ...  OpenLDAP
    ...  ${LDAP_AUTH_PORT}
    ...  ${LDAP_BASE_DN}

    Ldap Edit Isq End User Authentication Query
    ...  ${LDAP_PROFILE_NAME}
    ...  ${LDAP_ISQ_QUERY}
    ...  query_string=(uid={u})
    ...  email_attrs=mail
    ...  activate=${True}

    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=LDAP
    Commit Changes

Finalize Tvh703630c
    Blocklist Delete   ${NEW_ENTRY}
    Login To WebUI  SMA
    Ldap Client Delete Group   ${LDAP_CLASS}
    Ldap Client Delete User   ${LDAP_USER_NAME}
    Ldap Delete Server Profile   ${LDAP_PROFILE_NAME}
    Ldap Client Disconnect
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${False}
    ...  end_user_auth=None
    Commit Changes

Initialize Tvh704761c
    Set Appliance Under Test to ESA
    DefaultTestCaseSetup
    Login To WebUI  ESA
    ${local_spam_quarantine_enabled}=  Quarantines Spam Is Enabled
    Run Keyword If  ${local_spam_quarantine_enabled}  Quarantines Spam Disable
    Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    Commit Changes

    Set Appliance Under Test to SMA
    Login To WebUI  SMA
    ${res}=  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  isq=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Log  ${res}
    Commit Changes

    Set Test Variable   ${LIST_TYPE}  blocklist

Finalize Tvh704761c
   Set Appliance Under Test to SMA
   Login To WebUI  SMA
   Security Appliances Delete Email Appliance  ${ESA}
   Commit Changes
   Login To ISQ
   ...  ${DUT_ADMIN}
   ...  ${DUT_ADMIN_SSW_PASSWORD}
   Remove SLBL admin and Verify
   ...  ${LIST_TYPE}
   ...  ${RECIPIENT_ADDRESS}

   Set Appliance Under Test to ESA
   DefaultTestSuiteTeardown

Initialize Tvh704760c
   Set Appliance Under Test to ESA
   DefaultTestCaseSetup
   Login To WebUI  ESA
   ${local_spam_quarantine_enabled}=  Quarantines Spam Is Enabled
   Run Keyword If  ${local_spam_quarantine_enabled}  Quarantines Spam Disable
   Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
   Commit Changes

   Set Appliance Under Test to SMA
   Login To WebUI  SMA
   ${res}=  Security Appliances Add Email Appliance
   ...  ${ESA}
   ...  ${ESA_IP}
   ...  isq=${True}
   ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
   Log  ${res}
   Commit Changes

   Set Test Variable   ${LIST_TYPE}  safelist

Finalize Tvh704760c
   Set Appliance Under Test to SMA
   Login To WebUI  SMA
   Security Appliances Delete Email Appliance  ${ESA}
   Commit Changes
   Login To ISQ
   ...  ${DUT_ADMIN}
   ...  ${DUT_ADMIN_SSW_PASSWORD}
   Remove SLBL admin and Verify
   ...  ${LIST_TYPE}
   ...  ${RECIPIENT_ADDRESS}

   Set Appliance Under Test to ESA
   DefaultTestSuiteTeardown

Initialize Tvh704759c
   Set Appliance Under Test to ESA
   DefaultTestCaseSetup
   Login To WebUI  ESA
   ${local_spam_quarantine_enabled}=  Quarantines Spam Is Enabled
   Run Keyword If  ${local_spam_quarantine_enabled}  Quarantines Spam Disable
   Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
   Commit Changes

   Set Appliance Under Test to SMA
   Login To WebUI  SMA
   ${res}=  Security Appliances Add Email Appliance
   ...  ${ESA}
   ...  ${ESA_IP}
   ...  isq=${True}
   ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
   Log  ${res}
   Commit Changes

   Set Test Variable   ${LIST_TYPE}    safelist
   Set Test Variable   ${ENTRY}    ${LIST_TYPE}_x_${SENDER1}
   Set Test Variable   ${NEW_ENTRY}   ${LIST_TYPE}_${SENDER1}
   Set Test Variable   ${LDAP_USER_NAME}  ldap_user
   Set Test Variable   ${LDAP_PASSWORD}   ironport
   Set Test Variable   ${LDAP_CLASS}  ldap_admin_group
   Set Test Variable   ${LDAP_PROFILE_NAME}   main_ldap_profile
   Set Test Variable   ${LDAP_ISQ_QUERY}   isqauth
   Configure LDAP Server
   ...  ${LDAP_USER_NAME}
   ...  ${LDAP_PASSWORD}
   ...  ${LDAP_CLASS}

   Create ISQ Auth Profile  ${LDAP_PROFILE_NAME}  ${LDAP_ISQ_QUERY}

   Spam Quarantine Edit Enduser Access
   ...  end_user_access_enable=${True}
   ...  end_user_auth=LDAP
   Commit Changes

Finalize Tvh704759c
    Set Appliance Under Test to SMA
    Login To ISQ  ${LDAP_USERNAME}  ${LDAP_PASSWORD}
    Run Keyword And Ignore Error
    ...  Safelist Delete   ${ENTRY}
    Safelist Delete   ${NEW_ENTRY}
    Login To WebUI  SMA
    Delete LDAP Config
    ...  ${LDAP_CLASS}
    ...  ${LDAP_USER_NAME}
    Ldap Delete Server Profile   ${LDAP_PROFILE_NAME}
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${False}
    ...  end_user_auth=None
    Security Appliances Delete Email Appliance  ${ESA}
    Commit Changes

    Set Appliance Under Test to ESA
    DefaultTestSuiteTeardown

*** Test Cases ***
Tvh703627c
    [Documentation]  From WEBGUI, Verify that the admin is able to add/edit/delete safelist
    [Tags]  Tvh703627c  fat
    [Setup]  Run Keywords
    ...  Initialize Tvh703627c
    [Teardown]  Run Keywords
    ...  Handle Failed Test
    Set Test Variable   ${TEST_ID}  Tvh703627c

    Set Test Variable   ${list_type}  safelist

    Add SLBL admin and Verify
    ...  ${list_type}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${list_type}_1_${SENDER1}, ${list_type}_2_${SENDER2}

    Edit SLBL Recipient
    ...  ${list_type}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${list_type}_${SENDER1},${list_type}_${SENDER2}

    Verify SLBL Edit Recipient
    ...  ${list_type}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${list_type}_${SENDER1},${list_type}_${SENDER2}

    Remove SLBL admin and Verify
    ...   ${list_type}
    ...   ${RECIPIENT_ADDRESS}

Tvh703628c
    [Documentation]  From WEBGUI, Verify that the admin is able to add/edit/delete blocklist
    [Tags]  Tvh703628c  fat
    [Setup]  Run Keywords
    ...  Initialize Tvh703627c
    [Teardown]  Run Keywords
    ...  Handle Failed Test
    Set Test Variable   ${TEST_ID}   Tvh703628c

    Set Test Variable   ${list_type}   blocklist

    Add SLBL admin and Verify
    ...  ${list_type}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${list_type}_1_${SENDER1}, ${list_type}_2_${SENDER2}

    Edit SLBL Recipient
    ...  ${list_type}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${list_type}_${SENDER1},${list_type}_${SENDER2}

    Verify SLBL Edit Recipient
    ...  ${list_type}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${list_type}_${SENDER1},${list_type}_${SENDER2}

    Remove SLBL admin and Verify
    ...   ${list_type}
    ...   ${RECIPIENT_ADDRESS}

Tvh703630c
    [Documentation]  From WEBGUI, Verify that the endusers are able to see the changes made by the admin
    [Tags]   Tvh703630c  fat
    [Setup]  Run Keywords
    ...  Initialize Tvh703630c
    [Teardown]  Run Keywords
    ...  Handle Failed Test
    ...  Finalize Tvh703630c
    Set Test Variable  ${TEST_ID}   Tvh703630c

#   Log in as enduser to ISQ page for creating safelist/blocklist
    Login To ISQ
    ...  ${LDAP_USERNAME}
    ...  ${LDAP_PASSWORD}

    Blocklist Add   ${ENTRY}

#   Log in as admin to ISQ page and modify saelist enteries created by enduser
    Login To ISQ
    ...  ${DUT_ADMIN}
    ...  ${DUT_ADMIN_SSW_PASSWORD}

    Edit SLBL Recipient
    ...  ${LIST_TYPE}
    ...  ${LDAP_USER_NAME}@${CLIENT}
    ...  ${NEW_ENTRY}

#   Log in as enduser again to view the changes made my admin on safelist/blocklist enteries
    Login To ISQ
    ...  ${LDAP_USERNAME}
    ...  ${LDAP_PASSWORD}

    @{entries}  Blocklist Get
    Log  ${entries}
    Should Contain  ${entries}  ${NEW_ENTRY}

Tvh704761c
    [Documentation]  Verify that admin user can add blocklist and mail caught as spam positive
    [Tags]  Tvh704761c  srts
    [Setup]  Run Keywords
    ...  Initialize Tvh704761c
    [Teardown]  Run Keywords
    ...  Handle Failed Test
    ...  Finalize Tvh704761c
    ...  DefaultTestSuiteTeardown
    Set Test Variable   ${TEST_ID}  Tvh704761c

    ${RECIPIENT_ADDRESS}=  Get Recipient Address  ${ESA}
    Set suite variable  ${RECIPIENT_ADDRESS}
    Database Sync for Safelist Or Blocklist
    ...  ${LIST_TYPE}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${LIST_TYPE}_1_${SENDER1}, ${LIST_TYPE}_2_${SENDER2}

    ${rcpts}=  Create Recipients List File   ${RECIPIENT_ADDRESS}

    Inject Messages
    ...  mail-from=${LIST_TYPE}_1_${SENDER1}
    ...  address-list=${rcpts}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUB_LISTENER_IP}

    Verify And Wait For Log Records
    ...  MID .* ICID .* From: .*${LIST_TYPE}_1_${SENDER1}.* >= 1
    ...  MID .* using engine.* SLBL spam positive >= 1

Tvh704760c
    [Documentation]  Verify that admin user can add safelist and mail caught as spam negative
    [Tags]  Tvh704760c  srts
    [Setup]  Run Keywords
    ...  Initialize Tvh704760c
    [Teardown]  Run Keywords
    ...  Handle Failed Test
    ...  Finalize Tvh704760c
    ...  DefaultTestSuiteTeardown
    Set Test Variable   ${TEST_ID}  Tvh704760c

    ${RECIPIENT_ADDRESS}=  Get Recipient Address  ${ESA}
    Set suite variable  ${RECIPIENT_ADDRESS}
    Database Sync for Safelist Or Blocklist
    ...  ${LIST_TYPE}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${LIST_TYPE}_1_${SENDER1}, ${LIST_TYPE}_2_${SENDER2}

    ${rcpts}=  Create Recipients List File   ${RECIPIENT_ADDRESS}

    Inject Messages
    ...  mail-from=${LIST_TYPE}_1_${SENDER1}
    ...  address-list=${rcpts}
    ...  mbox-filename=${SPAM}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUB_LISTENER_IP}

    Verify And Wait For Log Records
    ...  MID .* ICID .* From: .*${LIST_TYPE}_1_${SENDER1}.* >= 1
    ...  MID .* using engine.* SLBL spam negative >= 1

Tvh704759c
    [Documentation]  Verify that admin user can add safelist and mail caught as spam negative
    [Tags]  Tvh704759c  srts
    [Setup]  Run Keywords
    ...  Initialize Tvh704759c
    [Teardown]  Run Keywords
    ...  Handle Failed Test
    ...  Finalize Tvh704759c
    ...  DefaultTestSuiteTeardown
    Set Test Variable   ${TEST_ID}  Tvh704759c

#   Log in as enduser to ISQ page for creating safelist
    Set Appliance Under Test to SMA
    Login To ISQ  ${LDAP_USERNAME}  ${LDAP_PASSWORD}

    Safelist Add    ${ENTRY}

    Set Appliance Under Test to ESA
    Roll Over Now  mail_logs
    Sleep  5s  msg=Wait for logs roll over

    Set Appliance Under Test to SMA
    Login To WebUI  SMA
    ${synced}=  Spam Quarantine Sync Appliances
    Log  "Database Synchronisation is ${synced}"

    Set Appliance Under Test to ESA
#   Wait For SLBL DB Update  1
    Verify And Wait For Log Records
    ...  wait_time=3 minutes
    ...  retry_time=1 minute
    ...  SLBL: Database watcher updated from snapshot >= 1

    ${rcpts}=  Create Recipients List File   ${LDAP_USER_NAME}@${CLIENT}

    Inject Messages
    ...  mail-from=${ENTRY}
    ...  address-list=${rcpts}
    ...  mbox-filename=${SPAM}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUB_LISTENER_IP}

    Verify And Wait For Log Records
    ...  MID .* ICID .* From: .*${ENTRY}.* >= 1
    ...  MID .* using engine.* SLBL spam negative >= 1

#   Backup the slbl file
    Set Appliance Under Test to SMA
    Login To WebUI  SMA
    ${filename}=  Configuration File Backup Slbl

#   Delete the slbl  enteries
    Login To ISQ  ${LDAP_USERNAME}  ${LDAP_PASSWORD}
    Safelist Delete    ${ENTRY}

    Login To WebUI  SMA
    ${synced}=  Spam Quarantine Sync Appliances
    Log  ${synced}

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  wait_time=3 minutes
    ...  retry_time=1 minute
    ...  SLBL: Database watcher updated from snapshot >= 1

#   Restore the slbl file
    Set Appliance Under Test to SMA
    Login To WebUI  SMA
    Configuration File Restore Slbl   ${filename}

    ${synced}=  Spam Quarantine Sync Appliances
    Log  "Database Synchronisation is ${synced}"

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  wait_time=3 minutes
    ...  retry_time=1 minute
    ...  SLBL: Database watcher updated from snapshot >= 1

#   Log in as admin to ISQ page and modify safelist enteries created by enduser
    Set Appliance Under Test to SMA
    Login To ISQ
    ...  ${DUT_ADMIN}
    ...  ${DUT_ADMIN_SSW_PASSWORD}

    Edit SLBL Recipient
    ...  ${LIST_TYPE}
    ...  ${LDAP_USER_NAME}@${CLIENT}
    ...  ${NEW_ENTRY}

    Set Appliance Under Test to SMA
    Login To WebUI  SMA
    ${synced}=  Spam Quarantine Sync Appliances
    Log  "Database Synchronisation is ${synced}"

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  wait_time=3 minutes
    ...  retry_time=1 minute
    ...  SLBL: Database watcher updated from snapshot >= 1

    Roll Over Now  mail_logs
    Sleep  5s  msg=Wait for logs roll over
    ${rcpts}=  Create Recipients List File   ${LDAP_USER_NAME}@${CLIENT}

#   Inject mail with new safelist entry and verify expected behaviour is seen
    Inject Messages
    ...  mail-from=${NEW_ENTRY}
    ...  address-list=${rcpts}
    ...  mbox-filename=${SPAM}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUB_LISTENER_IP}

    Wait Until Keyword Succeeds  5m  5s  Verify And Wait For Log Records
    ...  MID .* ICID .* From: .*${NEW_ENTRY}.* >= 1
    ...  MID .* using engine.* SLBL spam negative >= 1
