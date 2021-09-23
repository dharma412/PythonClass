# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/CT1886_SEC-LOG-NOSENS-3_2.txt#1 $
# $Date: 2020/09/08 $
# $Author: cballa $

*** Settings ***
Resource           sma/saml.txt
Variables          sma/saml_constants.py
Resource           sma/csdlresource.txt

Force Tags      csdl
Suite Setup     Initialize Suite
Suite Teardown  Finalize Suite

*** Variables ***
${INVALID_LDAP_USER_PASSWORD}=  Ldappswd12$
${INVALID_SAML_USER_PASSWORD}=  Samlpswd12$
${TEST_EUQ_SP_PROFILE}=         euq_sp_profile
${TEST_EUQ_IDP_PROFILE}=        euq_idp_profile
${TEMP_PASSWORD_1}=             Cisco12#
${TEMP_PASSWORD_2}=             Cisco12%
${USER_NAME}=                   testuser
${GROUP_GUESTS}=                Guests
${EXTERNAL_QUERY}=              ${LDAP_AUTH_SERVER}.externalauth


*** Keywords ***
Initialize Suite
    CSDL Suite Setup
    Log Config Edit  authentication  log_level=Debug
    Log Config Edit  smad_logs  log_level=Debug
    Log Config Edit  gui_logs  log_level=Debug
    Commit

Finalize Suite
    Log Config Edit  authentication  log_level=Info
    Log Config Edit  smad_logs  log_level=Info
    Log Config Edit  gui_logs  log_level=Info
    Commit
    CSDL Suite Teardown

Add LDAP Server Configurations With Anonymous
    LDAP Add Server Profile  ${LDAP_USER}  ${LDAP_AUTH_SERVER}
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit External Authentication Queries  ${LDAP_USER}  ${EXTERNAL_QUERY}
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

Add LDAP Server Configurations with Use Passphrase
    LDAP Add Server Profile  ${LDAP_USER}  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_BINDDN}:${LDAP_PASSWORD}
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit External Authentication Queries  ${LDAP_USER}  ${EXTERNAL_QUERY}
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Commit Changes

Add UI Login SAML Configurations From GUI
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID_Azure}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes

Add EUQ Login SAML Configurations From GUI
     ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP FOR EUQ  ${TEST_EUQ_SP_PROFILE}  ${TEST_EUQ_IDP_PROFILE}  ${settings}
    Commit Changes

Enable SAML External Authentication For Customer
    Userconfig External Setup Saml
    ...  cache_time=0
    ...  group_name=${SAML_GROUP_Azure}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    Commit

Reset Configuration
    Suspend
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_TMP_PASSWORD}
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_TMP_PASSWORD}

Tvh1468384c Setup
    DefaultTestCaseSetup
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Add LDAP Server Configurations With Anonymous
    Enable LDAP External Authentication For User
    Roll Over Now  logname=authentication

Tvh1468384c Teardown
    Restart CLI Session
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Users Disable External Authentication
    LDAP Delete Server Profile  ${LDAP_USER}
    Commit Changes
    DefaultTestCaseTeardown

Tvh1468386c Setup
    DefaultTestCaseSetup
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Add UI Login SAML Configurations From GUI
    Enable SAML External Authentication For Customer
    Log Out Of Dut
    Roll Over Now  logname=gui_logs

Tvh1468386c Teardown
    Selenium Login
    User Config External Setup Disable
    Saml Config Delete
    Commit
    DefaultTestCaseTeardown

Tvh1468397c Setup
    DefaultTestCaseSetup
    ${CONFIG_FILE}=  Save Config  yes
    Set Test Variable   ${CONFIG_FILE}
    User Config Policy Passwordstrength  reuse=no
    Commit
    Roll Over Now  logname=cli_logs
    Roll Over Now  logname=gui_logs

Tvh1468397c Teardown
    Load Config From File   ${CONFIG_FILE}
    commit
    DefaultTestCaseTeardown


