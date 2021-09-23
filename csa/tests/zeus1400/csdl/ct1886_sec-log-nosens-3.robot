# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/CT1886_SEC-LOG-NOSENS-3.txt#2 $
# $Date: 2020/10/08 $
# $Author: cballa $

*** Settings ***
Resource     esa/global.txt
Resource     sma/wsa_global.txt
Resource     sma/config_masters.txt
Resource     sma/csdlresource.txt
Resource     sma/saml.txt

Force Tags      csdl
Suite Setup     Initialize Suite
Suite Teardown  Finalize Suite
Test Setup      DefaultTestCaseSetup


*** Variables ***
${COMMON_CERTIFICATE}=        %{SARF_HOME}/tests/testdata/sma/csdl/csdl_common_cert.crt
${COMMON_CERTIFICATE_KEY}=    %{SARF_HOME}/tests/testdata/sma/csdl/csdl_common_cert.pem
${INBOUND_CERTIFICATE}=       %{SARF_HOME}/tests/testdata/sma/csdl/csdl_inbound_cert.crt
${INBOUND_CERTIFICATE_KEY}=   %{SARF_HOME}/tests/testdata/sma/csdl/csdl_inbound_cert.pem
${OUTBOUND_CERTIFICATE}=      %{SARF_HOME}/tests/testdata/sma/csdl/csdl_outbound_cert.crt
${OUTBOUND_CERTIFICATE_KEY}=  %{SARF_HOME}/tests/testdata/sma/csdl/csdl_outbound_cert.pem
${HTTPS_CERTIFICATE}=         %{SARF_HOME}/tests/testdata/sma/csdl/csdl_https_cert.crt
${HTTPS_CERTIFICATE_KEY}=     %{SARF_HOME}/tests/testdata/sma/csdl/csdl_https_cert.pem
${LDAP_CERTIFICATE}=          %{SARF_HOME}/tests/testdata/sma/csdl/csdl_ldap_cert.crt
${LDAP_CERTIFICATE_KEY}=      %{SARF_HOME}/tests/testdata/sma/csdl/csdl_ldap_cert.pem
${MAIL_PATH}=                 %{SARF_HOME}/tests/testdata/esa/


*** Keywords ***
Initialize Suite
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA
    DefaultTestSuiteSetup
    ${ESA_PRIVATE_LISTENER_IP}=  Get ESA Private IP
    Set Suite Variable  ${ESA_PRIVATE_LISTENER_IP}

    Set Appliance Under Test To WSA
    wsa_global.DefaultTestSuiteSetup

    Set Appliance Under Test To SMA
    global_sma.DefaultTestSuiteSetup
    Selenium Login
    Spam Quarantine Enable
    Centralized Web Reporting Enable
    Centralized Email Message Tracking Enable
    Commit Changes
    Log Config Edit  authentication  log_level=Debug
    Log Config Edit  smad_logs  log_level=Debug
    Log Config Edit  gui_logs  log_level=Debug
    Commit

Finalize Suite
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA
    Selenium Close
    DefaultTestSuiteTeardown

    Set Appliance Under Test To WSA
    wsa_global.DefaultTestSuiteTeardown

    Set Appliance Under Test To SMA
    Spam Quarantine Disable
    Centralized Web Reporting Disable
    Centralized Email Message Tracking Disable
    Commit Changes
    Log Config Edit  authentication  log_level=Info
    Log Config Edit  smad_logs  log_level=Info
    Log Config Edit  gui_logs  log_level=Info
    Commit
    Close All Browsers

Delete and Disable External Server
    User Config External Setup Disable
    User Config External Setup Delete  ${RADIUS_SERVER}
    Commit
    DefaultTestCaseTeardown

Delete Appliance Under SMA
    [Arguments]  ${appliance}
    Appliance Config Delete  ${appliance}
    Commit
    DefaultTestCaseTeardown

