# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/CT1738_SEC-AUT-AUTH-4_2.txt#4 $
# $Date: 2020/11/05 $
# $Author: mrmohank $


*** Settings ***
Resource     sma/csdlresource.txt
Variables    sma/saml_constants.py

Suite Setup  Initialize Suite
Suite Teardown  DefaultTestSuiteTeardown

*** Variables ***
${ca_cert_path}               %{SARF_HOME}/tests/testdata/ca.crt
${ca_key_path}                %{SARF_HOME}/tests/testdata/ca.key
${cli_log_path}               /data/pub/cli_logs/cli.current
${gui_log_path}               /data/pub/gui_logs/gui.current
${ldap_server_profile}        myldap

*** Keywords ***
Initialize Suite
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup
    ${SMA_BADE_BUILD}=  Get Current Dut Version
    Set Suite Variable  ${SMA_BADE_BUILD}
    Initialize Users
    Add Users
    ${SMA_ORIG_CONF}=  Configuration File Save Config
    Set Suite Variable  ${SMA_ORIG_CONF}

Get Current Dut Version
    Start Cli Session If Not Open
    ${out}=  Version
    ${CURRENT_DUT_VERSION}=  Evaluate
    ...  re.search(r'Version: (\\d+\.\\d+\.\\d+-\\d+)', '''${out}''').groups()[0]  re
    Log  ${CURRENT_DUT_VERSION}
    [Return]  ${CURRENT_DUT_VERSION}

Save Config File And Load Config File
    ${config_file}=  Configuration File Save Config
    Configuration File Load Config  ${config_file}
    Commit Changes

Add Users
    User Config New  ${TEST_USER8}   ${TEST_USER8}   ${TEST_USER_PSW}  ${sma_user_roles.ADMIN}
    User Config New  ${TEST_USER10}  ${TEST_USER10}  ${TEST_USER_PSW}  ${sma_user_roles.OPERATOR}
    User Config New  ${TEST_USER11}  ${TEST_USER11}  ${TEST_USER_PSW}  ${sma_user_roles.TECHNICIAN}
    User Config New  ${TEST_USER12}  ${TEST_USER12}  ${TEST_USER_PSW}  ${sma_user_roles.GUEST}
    User Config New  ${TEST_USER13}  ${TEST_USER13}  ${TEST_USER_PSW}  ${sma_user_roles.RO_OPERATOR}
    User Config New  ${TEST_USER14}  ${TEST_USER14}  ${TEST_USER_PSW}  ${sma_user_roles.HELP_DESK}
    Commit

Centralized Email And Web Feature Accessibility Test
    Centralized Email Reporting Enable
    Centralized Email Reporting Disable
    Centralized Email Reporting Enable
    Centralized Email Reporting Disable
    Centralized Email Message Tracking Enable
    Centralized Email Message Tracking Disable

    Centralized Web Reporting Enable
    Centralized Web Reporting Disable
    Centralized Web Configuration Manager Enable
    Centralized Web Configuration Manager Disable
    Centralized Upgrade Manager Enable
    Centralized Upgrade Manager Disable

Users Add Edit Delete From CLI
    [Arguments]  ${admin_psw}=${None}
    Set Test Variable  ${test_user_update}  Ironport941$
    User Config New  ${TEST_USER7}  ${TEST_USER7}  ${TEST_USER_PSW}
    ...  ${sma_user_roles.OPERATOR}
    ...  admin_passphrase=${admin_psw}
    Commit
    User Config Edit  ${TEST_USER7}  full_name=${TEST_USER7}_new  password=${test_user_update}
    ...  admin_passphrase=${admin_psw}
    Commit
    User Config Delete  ${TEST_USER7}  admin_passphrase=${admin_psw}
    Commit

Configure LDAP SAML RADIUS Test
    [Arguments]  ${user}=${DUT_ADMIN}  ${password}=${DUT_ADMIN_SSW_PASSWORD}
    Add Customer SAML Config Azure
    Commit Changes
    Enable Externalauth SAML
    User Config External Setup Disable
    Commit
    Add Cisco Ad As LDAP
    Edit External Authentication LDAP User Role  ${CISCO_AD}  ${TEST_USER_GROUP_MAPPING}  ${sma_user_roles.ADMIN}
    User Config External Setup Disable
    Commit
    Check User Login  ${user}  ${password}
    Edit External Authentication Radius User Role  ${sma_user_roles.ADMIN}
    Check User Login  ${user}  ${password}
    User Config External Setup Disable
    Commit

