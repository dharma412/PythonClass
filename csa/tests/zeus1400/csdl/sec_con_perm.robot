# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_con_perm.txt#2 $
# $Date: 2020/06/21 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${gui_access_denied_message}            .*Access to this interface is restricted. Please contact your system administrator.*
${gui_access_denied_message_element}    //td[@id='action-results-message']
${slice_server_prompt}                   $

*** Keywords ***
Setup Tvh1340562c
    ${slice_server_ip}=  global_sma.Get Host IP By Name   ${SLICE_SERVER}
    Set test variable  ${slice_server_ip}

Verify access denied message in SMA GUI due to IP restriction
    ${access_denied_message_text} =  Get Text  ${gui_access_denied_message_element}
    Should match regexp   ${access_denied_message_text}  ${gui_access_denied_message}  .

Enter options and read
    [Arguments]  @{options}

    FOR  ${option}  IN  @{options}
        Write  ${option}
        Sleep  1
    END
    ${out}=  Read
    [Return]  ${out}

*** Test Cases ***
Tvh1340562c
    [Documentation]  Tvh1340562c-Verify only users from IPs configured to access SMA are only able to connect to SMA using CLI/Legacy UI/ NGUI/
        ...  FLOW DETAILS
        ...  Login to SMA CLI
        ...  adminaccessconfig -> ipaccess -> new -> <slice_server IP> -> Enter -> y -> Enter -> Enter -> Commit
        ...  Try to SSH from Client- Check error message
        ...  Try to access legacy UI from Client- Check error message
        ...  Revert from slice server: adminaccessconfig -> ipaccess -> All -> Commit
        ...  SSH to SMA  from Client- Check success

    [Tags]  cli  gui Tvh1340562c
    [Setup]  Setup Tvh1340562c
    [Teardown]  Run Keywords  Admin access config ipaccess allow all
    ...  AND  Commit
    ...  AND  Set SSHLib Prompt  ${empty}

    # Step 1 .Login to SMA CLI
    # Step 2 .adminaccessconfig -> ipaccess -> new -> <slice_server IP> -> Enter -> y -> Enter -> Enter -> Commit
    Admin Access Config Ipaccess New  mode=Restrict  ip=${slice_server_ip}
    Run keyword and ignore error  Commit

    # Step 3. Try to SSH from Client- Check error message
    ${ssh_connection_status}=  Run keyword and return status  Connect to SMA  ${RTESTUSER}  ${RTESTUSER_PASSWORD}
    Should not be true  ${ssh_connection_status}

    # Step 4. Try to access legacy UI from Client- Check error message
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Verify access denied message in SMA GUI due to IP restriction

    # Step 5. Verify successful SSH access from authorised IP
    Establish SSH Connection To  ${SLICE_SERVER}  ${TESTUSER}  ${TESTUSER_PASSWORD}  ${slice_server_prompt}
    ${ssh_connection_to_sma_text}=  Enter options and read  ssh ${RTESTUSER}@${SMA}  yes  ${DUT_ADMIN_PASSWORD}
    Should match regexp  ${ssh_connection_to_sma_text}  .*Welcome to.*Content Security Virtual Management Appliance.*

    # Step 6. # Step 2 .adminaccessconfig -> ipaccess restricted. Please contact your system administrator.*s -> new -> <client_IP> -> Enter -> y -> Enter -> Enter -> Commit
    Admin Access Config Ipaccess New  mode=Restrict  ip=${CLIENT_IP}
    Commit

    # Step 7. Verify successful log in to SMA GUI from  from authorised IP
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ${gui_access_denied_status}=  Run keyword and return status  Verify access denied message in SMA GUI due to IP restriction
    Should not be true  ${gui_access_denied_status}