Set Variables For Certificates
    ${common_cert}=        OperatingSystem.Get File  ${COMMON_CERTIFICATE}
    Set Test Variable      ${common_cert}
    ${common_cert_key}=    OperatingSystem.Get File  ${COMMON_CERTIFICATE_KEY}
    Set Test Variable      ${common_cert_key}
    ${inbound_cert}=       OperatingSystem.Get File  ${INBOUND_CERTIFICATE}
    Set Test Variable      ${inbound_cert}
    ${inbound_cert_key}=   OperatingSystem.Get File  ${INBOUND_CERTIFICATE_KEY}
    Set Test Variable      ${inbound_cert_key}
    ${outbound_cert}=      OperatingSystem.Get File  ${OUTBOUND_CERTIFICATE}
    Set Test Variable      ${outbound_cert}
    ${outbound_cert_key}=  OperatingSystem.Get File  ${OUTBOUND_CERTIFICATE_KEY}
    Set Test Variable      ${outbound_cert_key}
    ${https_cert}=         OperatingSystem.Get File  ${HTTPS_CERTIFICATE}
    Set Test Variable      ${https_cert}
    ${https_cert_key}=     OperatingSystem.Get File  ${HTTPS_CERTIFICATE_KEY}
    Set Test Variable      ${https_cert_key}
    ${ldap_cert}=          OperatingSystem.Get File  ${LDAP_CERTIFICATE}
    Set Test Variable      ${ldap_cert}
    ${ldap_cert_key}=      OperatingSystem.Get File  ${LDAP_CERTIFICATE_KEY}
    Set Test Variable      ${ldap_cert_key}

Tvh1468408c Setup
    DefaultTestCaseSetup
    Initialize Variables
    Restart CLI Session
    Roll Over Now  logname=cli_logs

Enable PVO and DLP Configurations on SMA and ESA
    Set Appliance Under Test To SMA
    Restart CLI Session
    Pvo Quarantines Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes
    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes

    Set Appliance Under Test to ESA
    Run keyword and ignore error  Log Out Of Dut
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Message Tracking Enable  tracking=centralized
    Dlp Enable
    Dlp Edit Settings  enable_matched_content_logging=${True}
    Dlp Policy New
    ...  Privacy Protection
    ...  Credit Card Numbers
    ...  submit=${True}
    Dlp Message Action Edit  Default Action  msg_action=Quarantine
    ${settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  Credit Card Numbers  ${True}
    ...  Enable All  ${True}
    Mail Policies Edit DLP  outgoing  default  ${settings}
    Commit Changes

    ${pvo_global_settings}=  Create Dictionary
    ...  Quarantine IP Interface  ${DUT_DATA2}
    ...  Quarantine Port  7025

    PVO Quarantines Enable
    ...  ${pvo_global_settings}
    Commit Changes

Tvh1468413c Teardown
    Set Appliance Under Test to ESA
    Dlp Disable
    Pvo Quarantines Disable
    Commit Changes
    Set Appliance Under Test to SMA
    Delete Appliance Under SMA  ${ESA}

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}=${ESA_PRIVATE_LISTENER_IP}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}


*** Test Cases ***
Tvh1468406c
    [Documentation]  Add LDAP server profile using CLI - ldapconfig command, configure authtype to use
    ...  passphrase and provide credentials. Configure any of the queries and do Test query qith LDAP
    ...  user credentials, Verify the credentials are not logged and details relevant to event/action
    ...  alone logged in cli_logs on both checks.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468406c
    [Tags]  Tvh1468406c
    [Teardown]  Run keywords  LDAP Config Delete  ${LDAP_USER}
    ...  AND  Commit
    ...  AND  DefaultTestCaseTeardown

    #Add LDAP server profile using CLI
    LDAP Config New  ${LDAP_USER}  ${LDAP_AUTH_SERVER}  use_ssl=no  auth_type=Passphrase based
    ...   username=${LDAP_BINDDN}  password=${LDAP_PASSWORD}
    ...   validate_settings=no  server_type=${LDAP_SERVER_TYPE}  port=${LDAP_AUTH_PORT}
    ...   base=dc=${LDAP_BASE_DN}
    Commit

    # Verify password is not logged to cli_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${CLI_LOGS}
    ...  ${LDAP_SMA_USER_PASS} == 0

    Roll Over Now  logname=cli_logs

    #Do Test Query with LDAP user credentials.
    LDAP Config Add Externalauth   ${LDAP_USER}  identity=${LDAP_SMA_USER_GROUP}  password=${LDAP_SMA_USER_PASS}
    Commit

    # Verify password is not logged to cli_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${CLI_LOGS}
    ...  ${LDAP_SMA_USER_PASS} == 0

