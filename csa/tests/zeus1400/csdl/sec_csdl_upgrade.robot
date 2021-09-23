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
${LDAP_SERVER_CERTIFICATE_PATH}     //th[contains(text(),'Validate LDAP Server Certificate:')]
${LDAP_SERVER_CERTIFICATE_STATUS}   ${LDAP_SERVER_CERTIFICATE_PATH}/following-sibling::td
${LDAP_RPC_SERVER_LOG_PATH}         /data/log/heimdall/ldap_rpc_server
${LDAP_RPC_SERVER_LOG_NAME}         ${LDAP_RPC_SERVER_LOG_PATH}/ldap_rpc_server.current
${LDAP_SERVER_PROFILE}          myldap

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

Add LDAP Server Configurations From GUI
    LDAP Add Server Profile  ${LDAP_SERVER_PROFILE}  ${LDAP_AUTH_SERVER}
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    ...  use_ssl=${True}
    LDAP Edit External Authentication Queries  ${LDAP_SERVER_PROFILE}  ${EXTERNAL_QUERY}
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Commit Changes

Enable LDAP External Authentication For User
    User Config External Setup Ldap
    ...  ldap_query=${EXTERNAL_QUERY}
    ...  timeout=10
    ...  ext_group=${LDAP_SMA_USER_GROUP}
    ...  role=${sma_user_roles.ADMIN}
    Commit

Common Test Teardown
    LDAP Config Setup  ldap_server_certificate=No
    Commit
    Delete and Disable External Authentication and Ldap Server
    DefaultTestCaseTeardown

*** Test Cases ***
# Add pre upgrade test case steps here
CSDL pre upgrade validation
    [Documentation]  This test case verifies all the SMA functionalities before upgrade to the desired SMA build
    ...   Tvh1468369c - http://tims.cisco.com/view-entity.cmd?ent=1468369
    [Tags]  csdl  pre-upgrade  Tvh1468369c  Tvh1562989c  Tvh1562048c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    #Tvh1468369c
    Save Config File And Load Config File
    Configure LDAP SAML RADIUS Test
    Centralized Email And Web Feature Accessibility Test
    Users Add Edit Delete From CLI

    #Tvh1562989c
    @{cert_and_key}=  Create List  www.cisco.com.pem  www.cisco.com_key.pem  cisco.com.pem
    ...  cisco.com_key.pem
    Set suite variable  @{cert_and_key}
    Run Keyword If  '${SMA_LIB_VERSION}' >= 'zeus1400'
    ...  Verify FQDN For Valid Certificates  ${cert_and_key}
    Restart CLI Session

#    Tvh1562048c
    Add LDAP Server Configurations From GUI

Upgrade
    [Documentation]  This test case upgrades the SMA to the desired SMA build
    [Tags]  csdl  upgrade
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

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


# Add post upgrade test case steps here
Tvh1506355c
    [Documentation]  Verify default admin's role and its privileges \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1468369 \n
    ...  Verify SMA does not capture any critical/Sensitive/Personal configuration information \n
    ...  in logs after upgrade, revert to older build and verify the same happens. \n
    ...  Tvh1506355c- http://tims.cisco.com/view-entity.cmd?ent=1506355
    [Tags]   csdl  post-upgrade  Tvh1506355c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Verify CLI and GUI logs for critical sensitive or personal information

Tvh1562989c
    [Documentation]  Verify certificates with proper FQDN/DNS names can only be imported/created/ \n
    ...  validated after upgrade \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562989c \n
    [Tags]   Tvh1562989c  post-upgrade
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Verify FQDN For Valid Certificates  ${cert_and_key}

Tvh1562048c
    [Documentation]  Uprade- Verify in UI Ldap server connectivity after upgrade if
    ...  "Validate LDAP Server Certificate" option enabled and CA certificate loaded\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562048c\n
    [Tags]   Tvh1562048c  post-upgrade
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Common Test Teardown

     #Verify test connection and logs after Upgrade
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Navigate To  System Administration  LDAP
    ${status}=  Get Text  ${LDAP_SERVER_CERTIFICATE_STATUS}
    Log  ${status}
    Page Should Contain Element  ${LDAP_SERVER_CERTIFICATE_PATH}

    Ldap Edit Global Settings  interface=Auto  validate_ldap_server=${True}
    Edit Certificate Authorities  custom_list_enable=${True}
    ...  system_list_enable=${True}  custom_list_cert_path=${CUSTOM_CA_CERT}
    Commit Changes
    Enable LDAP External Authentication For User

    ${test_result} =  LDAP Run Server Profile Test  ${LDAP_SERVER_PROFILE}
    Log  ${test_result}
    Should Contain  ${test_result}  succeeded

    Verify And Wait For Log Records
    ...  search_path=mail
    ...  connected to server >=1

    Verify And Wait For Log Records
    ...  search_path=${LDAP_RPC_SERVER_LOG_NAME}
    ...  connected to server >=1

# Add post revert test case steps here
CSDL validations after revert
    [Documentation]  This test case has post revert steps for all the test cases that needs validations
    ...  to be done after reverting the SMA build to base build
    ...  Tvh1506355c- http://tims.cisco.com/view-entity.cmd?ent=1506355
    ...  Tvh1468369c - http://tims.cisco.com/view-entity.cmd?ent=1468369
    [Tags]  csdl  post-revert  Tvh1506355c  Tvh1468369c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    #Revert
    Start Cli Session If Not Open
    Revert
    ...  version=${SMA_BADE_BUILD}
    ...  continue_revert=yes
    ...  confirm_revert=yes
    Wait Until DUT Reboots  wait_for_ports=22,443,80
    ${current_build}=  Get Current Dut Version
    Should Be Equal  ${SMA_BADE_BUILD}  ${current_build}

    #Tvh1468369c
    Restart CLI Session
    Suspend  0
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Configure SSL For GUI

    #Tvh1506355c - Verify logs after Revert
    Verify CLI and GUI logs for critical sensitive or personal information