Common Admin Test Teardown
    Restart CLI Session
    ${cli_result}=  Load Config From File   ${SMA_ORIG_CONF}
    Log  ${cli_result}
    Commit
    Log Out Of Dut
    Log Into Dut
    DefaultTestCaseTeardown

Verify CLI and GUI logs for critical sensitive or personal information

    ${ca_certificate_file}=    OperatingSystem.Get File    ${ca_cert_path}
    Set Suite Variable  ${ca_certificate_file}
    ${ca_certificate_key}=    OperatingSystem.Get File    ${ca_key_path}
    Set Suite Variable  ${ca_certificate_key}
    Start CLI Session
    Roll Over Now

    # Browser close has been pt to make sure any open browsers are closed after upgrade
    Run keyword and ignore error  Selenium Close
    Selenium Login

    LDAP Add Server Profile  ${ldap_server_profile}  ${LDAP_AUTH_SERVER}
    ...  server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit External Authentication Queries  ${ldap_server_profile}
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Run keyword and ignore error  SAML DELETE SP IDP  sp_name=${TEST_SP_PROFILE}  idp_name=${TEST_IDP_PROFILE}  user_role=${USER_ROLE}
    Add Customer SAML Config Azure
    Commit Changes
    FOR  ${passwords}  IN   ${ca_certificate_key}  ${FTPUSER_PASSWORD}   ${DUT_ADMIN_SSW_PASSWORD}
      ${gui_log_password_status}=  Run keyword and return status   Verify logs  ${gui_log_path}  ${passwords}
      Should not be true  ${gui_log_password_status}
    END

    User Config New  ${RADIUS_USER}  ${RADIUS_USER}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  ${sma_user_roles.OPERATOR}
    Cert Config Setup  ${ca_certificate_file}  ${ca_certificate_key}  intermediate=no
    Commit

    FOR  ${passwords}  IN   ${ca_certificate_key}  ${FTPUSER_PASSWORD}   ${DUT_ADMIN_SSW_PASSWORD}
      ${cli_log_password_status}=  Run keyword and return status   Verify logs  ${cli_log_path}  ${passwords}
      Should not be true  ${cli_log_password_status}
    END

    LDAP Delete Server Profile  ${ldap_server_profile}
    SAML DELETE SP IDP  sp_name=${TEST_SP_PROFILE}  idp_name=${TEST_IDP_PROFILE}  user_role=${USER_ROLE}
    Commit Changes
    User config delete  ${RADIUS_USER}  confirm=yes
    Cert config clear certificates  clear=yes
    Commit

*** Test Cases ***
Tvh1472429c
    [Documentation]  Verify local Administrative user's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472429 \n
    [Tags]   Tvh1472429c  csdl  SEC-AUT-AUTH-4
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Run Keywords
    ...  Saml Config Delete
    ...  Commit
    ...  Common Admin Test Teardown
    Log Out Of Dut
    Log Into Dut  ${TEST_USER8}  ${TEST_USER_PSW}
    Save Config File And Load Config File
    Configure LDAP SAML RADIUS Test
    Log Out Of Dut
    Log Into Dut  ${TEST_USER8}  ${TEST_USER_PSW}

    Close Cli Session
    Start Cli Session   ${TEST_USER8}  ${TEST_USER_PSW}
    Users Add Edit Delete From CLI  ${TEST_USER_PSW}
    Run Keyword And Expect Error  *   Reset Config
    ${VERSION}=  Get Current Dut Version
    Run Keyword And Expect Error  *      Revert
    ...    version=${VERSION}
    ...    continue_revert=Yes
    ...    confirm_revert=Yes

