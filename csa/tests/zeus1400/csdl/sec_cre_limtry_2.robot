# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_cre_limtry_2.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/global_sma.txt
Resource     sma/csdlresource.txt

Force Tags   csdl
Suite Setup   CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${USER_ADMIN}  admin1
${FULL_NAME}  test user
${USER_ADMIN_PASS}  Cisco12$
${wrong_password}  abcd
${pasword_attempt}  3
${account_lock_attempt}  3
${authentication_log_name}   authentication
${authentication_log_path}  /data/pub/${authentication_log_name}/${authentication_log_name}.current
${authentication_login_failure_message}  The user admin has exceeded the limit of login attempts when trying to authenticate via the web interface
${cli_authentication_login_failure_message}  Too many authentication failures
${gui_toomany_wrong_authentication_message}  	Too many login attempts. Please try after sometime.
${gui_account_lock_message}    User account is locked. Contact Administrator to unlock it.


*** Keywords ***
Try to enter wrong password ${wrong_attempt} times in CLI

    Establish SSH Connection To  ${CLIENT_HOSTNAME}  ${TESTUSER}  ${TESTUSER_PASSWORD}  $
    Enter option ssh -o StrictHostKeyChecking=no ${DUT_ADMIN}@${SMA} and read
    FOR    ${INDEX}    IN RANGE       ${${wrong_attempt}-1}
       Log  Attempt_${INDEX}
       Enter option ${wrong_password} and read
    END

Precondition Tvh1209152c

    Run keyword and ignore error  Log Out Of Dut
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Enable Spam Quarantine On SMA
    Log Out Of Dut

Delete User and disable Account locking
    [Arguments]  ${user}
    Users Delete User   ${user}
    Disable account locking
    Commit Changes
    Log Out Of Dut

Verify too many authentication failures error message in CLI after password attempts
    [Arguments]  ${cli_authentication_login_failure_message}

    ${auth_failure}=  Enter option ${wrong_password} and read
    should contain   ${auth_failure}   ${cli_authentication_login_failure_message}

Login to DUT with new user and invalid password for max attempt and check account lock error
    [Arguments]  ${user_admin}  ${wrong_password}
    Run keyword and ignore error  Login To DUT  ${user_admin}  ${wrong_password}
    Page Should Contain  User account is locked. Contact Administrator to unlock it.

*** Test Cases ***
Tvh1209149c
    [Documentation]  Tvh1209149c-Verify that system will restrict attempts of authentication via CLI per minute on login failure
    ...  Tvh1209146c-Verify Option is provided to specify restrict attempts of authentication via CLI per minute on login failure
    ...  Tvh1209151c-Verify that authentication is successful a minute after system has limited attempts of authentication via CLI
    ...  FLOW DETAILS
    ...  Login to SMA- > Check Login attempt configuration attempts per minute option in CLI
    ...  Login to SMA- > Verify too many authentication failures error message in CLI
    ...  Login to SMA- > Check Login attempt configuration attempts per minute option in CLI and check lock in UI

    [Tags]  cli  Tvh1209149c  Tvh1209146c  Tvh1209151c  Tvh1209148c
    [Teardown]  Set SSHLib Prompt  ${empty}


    User Config Policy Account  login_attempts_minute=${pasword_attempt}
    Commit
    Try to enter wrong password ${pasword_attempt} times in CLI
    Verify too many authentication failures error message in CLI after password attempts  ${cli_authentication_login_failure_message}
    Wait for 60 seconds for the password expiration time
    Login to DUT with invalid password and check wrong password error  ${DUT_ADMIN}  ${wrong_password}   ${pasword_attempt}
    Login to DUT with invalid password and check multiple login attempt error  ${DUT_ADMIN}  ${wrong_password}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    Wait for 60 seconds for the password expiration time
    Login to DUT with invalid password and check wrong password error  ${DUT_ADMIN}  ${wrong_password}   ${pasword_attempt}
    Login to DUT with invalid password and check multiple login attempt error  ${DUT_ADMIN}  ${wrong_password}

    Wait for 60 seconds for the password expiration time
    Login to DUT and check login is successful  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

Tvh1209142c
    [Documentation]  Tvh1209142c-Verify Option is provided to specify restrict attempts of authentication via WebUI per minute on login failure
    ...  Tvh1209148c-Verify that system will restrict attempts of authentication via WebUI per minute on login failure
    ...  Tvh1209150c-Verify that authentication is successful a minute after system has limited attempts of authentication via WEBUI
    ...  FLOW DETAILS
    ...  Login to SMA and check option to enable login attempts to 3
    ...  Login with invalid credentials to SMA and try 4th time with invalid credential and check 'Too many failures' message
    ...  Verify authentication logs for login limit exceeded message
    ...  Login with invalid credentials to SMA and try 4th time with valid credential and check 'Too many failures' message

    [Tags]  gui  Tvh1209142c  Tvh1209148c  Tvh1209150c  Tvh1209154c
    [Setup]  Clear and Roll over logs  ${authentication_log_path}  ${authentication_log_name}

     Login to SMA and update Account login attempts  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}   ${pasword_attempt}
     Login to DUT with invalid password and check wrong password error  ${DUT_ADMIN}  ${wrong_password}  ${pasword_attempt}
     Login to DUT with invalid password and check multiple login attempt error  ${DUT_ADMIN}  ${wrong_password}
     Wait for 60 seconds for the password expiration time
     Verify logs  ${authentication_log_name}  The user ${DUT_ADMIN} has exceeded the limit of login attempts when trying to authenticate via the web interface
     Login to DUT with invalid password and check wrong password error  ${DUT_ADMIN}  ${wrong_password}  ${pasword_attempt}
     Login to DUT with valid password and check multiple login attempt error  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
     Wait for 60 seconds for the password expiration time
     Login to DUT and check login is successful  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

