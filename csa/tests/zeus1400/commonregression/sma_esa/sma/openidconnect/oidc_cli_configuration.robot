*** Settings ***
Resource     esa/logs_parsing_snippets.txt
Resource     sma/global_sma.txt
Resource     regression.txt
Variables    sma/saml_constants.py

Suite Setup     Open Id Suite Setup
Suite Teardown  Open Id Suite Teardown

*** Keywords ***
Open Id Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup
    ${role_mapping}=  Create Dictionary
    ...  logs_admin  Administrators
    Oidc Config Setup Config
    ...  metadata_url=${OIDC_METADATA_URL}
    ...  issuer=${OIDC_ISSUER}
    ...  role=role
    ...  audience=${OIDC_AUIDENCE}
    ...  create_group_mappings=Y
    ...  role_mappings=${role_mapping}
    Commit

Open Id Suite Teardown
    Oidc Config Delete Config
    ...  remove_oidc_config=Yes
    Commit
    DefaultTestSuiteTeardown

Copy Configuration File To Dut
    [Arguments]  ${config_file_path}  ${config_file_name}
    ${config_file}=  Join Path  ${config_file_path}  ${config_file_name}
    SCP
    ...  to_user=${RTESTUSER}
    ...  to_password=${RTESTUSER_PASSWORD}
    ...  from_location=${config_file}
    ...  to_location=${CONFIG_DIR}
    ...  to_host=${SMA}

Do Tvh1511748c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test variable   ${NEW_USER_ROLE_NAME}  Log_Access
    DefaultTestCaseSetup
    User Roles Email Role Add  ${NEW_USER_ROLE_NAME}  logsubscription_access=${True}
    Commit Changes
    ${role_mapping}=  Create Dictionary
    ...  log_collector  ${NEW_USER_ROLE_NAME}
    Set Test Variable  ${role_mapping}

Do Tvh1511748c Teardown
    Oidc Config Setup Mapping Delete
    ...  role_mappings=${role_mapping}
    Commit
    User Roles Email Role Delete  ${NEW_USER_ROLE_NAME}
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh1540303c Teardown
    Oidc Config Edit Config
    ...  audience=${OIDC_AUIDENCE}
    Commit
    DefaultTestCaseTeardown

Do Tvh1540339c Teardown
    Oidc Config Setup Mapping Delete
    ...  role_mappings=${role_mapping}
    Commit
    DefaultTestCaseTeardown

Do Tvh1511746c Teardown
    Oidc Config Setup Mapping Delete
    ...  role_mappings=${role_mapping}
    Commit
    ${mappings}=  Oidc Config Setup Mapping Print
    List Should Not Contain Value  ${mappings}  2. ${role1} -> Guests
    List Should Not Contain Value  ${mappings}  3. ${role2} -> Technicians

    Oidc Config Edit Config
    ...  metadata_url=${OIDC_METADATA_URL}
    ...  issuer=${OIDC_ISSUER}
    ...  role=role
    ...  audience=${OIDC_AUIDENCE}
    Commit

    DefaultTestCaseTeardown

Do Tvh1540309c Teardown
    Restart CLI Session
    ${role_mapping}=  Create Dictionary
    ...  logs_admin  Administrators
    Oidc Config Setup Config
    ...  metadata_url=${OIDC_METADATA_URL}
    ...  issuer=${OIDC_ISSUER}
    ...  role=role
    ...  audience=${OIDC_AUIDENCE}
    ...  create_group_mappings=Y
    ...  role_mappings=${role_mapping}
    Commit
    Log Subscriptions Delete  ${audit_log_name}
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh1540341c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut
    DefaultTestCaseSetup
    ${config_filename}=  Configuration File Save Config  mask_passwd=${False}
    Set Test Variable  ${config_filename}

Do Tvh1540341c Teardown
    Configure SSL For GUI
    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut
    Configuration File Load Config   ${config_filename}
    Commit Changes
    Run On DUT  rm -rf ${CONFIG_DIR}/${config_filename}
    DefaultTestCaseTeardown
    SMAGuiLibrary.Close Browser

