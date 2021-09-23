#$Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_cre_nolock.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/global_sma.txt
Resource     regression.txt
Resource     SSHLibrary
Resource     sma/csdlresource.txt


Force Tags   csdl
Suite Setup   CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown


*** Variables ***
${wrong_password}  abcd
${pasword_attempt}  30
${retry_attempt}  10
${cli_authentication_login_failure_message}  Too many authentication failures

*** Keywords ***

Setup Tvh1340565c
    Login to SMA and update Account login attempts  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}  ${pasword_attempt}
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Disable account locking
    Commit Changes
    Log Out Of Dut

Enter wrong password and check multiple authentication failure message in CLI
    [Arguments]  ${failure_message}

    Establish SSH Connection To  ${CLIENT_HOSTNAME}  ${TESTUSER}    ${TESTUSER_PASSWORD}  $
    Enter option ssh ${DUT_ADMIN}@${SMA} and read
    Wait until keyword succeeds  1 min  2 sec  Input wrong password and check failure message  ${failure_message}

Input wrong password and check failure message
    [Arguments]  ${failure_message}
    ${out}=  Enter option ${wrong_password} and read
    should contain  ${out}  ${failure_message}

*** Test Cases ***
Tvh1340565c
    [Documentation]  Tvh1340565c-Verify by default on SMA, Account Lock on login failures is not enabled
        ...  FLOW DETAILS
        ...  Login to SMA and check option to disable account lock--> Disable Account lock under Users
        ...  1a)Try to login to SMA 10 times from UI and verify wrong password error
        ...  1b)Login to SMA after unsuccessful attempts and loging should be successful
        ...  2a)Try to login to SMA via CLI with wrong password and verify multiple authentication failure
        ...  2b)After unsuccessfull attempts, try login attempt and login should be successful

    [Tags]  gui  cli  Tvh1340565c
    [Setup]  Setup Tvh1340565c
    [Teardown]  Set SSHLib Prompt  ${empty}

    Login to DUT with invalid password and check wrong password error  ${DUT_ADMIN}  ${wrong_password}  ${retry_attempt}
    Login to DUT and check login is successful  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Enter wrong password and check multiple authentication failure message in CLI    ${cli_authentication_login_failure_message}
    Connect to SMA  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}