Tvh1209156c
    [Documentation]  Tvh1209156c-Verify that system will restrict attempts of authentication per minute  and lock the user on login failure, if this and lock accounts options enabled
        ...  FLOW DETAILS
        ...  Create new user System Administration
        ...  Pre condition- Enable option <Lock accounts after _ failed login attempts> - 3
        ...  Precondition - Enable option <Allow up to _ login attempts per minute> - 3
        ...  Update from CLI and GUI
        ...  Login with new username and invalid passphrase for 3 times.
        ...  On 4th attempt check that new user account is locked

    [Tags]  gui  cli  Tvh1209156c
    [Teardown]  Delete User and disable Account locking  ${USER_ADMIN}

    Login to SMA and update Account login attempts   ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}  ${pasword_attempt}
    Add user in SMA  ${USER_ADMIN}  ${FULL_NAME}  ${USER_ADMIN_PASS}  ${sma_user_roles.ADMIN}
    Update Account locking attempts  ${account_lock_attempt}
    Login to DUT with new user and invalid password and check wrong password error  ${USER_ADMIN}  ${wrong_password}  ${pasword_attempt}
    Login to DUT with new user and invalid password for max attempt and check account lock error  ${USER_ADMIN}  ${wrong_password}
    Sleep  60
    Login to DUT with new user and valid password and check account error  ${USER_ADMIN}  ${USER_ADMIN_PASS}  ${gui_account_lock_message}
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Verify user status is  ${USER_ADMIN}  Locked
    Delete User and disable Account locking  ${USER_ADMIN}
    Add user in SMA  ${USER_ADMIN}  ${FULL_NAME}  ${USER_ADMIN_PASS}  ${sma_user_roles.ADMIN}
    Start CLI Session
    User Config Policy Account  login_attempts_minute=${pasword_attempt}  autolock=yes  attempts=${account_lock_attempt}
    Commit
    Login to DUT with new user and invalid password and check wrong password error  ${USER_ADMIN}  ${wrong_password}  ${pasword_attempt}
    Login to DUT with new user and invalid password for max attempt and check account lock error  ${USER_ADMIN}  ${wrong_password}
    Login to DUT with new user and valid password and check account error  ${USER_ADMIN}  ${USER_ADMIN_PASS}  ${gui_toomany_wrong_authentication_message}
    Sleep  60
    Login to DUT with new user and valid password and check account error  ${USER_ADMIN}  ${USER_ADMIN_PASS}  ${gui_account_lock_message}
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Verify user status is  ${USER_ADMIN}  Locked

Tvh1209152c

    [Documentation]  Tvh1209152c-Verify that system will restrict attempts of authentication via Spam Quarantine UI per minute on login failure
    ...  Tvh1209153c- Verify that authentication is successful a minute after system has limited attempts of authentication for Spam Quarantine UI
    ...  FLOW DETAILS
    ...  From SMA UI
    ...  Enable End User Spam Quarantine
    ...  Configure login attempts from UI to 3 attempts
    ...  Login with invalid credentials to Spam qurantine and try 4th time with invalid credential and check 'Too many failures' message
    ...  Login with invalid credentials to Spam qurantine and try 4th time with valid credential and check 'Too many failures' message
    ...  Login after 1 minute to check successful login

    [Tags]  gui  Tvh1209152c  Tvh1209153c
    [Setup]  Run Keywords
    ...  Precondition Tvh1209152c

    Login to SMA and update Account login attempts  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}   ${pasword_attempt}
    Launch SPAM Quarantine portal   ${SQ_USER}  ${SQ_USER_PASSWORD}
    Login to SPAM Quarantine with invalid password and check wrong password error  ${SQ_USER}  ${wrong_password}  ${pasword_attempt}
    Login to SPAM Quarantine with invalid password and check multiple login attempt error  ${SQ_USER}  ${wrong_password}
    Wait for 60 seconds for the password expiration time
    Login to SPAM Quarantine with invalid password and check wrong password error  ${SQ_USER}  ${wrong_password}  ${pasword_attempt}
    Login to SPAM Quarantine with valid password and check multiple login attempt error  ${SQ_USER}  ${SQ_USER_PASSWORD}
    Wait for 60 seconds for the password expiration time
    Login to SPAM Qurantine and check login is successful  ${SQ_USER}  ${SQ_USER_PASSWORD}