Do Tvh1540343c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut
    DefaultTestCaseSetup
    Interface Config Edit  Management  SSH=yes
    Commit
    ${config_filename}=  Configuration File Save Config   mask_passwd=${False}
    Set Test Variable  ${config_filename}
    Copy File From Dut To Remote Machine
    ...  from_loc=${CONFIG_DIR}/${config_filename}
    ...  remote_host=${CLIENT}
    ...  to_loc=%{HOME}/Downloads/
    ...  to_user=${TESTUSER}
    ...  to_password=${TESTUSER_PASSWORD}
    SMAGuiLibrary.Close Browser

Do Tvh1540343c Teardown
    Load License From File
    Copy Configuration File To Dut
    ...  %{HOME}/Downloads/
    ...  ${config_filename}
    Configure SSL For GUI
    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut
    Configuration File Load Config   ${config_filename}
    Commit Changes
    SMAGuiLibrary.Close Browser
    Remove File  %{HOME}/Downloads/${config_filename}
    Run On DUT  rm -rf ${CONFIG_DIR}/${config_filename}
    DefaultTestCaseTeardown

*** Test Cases ***

Tvh1511748c
    [Documentation]
    ...  add log_collector_only custom user role \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1511748 \n
    [Tags]   Tvh1511748c  srts
    [Setup]  Do Tvh1511748c Setup
    [Teardown]  Do Tvh1511748c Teardown

    Oidc Config Setup Mapping New
    ...  role_mappings=${role_mapping}
    Commit

Tvh1540305c
    [Documentation]
    ...  Verify configuring invalid value for OIDC parameters
    ...  and make sure the validation is thrown properly. \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1540305
    [Tags]   Tvh1540305c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Run Keyword And Expect Error  *IafCliValueError*  Oidc Config Edit Config  metadata_url=https://

Tvh1540303c
    [Documentation]
    ...  Verify adding more Audience OIDC parameter
    ...  and do commit changes. \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1540303
    [Tags]   Tvh1540303c  Tvh1540307c  Tvh1511749c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1540303c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${audience1}  https://audience1-vrouter.cisco.com
    Set Test Variable  ${audience2}  https://audience2-vrouter.cisco.com

    Oidc Config Edit Config
    ...  audience=${audience1},${audience2}
    Commit
    Go To Oidc Configuration
    Page Should Contain  ${audience1}
    Page Should Contain  ${audience2}

Tvh1511746c
    [Documentation]
    ...  Verify that user is able to update configuration (change all fields,
    ...   add / remove mappings)
    ...  http://tims.cisco.com/view-entity.cmd?ent=1511746c
    [Tags]   Tvh1511746c  Tvh1540304c  Tvh1540308c  Tvh1540340c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1511746c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${role1}  logs_admin3
    Set Test Variable  ${role2}  logs_guest3
    Set Test Variable  ${new_meta_data}  https://new.plugin.com/adfs/.well-known/openid-configuration
    Set Test Variable  ${new_issuer}  http://new.plugin.com/adfs/services/trust
    Set Test Variable  ${new_role}  newrole
    Set Test Variable  ${new_audience}  https://new-vrouter.cisco.com

    ${role_mapping}=  Create Dictionary
    ...  ${role1}  Guests
    ...  ${role2}  Technicians
    Set Test Variable  ${role_mapping}
    Oidc Config Edit Config
    ...  metadata_url=${new_meta_data}
    ...  issuer=${new_issuer}
    ...  role=${new_role}
    ...  audience=${new_audience}
    Commit
    Go To Oidc Configuration
    Page Should Contain  ${new_meta_data}
    Page Should Contain  ${new_issuer}
    Page Should Contain  ${new_role}
    Page Should Contain  ${new_audience}

    Oidc Config Setup Mapping New
    ...  role_mappings=${role_mapping}
    Commit
    ${mappings}=  Oidc Config Setup Mapping Print
    List Should Contain Value  ${mappings}  2. ${role1} -> Guests
    List Should Contain Value  ${mappings}  3. ${role2} -> Technicians

