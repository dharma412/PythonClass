# $Id: //prod/main/sarf_centos/tests/zeus1350/postel/regression/common/users/strong_password_controls/alerts/alerts.txt#5 $ $DateTime: 2020/07/19 22:21:01 $ $Author: vsugumar $

*** Settings ***
Resource  regression.txt

Suite Setup     Run Keywords  DefaultRegressionSuiteSetup
Suite Teardown  Run Keywords  DefaultRegressionSuiteTeardown  Close All Connections
Test Setup      Run Keywords  DefaultRegressionTestCaseSetup   Selenium Login
Test Teardown   Run Keywords  DefaultRegressionTestCaseTeardown  Selenium Close
Force Tags  users.strong_password_controls

*** Variables ***
${user_name}  user1
${full_user_name}  User1
${user2_name}  user2
${user2_password}  Ironport@12
${full_user2_name}  User2
${invalid_user_password}  invalid_password

${current_status_path}  //*[@id='action-results-title']
${current_msg_path}  //*[@id='action-results-message']

*** Keywords ***
Check Login Result
    [Arguments]  ${expected_status}  ${expected_msg}
    ${current_status}  Get Text  ${current_status_path}
    ${current_msg}    Get Text  ${current_msg_path}
    Should Contain  ${current_status}   ${expected_status}
    Should Contain  ${current_msg}   ${expected_msg}

*** Test Cases ***
Tvh570033c
    [Tags]  Tvh570033c  standard
    [Documentation]  Verify that alert is sent if user was locked automatically
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh570033c
    ...  \n 1. Add local user
    ...  \n 2. Enable option to show warning message for users with locked account, specify custom message
    ...  \n 3. As admin configure account locking after 3 unsuccessful login attempts
    ...  \n 4. As local user make 3 unsuccessful login attempt via GUI
    ...  \n 5. Check email for alerts
    ...  \n 6. Verify that alert was received
    ...  \n 7. As local user make 3 unsuccessful login attempt via CLI
    ...  \n 8. Check email for alerts
    ...  \n 9. Verify that alert was received

    Set Test Variable  ${Test_Id}  ${TEST NAME}
    Start CLI Session If Not Open
    Update Config Validate Certificates  validate_certificates=no
    Update Config Dynamichost  dynamic_host=${UPDATE_SERVER}:443
    Commit
    Sleep  2m
    Null Smtpd Start
    Selenium Login
    Alerts Add Recipient  ${TESTUSER}@${CLIENT_HOSTNAME}  all-all
    Alerts Edit Settings  ${None}  ${True}  30  60
    Users Add User  ${user_name}  ${full_user_name}  ${DUT_ADMIN_SSW_PASSWORD}
    Users Add User  ${user2_name}  ${full_user2_name}  ${user2_password}
    Users Edit Account Locking  lock_failed_login=3  display_message=Account has been locked
    Commit Changes

    Log Out Of DUT
    Set Test Variable  ${index}  3
    Set Test Variable  ${count}  0

    :FOR  ${i}  IN RANGE  0   2
    \  Run Keyword And Ignore Error  Log Into DUT  ${user_name}  ${invalid_user_password}
    \  ${count}=  Evaluate  ${count}+1
    \  ${attempt}=  Evaluate  ${index}-${count}
    \  Check Login Result  Error   Invalid username or passphrase. Attempts Left: ${attempt}

    Run Keyword And Ignore Error  Log Into DUT  ${user_name}  ${invalid_user_password}
    Check Login Result  Attention  User account is locked. Contact Administrator to unlock it.

    :FOR  ${msg_index}  IN RANGE  3
    \  ${msg} =  Null Smtpd Next Message  timeout=120
    \  ${msg}  Convert To String  ${msg}
    \  Log   msg= ${msg}
    \  @{key}  Run Keyword and Ignore Error  Should Match  "${msg}"  *User "${user_name}" is locked after 3 consecutive login failures*
    \  Run Keyword If  '@{key}[0]'=='PASS'  Exit For Loop
    \  Sleep  6s

    :FOR  ${i}  IN RANGE  0   3
    \  ${address} =  Get Host IP By Name  ${SMA}
    \  SSHLibrary.Open Connection  ${address}
    \  ${msg}=  Run Keyword And Expect Error    *    SSHLibrary.Login  ${user2_name}  ${invalid_user_password}
    \  Should Contain   ${msg}  Authentication failed

    :FOR  ${msg_index}  IN RANGE  3
    \  ${msg} =  Null Smtpd Next Message  timeout=120
    \  ${msg}  Convert To String  ${msg}
    \  Log   msg= ${msg}
    \  @{key}  Run Keyword and Ignore Error  Should Match  ${msg}  *User "${user2_name}" is locked after 3 consecutive login failures*
    \  Run Keyword If  '@{key}[0]'=='PASS'  Exit For Loop
    \  Sleep  6s
    Null Smtpd Stop

Tvh570257c
    [Tags]  Tvh570257c  standard
    [Documentation]  Verify that alert is not sent if user was locked manually
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh570257c
    ...  \n 1. Add local user
    ...  \n 2. Lock user account via GUI
    ...  \n 3. Check email for alerts
    ...  \n 4. Verify that alert was not received
    ...  \n 5. Lock user account via CLI
    ...  \n 6. Check email for alerts
    ...  \n 7. Verify that alert was not received

    Set Test Variable  ${Test_Id}  ${TEST NAME}

    Null Smtpd Start
    Alerts Add Recipient  ${TESTUSER}@${CLIENT_HOSTNAME}  all-all
    Users Add User  ${user_name}  ${full_user_name}  ${DUT_ADMIN_SSW_PASSWORD}
    Users Add User  ${user2_name}  ${full_user2_name}  ${user2_password}
    Commit Changes

    Users Lock Account  ${user_name}

    ${msg} =  Null Smtpd Next Message  timeout=60
    Should Not Match  "${msg}"  *User "${user_name}" is locked after 3 consecutive login failures*

    User Config Status Lock  ${user2_name}

    ${msg} =  Null Smtpd Next Message  timeout=60
    Null Smtpd Stop
    Should Not Match  "${msg}"  *User "${user2_name}" is locked after 3 consecutive login failures*
