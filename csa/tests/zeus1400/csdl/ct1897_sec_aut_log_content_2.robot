*** Settings ***
Resource     sma/csdlresource.txt
Variables    sma/saml_constants.py

Force Tags         csdl
Suite Setup        Initialize Suite
Suite Teardown     Finalize Suite


*** Variables ***
${USER_NAME}=                testuser
${PASSWORD}=                 Fdsag12$
${CUSTOM_USER_ROLE}=         tester
${CUSTOM_USER_PRIVILEGE}=    delegatedadmin
${ADMIN_USER_ROLE}=          Administrator
${ADMIN_USER_PRIVILEGE}=     admin
@{USER_NAMES_LIST}=          testuser1  testuser2  testuser3  testuser4
@{ROLES_LIST}=               Administrator  Operator  ${CUSTOM_USER_ROLE}  Technician
@{PRIVILEGES_LIST}=          admin  operators  ${CUSTOM_USER_PRIVILEGE}  technician  
@{EUQ_ROLES_LIST}=           Operator  Guest  Read-Only Operator  Help Desk User
@{EUQ_PRIVILEGES_LIST}=      operators  guest  readonly  helpdesk                                                       
@{NGUI_ROLES_LIST}=          Administrator  Operator  Guest  Read-Only Operator 
@{NGUI_PRIVILEGES_LIST}=     Administrator  Operator  Guest  Read-Only Operator 
${LOG_TYPE}=                 API Logs
${API_LOGS}=                 api
${API_PATH} =                /data/pub/${API_LOGS}/${API_LOGS}.current


*** Keywords ***
Initialize Suite
    CSDL Suite Setup 
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    Log Into Dut
    Log Config New  name=${API_LOGS}
    ...  log_file=${LOG_TYPE}  filename=${API_LOGS} 
    Commit
    User Roles Email Role Add  ${CUSTOM_USER_ROLE}
    Commit Changes

Finalize Suite
    Restart Cli Session
    Log Config Delete  ${API_LOGS}
    Commit
    User Roles Email Role Delete  ${CUSTOM_USER_ROLE}
    Commit Changes
    CSDL Suite Teardown

Add New User In Gui
    [Arguments]  ${user_name}  ${role}
    Users Add User  ${user_name}  ${user_name}  ${PASSWORD}  ${role}
    Commit Changes

Add LDAP Server With External Auth Query
    LDAP Add Server Profile  ${LDAP_USER}  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_BINDDN}:${LDAP_PASSWORD}
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit External Authentication Queries  ${LDAP_USER}  ${LDAP_AUTH_SERVER}.externalauth
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Commit Changes

Add LDAP Server With Isq End User Authentication Query
    LDAP Add Server Profile  ${LDAP_AUTH_SERVER}  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_BINDDN}:${LDAP_PASSWORD}
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit Isq End User Authentication Query
    ...  ${LDAP_AUTH_SERVER}
    ...  ${LDAP_AUTH_SERVER}.isq_auth
    ...  (uid={u})
    ...  mail
    ...  ${True}
    Commit Changes

Edit External Auth For LDAP
    [Arguments]  ${role}
    Users Edit External Authentication  LDAP  ldap_query=${LDAP_AUTH_SERVER}.externalauth    
    ...  auth_cache_timeout=200  group_mapping=${LDAP_SMA_USER_GROUP}:${role}  
    ...  response_timeout=6
    Commit Changes

Edit External Auth For Radius 
    [Arguments]  ${role}
    Users Edit External Authentication  RADIUS
    ...  radius_servers=${RADIUS_SERVER}:${RADIUS_PORT}:${RADIUS_SECRET}:10
    ...  auth_cache_timeout=20
    ...  group_mapping=${RADIUS_CLASS_ATTRIBUTE}:${role}
    Commit Changes

Enable Spam Quarantine
    Spam Quarantine Enable  interface=Management  port=6500 
    Commit Changes
    Spam Quarantine Edit 
    ...  local_users=${USER_NAME}
    ...  ldap_groups=Help Desk Users, Guests, Read-Only Operators,Operators 
    Spam Quarantine Edit EndUser Access 
    ...  end_user_access_enable=${True} 
    ...  end_user_auth=LDAP
    Commit Changes