Tvh1540309c
    [Documentation]
    ...  Verify validation is thrown if user tries to
    ...  submit without single Audience and Custom Role parameters. \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1540309
    [Tags]   Tvh1540309c  Tvh1542943c  Tvh1511747c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1540309c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${audit_log_name}  audit_logs
    Log Subscriptions Add Log
    ...  Audit Logs
    ...  ${audit_log_name}
    ...  filename=${audit_log_name}
    ...  log_size=5M
    Commit Changes

    Roll Over Now  ${audit_log_name}

    Oidc Config Delete Config
    ...  remove_oidc_config=Yes
    Commit

    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Appliance: ${DUT}, Interaction Mode: CLI, .* Event: User input was 'oidcconfig' >= 1
    ...  Appliance: ${DUT}, Interaction Mode: CLI, .* Event: User input was 'DELETE' >= 1

    ${role_mapping}=  Create Dictionary
    ...  logs_admin  Administrators
    Run Keyword And Expect Error  *Please enter a value*  Oidc Config Setup Config
    ...  metadata_url=${OIDC_METADATA_URL}
    ...  issuer=${OIDC_ISSUER}
    ...  role=role
    ...  audience=
    ...  create_group_mappings=Y
    ...  role_mappings=${role_mapping}

    Run Keyword And Expect Error  *unexpected EOF while parsing*  Oidc Config Setup Config
    ...  metadata_url=${OIDC_METADATA_URL}
    ...  issuer=${OIDC_ISSUER}
    ...  role=role
    ...  audience=${OIDC_AUIDENCE}
    ...  create_group_mappings=Y
    ...  role_mappings=

Tvh1540339c
    [Documentation]
    ...  Verify modifying the existing external group mapping in OIDC via CLI \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1540339
    [Tags]   Tvh1540339c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1540339c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${role1}  logs_readonly

    ${role_mapping}=  Create Dictionary
    ...  ${role1}  Read-Only Operators
    Set Test Variable  ${role_mapping}
    Oidc Config Setup Mapping New
    ...  role_mappings=${role_mapping}
    Commit
    ${mappings}=  Oidc Config Setup Mapping Print
    List Should Contain Value  ${mappings}  2. ${role1} -> Read-Only Operators
    ${role_mapping}=  Create Dictionary
    ...  ${role1}  Help Desk Users
    Set Test Variable  ${role_mapping}
    Oidc Config Setup Mapping Edit
    ...  role_mappings=${role_mapping}
    Commit
    ${mappings}=  Oidc Config Setup Mapping Print
    List Should Contain Value  ${mappings}  2. ${role1} -> Help Desk Users


Tvh1540341c
    [Documentation]
    ...   Verify after resetconfig all config done via CLI for OIDC gets removed \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1540341
    [Tags]  Tvh1540341c  srts
    [Setup]  Do Tvh1540341c Setup
    [Teardown]  Do Tvh1540341c Teardown

    Suspend  delay=5
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}

    Start CLI Session If Not Open

    Run Keyword And Expect Error
    ...  *IafCliValueError: DELETE*
    ...  Oidc Config Delete Config
    ...  remove_oidc_config=Yes

Tvh1540343c
    [Documentation]
    ...  Verify after diagnostic >> reload oidc parameters configured via CLI
    ...  gets removed
    ...   http://tims.cisco.com/view-entity.cmd?ent=1540343
    [Tags]  Tvh1540343c  srts  reload  reset
    [Setup]  Do Tvh1540343c Setup
    [Teardown]  Do Tvh1540343c Teardown

    Diagnostic Reload  confirm=yes   wipedata=no
    Wait Until DUT Is Accessible

    Wait Until Keyword Succeeds  10 minutes  15 seconds
    ...  Start CLI Session if Not Open

    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}

    Start CLI Session If Not Open

    Run Keyword And Expect Error
    ...  *IafCliValueError: DELETE*
    ...  Oidc Config Delete Config
    ...  remove_oidc_config=Yes

