*** Settings ***
Resource     esa/logs_parsing_snippets.txt
Resource     regression.txt
Resource     sma/global_sma.txt
Variables    sma/saml_constants.py 

Suite Setup   Audit Log Suite Setup
Suite Teardown  DefaultTestSuiteTeardown

*** Variables ***
${CONFIG_DIR}         /data/pub/configuration

*** Keywords  ***
Audit Log Suite Setup
    Set Suite Variable  ${audit_log_name}  audit_logs
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA

    global_sma.DefaultTestSuiteSetup
    Log Subscriptions Add Log
    ...  Audit Logs
    ...  ${audit_log_name}
    ...  filename=${audit_log_name}
    ...  log_size=5M
    Commit Changes

Audit Log Suite Teardown
    DefaultTestCaseTeardown
    Log Subscriptions Delete  ${audit_log_name}
    Commit Changes
    DefaultTestSuiteTeardown 

Do Tvh1517602c Teardown
    Spam Quarantine SlBl Disable
    Spam Quarantine Disable
    Commit Changes

Do Tvh1517604c Teardown
    Pvo Quarantines Disable
    Commit Changes

Do Tvh1517605c Teardown
    Centralized Email Reporting Disable
    Centralized Email Message Tracking Disable
    Commit Changes

Do Tvh1517609c Teardown
    Centralized Web Configuration Manager Disable
    Centralized Upgrade Manager Disable
    Commit Changes

Do Tvh1517610c Teardown
   Centralized Web Reporting Disable
   Commit Changes

Do Tvh1515377c Teardown
    Alerts Delete Recipient  ${TESTUSER}@${CLIENT_HOSTNAME}
    Commit Changes
    
Do Tvh1515378c Teardown
    Log Subscriptions Edit Log  
    ...  ${log_name}
    ...  log_size=95M
    Commit Changes

Do Tvh1515381c Teardown
    Launch Dut Browser
    Log Into Dut
    Edit SSL Configuration Settings
    ...  ${service}
    ...  TLS v1.0
    ...  enable=${True}
    Run Keyword And Ignore Error  Commit Changes
    Wait Until Dut Is Accessible  timeout=900  wait_for_ports=22,80,443
    Close Browser

Do Tvh1515382c Teardown
    Network Access Edit Settings  30
    Commit Changes

Do Tvh1515383c Teardown
   Run On DUT  rm -rf ${CONFIG_DIR}/${config_filename}

Do Tvh1515384c Teardown
    ${settings}=  Create Dictionary
    ...  AsyncOS Upgrade Notification  ${True}
    System Upgrade Edit Notification Settings  ${settings}    
    Commit Changes

Do Tvh1515385c Teardown
    Update Settings Edit Settings
    ...  auto_update=${True}
    Commit Changes

Do Tvh1515386c Teardown
    Edit General Settings  edit_analytics=${True}
    Commit Changes

Do Tvh1515387c Teardown
    Disk Management Edit Quotas  spam_quarantine=32
    Spam Quarantine Disable
    Commit Changes

Do Tvh1515388c Teardown
    Time Settings Edit Settings  ntp  delete_ntp_server=True
    Commit Changes

Do Tvh1515389c Teardown
    Feature Key Settings Edit  autocheck=${True}
    Commit Changes

Do Tvh1517617c Teardown
    SmaGuiLibrary.Return Addresses Edit Other  hostname=${EMPTY}
    Commit Changes

Do Tvh1517618c Teardown
    Users Delete User  ${user_name}
    Commit Changes

Do Tvh1517619c Teardown
    SmaGuiLibrary.User Roles Email Role Delete  ${role}
    Commit Changes

Do Tvh1517620c Teardown
    LDAP Delete Server Profile  ${ldap_server_profile}
    Commit Changes    

Do Tvh1517621c Teardown
    SAML Delete SP IDP  sp_name=${TEST_SP_PROFILE_EDIT}  idp_name=${TEST_IDP_PROFILE_EDIT}
    Commit Changes

Do Tvh1517623c Teardown
    Time Zone Edit  America  United States  Los_Angeles
    Commit Changes

Do Tvh1517629c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    DefaultTestCaseSetup
    Pvo Quarantines Enable
    Commit Changes

Do Tvh1517629c Teardown
    Pvo Quarantines Disable
    Commit Changes

Do Tvh1517614c Teardown
    Smtp Routes Delete  ${recv_domain}
    Commit Changes

Do Tvh1517615c Teardown
    DNS Delete Alternate Servers  ${dns_ip}  dns=Root
    Commit Changes

Do Tvh1517616c Teardown
    Routing Delete Routes  ${route_name}
    Commit Changes

Do Tvh1517612c Teardown
    IP Interfaces Edit  Management   ftp_service=${False}
    Commit Changes

