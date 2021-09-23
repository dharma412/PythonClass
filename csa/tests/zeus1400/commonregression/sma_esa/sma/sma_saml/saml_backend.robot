# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/saml_backend.txt#2 $
# $DateTime: 2020/04/17 06:10:54 $
# $Author: sarukakk $

*** Settings ***
Resource           sma/global_sma.txt
Resource           sma/saml.txt
Resource           esa/logs_parsing_snippets.txt
Variables          sma/saml_constants.py
Suite Setup        Test Suite Setup
Suite Teardown     Test Suite Teardown

*** Variables ***
${sso_service_log_path}=        /data/log/heimdall/sso_service/sso_service.current
${ldap_server_profile}=         myldap

*** Keywords ***
Test Suite Setup
    DefaultTestSuiteSetup
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  cloud
    Restart CLI Session

Test Suite Teardown
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Delete Key  cloud
    DefaultTestSuiteTeardown

Enable Externalauth Customer
    Userconfig External Setup Saml
    ...  cache_time=5
    ...  group_name=${SAML_GROUP}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    ...  group_attribute=${SAML_GROUP_ATTRIB}
    Commit

Enable Externalauth Devops
    Userconfig External Devopssetup
    ...  use_ext_auth=YES
    ...  cache_time=0
    ...  mechanism=saml
    ...  group_name=${SAML_GROUP}
    ...  role=1
    ...  group_attribute=${SAML_GROUP_ATTRIB}
    ...  sso_string=samluser,testuser
    Commit

Customer Devops Teardown
    Delete/Clear Customer SMAL Config
    Delete/Clear Devops SMAL Config
    DefaultTestCaseTeardown

Customer Teardown
    Delete/Clear Customer SMAL Config
    DefaultTestCaseTeardown

Devops Teardown
    Delete/Clear Devops SMAL Config
    DefaultTestCaseTeardown

Externalauth Teardown
    User Config External Setup Disable
    Commit
    Centralized Email Reporting Disable
    Spam Quarantine Disable
    Commit Changes
    Customer Devops Teardown

Edit External Authentication LDAP User Role
    [Arguments]  ${user_role}=${sma_user_roles.GUEST}
    Users Edit External Authentication  LDAP
    ...  ldap_query=${ldap_server_profile}.externalauth
    ...  group_mapping=${LDAP_SMA_USER_GROUP}:${user_role}
    Commit Changes
    Run Keyword And Ignore Error  Log Out Of Dut

Edit External Authentication Radius User Role
    [Arguments]  ${user_role}=Guests
    Run Keyword And Ignore Error  User Config External Setup Clear  confirm=yes
    User Config External Setup New  ${RADIUS_SERVER}  ${RADIUS_SECRET}  reply_timeout=10
    ...  create_mapping=yes
    ...  group_name=${RADIUS_USER_GROUP}
    ...  role=${user_role}
    Commit
    Run Keyword And Ignore Error  Log Out Of Dut

Verify Centralized Services Naviagtion Not Allowed For Guset Role
    Run Keyword And Expect Error
    ...   *  Navigate To  Centralized Services  Spam Quarantine
    Run Keyword And Expect Error
    ...   *  Navigate To  Centralized Services  Centralized Reporting
    Run Keyword And Expect Error
    ...   *  Navigate To  Centralized Services  Centralized Message Tracking

Verify User With Admin Role Allowed To Enable Spam Quarantine And Centralized Reporting
    Spam Quarantine Enable
    Centralized Email Reporting Enable
    Commit Changes

Verify LDAP/Radius User Accessiblity Based User Role
    [Arguments]  ${user}  ${user_password}  ${user_role}=${sma_user_roles.GUEST}
    Log Into DUT  user=${user}  password=${user_password}
    Run Keyword If  """${user_role}""".strip() == """${sma_user_roles.GUEST}""".strip()
    ...  Verify Centralized Services Naviagtion Not Allowed For Guset Role
    Run Keyword If  """${user_role}""".strip() == """${sma_user_roles.ADMIN}""".strip()
    ...  Verify User With Admin Role Allowed To Enable Spam Quarantine And Centralized Reporting
    Log Out of DUT
    Log Into DUT