Tvh1468417c
    [Documentation]  Configure Radius server under GUI - System Administration > Users > External Authentication
    ...  with server's shared secret and login to GUI as Radius user, verify shared secrets/user
     ...  credentials are not logged in to gui_logs on configuration and communication
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468417c
    [Tags]  Tvh1468417c
    [Teardown]  Run keywords  Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  AND  Delete and Disable External Server

    #Configure Radius server under GUI
    Users Edit External Authentication  RADIUS
    ...  radius_servers=${RADIUS_SERVER}:${RADIUS_PORT}:${RADIUS_SECRET}:10
    ...  auth_cache_timeout=20
    ...  group_mapping=${RADIUS_CLASS_ATTRIBUTE}:Administrator
    Commit Changes

    Login to SMA via GUI  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    # Verify password is not logged to gui_logs logs in successful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  SourceIP:${CLIENT_IP} .* Username:${RADIUS_CLASS_ATTRIBUTE} .* Action: The HTTPS session has been established successfully. >= 1
    ...  ${RADIUS_USER_PASSWORD} == 0

Tvh1468419c
    [Documentation]  CConfigure Radius server through CLI - userconfig > external command with server's
    ...  shared secret and login to CLI as Radius user, verify shared secrets/user credentials are not
    ...  logged in to gui_logs/authentication on configuration and communication.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468419c
    [Tags]	 Tvh1468419c
    [Teardown]  Run keywords  Restart CLI Session
    ...  AND  Delete and Disable External Server
    ...  AND  DefaultTestCaseTeardown

    #Configure Radius server under CLI
    User Config External Setup New  ${RADIUS_SERVER}
    ...  ${RADIUS_SECRET}
    ...  create_mapping=yes
    ...  group_name=${RADIUS_CLASS_ATTRIBUTE}
    ...  role=Administrator
    Commit

    Start Cli Session  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}

    # Verify password is not logged to authentication logs in successful attempts, only event is logged
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${AUTHENTICATION_LOGS}
    ...  User ${RADIUS_CLASS_ATTRIBUTE} from ${CLIENT_IP} was authenticated successfully by CLI based authentication using an SSH connection. >=1
    ...  ${RADIUS_USER_PASSWORD} == 0

Tvh1468380c
    [Documentation]  Add ESA appliance to SMA under CLI - applianceconfig command, configure ESA and try to establish
	...  connection with  valid & invalid Password. Verify credentials are not logged and details relevant to event/action
	...  alone logged in cli_logs/smad  logs on both events.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468380c
    [Tags]	 Tvh1468380c
    [Teardown]  Delete Appliance Under SMA  ${ESA}

    # Try to Add Email Security Appliance with invalid credentials, verify it is failed to add appliance
    Run Keyword And Expect Error  AuthError:*
    ...  Appliance Config Add
    ...  ${ESA_IP}
    ...  ${ESA}
    ...  esa
    ...  username=${INVALID_ADMIN}
    ...  password=${INVALID_ADMIN_PASSWORD}

    # Verify password is not logged to smad_logs in unsuccessful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${SMAD_LOGS}
    ...  Configuring a remote appliance at ip ${ESA_IP} with user ${INVALID_ADMIN} >= 1
    ...  ${INVALID_ADMIN_PASSWORD} == 0

    Restart CLI Session
    Roll Over Now  logname=smad_logs

    # Add Email Security Appliance with valid credentials
    Appliance Config Add
    ...  ${ESA_IP}
    ...  ${ESA}
    ...  esa
    ...  username=${DUT_ADMIN}
    ...  password=${DUT_ADMIN_SSW_PASSWORD}
    Commit

    # Verify password is not logged to smad_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${SMAD_LOGS}
    ...  Configuring a remote appliance at ip ${ESA_IP} with user ${DUT_ADMIN} >= 1
    ...  Connection to remote appliance at ip ${ESA_IP} was successful >= 1
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

