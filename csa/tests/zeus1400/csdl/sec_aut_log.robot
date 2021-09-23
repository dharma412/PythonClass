# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_aut_log.txt#2 $
# $Date: 2020/05/04 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/global_sma.txt
Resource     csdlresource.txt

Force Tags   csdl
Suite Setup   CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown
Test Setup  Clear and Roll over logs  ${authentication_log}  ${authentication_log_name}

*** Variables ***
${authentication_log_name}   authentication
${authentication_log}  /data/pub/${authentication_log_name}/${authentication_log_name}.current
${inactivity_timeout}  5
${default_inactivity_timeout}  30

*** Keywords ***
Set inactivity timeout
    [Arguments]  ${gui_timeout}=30  ${cli_timeout}=30
    Run keyword and ignore error  Log Out Of Dut
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  timeout=${gui_timeout}  cli_timeout=${cli_timeout}
    Commit Changes

Teardown Tvh1217397c
    Go To  https://${DUT}
    Run keyword and ignore error  Log Out Of Dut
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  ${default_inactivity_timeout}
    Commit Changes

*** Test Cases ***
Tvh1217390c
    [Documentation]  Tvh1217390c-Verify authentication logs  for WEBUI login
        ...  Tvh1217399c-Verify authentication logs by manually logout from GUI
        ...  Tvh1341290c-Communicate Session State
        ...  FLOW DETAILS
        ...  Pre-Condition- Clear authentication logs
        ...  Login to WebUI
        ...  Verify Authentication log for ""authentication successful"" message
        ...  Logout of WebUI
        ...  Verify Authentication log for "logged out successfully" message

    [Tags]  gui  Tvh1217390c  Tvh1217399c  Tvh1341290c

    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log}  User ${DUT_ADMIN} from ${CLIENT_IP} was authenticated successfully with privilege admin using an HTTPS connection
    Sleep  1
    Log Out Of Dut
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log}  User ${DUT_ADMIN} logged out of GUI session

Tvh1217393c
     [Documentation]  Tvh1217393c-Verify authentication logs for CLI login.
        ...  Tvh1341290c-Communicate Session State
        ...  FLOW DETAILS
        ...  Pre-Condition- Clear authentication logs
        ...  Login to SMA CLI.
        ...  Verify Authentication log for ""authentication successful"" message

    [Tags]  cli  Tvh1217393c  Tvh1341290c

    Start CLI Session
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${authentication_log}  User ${DUT_ADMIN} from ${CLIENT_IP} was authenticated successfully with privilege admin by CLI based authentication using an SSH connection.

Tvh1217402c
    [Documentation]  Tvh1217402c-Verify Authentication logs by login in command prompt with rlogins like rtestuser and then login to cli.
        ...  Tvh1341290c-Communicate Session State
        ...  FLOW DETAILS
        ...  Login to SMA as rtestuser
        ...  Enter CLI mode
        ...  Verify Authentication log for "authentication successful" message

    [Tags]  cli  Tvh1217402c  Tvh1341290c
    [Teardown]  Set SSHLib Prompt  ${empty}

    Connect to SMA  ${RTESTUSER}  ${RTESTUSER_PASSWORD}
    Enter option cli and read
    Wait until keyword succeeds  5 min  2 sec  Verify logs  ${authentication_log}   User ${RTESTUSER} from ${CLIENT_IP} was authenticated successfully with privilege .* by password based authentication using an SSH connection.

Tvh1217391c
    [Documentation]  Tvh1217391c-Verify WEBUI Inactivity timeout authentication logs.
        ...  Tvh1217394c-Verify CLI inactivity timeout authentication logs.
        ...  Tvh1341290c-Communicate Session State
        ...  FLOW DETAILS
        ...  Pre-Condition- Clear authentication logsde
        ...  Pre-Condition- WebUI and navigate to Sytem administration-> Network access and set the WebUI inactivity timeout.
        ...  Login to SMA and keep it idle for the time that is set.
        ...  Login to CLI with user admin and keep it idle for the CLI inactivity timeout.
        ...  Verify Authentication log for "logged out from session because of inactivity timeout"" message for both CLI and GUI
        ...  Post Condition - Update Web UI inactivity timeout to default value of 30 minutes

    [Tags]  gui  Tvh1217391c  Tvh1217394c  Tvh1341290c
    [Setup]  Run keywords  Clear and Roll over logs  ${authentication_log}  ${authentication_log_name}
    ...  AND  Set inactivity timeout  gui_timeout=${inactivity_timeout}  cli_timeout=${inactivity_timeout}
    [Teardown]  Set inactivity timeout  gui_timeout=${default_inactivity_timeout}  cli_timeout=${default_inactivity_timeout}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Start CLI Session
    Sleep  300
    Wait until keyword succeeds  5 min  2 sec  Verify logs  ${authentication_log}  GUI: User ${DUT_ADMIN} logged out from session .* because of inactivity timeout
    Wait until keyword succeeds  5 min  2 sec  Verify logs  ${authentication_log}  CLI: User ${DUT_ADMIN} logged out from ${CLIENT_IP} because of inactivity timeout


Tvh1217400c

    [Documentation]  Tvh1217400c-Verify Authentication logs by manually logout from CLI
        ...  Tvh1341290c-Communicate Session State
        ...  FLOW DETAILS
        ...  Pre-Condition- Clear authentication logs
        ...  Login to SMA CLI with user admin.
        ...  Logout from CLI manually by giving exit
        ...  Verify log for 'logged out successfully' in authetication logs

    [Tags]  cli  Tvh1217400c  Tvh1341290c

    Start CLI Session
    Write to CLI  exit
    Wait until keyword succeeds  5 min  1 sec  Verify logs  ${authentication_log}  User ${DUT_ADMIN} logged out of SSH session ${CLIENT_IP}

Tvh1217397c

     [Documentation]  Tvh1217397c-Verify End User Spam Quarantine UI inactivity authentication logs.
        ...  Tvh1217395c-Verify authentication logs for End User Spam Quarantine UI Login.
        ...  Tvh1341290c-Communicate Session State
        ...  FLOW DETAILS
        ...  Pre-Condition- Clear authentication logs
        ...  Pre-Condition- WebUI and navigate to Sytem administration-> Network access and set the WebUI inactivity timeout.
        ...  Pre-Condition- Enable Spam Quarantine
        ...  Login to EUQ UI and keep it idle for the time that is set.
        ...  Verify Authentication log for ""authentication successful"" message
        ...  Verify Authentication log for "logged out from session because of inactivity timeout"" message
        ...  Post Condition - Update Web UI inactivity timeout to default value of 30 minutes

    [Tags]  gui  Tvh1217397c  Tvh1217395c  Tvh1341290c
    [Setup]  Run keywords  Clear and Roll over logs  ${authentication_log}  ${authentication_log_name}
    ...  AND  Set inactivity timeout  gui_timeout=${inactivity_timeout}
    ...  AND  Enable Spam Quarantine On SMA
    ...  AND  Close All Browsers
    [Teardown]  Teardown Tvh1217397c

    Launch SPAM Quarantine portal  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Verify logs  ${authentication_log}  Authentication OK, user ${DUT_ADMIN} with privilege admin logged in to Spam Quarantine
    Verify logs  ${authentication_log}  User - logged out from Spam Quarantine
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Sleep  300
    Wait until keyword succeeds  5 min  1 sec  Verify logs  ${authentication_log}  User ${DUT_ADMIN} logged out from session .* because of inactivity timeout