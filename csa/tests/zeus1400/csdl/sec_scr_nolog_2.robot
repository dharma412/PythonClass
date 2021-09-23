# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/sec_scr_nolog_2.robot $
# $Date: 2020/10/12 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${log_name}                   aggregatord_logs
${ftp_server_directory}       /home/user
${cli_log_path}               /data/pub/cli_logs/cli.current
${gui_log_path}               /data/pub/gui_logs/gui.current

*** Test Cases ***
Tvh1506349c
    [Documentation]  Edit Log Subscription for any of the logs through CLI to configure FTP push, provide
    ...              remote servers credentials under config command.
    ...  Verify the credentials are not logged and details relevant to event/action alone logged in cli_logs
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506349
    
    [Setup]  Roll Over Now
    [Teardown]  Run keywords  Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  AND  Log subscriptions set retrieval method to manually download   ${log_name}
    ...  AND  Commit Changes
    [Tags]  cli  Tvh1506349c

    # Step 1. Login to CLI with admin credentials.
    Start CLI session

    # Step 2. Edit Log Subscription for any of the logs through CLI - logconfig > edit > <select log>
    # Step 3. Enable FTP log push and configure remote server's details including username and password.
    Log Config Edit  ${log_name}
    ...  retrieval=FTP Push  hostname=${FTP_SERVER}  username=${FTPUSER}
    ...  password=${FTPUSER_PASSWORD}  directory=${ftp_server_directory}  filename=agg_files
    Commit

    # Step 4. Verify the Password configured for FTP server is not captured anywhere in cli_logs
    ${cli_log_password_status}=  Run keyword and return status   Verify logs  ${cli_log_path}  ${FTPUSER_PASSWORD}
    Should not be true  ${cli_log_password_status}

Tvh1506350c
    [Documentation]  Edit Log Subscription for any of the logs through GUI to configure FTP push, provide
    ...              remote servers credentials under config command.
    ...  Verify the credentials are not logged and details relevant to event/action alone logged in gui_logs
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506350
    
    [Setup]  Roll Over Now
    [Teardown]  Run keywords  Log subscriptions set retrieval method to manually download   ${log_name}
    ...  AND  Commit Changes
    [Tags]  gui  Tvh1506350c

    # Step 1. Login to UI with admin credentials.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    #.Step 2. Edit Log Subscription for any of the logs through GUI - System Administration > Log Subscriptions > <Log name> >
    # Step 3. Enable FTP log push and configure remote server's details including username and password.
    Log subscriptions set retrieval method to ftp push  ${log_name}  ${FTP_SERVER}  ${ftp_server_directory}  ${FTPUSER}  ${FTPUSER_PASSWORD}
    Commit Changes

    # Step 4. Verify the Password configured for FTP server is not captured anywhere in cli_logs
    ${gui_log_password_status}=  Run keyword and return status   Verify logs  ${gui_log_path}  ${FTPUSER_PASSWORD}
    Should not be true  ${gui_log_password_status}