Tvh1468381c
    [Documentation]  Add WSA appliance to SMA under CLI - applianceconfig command, configure WSA and
    ...   try to establish connection with  valid & invalid Password. Verify credentials
    ...   are not logged and details relevant to event/action alone logged in cli_logs/smad
    ...   logs on both events.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468381c
    [Tags]	 Tvh1468381c
    [Teardown]  Delete Appliance Under SMA  ${WSA}

    # Try to Add Email Security Appliance with invalid credentials, verify it is failed to add appliance
    Run Keyword And Expect Error  RemoteConnectionError:*
    ...  Appliance Config Add
    ...  ${WSA_M1_IP}
    ...  ${WSA}
    ...  wsa
    ...  username=${INVALID_ADMIN}
    ...  password=${INVALID_ADMIN_PASSWORD}

    # Verify password is not logged to smad_logs in unsuccessful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${SMAD_LOGS}
    ...  Configuring a remote appliance at ip ${WSA_M1_IP} with user ${INVALID_ADMIN} >= 1
    ...  ${INVALID_ADMIN_PASSWORD} == 0

    Restart CLI Session
    Roll Over Now  logname=smad_logs

    # Add Email Security Appliance with valid credentials
    Appliance Config Add
    ...  ${WSA_M1_IP}
    ...  ${WSA}
    ...  wsa
    ...  username=${DUT_ADMIN}
    ...  password=${DUT_ADMIN_SSW_PASSWORD}
    Commit

    # Verify password is not logged to smad_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${SMAD_LOGS}
    ...  Configuring a remote appliance at ip ${WSA_M1_IP} with user ${DUT_ADMIN} >= 1
    ...  Connection to remote appliance at ip ${WSA_M1_IP} was successful >= 1
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

Tvh1468378c
    [Documentation]  Add ESA appliance to SMA under GUI - Centralized Services > Security Appliances > Email,
    ...  configure ESA and try to establish connection with  valid & invalid Password. Verify credentials are not logged
    ...  and details relevant to event/action alone logged in gui_logs/smad logs on both events \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468378c
    [Tags]  Tvh1468378c
    [Teardown]  Delete Appliance Under SMA  ${ESA}

    # Try to Add Email Security Appliance with invalid credentials, verify it is failed to add appliance
    Run Keyword And Expect Error  * Authentication Failed *
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  ssh_credentials=${INVALID_ADMIN}:${INVALID_ADMIN_PASSWORD}

    # Verify password is not logged to smad_logs in unsuccessful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${SMAD_LOGS}
    ...  Configuring a remote appliance at ip ${ESA_IP} with user ${INVALID_ADMIN} >= 1
    ...  ${INVALID_ADMIN_PASSWORD} == 0

    # Verify password is not logged to gui_logs in unsuccessful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${INVALID_ADMIN_PASSWORD} == 0

    Roll Over Now  logname=smad_logs
    Roll Over Now  logname=gui_logs

    # Add Email Security Appliance with valid credentials
    Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes

    # Verify password is not logged to smad_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${SMAD_LOGS}
    ...  Configuring a remote appliance at ip ${ESA_IP} with user ${DUT_ADMIN} >= 1
    ...  Connection to remote appliance at ip ${ESA_IP} was successful >= 1
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

    # Verify password is not logged to gui_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

Tvh1468379c
    [Documentation]  Add WSA appliance to SMA under GUI - Centralized Services > Security Appliances > Web,
    ...  configure WSA and try to establish connection with  valid & invalid Password. Verify credentials are not logged
    ...  and details relevant to event/action alone logged in gui_logs/smad logs on both events \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468379c
    [Tags]  Tvh1468379c
    [Teardown]  Delete Appliance Under SMA  ${WSA}

    # Try to Add Web Security Appliance with invalid credentials, verify it is failed to add appliance
    Run Keyword And Expect Error  *
    ...  Security Appliances Add Web Appliance
    ...  ${WSA}
    ...  ${WSA_M1_IP}
    ...  ssh_credentials=${INVALID_ADMIN}:${INVALID_ADMIN_PASSWORD}

    # Verify password is not logged to smad_logs in unsuccessful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${SMAD_LOGS}
    ...  Configuring a remote appliance at ip ${WSA_M1_IP} with user ${INVALID_ADMIN} >= 1
    ...  ${INVALID_ADMIN_PASSWORD} == 0

    # Verify password is not logged to gui_logs in unsuccessful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${INVALID_ADMIN_PASSWORD} == 0

    Roll Over Now  logname=smad_logs
    Roll Over Now  logname=gui_logs

    # Add Email Security Appliance with valid credentials
    Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Web Appliance
    ...  ${WSA}
    ...  ${WSA_M1_IP}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes

    # Verify password is not logged to smad_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${SMAD_LOGS}
    ...  Configuring a remote appliance at ip ${WSA_M1_IP} with user ${DUT_ADMIN} >= 1
    ...  Connection to remote appliance at ip ${WSA_M1_IP} was successful >= 1
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

    # Verify password is not logged to gui_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${DUT_ADMIN_SSW_PASSWORD} == 0

