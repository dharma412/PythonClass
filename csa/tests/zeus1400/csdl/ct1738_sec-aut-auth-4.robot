# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/CT1738_SEC-AUT-AUTH-4.txt#1 $
# $Date: 2020/10/08 $
# $Author: nthallap $


*** Settings ***
Resource     sma/csdlresource.txt
Resource     esa/logs_parsing_snippets.txt

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Set Appliance Under Test to SMA
...  Initialize Suite

Suite Teardown  DefaultTestSuiteTeardown


*** Variables ***
${CHANGE_PASSPHRASE}=            //h1[contains(text(), 'Change Passphrase')]
${ACTION_MESSAGE}=               //td[@id="action-results-message"]
${OLD_PASSWORD_TEXTBOX}=         //input[@name='old_pwd']
${NEW_PASSWORD_TEXTBOX}=         //input[@name='passwdv']
${RETYPE_NEW_PASSWORD_TEXTBOX}=  //input[@name='repasswd']
${SUBMIT_BTN}=                   //input[@value='Submit']


*** Keywords ***
Initialize Suite
    global_sma.DefaultTestSuiteSetup
    Initialize Users

Verify SCP Log Push
    Log Subscriptions Rollover  gui_logs
    Sleep  5s  msg=Wait for logs roll over
    Verify And Wait For Log Records
    ...  search_path=/data/pub/system_logs/system.current
    ...  wait_time=2 mins
    ...  Push success for subscription gui_logs >= 1

Verify Local User Role
	[Arguments]  ${user_name}  ${local_user_role}
    ${users_info} =  Users Get List
    Log    ${users_info}
    ${user} =  Get From Dictionary  ${users_info}  ${user_name}
    ${user_role} =  Get From List  ${user}  1
    Should Be Equal  ${user_role}  ${local_user_role}

Add LDAP Server
    LDAP Add Server Profile  ${LDAP_SERVER_PROFILE}  ${LDAP_AUTH_SERVER}
    ...  server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit External Authentication Queries  ${LDAP_SERVER_PROFILE}
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Commit Changes

Tvh1468362c Setup
    DefaultTestCaseSetup
    Users Add User  ${TEST_USER1}  ${TEST_USER1}  ${TEST_USER_PSW}  ${sma_user_roles.ADMIN}
    Users Add User  ${TEST_USER2}  ${TEST_USER2}  ${TEST_USER_PSW}  ${sma_user_roles.OPERATOR}
    Users Add User  ${TEST_USER7}  ${TEST_USER7}  ${TEST_USER_PSW}  ${sma_user_roles.RO_OPERATOR}
    Users Add User  ${TEST_USER8}  ${TEST_USER8}  ${TEST_USER_PSW}  ${sma_user_roles.GUEST}
    Users Add User  ${TEST_USER9}  ${TEST_USER9}  ${TEST_USER_PSW}  ${sma_user_roles.TECHNICIAN}
    Users Add User  ${TEST_USER10}  ${TEST_USER10}  ${TEST_USER_PSW}  ${sma_user_roles.EMAIL_ADMIN}
    Users Add User  ${TEST_USER11}  ${TEST_USER11}  ${TEST_USER_PSW}  ${sma_user_roles.WEB_ADMIN}
    Commit Changes
    @{users}  Create List  ${TEST_USER1}   ${TEST_USER2}  ${TEST_USER7}  ${TEST_USER8}  ${TEST_USER9}  ${TEST_USER10}  ${TEST_USER11}
    Set Test Variable   @{users}

Common Test Setup
	[Arguments]  ${user_name}  ${user_role}
    DefaultTestCaseSetup
    Users Add User  ${user_name}  ${user_name}  ${TEST_USER_PSW}  ${user_role}
    Commit Changes
    @{users}  Create List  ${user_name}
    Set Test Variable   @{users}

Tvh1468361c And Tvh1468377c Teardown
	[Arguments]  ${profile}
    Restart CLI Session
    Run Keyword And Ignore Error    Log Out Of Dut
    Log Into Dut
    LDAP Delete Server Profile  ${profile}
    Commit Changes
    User Config External Setup Disable
    Commit
    DefaultTestCaseTeardown

Common Test Teardown
    [Arguments]  @{users}
    Restart CLI Session
    Log Out Of Dut
    Log Into Dut
    FOR  ${user}  IN  @{users}
       Users Delete User  ${user}
       Commit Changes
    END
    DefaultTestCaseTeardown