*** Test Cases ***
Tvh1344362c
    [Documentation]   Check SAVE/LOAD config when logged in as admin\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344362
    ...  To verify that admin user able to logged into\n
    ...  legacy UI if saml customer and devops are configured\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344780
    ...  To Check if single sign on option in login page can be viewed if SAML\n
    ...  is configured in External auth for customers\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344284\n
    ...  To verify if single sign on is a hyperlink and can be entered\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344285\n
    ...  To verify local login irrespective of SAML login fails/sucess\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344283\n
    [Tags]  Tvh1344362c  Tvh1344780c  Tvh1344283c  Tvh1344284c  Tvh1344285c  srts  invalid_not_applicable_for_smart_license
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_NAME}
    SAML Add SP And IDP Profile For Devops  ${TEST_NAME}  ${TEST_NAME}
    ${config_file} =  Configuration File Save Config
    Configuration File Load Config  ${config_file}
    Commit Changes
    Enable Externalauth Customer
    Enable Externalauth Devops
    Log Out Of Dut
    Page Should Contain Element   //a[@id='sso_link']
    Log Into DUT
    User Config External Setup Disable
    Commit
    Userconfig External Devopssetup  use_ext_auth=NO
    Commit
    [Teardown]  Customer Devops Teardown

Tvh1344334c
    [Documentation]  Logs for metadata and certificate changes\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344334
    [Tags]  Tvh1344334c    srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP IDP COnfig Manual For Customer
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  SP Certificate                     ${CERT_FILE}
    ...  Private Key                        ${CERT_KEY}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_METADATA}
    SAML EDIT SP AND IDP  ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes
    Verify And Wait For Log Records
    ...  search_path= ${sso_service_log_path}
    ...  wait_time=2 mins
    ...  Validating IDP metadata >= 1
    ...  IDP metadata ok >= 1
    [Teardown]  Customer Teardown

Tvh1344309c
    [Documentation]  IF SAML in external auth is elected,verify configured SAML profile\n
    ...  is shown as hyperlink\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344309
    [Tags]  Tvh1344309c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_NAME}
    Navigate To  System Administration  Users
    Click Button  //input[@id='user']
    Select From List    //select[@id='ext_auth']  SAML
    Page Should Contain Element   //div[contains(text(),'SAML profile has been configured at')]
    [Teardown]  Customer Teardown

Tvh1344348c
    [Documentation]  To Check if single sign on option in login page can be viewed\n
    ...  if SAML is configured in External auth for devops\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344348\n
    ...  To verify if single sign on is a hyperlink and can be entered\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344346\n
    ...  To verify local login irrespective of SAML login fails/sucess\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344342\n
    ...  To check for "standard login" tab when devops string is given\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344339\n
    ...  To check for "standard login" tab when devops string is given\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344340
    [Tags]    Tvh1344348c  Tvh1344346c  Tvh1344342c  Tvh1344339c  Tvh1344340c  srts  invalid_not_applicable_for_smart_license
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Devops  ${TEST_NAME}  ${TEST_NAME}
    Enable Externalauth Devops
    Log Out Of Dut
    Input Text  //input[@name='username']   samluser
    Page Should Contain Element   //input[@id='sso_devops']
    Page Should Contain Element   //a[@id='devops_login']
    Log Into DUT
    Userconfig External Devopssetup  use_ext_auth=NO
    Commit
    [Teardown]  Devops Teardown

Tvh1344774c
    [Documentation]  To verify that if saml customer UI and devops  are configured\n
    ...  and external users is LDAP then saml IDP page will not come for credentials\n
    ...  and LDAP user able to logged into the legacy UI and check the quarantine,\n
    ...  reporting and tracking (based on the user roles)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344774
    [Tags]  Tvh1344774c   srts  invalid_not_applicable_for_smart_license
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_NAME}
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  SAML Add SP And IDP Profile For Devops  ${TEST_NAME}  ${TEST_NAME}
    LDAP Add Server Profile  ${ldap_server_profile}  ${LDAP_AUTH_SERVER}
    ...  server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit External Authentication Queries  ${ldap_server_profile}
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Commit Changes
    Edit External Authentication LDAP User Role
    Verify LDAP/Radius User Accessiblity Based User Role  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    Edit External Authentication LDAP User Role  ${sma_user_roles.ADMIN}
    Verify LDAP/Radius User Accessiblity Based User Role  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}  ${sma_user_roles.ADMIN}
    [Teardown]  Externalauth Teardown

Tvh1344775c
    [Documentation]  To verify that if saml customer UI and devops  are configured\n
    ...  and external users  is Radius then saml IDP page will not come for \n
    ...  credentials and Radius user able to logged into the legacy UI and check\n
    ...  the quarantine, reporting and tracking(based on the user role given)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344775
    [Tags]  Tvh1344775c   srts  invalid_not_applicable_for_smart_license
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_NAME}
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  SAML Add SP And IDP Profile For Devops  ${TEST_NAME}  ${TEST_NAME}
    Edit External Authentication Radius User Role
    Verify LDAP/Radius User Accessiblity Based User Role  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    Edit External Authentication Radius User Role  Administrators
    Verify LDAP/Radius User Accessiblity Based User Role  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}  ${sma_user_roles.ADMIN}
    [Teardown]  Externalauth Teardown