Tvh1468408c
    [Documentation]  Add SAML SP profile for UI login using CLI - samlconfig, upload .pem/.p12
    ...  certificates with password. Verify the credentials are not logged and details relevant
    ...  to event/action alone logged in gui_logs, repeat the steps for EUQ login.
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468408c
    ...  Add SAML SP profile for UI login using CLI - samlconfig, upload .pem/.p12 certificates
    ...  and private keys. Verify the credentials are not logged and details relevant to
    ...  event/action alone captured in cli_logs, repeat the steps for EUQ login
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468391c
    [Tags]      Tvh1468408c  Tvh1468391c
    [Setup]     Tvh1468408c Setup
    [Teardown]  Run keywords  Delete/Clear Customer SMAL Config
    ...  AND  DefaultTestCaseTeardown

    #Add SAML SP and IDP setup for CLI login with Certificates through CLI.
    Add Customer SAML Config
    # Verify certificate's private key and password are not logged to cli_logs logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${CLI_LOGS}
    ...  ${CERTIFICATE_PASSPHRASE} == 0
    ...  BEGIN RSA PRIVATE KEY == 0

Tvh1468389c
    [Documentation]  Add certificate and its private key through CLI certconfig > certificate
    ...  command and Verify the related private keys are not logged and details relevant to
    ...  event/action alone logged in cli_logs.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468389c
    [Tags]      Tvh1468389c
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Variables For Certificates
    Roll Over Now  logname=cli_logs
    # Configure one common certificate for mail, https and ldap through certconfig.
    Cert Config Setup
    ...  ${common_cert}
    ...  ${common_cert_key}
    ...  intermediate=no
    Commit

    # Verify private key is not logged to cli_logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${CLI_LOGS}
    ...  BEGIN RSA PRIVATE KEY == 0

    Roll Over Now  logname=cli_logs

    # Configure separate certificates for mail, https and ldap through certconfig.
    Cert Config Setup  ${inbound_cert}  ${inbound_cert_key}
    ...  one_cert=no
    ...  intermediate=no
    ...  rsa_cert_outbound=${outbound_cert}
    ...  rsa_key_outbound=${outbound_cert_key}
    ...  rsa_cert_https=${https_cert}
    ...  rsa_key_https=${https_cert_key}
    ...  rsa_cert_ldap=${ldap_cert}
    ...  rsa_key_ldap=${ldap_cert_key}
    Commit

    #Verify private key is not logged to cli_logs.
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${CLI_LOGS}
    ...  BEGIN RSA PRIVATE KEY == 0

Tvh1468413c
    [Documentation]  Verify SMA does not log content of emails that quarantined in PVO/ Spam Quarantines \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468413c
    [Tags]      Tvh1468413c
    [Teardown]  Tvh1468413c Teardown
    Set Test Variable  ${TEST_ID}  Tvh1468413c

    Enable PVO and DLP Configurations on SMA and ESA

    Inject Custom Message  dlp/credit_card.mbox
    Set Appliance Under Test To SMA
    # Verify password is not logged to cli_logs in successful attempts
    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=mail
    ...  MID.*received from the ESA ${ESA_IP} for centralized quarantine >=1
    ...  'reason_string': 'Credit Card Numbers' >=1
    ...  'matched_content': '< the matched content. >' >=1