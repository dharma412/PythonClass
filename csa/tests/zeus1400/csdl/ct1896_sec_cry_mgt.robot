*** Settings ***
Resource           sma/csdlresource.txt

Force Tags         csdl
Suite Setup        CSDL Suite Setup
Suite Teardown     CSDL Suite Teardown
Test Setup         DefaultTestCaseSetup
Test Teardown      DefaultTestCaseTeardown


*** Variables ***
${MANAGEMENT}=         //table[@class='cols']//a[contains(text(),"Management")]
${HTTPS}=              //input[@id="httpsd"]
${NG_HOME_PAGE}=       //h1[contains(text(),'Security Management Appliance')]
${NGUI_PORT}=          4431
${EUQ_PORT}=           83
${EUQ_HTTPS}=          //input[@id="euq_httpsd"]


*** Keywords ***
Verify SMA connection through SSHV2
    FOR  ${user_name}  IN  ${RTESTUSER}  ${DUT_ADMIN}
    ${ssh_output}=  Run On Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}
    ...  ssh -v ${user_name}@${SMA_IP}  error=True
    Log  ${ssh_output}
    ${match}=  Should contain  ${ssh_output}  SSH2
    END

Verify SMA connection through SSHV1
    FOR  ${user_name}  IN  ${RTESTUSER}  ${DUT_ADMIN}
    ${ssh_output}=  Run On Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}
    ...  ssh -1 -v ${user_name}@${SMA_IP}  error=True
    Log  ${ssh_output}
    ${match}=  Should contain  ${ssh_output}  Protocol major versions differ: 1 vs. 2
    END

Verify Telnet Connection to SMA
    ${exit_code}  ${telnet_output}=  Run And Return Rc And Output
    ...  telnet ${SMA_IP}
    Log  ${telnet_output}
    Should Be Equal As Numbers  ${exit_code}  1
    Should contain  ${telnet_output}  connect to address ${SMA_IP}: Connection refused

Verify GUI service uses default protocol as HTTPS
    [Arguments]  ${url}
    Go To  ${url}
    Sleep  5s  msg=Wait for page load
    ${current_url}=  Get Location
    Log  ${current_url}
    Should Contain  ${current_url}  https

Verify TLS1.2 is used for communication
    [Arguments]  ${port}
    ${open_ssl_output}=  Run On Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}
    ...  openssl s_client -connect ${SMA_IP}:${port}
    Log  ${open_ssl_output}
    Should contain  ${open_ssl_output}  : TLSv1.2
    Should Not Contain  ${open_ssl_output}  : TLSv1.1


*** Test Cases ***
Tvh1530821c
    [Documentation]  Verify SMA uses SSHv2 for CLI access by default.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1530821c \n
    [Tags]   Tvh1530821c
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Verify SMA connection through SSHV2

Tvh1530822c
    [Documentation]  Verify SMA does not support CLI access using SSHv1 or Telnet by default.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1530822c \n
    [Tags]   Tvh1530822c
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Verify SMA connection through SSHV1
    Verify Telnet Connection to SMA

Tvh1530823c
    [Documentation]  Verify SMA uses HTTPS (TLSv1.2 should be used) for GUI service by default.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1530823c \n
    [Tags]   Tvh1530823c
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Verify GUI service uses default protocol as HTTPS  http://${DUT}
    Verify TLS1.2 is used for communication  ${DUT_PORT}
    Navigate To  Network  IP Interfaces
    Click Element  ${MANAGEMENT}
    ${https_service_status}=  Get Element Attribute  ${HTTPS}  checked
    Log  ${https_service_status}
    Should Be Equal  ${https_service_status}  true

Tvh1530824c
    [Documentation]  Verify SMA uses HTTPS (TLSv1.2 should be used)  for Spam Quarantine \n
    ...  UI service by default \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1530824c \n
    [Tags]   Tvh1530824c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Spam Quarantine Enable
    IP Interfaces Edit  Management  redirect_isq_http=${True}
    Commit changes
    Verify GUI service uses default protocol as HTTPS  http://${DUT}:82
    ${current_url}=  Get Location
    Should Contain  ${current_url}  https://${DUT}:${EUQ_PORT}
    Verify TLS1.2 is used for communication  ${EUQ_PORT}
    Navigate To  Network  IP Interfaces
    Click Element  ${MANAGEMENT}
    ${https_service_status}=  Get Element Attribute  ${EUQ_HTTPS}  checked
    Log  ${https_service_status}
    Should Be Equal  ${https_service_status}  true

Tvh1530825c
    [Documentation]  Verify SMA uses HTTPS (TLSv1.2 should be used) for NGUI service by default.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1530825c \n
    [Tags]   Tvh1530825c
    [Teardown]  Run Keywords  DefaultTestCaseTeardown
    ...  AND  Go To  http://${DUT}
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Verify TLS1.2 is used for communication  ${NGUI_PORT}
    Navigate To  Network  IP Interfaces
    Click Element  ${MANAGEMENT}
    ${https_service_status}=  Get Element Attribute  ${HTTPS}  checked
    Log  ${https_service_status}
    Should Be Equal  ${https_service_status}  true
    Go To  http://${DUT}:${NGUI_PORT}/ng-login
    Sleep  5s  msg=Wait for page load
    Page Should Not Contain  ${NG_HOME_PAGE}

Tvh1530828c
    [Documentation]  Verify SMA uses SSHv2 for CLI access and HTTPS for GUI, Spam Quarantine \n
    ...  UI and NGUI by default after Save, Reset, load configuration. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1530828c \n
    [Tags]   Tvh1530828c
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${SMA_ORIG_CONFIG}=  Save Config
    Set Test Variable  ${SMA_ORIG_CONFIG}
    Suspend  0
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Configure SSL For GUI
    Restart CLI Session
    Load Config From File  ${SMA_ORIG_CONFIG}
    Commit
    Close Browser
    Selenium Login
    Verify SMA connection through SSHV1
    Verify SMA connection through SSHV2
    Verify GUI service uses default protocol as HTTPS  http://${DUT}
    Verify GUI service uses default protocol as HTTPS  http://${DUT}:82

    Go To  http://${DUT}:${NGUI_PORT}/ng-login
    Sleep  5s  msg=Wait for page load
    Page Should Not Contain  ${NG_HOME_PAGE}
    Go To  http://${DUT}

    FOR  ${port}  IN  ${NGUI_PORT}  ${DUT_PORT}  ${EUQ_PORT}
       Verify TLS1.2 is used for communication  ${port}
    END
    Verify Telnet Connection to SMA