*** Test Cases ***
Tvh1468376c
    [Documentation]  Configure SAML for external authentication and map group of users to pre-defined \n
    ...  roles, verify users from configured groups can only be authenticated and others \n
    ...  failed to access SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468376 \n
    [Tags]   Tvh1468376c  csdl  SEC-AUT-AUTH-4
    [Setup]  Run Keywords
    ...  DefaultTestCaseSetup
    ...  Add Customer SAML Config Azure
    ...  Commit Changes
    ...  Enable Externalauth SAML
    ...  Log Out Of Dut
    [Teardown]    Run Keywords
    ...  Close Browser
	...  Selenium Login
    ...  User Config External Setup Disable
    ...  Saml Config Delete
    ...  Commit
    ...  DefaultTestCaseTeardown
    SSO Log Into Dut    customer    ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}
    Close Browser
    Launch Dut Browser
    Run Keyword And Expect Error  *  SSO Log Into Dut    customer    user1@gmail.com     Ironport159$

Tvh1468377c
    [Documentation]  Configure Cisco AD for external authentication and map group of users/alias to pre \n
    ...  -defined roles, verify users from configured groups/alias can only be authenticated \n
    ...  and others failed to access SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468377 \n
    ...  Verify users from Cisco Active Directory Group can access SMA based on permissions given \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468375 \n
    [Tags]   Tvh1468377c  Tvh1468375c  csdl  SEC-AUT-AUTH-4
    [Setup]   Run Keywords
    ...  DefaultTestCaseSetup
    ...  AND  Add Cisco Ad As LDAP
    ...  AND  Edit External Authentication LDAP User Role  ${CISCO_AD}  ${TEST_USER_GROUP_MAPPING}  ${sma_user_roles.ADMIN}
    [Teardown]  Run Keyword  Tvh1468361c And Tvh1468377c Teardown  ${CISCO_AD}
    #If Login Failed It can be due to password expiry
    Log Out Of Dut
    Log Into Dut  ${CISCO_TEST_USER_MAIL}  ${CISCO_TEST_PASSWORD}
    Log Out Of Dut
    Log Into Dut
    Edit External Authentication LDAP User Role  ${CISCO_AD}  ${TEST_USER_GROUP_MAPPING}  ${sma_user_roles.OPERATOR}
    Log Out Of Dut
    Log Into Dut  ${CISCO_TEST_USER_MAIL}  ${CISCO_TEST_PASSWORD}
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Log Out Of Dut
    Log Into Dut
    Edit External Authentication LDAP User Role  ${CISCO_AD}  ${TEST_USER_GROUP_MAPPING}  ${sma_user_roles.GUEST}
    Log Out Of Dut
    Log Into Dut  ${CISCO_TEST_USER_MAIL}  ${CISCO_TEST_PASSWORD}
    Run Keyword And Expect Error  *  DNS Add Local Server  10.92.144.4
    Navigate To  Centralized Services  System Status
    Log Out Of Dut
    Run Keyword And Expect Error  *  Log Into Dut  test   ironport
    Close Cli Session
    Start Cli Session  ${CISCO_TEST_USER_NAME}  ${CISCO_TEST_PASSWORD}
    ${log}=   Version
    Log  ${log}

Tvh1468362c
    [Documentation]  Verify SMA provides option to assign roles to each users created internally \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468362 \n
    [Tags]   Tvh1468362c  csdl  SEC-AUT-AUTH-4
    [Setup]  Tvh1468362c Setup
    [Teardown]  Common Test Teardown  @{users}
    Log Out Of Dut
    Log Into Dut  ${TEST_USER1}  ${TEST_USER_PSW}
    #Verifying Users roles created internally
    #Added user as Administrator. Verifying  user role should be Administrator
    Verify Local User Role  ${TEST_USER1}  ${sma_user_roles.ADMIN}

    #Verifying Users roles created internally
    #Added user as Operator. Verifying  user role should be Operator
    Verify Local User Role  ${TEST_USER2}  ${sma_user_roles.OPERATOR}

    #Verifying Users roles created internally
    #Added user as Read only operator. Verifying  user role should be Readonly operator
    Verify Local User Role  ${TEST_USER7}  ${sma_user_roles.RO_OPERATOR}

    #Verifying Users roles created internally
    #Added user as Guest. Verifying  user role should be  guest
    Verify Local User Role  ${TEST_USER8}  ${sma_user_roles.GUEST}

    #Verifying Users roles created internally
    #Added user as Technician. Verifying  user role should be Technician
    Verify Local User Role  ${TEST_USER9}  ${sma_user_roles.TECHNICIAN}

    #Verifying Users roles created internally
    #Added user as Email Admin. Verifying  user role should be Email Admin
    Verify Local User Role  ${TEST_USER10}  ${sma_user_roles.EMAIL_ADMIN}

    #Verifying Users roles created internally
    #Added user as  Web Admin. Verifying  user role should be Web Admin
    Verify Local User Role  ${TEST_USER11}  ${sma_user_roles.WEB_ADMIN}