Create SAML Users
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
    SAML Add Sp And Idp  ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes

Edit SAML External Authentication For Customer
    [Arguments]  ${role}
    Users Edit External Authentication  SAML 
    ...  extauth_attribute_name_map= 
    ...  group_mapping= ${SAML_GROUP_Azure}:${role}
    Commit Changes

Verify SAML Users Privileges Are Displayed In GUI Logs
    [Arguments]  ${privilege}
    Log Out Of Dut
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}
    Log Out Of Dut

    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}                                                                     
    ...  SourceIP:(.)* Username:${SAML_AZUR_USER} Privilege:${privilege} (.)* The HTTPS session has been established successfully. >= 1
    Close Browser
    Launch Dut Browser
    Log Into Dut

Verify NGUI Users Privileges Are Displayed In API Logs 
    [Arguments]  ${user_name}  ${password}  ${privilege}
    Close Browser
    SMANGGuiLibrary.Launch Dut Browser
    SMANGGuiLibrary.Login Into Dut  ${user_name}  ${password}
    SMANGGuiLibrary.Close Browser

    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${API_PATH}                                                                         
    ...  Login: JWT Token Generated for user ${user_name} >= 1
    ...  Checking access for user ${user_name} role ${privilege} >= 1
    Launch Dut Browser
    Log Into Dut

Verify Spam Quarantine Users Privileges Are Displayed In Authentication Logs
    [Arguments]  ${user_name}  ${password}  ${privilege}
    Go To  https://${SMA}:83
    Login to SMA via GUI  ${user_name}  ${password}  

    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=authentication
    ...  Info: Authentication OK, user ${user_name} with privilege ${privilege} logged in to Spam Quarantine >= 1  
    Go To  https://${SMA}

Do Common Setup
    DefaultTestCaseSetup
    Roll Over Now  logname=authentication

Do Common Teardown
    Restart Cli Session
    FOR  ${user_name}  IN  @{USER_NAMES_LIST}
        Users Delete User  ${user_name}
        Commit Changes
    END
    DefaultTestCaseTeardown

Do Tvh1557736c And Tvh1557737c Teardown
    Users Disable External Authentication
    LDAP Delete Server Profile  ${LDAP_USER}
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh1557738c And Tvh1557739c Teardown
    Users Disable External Authentication
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh1557740c Setup
    DefaultTestCaseSetup
    Roll Over Now  logname=gui_logs                                           
    Create SAML Users

Do Tvh1557740c Teardown
    Users Disable External Authentication
    SAML Delete Sp Idp  sp_name=${TEST_SP_PROFILE}  idp_name=${TEST_IDP_PROFILE}
    Commit Changes
    DefaultTestCaseTeardown 

Do Tvh1558638c Setup
    DefaultTestCaseSetup
    Roll Over Now  logname=${API_LOGS}                                           
    Add LDAP Server With External Auth Query
    Add New User In Gui  ${USER_NAME}  Guest

Do Tvh1558638c Teardown
    Users Delete User  ${USER_NAME}
    Users Disable External Authentication
    LDAP Delete Server Profile  ${LDAP_USER}
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh1558639c Setup
    DefaultTestCaseSetup
    Roll Over Now  logname=authentication
    Add LDAP Server With Isq End User Authentication Query
    Add LDAP Server With External Auth Query
    Edit External Auth For LDAP  ${ADMIN_USER_ROLE}
    Add New User In Gui  ${USER_NAME}  Guest
    Enable Spam Quarantine 

Do Tvh1558639c Teardown
    Users Delete User  ${USER_NAME}
    Users Disable External Authentication
    LDAP Delete Server Profile  ${LDAP_USER}
    LDAP Delete Server Profile  ${LDAP_AUTH_SERVER}
    Spam Quarantine Disable
    Commit Changes
    DefaultTestCaseTeardown   


