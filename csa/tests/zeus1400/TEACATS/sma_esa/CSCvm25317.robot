# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/TEACATS/sma_esa/CSCvm25317.txt#4 $ $DateTime: 2020/06/08 21:33:15 $ $Author: sumitada $

*** Settings ***
Library           SmaGuiLibrary
Library           Collections
Resource          sma/global_sma.txt
Resource          regression.txt

Suite Setup   Do Suite Setup
Suite Teardown   global_sma.DefaultTestSuiteTeardown

*** Variables ***

*** Keywords ***

Do Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup
    SSL Config Gui  versions=All Services  ssl_method=TLSv1.0  confirm=Enable for all services
    Commit

SSLConfig TLS
    [Arguments]  ${tls}
    SSL Config Gui  versions=WebUI  ssl_method=${tls}  confirm=Yes
    Commit

Update TLS Version
    [Arguments]  ${out}  ${tls}
    ${tls_status} =  Evaluate
    ...  re.search('${tls}\\s+\\w+\\s+\\w+\\s+(\\w+)\\s+\\w+', '''${out}''').group(1)
    ...  re
    Log  ${tls_status}
    Run Keyword If  '${tls_status}'=='N'
    ...  SSLConfig TLS  ${tls}

Close SSH connection
   Set SSHLib Prompt  ${Empty}
   SSHLibrary.Close Connection

*** Test Cases ***

Tvh1231018c
    [Documentation]  sslconfig does not enable TLSv1.0 when configured to do so
    ...  1. Enable TLS for TLS 1.0,1.1 and 1.2
    ...  2. Run openssl command to verify all TLS started
    ...  http://tims/view-entity.cmd?ent=1231018
    [Tags]  srts  teacat  CSCvm25317  Tvh1231018c  CSCvr36463

    Set Test Variable  ${TEST_ID}  Tvh1231018c
    ${address} =  Get Host IP By Name  ${DUT}
    SSHLibrary.Open Connection  ${address}
    Set SSHLib Prompt  >
    SSHLibrary.Login    ${DUT_ADMIN}    ${DUT_ADMIN_SSW_PASSWORD}
    Write  sslconfig
    Read Until Prompt
    Write  VERSIONS
    ${out}  Read Until Prompt
    Log  ${out}
    Set SSHLib Prompt  ${EMPTY}
    SSHLibrary.Close Connection
    Update TLS Version  ${out}  TLSv1.0
    Update TLS Version  ${out}  TLSv1.1
    Update TLS Version  ${out}  TLSv1.2
    ${out}=  Run  openssl s_client -connect ${SMA} -tls1
    Should Not Contain  ${out}  wrong version number
    ${out}=  Run  openssl s_client -connect ${SMA} -tls1_1
    Should Not Contain  ${out}  wrong version number
    ${out}=  Run  openssl s_client -connect ${SMA} -tls1_2
    Should Not Contain  ${out}  wrong version number
    SSHLibrary.Open Connection  ${address}
    Set SSHLib Prompt  ]
    SSHLibrary.Login    ${RTESTUSER}    ${RTESTUSER_PASSWORD}
    Write  openssl version
    ${out}  Read Until Prompt
    Log  ${out}
    Should Match Regexp  ${out}  CiscoSSL 1.0.2\.*fips
    SSHLibrary.Close Connection
