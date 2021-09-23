*** Settings ***
Resource     sma/global_sma.txt

Suite Setup     Open Id Suite Setup
Suite Teardown  DefaultTestSuiteTeardown

*** Keywords  ***
Open Id Suite Setup
    global_sma.DefaultTestSuiteSetup
    ${audience}=  Create List  add::${OIDC_AUIDENCE}
    ${idp_role_to_appliance_role_map}=  Create Dictionary
    ...  add::managers  Administrator
    ${settings}=  Create Dictionary
    ...  Metadata URL    ${OIDC_METADATA_URL}
    ...  Issuer          ${OIDC_ISSUER}
    ...  Audience        ${audience}
    ...  Claim for Role  role
    ...  Identity Provider Role to Appliance Role Mappings  ${idp_role_to_appliance_role_map}
    Oidc Configuration Edit Settings  ${settings}
    Commit Changes

Copy Configuration File To Dut
    [Arguments]  ${config_file_path}  ${config_file_name}
    ${config_file}=  Join Path  ${config_file_path}  ${config_file_name}
    SCP
    ...  to_user=${RTESTUSER}
    ...  to_password=${RTESTUSER_PASSWORD}
    ...  from_location=${config_file}
    ...  to_location=${CONFIG_DIR}
    ...  to_host=${SMA}

Do Tvh1511742c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test variable   ${NEW_USER_ROLE_NAME}  Log_Access
    DefaultTestCaseSetup
    User Roles Email Role Add  ${NEW_USER_ROLE_NAME}  logsubscription_access=${True}
    Commit Changes

Do Tvh1511742c Teardown
    ${idp_role_to_appliance_role_map}=  Create Dictionary
    ...  delete::log_collector  ${NEW_USER_ROLE_NAME}
    ${settings}=  Create Dictionary
        ...  Identity Provider Role to Appliance Role Mappings  ${idp_role_to_appliance_role_map}
    Oidc Configuration Edit Settings  ${settings}
    User Roles Email Role Delete  ${NEW_USER_ROLE_NAME}
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh1512863c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    DefaultTestCaseSetup

Do Tvh1512876c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut
    DefaultTestCaseSetup
    ${config_filename}=  Configuration File Save Config
    Set Test Variable  ${config_filename}

Do Tvh1512876c Teardown
    Configuration File Load Config   ${config_filename}
    Run On DUT  rm -rf ${CONFIG_DIR}/${config_filename}
    DefaultTestCaseTeardown
    SMAGuiLibrary.Close Browser

Do Tvh1512877c Setup
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

Do Tvh1512877c Teardown
    Load License From File
    Copy Configuration File To Dut
    ...  %{HOME}/Downloads/
    ...  ${config_filename}

    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut
    Configuration File Load Config   ${config_filename}
    Commit Changes
    Configure SSL For GUI
    SMAGuiLibrary.Close Browser
    Remove File  %{HOME}/Downloads/${config_filename}
    Run On DUT  rm -rf ${CONFIG_DIR}/${config_filename}
    DefaultTestCaseTeardown


*** Test Cases ***
Tvh1511739c
    [Documentation]
    ...  Enable OIDC Configuration \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1511739 \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1511738
    [Tags]   Tvh1511739c  Tvh1511738c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${settings}=  Create Dictionary
    ...  Metadata URL    ${OIDC_METADATA_URL}
    ...  Issuer          ${OIDC_ISSUER}
    ...  Claim for Role  role
    Oidc Configuration Edit Settings  ${settings}
    Commit Changes

Tvh1511740c
    [Documentation]
    ...  update configuration (change all fields, add / remove mappings) \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1511740 \n
    [Tags]   Tvh1511740c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${audience}=  Create List
    ...  add::https://vrouter.cisco.com/2/
    ...  add::microsoft:identitysever:OAuth Test
    ${settings}=  Create Dictionary
    ...  Audience        ${audience}
    Oidc Configuration Edit Settings  ${settings}
    Commit Changes

    ${audience}=  Create List
    ...  delete::https://vrouter.cisco.com/2/
    ...  delete::microsoft:identitysever:OAuth Test
    ${settings}=  Create Dictionary
    ...  Audience        ${audience}
    Oidc Configuration Edit Settings  ${settings}
    Commit Changes

Tvh1511742c
    [Documentation]
    ...  add log_collector_only custom user role \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1511742 \n
    [Tags]   Tvh1511742c  srts
    [Setup]  Do Tvh1511742c Setup
    [Teardown]  Do Tvh1511742c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${idp_role_to_appliance_role_map}=  Create Dictionary
    ...  add::log_collector  ${NEW_USER_ROLE_NAME}
    ${settings}=  Create Dictionary
        ...  Identity Provider Role to Appliance Role Mappings  ${idp_role_to_appliance_role_map}
    Oidc Configuration Edit Settings  ${settings}
    Commit Changes

Tvh1512863c
    [Documentation]
    ...   Verify OIDC configurations are retained after shutdown 
    ...        and power on of the appliance \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1512863
    [Tags]  Tvh1512863c  srts
    [Setup]  Do Tvh1512863c Setup
    [Teardown]  DefaultTestCaseTeardown

    Go To Oidc Configuration

    Page Should Contain  ${OIDC_METADATA_URL}

    SmaCliLibrary.Reboot
    Wait Until Dut Is Accessible  timeout=900  wait_for_ports=22,80,443
    Restart CLI Session

    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut

    Go To Oidc Configuration

    Page Should Contain  ${OIDC_METADATA_URL}

Tvh1512876c
    [Documentation]
    ...   Verify OIDC configurations are removed after resetconfig 
    ...   and then user is allowed to enter those values 
    ...   again and check functionality \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1512876
    [Tags]  Tvh1512876c  srts
    [Setup]  Do Tvh1512876c Setup
    [Teardown]  Do Tvh1512876c Teardown

    Suspend  delay=5
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}

    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut

    Go To Oidc Configuration

    Set Test Variable  ${oidc_text}  You have not configured OpenID Connect to access the AsyncOS API.
    Page Should Contain  ${oidc_text}

Tvh1512877c
    [Documentation]
    ...   Verify OIDC configurations are removed after diagnostic >> reload and then
    ...   user is allowed to enter those values again and check functionality \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1512877
    [Tags]  Tvh1512877c  srts  reload  reset
    [Setup]  Do Tvh1512877c Setup
    [Teardown]  Do Tvh1512877c Teardown

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

    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut

    Go To Oidc Configuration

    Set Test Variable  ${oidc_text}  You have not configured OpenID Connect to access the AsyncOS API.
    Page Should Contain  ${oidc_text}