Tvh1468371c
    [Documentation]  Verify local users has provision to reset/manage their credentials \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468371 \n
    [Tags]   Tvh1468371c  csdl  SEC-AUT-AUTH-4
    [Setup]  Common Test Setup  ${TEST_USER3}  ${sma_user_roles.ADMIN}
    [Teardown]  Common Test Teardown  @{users}
    Set Test Variable  ${test_user_update}  Ironport490$
    Set Test Variable  ${test_user_update_2}  Ironport186$
    Log Out Of Dut
    Log Into Dut  ${TEST_USER3}  ${TEST_USER_PSW}
    Change Password  ${TEST_USER_PSW}  ${test_user_update}
    Log Out Of Dut
    Log Into Dut  ${TEST_USER3}  ${test_user_update}

    Close Cli Session
    Start Cli Session  ${TEST_USER3}  ${test_user_update}
    Passwd  old_pwd=${test_user_update}  new_pwd=${test_user_update_2}

    Log Out Of Dut
    Log Into Dut  ${TEST_USER3}   ${test_user_update_2}

Tvh1468366c
    [Documentation]  Verify Root admin can grant/revoke access for other admin/non-admin users \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468366 \n
    [Tags]   Tvh1468366c  csdl  SEC-AUT-AUTH-4
    [Setup]  Common Test Setup  ${TEST_USER4}  ${sma_user_roles.ADMIN}
    [Teardown]  Common Test Teardown  @{users}
    Users Lock Account  ${TEST_USER4}
    Commit Changes
    ${users_info}=  Users Get List
    Log    ${users_info}
    ${user} =  Get From Dictionary  ${users_info}  ${TEST_USER4}
    ${user_status} =  Get From List  ${user}  2
    Should Be Equal  ${user_status}  Locked
    Users Unlock Account  ${TEST_USER4}
    Commit Changes
    ${users_info} =  Users Get List
    Log    ${users_info}
    ${user} =  Get From Dictionary  ${users_info}  ${TEST_USER4}
    ${user_status} =  Get From List  ${user}  2
    Should Be Equal  ${user_status}  Active

    #Locking user from CLI
	User Config Status Lock  ${TEST_USER4}
    ${users_info}=  Users Get List
    Log    ${users_info}
    ${user} =  Get From Dictionary  ${users_info}  ${TEST_USER4}
    ${user_status} =  Get From List  ${user}  2
    Should Be Equal  ${user_status}  Locked

    #Unlock user from CLI
    user_config_status_unlock  ${TEST_USER4}
    ${users_info} =  Users Get List
    Log    ${users_info}
    ${user} =  Get From Dictionary  ${users_info}  ${TEST_USER4}
    ${user_status} =  Get From List  ${user}  2
    Should Be Equal  ${user_status}  Active

Tvh1468367c
    [Documentation]  Verify an admin can change a role/privileges of any user account at any time \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468367 \n
    [Tags]   Tvh1468367c  csdl  SEC-AUT-AUTH-4
    [Setup]  Common Test Setup  ${TEST_USER5}  ${sma_user_roles.ADMIN}
    [Teardown]  Common Test Teardown  @{users}
    Set Test Variable  ${test_user_update}  Ironport179$
    Set Test Variable  ${test_user_update_2}  Ironport130$
    ${users_info} =  Users Get List
    Log    ${users_info}
    ${user} =  Get From Dictionary  ${users_info}  ${TEST_USER5}
    ${user_role} =  Get From List  ${user}  1
    Should Be Equal  ${user_role}  ${sma_user_roles.ADMIN}
    Users Edit User  ${TEST_USER5}  password=${test_user_update}  user_role=${sma_user_roles.OPERATOR}
    Commit Changes
    ${users_info} =  Users Get List
    Log    ${users_info}
    ${user} =  Get From Dictionary  ${users_info}  ${TEST_USER5}
    ${user_role} =  Get From List  ${user}  1
    Should Be Equal  ${user_role}  ${sma_user_roles.OPERATOR}
    Log Out Of Dut
    Log Into Dut  ${TEST_USER5}  ${test_user_update}
    Restart CLI Session
    User Config Edit  ${TEST_USER5}  password=${test_user_update_2}  group=${sma_user_roles.GUEST}
    Commit
    Log Out Of Dut
    Log Into Dut  ${TEST_USER5}  ${test_user_update_2}

