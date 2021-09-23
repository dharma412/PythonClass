# $Id: //prod/main/sarf_centos/tests/zeus1350/csdl/sec_cre_nolock.txt#1 $
# $Date: 2020/04/23 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/global_sma.txt
Resource     regression.txt
Resource     SSHLibrary
Resource     csdlresource.txt


Force Tags   csdl
Suite Setup   CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${authentication_log_name}   authentication
${inactivity_timeout}  5
${default_inactivity_timeout}  30

*** Keywords ***
Set inactivity timeout   #Move to csdl resource file
    [Arguments]  ${gui_timeout}=30  ${cli_timeout}=30
    Run keyword and ignore error  Log Out Of Dut
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  timeout=${gui_timeout}  cli_timeout=${cli_timeout}
    Commit Changes

*** Test Cases ***
Tvh1341290c
    [Documentation]  Tvh1341290c-SEC-WEB-STATE: Communicate Session State
        ...  FLOW DETAILS
        ...  Login to SMA and set pre-condition
        ...  Navigate to system administration >> Network access to change the default time out- 5 minutes
        ...  Clear all logs
        ...  Verify SMA has authentication logs which shows who has logged into the appliances and what role they have.
        ...  Verify in /data/pub/authetication->authentication logs

    [Tags]  gui  cli  Tvh1341290c
    [Setup]  Run Keywords  Clear and Roll over logs  ${authentication_log_name}
    ...  AND  Set inactivity timeout  gui_timeout=${inactivity_timeout}  cli_timeout=${inactivity_timeout}
    [Teardown]  Run keywords  Set inactivity timeout  gui_timeout=${default_inactivity_timeout}  cli_timeout=${default_inactivity_timeout}
    ...  AND  Unset SMA prompt

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Log Out Of Dut
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log_name}  User ${DUT_ADMIN} logged out of GUI session
    Connect to SMA  ${RTESTUSER}  ${RTESTUSER_PASSWORD}
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log_name}   User ${RTESTUSER} from ${CLIENT_IP} was authenticated successfully by password based authentication using an SSH connection.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Start CLI Session
    Sleep  300
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log_name}  User ${DUT_ADMIN} from ${CLIENT_IP} was authenticated successfully by CLI based authentication using an SSH connection.
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log_name}  User ${DUT_ADMIN} from ${CLIENT_IP} was authenticated successfully using an HTTPS connection
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log_name}  GUI: User ${DUT_ADMIN} logged out from session .* because of inactivity timeout
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log_name}  CLI: User ${DUT_ADMIN} logged out from ${CLIENT_IP} because of inactivity timeout