Tvh1472431c
    [Documentation]  Verify Technician user's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472431 \n
    [Tags]   Tvh1472431c  csdl  SEC-AUT-AUTH-4
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Common Admin Test Teardown
    Log Out Of Dut
    Log Into Dut  ${TEST_USER11}  ${TEST_USER_PSW}
    ${config_file}=  Configuration File Save Config
    Navigate To  System Administration  System Administration
    Page Should Contain  Feature Keys
    Run Keyword And Expect Error  *   Users Add User  ${TEST_USER9}  ${TEST_USER9}  ${TEST_USER_PSW}  ${sma_user_roles.TECHNICIAN}
    Run Keyword And Expect Error  *   Configuration File Load Config  ${config_file}
    Run Keyword And Expect Error  *   My Dashboard Reports Add
    ...   Time Range
    ...   Incoming Malicious Threat Files
    Close Cli Session
    Start Cli Session   ${TEST_USER11}  ${TEST_USER_PSW}
    Run Keyword And Expect Error  *   Reset Config
    Reboot  5
    Sleep  5  Compensate reboot delay
    Wait until DUT Reboots  wait_for_ports=${DUT_PORT}
    Start CLI Session   ${TEST_USER11}  ${TEST_USER_PSW}

Tvh1472432c
    [Documentation]  Verify Guest user's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472432 \n
    [Tags]   Tvh1472432c  csdl  SEC-AUT-AUTH-4
#    [Setup]  DefaultTestCaseSetup
#    [Teardown]  Common Admin Test Teardown
#    Log Out Of Dut
#    Log Into Dut  ${TEST_USER12}  ${TEST_USER_PSW}
#    My Dashboard Reports Add
#    ...   Time Range
#    ...   Incoming Malicious Threat Files
    ${names}=  My Reports Get Modules List
    My Reports Add Module
    ...  Time Range
    ...  Users
    ...  Top Users: Bandwidth Used

#    ${result}  Web Tracking Search
#    ...   application_filter=app_name, Wikipedia
#    Run Keyword And Expect Error  *   Users Add User  ${TEST_USER9}  ${TEST_USER9}  ${TEST_USER_PSW}  ${sma_user_roles.TECHNICIAN}
#    Run Keyword And Expect Error  *   Configuration File Save Config
#    Run Keyword And Expect Error  *   Configuration File Load Config  ${SMA_ORIG_CONF}
#    Run Keyword And Expect Error  *   Centralized Email Message Tracking Enable
#    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
#    Close Cli Session
#    Start Cli Session   ${TEST_USER12}  ${TEST_USER_PSW}
#    Run Keyword And Expect Error  *   Reset Config

Tvh1472433c
    [Documentation]  Verify Read only user's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472433 \n
    [Tags]   Tvh1472433c  csdl  SEC-AUT-AUTH-4
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Common Admin Test Teardown
    Log Out Of Dut
    Log Into Dut  ${TEST_USER13}  ${TEST_USER_PSW}
    My Dashboard Reports Add
    ...   Time Range
    ...   Incoming Malicious Threat Files
    My Reports Add Module
    ...  Time Range
    ...  Users
    ...  Top Users: Bandwidth Used
    Run Keyword And Expect Error  *   Configuration File Save Config
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Add Customer SAML Config Azure
    Run Keyword And Expect Error  *   Commit Changes
    Go To  https://${SMA}
    Abandon Changes
    Close Cli Session
    Start Cli Session   ${TEST_USER13}  ${TEST_USER_PSW}
    Run Keyword And Expect Error  *   Reset Config

Tvh1472434c
    [Documentation]  Verify Help desk user's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472434 \n
    [Tags]   Tvh1472434c  csdl  SEC-AUT-AUTH-4
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Common Admin Test Teardown
    Log Out Of Dut
    Log Into Dut  ${TEST_USER14}  ${TEST_USER_PSW}
    ${messages}=   Email Message Tracking Search
    Run Keyword And Expect Error  *   Configuration File Save Config
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Run Keyword And Expect Error  *   My Reports Add Module
    ...  System Overview
    ...  System Status
    ...  System Uptime
    Close Cli Session
    Start Cli Session   ${TEST_USER14}  ${TEST_USER_PSW}
    Run Keyword And Expect Error  *   Reset Config