*** Test Cases ***
Tvh1517602c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Enable or configure Spam Quarantine and SLBL enable \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517602
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517603
    [Tags]  Tvh1517602c  Tvh1517603c  srts
    [Setup]  DefaultTestCaseSetup 
    [Teardown]  Do Tvh1517602c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}

    Spam Quarantine Enable
    Spam Quarantine SlBl Enable
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Enable or Disable on-box EUQ. >= 1
    ...  Enable or Disable Safe/Block lists in End-User Quarantine. >= 1

Tvh1517604c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Enable or cofigure Policy, Virus and Outbreak Quarantines \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517604
    [Tags]  Tvh1517604c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517604c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    
    Pvo Quarantines Enable
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Listeners Configuration. >= 1
    ...  Recipient Access Table for the listener. >= 1
    ...  Enable or Disable Centralized System Quarantine. >= 1

Tvh1517605c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Enable or cofigure Centralized Email Reporting Service 
    ...  and Centralized Email Message Tracking Enable \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517605 \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517606
    [Tags]  Tvh1517605c  Tvh1517606c  Tvh1517607c  Tvh1517608c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517605c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Enable or Disable Centralized Reporting. >= 1
    ...  Enable or Disable Centralized Message Tracking. >= 1

Tvh1517609c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Enable or cofigure Centralized Web Configuration Manager
    ...  Centralized Web Reporting Service and Centralized Upgrade Manager \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517609 \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517611
    [Tags]  Tvh1517609c  Tvh1517611c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517609c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
 
    Centralized Web Configuration Manager Enable
    Centralized Upgrade Manager Enable  
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Enable or Disable ICCM. >= 1
    ...  Whether centralized upgrade manager is enabled. >= 1

Tvh1515377c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> System health \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515377
    [Tags]  Tvh1515377c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515377c Teardown
    
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Alerts Add Recipient  ${TESTUSER}@${CLIENT_HOSTNAME}  all-all
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Email address configuration to send alert messages to. >= 1

Tvh1515378c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Log Subscriptions \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515378
    [Tags]  Tvh1515378c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515378c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${log_name}  mail_logs
    Roll Over Now  ${audit_log_name}
    Log Subscriptions Edit Log  
    ...  ${log_name}
    ...  log_size=10M
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Log subscriptions for the mail server. >= 1

Tvh1515382c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Network Access \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515382
    [Tags]  Tvh1515382c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515382c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Network Access Edit Settings  60
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Number of seconds before the Web UI session times out. >= 1

Tvh1515383c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Configuration File \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515383
    [Tags]  Tvh1515383c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515383c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}

    ${config_filename}=  Configuration File Save Config  mask_passwd=${True}
    Set Test Variable  ${config_filename}
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Appliance: ${DUT}, Interaction Mode: GUI, User: admin, .* Location: \\/system_administration\\/configuration_file, Event: User visited the web page. >= 1

Tvh1515385c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Update Settings \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515385
    [Tags]  Tvh1515385c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515385c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Update Settings Edit Settings
    ...  auto_update=${False}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Time interval to check and fetch new update manifests \\(in seconds\\). >= 1

Tvh1515386c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> General Settings \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515386
    [Tags]  Tvh1515386c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515386c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Edit General Settings  edit_analytics=${False}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Enable or Disable Usage Analytics. >= 1

Tvh1515387c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Data disk Management \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515387
    [Tags]  Tvh1515387c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515387c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Spam Quarantine Enable
    Disk Management Edit Quotas  spam_quarantine=2
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  The database total size for EUQ in bytes. >= 1

Tvh1515388c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Time Settings \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515388
    [Tags]  Tvh1515388c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515388c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${ntp}  time.sco.cisco.com,time.ironport.com
    Roll Over Now  ${audit_log_name}
    Time Settings Edit Settings  ntp  ntp_servers=${ntp}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  List of servers used to acquire the current time. >= 1

Tvh1515389c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Feature Key Settings \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515389
    [Tags]  Tvh1515389c  Tvh1517624c  srts  invalid_not_applicable_for_smart_license
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515389c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Feature Key Settings Edit  autocheck=${False}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Determines whether or not to automatically check for feature keys. >= 1
   
Tvh1517617c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Return Address \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517617
    [Tags]  Tvh1517617c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517617c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    SmaGuiLibrary.Return Addresses Edit Other  hostname=myhost.com
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  The email address from which all Other mails will be addressed. >= 1

Tvh1517618c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Users \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517618
    [Tags]  Tvh1517618c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517618c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${user_name}  guest 
    Roll Over Now  ${audit_log_name}
    Users Add User  ${user_name}  GuestUser  ${DUT_ADMIN_SSW_PASSWORD}  ${sma_user_roles.GUEST}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Local User Account Settings. >= 1
    ...  List of local users and their account settings. >= 1

Tvh1517619c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> User Roles \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517619
    [Tags]  Tvh1517619c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517619c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${role}  emailrole
    Roll Over Now  ${audit_log_name}
    SmaGuiLibrary.User Roles Email Role Add  ${role}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  List of custom user roles. >= 1