Tvh1468357c
    [Documentation]  Verify logs can be pushed only to authenticated servers via SCP \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468357 \n
    [Tags]   Tvh1468357c  csdl  SEC-AUT-AUTH-4
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown
    Roll Over Now  system_logs
    OperatingSystem.Run And Return Rc  rm -f %{HOME}/.ssh/authorized_keys
    OperatingSystem.Create File  %{HOME}/.ssh/authorized_keys
	${scp_log_folder}=  Evaluate  tempfile.mkdtemp()  tempfile
    Log Subscriptions Set Retrieval Method to SCP Push  gui_logs
    ...  ${CLIENT_IP}
    ...  ${scp_log_folder}
    ...  %{USER}
    ...  port=22
    ...  enable_key_checking=${False}
    ${ssh_text}=  Get Text  xpath=${ACTION_MESSAGE}

    ${ssh_text}=  Get Lines Containing String  ${ssh_text}  ssh-
    Log  ${ssh_text}
    Commit Changes
    Log Subscriptions Rollover  gui_logs
    Sleep  5s  msg=Wait for logs roll over
    Verify And Wait For Log Records
    ...  search_path=/data/pub/system_logs/system.current
    ...  wait_time=2 mins
    ...  Push error for subscription gui_logs >= 1

    OperatingSystem.Append to File  %{HOME}/.ssh/authorized_keys  ${ssh_text}
	Wait Until Keyword Succeeds  4 min  20 sec  Verify SCP Log Push
	OperatingSystem.Directory Should Not Be Empty  ${scp_log_folder}
	@{items}=  OperatingSystem.List Directory  ${scp_log_folder}
	Log  ${items}
	OperatingSystem.Run And Return Rc  rm -rf ${scp_log_folder}

Tvh1468361c
    [Documentation]  Verify External users from LDAP should be authenticated before \n
    ...  accessing SMA's CLI or GUI \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468361 \n
    ...  Verify SMA has control to assign roles to External users authenticated via LDAP \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468363 \n
    ...  Configure LDAP for external authentication and map group of users to pre-defined \n
    ...  roles, verify users from configured groups can only be authenticated and others \n
    ...  failed to access SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468372 \n
    ...  Verify External users can access UI/CLI based on roles assigned by admin \n
    ...  tims.cisco.com/view-entity.cmd?ent=1468370 \n
    [Tags]   Tvh1468361c  Tvh1468363c  Tvh1468372c  Tvh1468370c  csdl  SEC-AUT-AUTH-4
    [Setup]    Run Keywords
    ...  DefaultTestCaseSetup
    ...  Add LDAP Server
    [Teardown]  Run Keyword  Tvh1468361c And Tvh1468377c Teardown  ${LDAP_SERVER_PROFILE}
    #Verifying Non LDAP user tying to access SMA from GUI and CLI
    Log Out Of Dut
    Run Keyword And Expect Error  *  Log Into Dut  non_ldap_user  non_ldap_psw
    Log Into Dut

    #Verifying LDAP Administrator user accessibility
    Edit External Authentication LDAP User Role  ${LDAP_SERVER_PROFILE}  ${LDAP_SMA_USER_GROUP}  ${sma_user_roles.ADMIN}
    Log Out Of Dut
    Log Into Dut  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    Navigate To  System Administration  System Setup Wizard
    Navigate To  System Administration  System Upgrade
    Close Cli Session
    Start Cli Session  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    ${log}=   Version
    Log  ${log}

    #Verifying LDAP Operator user accessibility
    Log Out Of Dut
    Log Into Dut
    Edit External Authentication LDAP User Role  ${LDAP_SERVER_PROFILE}  ${LDAP_SMA_USER_GROUP}  ${sma_user_roles.OPERATOR}
    Log Out Of Dut
    Log Into Dut  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Navigate To  Network  DNS
    Close Cli Session
    Start Cli Session  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    ${log}=   Version
    Log  ${log}

    #Verifying LDAP Guest user accessibility
    Log Out Of Dut
    Log Into Dut
    Edit External Authentication LDAP User Role  ${LDAP_SERVER_PROFILE}  ${LDAP_SMA_USER_GROUP}  ${sma_user_roles.GUEST}
    Log Out Of Dut
    Log Into Dut  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Run Keyword And Expect Error  *  DNS Add Local Server  10.92.144.4
    Navigate To  Centralized Services  System Status
    Close Cli Session
    Start Cli Session  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    ${log}=   Version
    Log  ${log}