Tvh1472430c
    [Documentation]  Verify Operator user's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1472430 \n
    [Tags]   Tvh1472430c  csdl  SEC-AUT-AUTH-4
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Common Admin Test Teardown
    Log Out Of Dut
    Log Into Dut  ${TEST_USER10}  ${TEST_USER_PSW}
    Save Config File And Load Config File
    Add Customer SAML Config Azure
    Commit Changes
    Saml Config Delete
    Commit
    Add Cisco Ad As LDAP
    Centralized Email And Web Feature Accessibility Test
    Run Keyword And Expect Error  *   Spam Quarantine Search Page Open  user=${TEST_USER10}  password=${TEST_USER_PSW}
    Run Keyword And Expect Error  *   System Setup Wizard Run  admin@${CLIENT}
    Selenium Close
    Selenium Login
    Log Out Of Dut
    Log Into Dut  ${TEST_USER10}  ${TEST_USER_PSW}
    Close Cli Session
    Start Cli Session   ${TEST_USER10}  ${TEST_USER_PSW}
    Set Test Variable  ${test_user_update}  Ironport941$
    Run Keyword And Expect Error  *   User Config New  ${TEST_USER11}  ${TEST_USER11}  ${TEST_USER_PSW}
    ...  ${sma_user_roles.OPERATOR}
    ...  admin_passphrase=${TEST_USER_PSW}
    Run Keyword And Expect Error  *   User Config Edit  ${TEST_USER11}  full_name=${TEST_USER11}_new  password=${test_user_update}
    ...  admin_passphrase=${TEST_USER_PSW}
    Run Keyword And Expect Error  *   User Config Delete  ${TEST_USER11}  admin_passphrase=${TEST_USER_PSW}
    Run Keyword And Expect Error  *   Reset Config
    ${VERSION}=  Get Current Dut Version
    Run Keyword And Expect Error  *   Revert
    ...    version=${VERSION}
    ...    continue_revert=Yes
    ...    confirm_revert=Yes

Tvh1468369c
    [Documentation]  Verify default admin's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468369 \n
    ...  Verify SMA does not capture any critical/Sensitive/Personal configuration information \n
    ...  in logs after upgrade, revert to older build and verify the same happens. \n
    ...  Tvh1506355c- http://tims.cisco.com/view-entity.cmd?ent=1506355
    [Tags]   Tvh1468369c  csdl  SEC-AUT-AUTH-4  upgrade  Tvh1506355c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown
    Save Config File And Load Config File
    Configure LDAP SAML RADIUS Test
    Centralized Email And Web Feature Accessibility Test
    Users Add Edit Delete From CLI

    #Upgrade to SMA_UPGRADE_VERSION
    ${current_build}=  Get Current Dut Version
    Should Be Equal  ${SMA_BADE_BUILD}  ${current_build}
    Update Config Dynamic Host  dynamic_host=${UPDATE_SERVER}:443
    Update Config Validate Certificates  validate_certificates=no
	Commit

    Upgrade Downloadinstall
    ...  ${SMA_UPGRADE_VERSION}
    ...  seconds=10
    ...  save_cfg=yes
    ...  email=yes
    ...  email_addr=${ALERT_RCPT}
    Sleep  1m  Compensate default reboot delay
    Wait until DUT Reboots    wait_for_ports=80,443,22
    ${current_build}=  Get Current Dut Version
    Should Be Equal  ${SMA_UPGRADE_VERSION}  ${current_build}

    #Tvh1506355c - Verify logs after Upgrade
    Verify CLI and GUI logs for critical sensitive or personal information

    #Revert to Base version
    Start Cli Session If Not Open
    Revert
    ...  version=${SMA_BADE_BUILD}
    ...  continue_revert=yes
    ...  confirm_revert=yes
    Wait Until DUT Reboots  wait_for_ports=22,443,80
    ${current_build}=  Get Current Dut Version
    Should Be Equal  ${SMA_BADE_BUILD}  ${current_build}
    Restart CLI Session
    Suspend  0
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Configure SSL For GUI

    #Tvh1506355c - Verify logs after Revert
    Verify CLI and GUI logs for critical sensitive or personal information