Tvh1517620c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> LDAP \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517620
    [Tags]  Tvh1517620c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517620c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${ldap_server_profile}  ldapprofile
    Roll Over Now  ${audit_log_name}
    LDAP Add Server Profile  ${ldap_server_profile}  ${LDAP_AUTH_SERVER}
    ...  server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  LDAP Server Configuration. >= 1

Tvh1517621c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> SAML \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517621
    [Tags]  Tvh1517621c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517621c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Profile Name                    ${TEST_SP_PROFILE_EDIT}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  Assertion Consumer URL             http://${SMA}
    ...  SP Certificate                     ${CERT_FILE}
    ...  Private Key                        ${CERT_KEY}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Sign Requests                      ${SIGN_REQUEST}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  IDP Profile Name                   ${TEST_IDP_PROFILE_EDIT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_METADATA}
    SAML Add SP And IDP  ${TEST_SP_PROFILE_EDIT}  ${TEST_IDP_PROFILE_EDIT}  ${settings}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Identity Provider medatada information for SAML. >= 1
    ...  Service Provider information for SAML. >= 1

Tvh1517623c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> time zone \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517623
    [Tags]  Tvh1517623c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517623c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Time Zone Edit  Asia  India  Kolkata
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Timezone for the system. >= 1

Tvh1517625c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Feature Keys \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517625
    [Tags]  Tvh1517625c  srts  invalid_not_applicable_for_smart_license
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Feature Keys Check New Keys
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Appliance: ${DUT}, Interaction Mode: GUI, User: admin, .* Location: \\/system_administration\\/feature_keys\\/feature_keys, Event: User visited the web page. >= 1

Tvh1517626c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> Smart Software Licensing \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517626
    [Tags]  Tvh1517626c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    Run Keyword And Ignore Error  Smart License Get Status Details
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Appliance: ${DUT}, Interaction Mode: GUI, User: admin, .* Location: \\/system_administration\\/feature_keys\\/smart_licensing, Event: User visited the web page. >= 1

Tvh1517629c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration Email -
    ...  -> Message quarantine -> add Policy, Virus and Outbreak Quarantines \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517629
    [Tags]  Tvh1517629c  srts
    [Setup]  Do Tvh1517629c Setup
    [Teardown]  Do Tvh1517629c Teardown

    Roll Over Now  ${audit_log_name}
    Add Policy Quarantine
    ...  name=upq
    ...  retention_period=20
    ...  retention_unit=Hours
    ...  default_action=delete
    Commit Changes 
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  System Quarantines Configuration >= 1   

Tvh1517612c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration
    ...  Network Settings -> Edit Management Interface \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517612
    [Tags]  Tvh1517612c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517612c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set TestVariable  ${data_01}  data1
    Roll Over Now  ${audit_log_name}
    IP Interfaces Edit  Management   ftp_service=${True}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Defines the IP address interfaces of the system. >= 1


Tvh1517614c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration
    ...  Network Settings -> Add SMTP ROutes \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517613
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517614 
    [Tags]  Tvh1517614c  Tvh1517613c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517614c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${recv_domain}  ironport.com
    Set Test Variable  ${dest_hosts}  smtp.cisco.com
    Roll Over Now  ${audit_log_name}    
    Smtp Routes Add  ${recv_domain}  ${dest_hosts}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  The SMTP Route Map Configuration. >= 1

Tvh1517615c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration
    ...  Network Settings -> DNS - edit Settings \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517615
    [Tags]  Tvh1517615c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517615c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${dns_ip}  10.0.0.3
    Roll Over Now  ${audit_log_name}
    DNS Add Alternate Server
    ...  dns=Root
    ...  domains=example.com
    ...  FQDN=dns.example.com
    ...  dns_ip=${dns_ip}
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Alternate DNS servers override settings for Internet Root DNS Server. >= 1

Tvh1517616c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration
    ...  Network Settings -> Routing -> add routing \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1517616
    [Tags]  Tvh1517616c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1517616c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set TestVariable  ${route_name}  new_route
    Roll Over Now  ${audit_log_name}
    Routing Add Route  ${route_name}
    ...  192.168.20.0/24
    ...  10.0.0.2
    Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Manually configured IP routing table. >= 1


Tvh1515381c
    [Documentation]
    ...  Verify that audit log is populated for editing of configuration System
    ...  Administration -> SSL Configuration \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1515381
    [Tags]  Tvh1515381c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1515381c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${service}  Appliance Management Web User Interface
    Roll Over Now  ${audit_log_name}
    Launch Dut Browser
    Log Into Dut
    Edit SSL Configuration Settings
    ...  ${service}
    ...  TLS v1.0
    ...  enable=${False}
    Run Keyword And Ignore Error  Commit Changes
    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  SSL method for GUI HTTPS >= 1
    ...  List of Secure protocol versions supported by GUI >= 1
    Close Browser