*** Test Cases ***
Tvh1557732c
    [Documentation]  Verify Local users privilages are added into authentication logs while login to GUI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557732c
    ...  Verify Custom users privilages are added into authentication logs while login to GUI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557734c
    [Tags]      Tvh1557732c  Tvh1557734c  SEC-LOG-CONTENT-2
    [Setup]     Do Common Setup
    [Teardown]  Do Common Teardown

    FOR  ${user_name}  ${role}  ${privilege}  IN ZIP  ${USER_NAMES_LIST}  ${ROLES_LIST}  ${PRIVILEGES_LIST}
        Add New User In Gui  ${user_name}  ${role}

        Login to SMA via GUI  ${user_name}  ${PASSWORD}  

        Verify And Wait For Log Records
        ...  wait_time=180 seconds
        ...  retry_time=10 seconds
        ...  search_path=authentication
        ...  User ${user_name} (.)* was authenticated successfully with privilege ${privilege} using an HTTPS connection. == 1
        Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    END

Tvh1557733c
    [Documentation]  Verify Local users privilages are added into authentication logs while login to CLI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557733c
    ...  Verify Custom users privilages are added into authentication logs while login to CLI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557735c
    [Tags]      Tvh1557733c  Tvh1557735c  SEC-LOG-CONTENT-2
    [Setup]     Do Common Setup
    [Teardown]  Do Common Teardown

    FOR  ${user_name}  ${role}  ${privilege}  IN ZIP  ${USER_NAMES_LIST}  ${ROLES_LIST}  ${PRIVILEGES_LIST}
        Add New User In Gui  ${user_name}  ${role}
          
        Start Cli Session  ${user_name}  ${PASSWORD} 
    
        Verify And Wait For Log Records
        ...  wait_time=180 seconds
        ...  retry_time=10 seconds
        ...  search_path=authentication
        ...  User ${user_name} (.)* was authenticated successfully with privilege ${privilege} by CLI based authentication using an SSH connection. == 1 
        Close Cli Session
    END

Tvh1557736c
    [Documentation]  Verify LDAP user privilages are added into authentication logs while login to GUI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557736c
    [Tags]      Tvh1557736c  SEC-LOG-CONTENT-2
    [Setup]     Do Common Setup
    [Teardown]  Do Tvh1557736c And Tvh1557737c Teardown

    Add LDAP Server With External Auth Query
    FOR  ${role}  ${privilege}  IN ZIP  ${ROLES_LIST}  ${PRIVILEGES_LIST}
        Edit External Auth For LDAP  ${role} 
         
        Login to SMA via GUI  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}

        Verify And Wait For Log Records
        ...  wait_time=180 seconds
        ...  retry_time=10 seconds
        ...  search_path=authentication
        ...  User ${LDAP_SMA_USER} (.)* was authenticated successfully with privilege ${privilege} using an HTTPS connection. == 1
        Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    END

Tvh1557737c
    [Documentation]  Verify LDAP user privilages are added into authentication logs while login to CLI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557737c
    [Tags]      Tvh1557737c  SEC-LOG-CONTENT-2
    [Setup]     Do Common Setup
    [Teardown]  Do Tvh1557736c And Tvh1557737c Teardown

    Add LDAP Server With External Auth Query
    FOR  ${role}  ${privilege}  IN ZIP  ${ROLES_LIST}  ${PRIVILEGES_LIST}
        Edit External Auth For LDAP  ${role} 
         
        Start Cli Session  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS} 
        
        Verify And Wait For Log Records
        ...  wait_time=180 seconds
        ...  retry_time=10 seconds
        ...  search_path=authentication
        ...  User ${LDAP_SMA_USER} (.)* was authenticated successfully with privilege ${privilege} by CLI based authentication using an SSH connection. == 1
        Close Cli Session 
    END

Tvh1557738c
    [Documentation]  Verify RADIUS user privilages are added into authentication logs while login to GUI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557738c
    [Tags]      Tvh1557738c  SEC-LOG-CONTENT-2
    [Setup]     Do Common Setup
    [Teardown]  Do Tvh1557738c And Tvh1557739c Teardown

    FOR  ${role}  ${privilege}  IN ZIP  ${ROLES_LIST}  ${PRIVILEGES_LIST}
        Edit External Auth For Radius  ${role} 
         
        Login to SMA via GUI  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}      

        Verify And Wait For Log Records
        ...  wait_time=180 seconds
        ...  retry_time=10 seconds
        ...  search_path=authentication
        ...  User ${RADIUS_USER} (.)* was authenticated successfully with privilege ${privilege} using an HTTPS connection. == 1
        Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    END