*** Test Cases ***
Tvh1468398c
    [Documentation]  Configure password for new user under CLI - userconfig > new and update user's
    ...  password through CLI - userconfig > edit, Verify the credentials are not logged and details
    ...  relevant to event/action alone logged in cli_logs. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468398c
    [Tags]      Tvh1468398c
    [Setup]     DefaultTestCaseSetup
    [Teardown]  Run keywords  User Config Delete  ${USER_NAME}  confirm=yes
    ...  AND  Commit
    ...  DefaultTestCaseTeardown
    Set Test Variable  ${TEST_ID}    Tvh1468398c

    #Create new user through CLI.
    User Config New  ${USER_NAME}  ${TEST_ID}  ${TEMP_PASSWORD_1}  group=${GROUP_GUESTS}
    Commit

    #Edit user's password through CLI.
    User Config Edit  ${USER_NAME}  ${TEST_ID}  ${TEMP_PASSWORD_2}  group=${GROUP_GUESTS}
    Commit

    # Verify old and new passwords are not logged to cli_logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${CLI_LOGS}
    ...  ${TEMP_PASSWORD_1} == 0
    ...  ${TEMP_PASSWORD_1} == 0

Tvh1468382c
    [Documentation]  Login to SMA CLI (SSH) with valid & invalid admin/other users' credentials, \n
    ...  Verify credentials are not logged and details relevant to event/action alone logged in \n
    ...  cli_logs/authentication logs on both events \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468382c
    [Tags]      Tvh1468382c
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Roll Over Now  logname=authentication

    # Try to login to SMA CLI with invalid credentials, verify it is failed to login
    ${ready}    ${is_login_success}    Run Keyword And Ignore Error
    ...    Start CLI Session  ${INVALID_ADMIN}  ${INVALID_ADMIN_PASSWORD}
    Should Not Be True  ${is_login_success}

    # Verify password is not logged to authentication logs in unsuccessful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  User (.)* failed authentication. >= 1
    ...  ${INVALID_ADMIN_PASSWORD} == 0

    Start CLI Session If Not Open
    Roll Over Now  logname=authentication

    # Try to login to SMA CLI with valid credentials. Here, admin session is restarted to verify the logs
    Restart Cli Session

    # Verify password is not logged to authentication logs in successful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  User ${DUT_ADMIN} from ${CLIENT_IP} was authenticated successfully with privilege admin by CLI based authentication using an SSH connection. >= 1
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

Tvh1468383c
    [Documentation]  Login to SMA GUI (SSL/HTTPS) with  valid & invalid admin/other users' credentials, Verify credentials are \n
    ...  not logged and details relevant to event/action alone logged in gui_logs/authentication logs on both events \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468383c
    [Tags]      Tvh1468383c
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown
    Roll Over Now  logname=authentication

    # Try to login to SMA GUI with valid credentials.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    # Verify password is not logged to authentication logs in successful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  User ${DUT_ADMIN} from ${CLIENT_IP} was authenticated successfully with privilege admin using an HTTPS connection. >= 1
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

    Roll Over Now  logname=authentication

    # Try to login to SMA GUI with invalid credentials, verify it is failed to login
    Run Keyword And Expect Error  *  Login to SMA via GUI  ${INVALID_ADMIN}  ${INVALID_ADMIN_PASSWORD}

    # Verify password is not logged to authentication logs in unsuccessful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  ${CLIENT_IP} failed authentication. >= 1
    ...  ${INVALID_ADMIN_PASSWORD} == 0

Tvh1468384c
    [Documentation]  Login to SMA CLI with  valid & invalid LDAP user credentials, Verify credentials are not logged \n
     ...  and details relevant to event/action alone logged in cli_logs/authentication logs on both events \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468384c
    [Tags]      Tvh1468384c
    [Setup]     Tvh1468384c Setup
    [Teardown]  Tvh1468384c Teardown

    # Add Email Security Appliance with valid credentials
    Start CLI Session  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}

    # Verify password is not logged to smad_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  User ${LDAP_SMA_USER} from ${CLIENT_IP} was authenticated successfully with privilege admin by CLI based authentication using an SSH connection. >= 1
    ...  ${LDAP_SMA_USER_PASS} == 0

    Restart CLI Session
    Roll Over Now  logname=authentication

    # Try to login to SMA CLI with invalid LDAP user credentials, verify it is failed to login
    ${ready}    ${is_login_success}    Run Keyword And Ignore Error
    ...    Start CLI Session  ${LDAP_USER}  ${INVALID_LDAP_USER_PASSWORD}
    Should Not Be True  ${is_login_success}

    # Verify password is not logged to authentication logs in unsuccessful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  User (.)* failed authentication. >= 1
    ...  ${INVALID_LDAP_USER_PASSWORD} == 0

