# $Id: //prod/main/sarf_centos/tests/zeus138/csdl/sec_off_proc.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${nmap_command_host_timeout}        1200s
${nmap_protocols_command}           nmap sR -n -vvv -p 1-65535
${nmap_active_connections_command}  netstat -p | grep tcp
${tcp_open_port_22}                 .*22/tcp.*open.*ssh.*
${tcp_open_port_8123}               .*8123/tcp.*open.*polipo.*
@{nmap_tcp_open_port_lists}         80/tcp.*open.*http
    ...  443/tcp.*open.*https
    ...  4431/tcp.*open.*unknown
    ...  6080/tcp.*open.*unknown
    ...  6443/tcp.*open.*unknown
    ...  82/tcp.*open.*xfer
    ...  83/tcp.*open.*mit-ml-dev

*** Keywords ***
Run nmap command and verify ports and protocols running for services
    [Arguments]  ${mode}
    ${nmap_command_output}=  Run On Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}   ${nmap_protocols_command} ${SMA_IP} --host-timeout ${nmap_command_host_timeout}
    Should match regexp  ${nmap_command_output}  ${tcp_open_port_22}
    Should match regexp  ${nmap_command_output}  ${tcp_open_port_8123}
    FOR  ${expected_port}  IN  @{nmap_tcp_open_port_lists}
      ${nmap_scan_for_sma_text}=  Set Variable  (?s)Nmap scan report for ${SMA_IP}(.*?)${expected_port}
      Run keyword if  '${mode}'=='enabled'   Should match regexp  ${nmap_command_output}  ${nmap_scan_for_sma_text}
      ...  ELSE IF  '${mode}'=='disabled'  Should not match regexp  ${nmap_command_output}  ${nmap_scan_for_sma_text}
      ...  ELSE  Run keywords  Should be equal as strings  ${mode}  enabled  AND  Should be equal as strings  ${mode}  disabled
    END

Check active internet connections
    [Arguments]  ${connection_detail}
    ${nmap_active_output}=  Run On Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}   ${nmap_active_connections_command}
    Should match regexp  ${nmap_active_output}  ${connection_detail}

*** Test Cases ***
Tvh1340825c
    [Documentation]  Tvh1340825c-SEC-OFF-PROC: Selectively enable TCP/IP SERVICEs/OPEN PORTS
    ...  Pre-Condition: Client configured with nmap

    [Tags]  cli  gui Tvh1340825c
    [Setup]  Verify and install nmap package
    [Teardown]  Run keywords  Start CLI Session
    ...  AND  Interface config edit  if_name=Management  http_enable=yes  https_enable=yes  spamhttp_enable=yes  spamhttps_enable=yes  asyncos_https=yes  asyncos_confirm=yes
    ...  AND  Commit

    # Step 1. Login to GUI.
    # Step 2. Click Network > IP Interfaces > Click on Management.
    # Step 3. Enable services->HTTP, HTTPS , AsyncOS API HTTP, AsyncOS API HTTPS, Spam Quarantine HTTP, Spam Quarantine HTTPS
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    IP Interfaces Edit  Management  http_service=${True}  https_service=${True}  isq_http_service=${True}  isq_https_service=${True}  api_http_service=${True}  api_https_service=${True}
    Enable Spam Quarantine On SMA

    # Step 4. Run the command nmap sR -n -vvv -p 1-65535 <SMA IP> and get ouput of command
    # Step 5. Verify ports and protocols running-
    #               22/tcp open ssh
    #               80/tcp open http
    #               82/tcp open xfer
    #               83/tcp open mit-ml-dev
    #               443/tcp open https
    #               4431/tcp open unknown >> This port is for NGUI
    #               6080/tcp open unknown
    #               8123/tcp open polipo
    Run nmap command and verify ports and protocols running for services  enabled

    # Step 6. Disable services->HTTP, HTTPS , AsyncOS API HTTP, AsyncOS API HTTPS, Spam Quarantine HTTP, Spam Quarantine HTTPS
    # Step 7. CLI - Run ->trailblazerconfig-> disable
    # Step 8. Run the command nmap sR -n -vvv -p 1-65535 <SMA IP> and get ouput of command
    # Step 9. Verify ports and protocols running-
            #   22/tcp open ssh
            #   8123/tcp open polipo
    IP Interfaces Edit  Management  http_service=${False}  https_service=${False}  isq_http_service=${False}  isq_https_service=${False}  api_http_service=${False}  api_https_service=${False}
    Run keyword and ignore error  Commit Changes
    Run keyword and ignore error  Start CLI Session
    Run keyword and ignore error  Trailblazer config disable
    Run nmap command and verify ports and protocols running for services  disabled

    # Step 10. Run 'netstat -p tcp'
    # Step 11. Verify active internet connections
    Wait until keyword succeeds  2min  2sec  Check active internet connections  .*tcp.*ESTABLISHED.*
    Wait until keyword succeeds  2min  2sec  Check active internet connections  .*tcp.*${SMA}:ssh.*ESTABLISHED.*