Tvh1557739c
    [Documentation]  Verify RADIUS user privilages are added into authentication logs while login to CLI. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557739c
    [Tags]      Tvh1557739c  SEC-LOG-CONTENT-2
    [Setup]     Do Common Setup
    [Teardown]  Do Tvh1557738c And Tvh1557739c Teardown

    FOR  ${role}  ${privilege}  IN ZIP  ${ROLES_LIST}  ${PRIVILEGES_LIST}
        Edit External Auth For Radius  ${role} 
         
        Start Cli Session  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
        
        Verify And Wait For Log Records
        ...  wait_time=180 seconds
        ...  retry_time=10 seconds
        ...  search_path=authentication
        ...  User ${RADIUS_USER} (.)* was authenticated successfully with privilege ${privilege} by CLI based authentication using an SSH connection. == 1
        Close Cli Session  
    END

Tvh1557740c
    [Documentation]  Verify SAML user privilages are added into authentication logs. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1557740c
    [Tags]      Tvh1557740c  SEC-LOG-CONTENT-2
    [Setup]     Do Tvh1557740c Setup
    [Teardown]  Do Tvh1557740c Teardown

    FOR  ${role}  ${privilege}  IN ZIP  ${ROLES_LIST}  ${PRIVILEGES_LIST}
        Edit SAML External Authentication For Customer  ${role}

        Verify SAML Users Privileges Are Displayed In GUI Logs  ${privilege}
    END

Tvh1558638c
    [Documentation]  Verify Local /External users privilages are added into \n
    ...  authentication logs while login to NGUI \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1558638c
    [Tags]      Tvh1558638c  SEC-LOG-CONTENT-2
    [Setup]     Do Tvh1558638c Setup
    [Teardown]  Do Tvh1558638c Teardown

    FOR  ${role}  ${privilege}  IN ZIP  ${NGUI_ROLES_LIST}  ${NGUI_PRIVILEGES_LIST}
        Users Edit User  ${USER_NAME}  user_role=${role}
        Commit Changes
        Verify NGUI Users Privileges Are Displayed In API Logs  ${USER_NAME}  ${PASSWORD}  ${privilege}
    END

    FOR  ${role}  ${privilege}  IN ZIP  ${NGUI_ROLES_LIST}  ${NGUI_PRIVILEGES_LIST}
        Edit External Auth For LDAP  ${role}
        Verify NGUI Users Privileges Are Displayed In API Logs  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}  ${privilege}
    END

Tvh1558639c
    [Documentation]  Verify Local users privilages are added into authentication logs. \n
    ...  while login to spam quantine \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1558639c
    [Tags]      Tvh1558639c  SEC-LOG-CONTENT-2
    [Setup]     Do Tvh1558639c Setup
    [Teardown]  Do Tvh1558639c Teardown

    Verify Spam Quarantine Users Privileges Are Displayed In Authentication Logs  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}  ${ADMIN_USER_PRIVILEGE}
   
    FOR  ${role}  ${privilege}  IN ZIP  ${EUQ_ROLES_LIST}  ${EUQ_PRIVILEGES_LIST}
        Users Edit User  ${USER_NAME}  user_role=${role}
        Commit Changes
        Verify Spam Quarantine Users Privileges Are Displayed In Authentication Logs  ${USER_NAME}  ${PASSWORD}  ${privilege}
    END

    Verify Spam Quarantine Users Privileges Are Displayed In Authentication Logs  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}  ${ADMIN_USER_PRIVILEGE}

    FOR  ${role}  ${privilege}  IN ZIP  ${EUQ_ROLES_LIST}  ${EUQ_PRIVILEGES_LIST}
        Edit External Auth For LDAP  ${role}
        Verify Spam Quarantine Users Privileges Are Displayed In Authentication Logs  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}  ${privilege}
    END