Tvh1468385c
    [Documentation]  Login to SMA GUI with  valid & invalid LDAP user credentials, Verify credentials are not \n
    ...  logged and details relevant to event/action alone logged in gui_logs/authentication logs on both events \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468385c
    [Tags]      Tvh1468385c
    [Setup]     Tvh1468384c Setup
    [Teardown]  Tvh1468384c Teardown

    # Try to login to SMA GUI with valid LDAP user credentials.
    Login to SMA via GUI  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}

    # Verify password is not logged to authentication logs in successful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  User ${LDAP_SMA_USER} from ${CLIENT_IP} was authenticated successfully with privilege admin using an HTTPS connection. >= 1
    ...  ${LDAP_SMA_USER_PASS} == 0

    Roll Over Now  logname=authentication

    # Try to login to SMA GUI with invalid LDAP user credentials, verify it is failed to login
    Run Keyword And Expect Error  *  Login to SMA via GUI  ${LDAP_USER}  ${INVALID_LDAP_USER_PASSWORD}

    # Verify password is not logged to authentication logs in unsuccessful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  ${CLIENT_IP} failed authentication. >= 1
    ...  ${INVALID_LDAP_USER_PASSWORD} == 0

Tvh1468386c
    [Documentation]  Login to SMA GUI with  valid & invalid SAML users' credentials, Verify credentials are not logged \n
    ...  and details relevant to event/action alone logged in gui_logs/authentication logs on both events \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468386c
    [Tags]      Tvh1468386c
    [Setup]     Tvh1468386c Setup
    [Teardown]  Tvh1468386c Teardown

    # Try to login to SMA GUI with valid SAML user credentials.
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}
    Log Out Of Dut
    Close Browser

    # Verify password is not logged to gui_logs logs in successful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  SourceIP:${CLIENT_IP} .* Username:${SAML_AZUR_USER} .* Action: The HTTPS session has been established successfully. >= 1
    ...  ${SAML_AZUR_USER_PASSWORD} == 0

    Roll Over Now  logname=authentication
    Launch Dut Browser

    # Try to login to SMA GUI with invalid SAML user credentials, verify it is failed to login
    Run Keyword And Expect Error  *  SSO Log Into Dut  ${USER_ROLE_CUSTOMER}   ${SAML_AZUR_USER}  ${INVALID_SAML_USER_PASSWORD}
    Close Browser

    # Verify password is not logged to authentication logs in unsuccessful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  ${INVALID_SAML_USER_PASSWORD} == 0

Tvh1468390c
    [Documentation]  Add SAML SP profile for UI login under GUI - System Administration > SAML, upload
    ...  .pem/.p12 certificates and private keys. Verify the private keys are not logged and details relevant
    ...  to event/action alone logged in gui_logs, repeat the steps for EUQ login. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468390c.\n
    ...  Add SAML SP profile for UI login under GUI - System Administration > SAML, upload .pem/.p12
    ...  certificates with password. Verify the credentials are not logged and details relevant to event/action
    ...  alone logged in gui_logs, repeat the steps for EUQ login.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468407c
    [Tags]      Tvh1468390c  Tvh1468407c
    [Setup]     DefaultTestCaseSetup
    [Teardown]  Run keywords  SAML DELETE EUQ PROFILES  sp_name=${TEST_EUQ_SP_PROFILE}  idp_name=${TEST_EUQ_IDP_PROFILE}
    ...   AND  Delete SP IDP For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    ...   AND  DefaultTestCaseTeardown

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    #Add SAML SP and IDP setup for GUI login with Certificates through GUI.
    Add UI Login SAML Configurations From GUI

    # Verify certificate's private key is not logged to gui_logs logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  system_admini.*saml >= 1
    ...  ${CERT_FILE_KEY_SP_Azure} == 0
    ...  ${CERTIFICATE_PASSPHRASE} == 0

    Roll Over Now  logname=gui_logs
    #Add SAML SP and IDP setup for GUI login with Certificates through GUI.
    Add EUQ Login SAML Configurations From GUI

    # Verify certificate's private key is not logged to gui_logs logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  system_admini.*saml >= 1
    ...  ${CERT_FILE_KEY_SP_Azure} == 0
    ...  ${CERTIFICATE_PASSPHRASE} == 0