Tvh1472042c
    [Documentation]  Verify SMA has control to assign roles to External users authenticated via Radius \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472042 \n
    ...  Configure RADIUS for external authentication and map group of users to pre -defined \n
    ...  roles, verify users from configured groups can only be authenticated and others \n
    ...  failed to access SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472043 \n
    ...  Verify External users from Radius should be authenticated before accessing SMA's CLI or GUI \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472044 \n
    [Tags]   Tvh1472042c  Tvh1472043c  Tvh1472044c  csdl  SEC-AUT-AUTH-4
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Run Keywords
    ...  Restart CLI Session
    ...  Log Out Of Dut
    ...  Log Into Dut
    ...  User Config External Setup Disable
    ...  Commit
    ...  DefaultTestCaseTeardown
    #Verifying Non RADIUS user tying to access SMA from GUI and CLI
    Log Out Of Dut
    Run Keyword And Expect Error  *  Log Into Dut  non_radius_user  non_radius_psw
    Log Into Dut

    #Verifying Radius Administrator user accessibility
    Edit External Authentication Radius User Role  ${sma_user_roles.ADMIN}
    Log Out Of Dut
    Log Into Dut  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    Navigate To  System Administration  System Setup Wizard
    Navigate To  System Administration  System Upgrade
    Close Cli Session
    Start Cli Session  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    ${log}=   Version
    Log  ${log}

    #Verifying Radius Read only Operator user accessibility
    Log Out Of Dut
    Log Into Dut
    Edit External Authentication Radius User Role  ${sma_user_roles.RO_OPERATOR}
    Log Out Of Dut
    Log Into Dut  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Navigate To  Network  DNS
    Close Cli Session
    Start Cli Session  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    ${log}=   Version
    Log  ${log}

    #Verifying Radius TECHNICIAN user accessibility
    Log Out Of Dut
    Log Into Dut
    Edit External Authentication Radius User Role  ${sma_user_roles.TECHNICIAN}
    Log Out Of Dut
    Log Into Dut  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    Run Keyword And Expect Error  *  DNS Add Local Server  10.92.144.4
    Navigate To  Centralized Services  System Status
    Navigate To  System Administration  Feature Keys
    Close Cli Session
    Start Cli Session  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    ${log}=   Version
    Log  ${log}

Tvh1468368c
    [Documentation]  Verify Root /other admins can assign/force other users to modify their credentials \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468368 \n
    [Tags]   Tvh1468368c  csdl  SEC-AUT-AUTH-4
    [Setup]  Common Test Setup  ${TEST_USER6}  ${sma_user_roles.OPERATOR}
    [Teardown]  Common Test Teardown  @{users}
    Set Test Variable  ${test_user_update}  Ironport169$
    Set Test Variable  ${test_user_update2}  Ironport179$
    Log Out Of Dut
    Log Into Dut  ${TEST_USER6}  ${TEST_USER_PSW}
    Log Out Of Dut
    Log Into Dut
    User Config Edit  ${TEST_USER6}  password=${test_user_update}  group=${sma_user_roles.GUEST}
    Commit
    Log Out Of Dut
    Log Into Dut  ${TEST_USER6}  ${test_user_update}
    User Config Password Force  ${TEST_USER6}
    Log Out Of Dut
    Log Into Dut  ${TEST_USER6}  ${test_user_update}
    Page Should Contain Element  ${CHANGE_PASSPHRASE}

    #Not able to Use Change Password Keyword here.
    Input Text  ${OLD_PASSWORD_TEXTBOX}  ${test_user_update}
    Input Text  ${NEW_PASSWORD_TEXTBOX}  ${test_user_update2}
    Input Text  ${RETYPE_NEW_PASSWORD_TEXTBOX}  ${test_user_update2}
    Click Element  ${SUBMIT_BTN}
    Log Out Of Dut
    Log Into Dut  ${TEST_USER6}  ${test_user_update2}

