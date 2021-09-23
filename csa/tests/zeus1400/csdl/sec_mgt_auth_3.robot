# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_mgt_auth_3.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/csdlresource.txt

Force Tags   csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${redirection_check_url}        https://${SMA}/network/ip_interfaces
${sma_login_page_title}         .*Cisco Email and Web Virtual Gateway.*Welcome.*

*** Keywords ***
Verify page redirection to login page
    ${login_page_title}=  Get Title
    Should match regexp   ${login_page_title}  ${sma_login_page_title}

Verify SSH command without providing password and check password prompt
   Establish SSH Connection To  ${CLIENT_HOSTNAME}  ${TESTUSER}  ${TESTUSER_PASSWORD}  $
   ${ssh_password_prompt}=  Enter option ssh ${RTESTUSER}@${SMA} -p 22 ls and read
   Should contain  ${ssh_password_prompt}  Password:
   ${ssh_password_no_prompt}=  Enter option ${RTESTUSER_PASSWORD} and read
   Should not contain  ${ssh_password_no_prompt}  Password:

*** Test Cases ***
Tvh1340818c
    [Documentation]  Tvh1340818c-SEC-MGT-AUTH-3: Require configuring administration authentication
        ...  FLOW DETAILS
        ...  Pre-Condition: Client configured with nmap
        ...  Enter nmap <SMA IP>
        ...  Verify 22/tcp open ssh and 443/tcp open https
        ...  Verify without doing user authentication, user is not able to perform any actions

    [Tags]  cli  gui Tvh1340818c
    [Setup]  Verify and install nmap package
    [Teardown]  Set SSHLib Prompt  ${empty}

   ${nmap_output}=  Run On Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}  nmap ${SMA_IP}
   Should match regexp  ${nmap_output}  .*22/tcp.*open.*ssh.*
   Should match regexp  ${nmap_output}  .*443/tcp.*open.*https.*
   Verify SSH command without providing password and check password prompt
   Connect to SMA  ${RTESTUSER}  ${RTESTUSER_PASSWORD}
   Go To  ${redirection_check_url}
   Verify page redirection to login page
   Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}