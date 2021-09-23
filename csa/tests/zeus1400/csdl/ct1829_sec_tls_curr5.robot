*** Settings ***
Resource           sma/csdlresource.txt

Force Tags         csdl
Suite Setup        Initialize Suite
Suite Teardown     CSDL Suite Teardown


*** Variables ***
${NGUI_HTTPS_PORT}=             4431


*** Keywords ***
Initialize Suite
    CSDL Suite Setup
    # In CSDL Suite Setup, TLSv1.0 is enabling. To get back default SSL configurations, doing reset configuration.
    Suspend
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Log Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

Verify TLS version in Open SSL Certificate
    [Arguments]  ${tls_version}  ${tls_version_text}  ${port_number}
    ${rc}  ${cmd_out}=  Run And Return Rc And Output
    ...  echo "Q" | openssl s_client -connect ${SMA_IP}:${port_number} -showcerts ${tls_version}
    Should Be Equal As Integers  ${rc}  0
    Log  ${cmd_out}
    Should Contain  ${cmd_out}    BEGIN CERTIFICATE
    Should Contain  ${cmd_out}    : ${tls_version_text}

Do Common Setup
    DefaultTestCaseSetup
    FOR  ${service}  IN   Appliance Management Web User Interface
    ...  Secure LDAP Services  Updater Service
        Edit SSL Configuration Settings
        ...  ${service}
        ...  TLS v1.0
        ...  enable
    END
    # The changes in the settings of SSL configuration causing all related services to restart.
    # In Automation, it is throwing reboot error while committing changes.
    Run Keyword And Expect Error  RebootError: wait_until_not_reachable: *  Commit Changes
    Close All Browsers
    Launch Dut Browser
    Log Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

Do Common Teardown
    FOR  ${service}  IN   Appliance Management Web User Interface
    ...  Secure LDAP Services  Updater Service
        Edit SSL Configuration Settings
        ...  ${service}
        ...  TLS v1.0
    END
    Run Keyword And Expect Error  RebootError: wait_until_not_reachable: *  Commit Changes
    Close All Browsers
    Launch Dut Browser
    Log Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    DefaultTestCaseTeardown


*** Test Cases ***
Tvh1498097c
    [Documentation]  Verify whether SMA supports TLS version 1.2 at CLI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1498097c
    [Tags]      Tvh1498097c  SEC-TLS-CURR-5
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    ${dict}=  SSL Config Get Settings  as_dictionary=YES

    Log Dictionary  ${dict}
    FOR  ${key}  In  LDAPS  Updater  WebUI
        ${value}=    Get From Dictionary   ${dict}  ${key}
        Should Contain  ${value}  TLSv1.2
    END

Tvh1498098c
    [Documentation]  Verify if TLS 1.0 is not enabled by default at CLI \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1498098c
    [Tags]      Tvh1498098c  SEC-TLS-CURR-5
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    ${dict}=  SSL Config Get Settings  as_dictionary=YES

    Log Dictionary  ${dict}
    FOR  ${key}  In  LDAPS  Updater  WebUI
        ${value}=    Get From Dictionary   ${dict}  ${key}
        Should Not Contain  ${value}  TLSv1.0
    END

Tvh1518496c
    [Documentation]  Verify whether SMA - NGUI is working fine with default TLS version 1.2  \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1518496c
    [Tags]      Tvh1518496c  SEC-TLS-CURR-5
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    ${dict}=  SSL Config Get Settings  as_dictionary=YES

    Log Dictionary  ${dict}
    FOR  ${key}  In  LDAPS  Updater  WebUI
        ${value}=    Get From Dictionary   ${dict}  ${key}
        Should Contain  ${value}  TLSv1.2
    END

    Verify TLS version in Open SSL Certificate  -tls1_2  TLSv1.2  ${NGUI_HTTPS_PORT}

Tvh1518497c
    [Documentation]  Verify whether SMA - NGUI is working fine with configured TLS version 1.1 \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1518497c
    [Tags]      Tvh1518497c  SEC-TLS-CURR-5
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Verify TLS version in Open SSL Certificate  -tls1_1  TLSv1.1  ${NGUI_HTTPS_PORT}

Tvh1518498c
    [Documentation]  Verify whether SMA - NGUI is working fine with configured TLS version 1.0 \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1518498c
    [Tags]      Tvh1518498c  SEC-TLS-CURR-5
    [Setup]     Do Common Setup
    [Teardown]  Do Common Teardown

    Verify TLS version in Open SSL Certificate  -tls1  TLSv1  ${NGUI_HTTPS_PORT}

Tvh1498101c
    [Documentation]  Verify if SMA does not support SSL 2.0 at CLI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1498101c
    [Tags]      Tvh1498097c  csdl  SEC-TLS-CURR-5
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    ${dict}=  SSL Config Get Settings  as_dictionary=YES

    Log Dictionary  ${dict}
    FOR  ${key}  IN  LDAPS  Updater  WebUI
        ${value}=    Get From Dictionary   ${dict}  ${key}
        Should Not Contain  ${value}  SSLv2
    END

Tvh1543196c
    [Documentation]  Verify whether SMA - GUI is working fine with default TLS version 1.2  \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1543196c
    [Tags]      Tvh1518499c  csdl  SEC-TLS-CURR-5
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown
    ${dict}=  SSL Config Get Settings  as_dictionary=YES

    Log Dictionary  ${dict}
    FOR  ${key}  IN  LDAPS  Updater  WebUI
        ${value}=    Get From Dictionary   ${dict}  ${key}
        Should Contain  ${value}  TLSv1.2
    END

    Verify TLS version in Open SSL Certificate  -tls1_2  TLSv1.2  ${DUT_PORT}

Tvh1543197c
    [Documentation]  Verify whether SMA - GUI is working fine with configured TLS version 1.1 \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1543197c
    [Tags]      Tvh1543197c  csdl  SEC-TLS-CURR-5
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Verify TLS version in Open SSL Certificate  -tls1_1  TLSv1.1  ${DUT_PORT}

Tvh1543198c
    [Documentation]  Verify whether SMA - GUI is working fine with configured TLS version 1.0 \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1543198ci
    [Tags]      Tvh1543198c  csdl  SEC-TLS-CURR-5
    [Setup]     Do Common Setup
    [Teardown]  Do Common Teardown

    Verify TLS version in Open SSL Certificate  -tls1  TLSv1  ${DUT_PORT}