Tvh1468401c
    [Documentation]  Configure password for new user under GUI - System Administration > Users and
    ...  update user's password through GUI - System Administration > Users (Click on user and update),
    ...  verify the credentials are not logged and details relevant to event/action alone logged in gui_logs.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468401c
    [Tags]      Tvh1468401c
    [Setup]     DefaultTestCaseSetup
    [Teardown]  Run keywords  User Config Delete  ${USER_NAME}  confirm=yes
    ...  AND  Commit
    ...  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  Tvh1468401c
    Roll Over Now  logname=gui_logs

    #Create new user through GUI.
    Users Add User
    ...  ${USER_NAME}
    ...  Operator User
    ...  ${TEMP_PASSWORD_1}
    ...  user_role=${sma_user_roles.OPERATOR}
    Commit Changes

    #Edit user's password through GUI.
    Users Edit User  ${USER_NAME}  password=${TEMP_PASSWORD_2}
    Commit Changes

    # Verify old and new passwords are not logged to gui_logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${TEMP_PASSWORD_1} == 0
    ...  ${TEMP_PASSWORD_2} == 0

Tvh1468405c
    [Documentation]  Add LDAP server profile under GUI - System Administration > LDAP,
    ...  configure Authentication Method to use passphrase and provide credentials. Configure
    ...  any of the queries and do Test query qith LDAP user credentials, Verify the credentials
    ...  are not logged and details relevant to event/action alone logged in gui_logs on both checks
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468405c
    [Tags]      Tvh1468405c
    [Setup]     DefaultTestCaseSetup
    [Teardown]  Run keywords  LDAP Delete Server Profile  ${LDAP_USER}
    ...  AND  Commit Changes
    ...  AND  DefaultTestCaseTeardown

    Roll Over Now  logname=gui_logs
    Add LDAP Server Configurations with Use Passphrase
    #External Authentication User Accounts Query Test
    ${query_result} =  LDAP Run External Authentication Queries Test  ${LDAP_USER}
    ...  user  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    Should Contain  ${query_result}  match positive

    #Verify password is not logged to gui logs
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${LDAP_SMA_USER_PASS} == 0

Tvh1468397c
    [Documentation]  Change admin passphrase through passphrase/passwd commands in CLI, verify the credentials \n
    ...  are not logged and details relevant to event/action alone logged in cli_logs \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468397c
    ...  Change admin passphrase through GUI - Options > Change Passphrase, verify the credentials are not logged \n
    ...  and details relevant to event/action alone logged in gui_logs \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468400c
    [Tags]      Tvh1468397c  Tvh1468400c
    [Setup]     Tvh1468397c Setup
    [Teardown]  Tvh1468397c Teardown

    #Change admin password through CLI passwd command.
    Passwd  old_pwd=${DUT_ADMIN_SSW_PASSWORD}  new_pwd=${DUT_ADMIN_TMP_PASSWORD}

    # Verify old and new passwords are not logged to cli_logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${CLI_LOGS}
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0
    ...  ${DUT_ADMIN_TMP_PASSWORD} == 0

    #Change admin password through GUI.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_TMP_PASSWORD}
    Change Password  ${DUT_ADMIN_TMP_PASSWORD}  ${DUT_ADMIN_SSW_PASSWORD}

    # Verify old and new passwords are not logged to gui_logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${DUT_ADMIN_TMP_PASSWORD} == 0
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

Tvh1468402c
    [Documentation]  Change admin passphrase through GUI - System Administration > System Setup Wizard,
    ...   verify the credentials are not logged and details relevant to event/action alone logged in gui_logs.\n
    ...   http://tims.cisco.com/warp.cmd?ent=Tvh1468402c
    [Tags]      Tvh1468402c
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Reset Configuration
    Roll Over Now  logname=gui_logs

    #change passphrase through GUI- SSW
    System setup wizard run  ${EMAIL_ALERTS}  userpasswd=${DUT_ADMIN_SSW_PASSWORD}

    # Verify passwords are not logged to gui_logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0