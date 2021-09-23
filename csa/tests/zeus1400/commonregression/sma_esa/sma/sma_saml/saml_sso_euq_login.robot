# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/saml_sso_euq_login.txt#1 $
# $DateTime: 2020/01/23 21:48:51 $
# $Author: amanikaj $

*** Settings ***
Resource           sma/saml.txt
Variables          sma/saml_constants.py
Suite Setup        Test Suite Setup
Suite Teardown     Test Suite Teardown
Force Tags         sso_login

*** Variables ***
${TEST_EUQ_SP_PROFILE}=        euq_sp_profile
${TEST_EUQ_IDP_PROFILE}=       euq_idp_profile
${ldap_server_profile}=        myldap
${LOCAL_USER_ADMIN}=           admin1
${LOCAL_USER_GUEST}=           guest1
${EUQ_IDP_EDIT_BUTTON}=        //a[contains(text(),'${TEST_EUQ_IDP_PROFILE}')]
${COPY_BUTTON}=                //input[@name='copy_user_idp']
${SUBMIT_BUTTON}=              //input[@name='SubmitIDP']


*** Keywords ***
Test Suite Setup
    DefaultTestSuiteSetup
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  cloud
    Restart CLI Session
    Add Customer/Devops SAML Config Azure  ${USER_ROLE}
    Userconfig External Setup Saml
    ...  cache_time=0
    ...  group_name=${SAML_GROUP_Azure}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    Commit
    Add Euq SAML Config
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Add Customer/Devops SAML Config Azure  ${USER_ROLE_DEVOPS}
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Enable external auth for Devops
    LDAP Add Server Profile  ${ldap_server_profile}  ${LDAP_AUTH_SERVER}
    ...  server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit External Authentication Queries  ${ldap_server_profile}
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Commit Changes
    Set Suite Variable  ${USER_PASSWORD}  ${DUT_ADMIN_SSW_PASSWORD}

Test Suite Teardown
    User Config External Setup Disable
    Delete/Clear Customer SMAL Config
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Userconfig External Devopssetup  use_ext_auth=NO
    Commit
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Delete/Clear Devops SMAL Config
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Delete Key  cloud
    SAML DELETE EUQ PROFILES  sp_name=${TEST_EUQ_SP_PROFILE}  idp_name=${TEST_IDP_PROFILE}
    LDAP Delete Server Profile  ${ldap_server_profile}
    Commit Changes
    DefaultTestSuiteTeardown

SAML Selenium Setup
    Set Up Selenium Environment
    Launch DUT Browser
    Log Into DUT

SAML Selenium Close
    Log Out Of Dut
    Selenium Close

Enable Externalauth Customer
    [Arguments]  ${user_role}=${SAML_GROUP_ROLE_ADMIN}
    User Config External Setup Disable
    Userconfig External Setup Saml
    ...  cache_time=0
    ...  group_name=${SAML_GROUP_Azure}
    ...  role=${user_role}
    Commit

Enable external auth for Devops
    [Arguments]  ${user_role}=${SAML_GROUP_ROLE_ADMIN}
    Userconfig External Devopssetup
    ...  use_ext_auth=YES
    ...  cache_time=0
    ...  mechanism=saml
    ...  group_name=${SAML_GROUP_Azure}
    ...  role=${user_role}
    ...  sso_string=samluser
    Commit

Add Customer/Devops SAML Config Azure
    [Arguments]  ${user_role}
    ${settings}=  Create Dictionary
    ...  User Role                          ${user_role}
    ...  SP Entity ID                       ${SP_ENTITY_ID_Azure}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP  ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes

Add Euq SAML Config
     ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP FOR EUQ  ${TEST_EUQ_SP_PROFILE}  ${TEST_EUQ_IDP_PROFILE}  ${settings}
    Commit Changes

Verify User With Admin Role Allowed To Enable And Disable Spam Quarantine Centralized Reporting And Tracking
    Spam Quarantine Enable
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Disable
    Spam Quarantine Disable
    Centralized Email Message Tracking Disable
    Commit Changes

Verify Centralized Services Naviagtion Not Allowed For Guset Role
    Run Keyword And Expect Error
    ...   *  Navigate To  Centralized Services  Spam Quarantine
    Run Keyword And Expect Error
    ...   *  Navigate To  Centralized Services  Centralized Reporting
    Run Keyword And Expect Error
    ...   *  Navigate To  Centralized Services  Centralized Message Tracking

Verify SAML User Accessiblity Based User Role
    [Arguments]  ${user_type}  ${user}  ${user_password}  ${user_role}=${sma_user_roles.ADMIN}
    SAML Selenium Close
    SAML Selenium Setup
    Log Out Of Dut
    SSO Log Into Dut    ${user_type}  ${user}  ${user_password}  azure  samluser
    Run Keyword If  """${user_role}""".strip() == """${sma_user_roles.ADMIN}""".strip()
    ...  Verify User With Admin Role Allowed To Enable And Disable Spam Quarantine Centralized Reporting And Tracking
    Run Keyword If  """${user_role}""".strip() == """${sma_user_roles.GUEST}""".strip()
    ...  Verify Centralized Services Naviagtion Not Allowed For Guset Role
    Log Out Of Dut
    Log Into DUT

Test Case Teardown
    Enable Externalauth Customer
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Userconfig External Devopssetup  use_ext_auth=NO
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Enable external auth for Devops
    DefaultTestCaseTeardown

Tvh1344771c Teardown
    Log Out Of Dut
    Log Into DUT
    Users Delete User  admin1
    Users Delete User  guest1
    Commit Changes
    DefaultTestCaseTeardown

Tvh1344777c Teardown
    Log Out Of Dut
    Log Into DUT
    Spam Quarantine Disable
    Commit Changes
    DefaultTestCaseTeardown

Tvh1344366c Teardown
    Close Browser
    SAML Selenium Setup
    Enable Externalauth Customer
    Spam Quarantine Disable
    Commit Changes
    DefaultTestCaseTeardown

Go To Euq Gui
    [Arguments]  ${user}  ${password}
    Close Browser
    Add Cert Exception For Quarantine Page
    Launch Dut Browser
    Go To  https://${DUT}:83
    Log Into Dut  ${user}  ${password}

Login to EUQ via AZURE
   Close Browser
   Launch DUT Browser  https://${SMA}:83
   SSO login to dut  sso_username=${SAML_AZUR_USER}  sso_password=${SAML_AZUR_USER_PASSWORD}  idp='azure'
   Run Keyword And Ignore Error  Capture Screenshot

Enable Spam Qurantine for SAML/LDAP
    [Arguments]  ${auth}
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=${auth}
    Commit Changes

Enable Externalauth for LDAP
    Users Edit External Authentication  LDAP
    ...  ldap_query=${ldap_server_profile}.externalauth
    ...  group_mapping=${LDAP_SMA_USER_GROUP}:${sma_user_roles.ADMIN}
    Commit Changes

Verify SSO Login for Devops User
    Close Browser
    Launch DUT Browser
    SSO Log Into Dut    ${USER_ROLE_DEVOPS}    ${SAML_AZUR_USER}     ${SAML_AZUR_USER_PASSWORD}  azure   samluser
    Run Keyword And Ignore Error  Capture Screenshot

Verify Devops User Accessiblity
    Verify SAML User Accessiblity Based User Role  ${USER_ROLE_DEVOPS}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}
    Userconfig External Devopssetup  use_ext_auth=NO
    Enable external auth for Devops    ${SAML_GROUP_ROLE_GUEST}
    Verify SAML User Accessiblity Based User Role  ${USER_ROLE_DEVOPS}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}    ${sma_user_roles.GUEST}


*** Test Cases ***
Tvh1344769c
    [Documentation]  To verify that user able to logged in as "saml" external user in legacy\n
    ...  UI if saml is configured for euq, customer UI and devops and after logged in check\n
    ...  the spam quarantine, reporting and tracking based on the user role given to external user.\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344769
    ...  To verify tha saml external user able to access the spam quarantine from customer\n
    ...  legacy UI if access given for spam quarantine to external users (based on user role\n
    ...  can verify) otherwise user does not have access to spam quarantine page.\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344770
    ...  To verify tha saml devop user able to access the spam quarantine from devops legacy
    ...  UI if access given for spam quarantine to external users (based on user role can
    ...  verify) otherwise user does not have access to spam quarantine page.\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344773
    [Tags]  Tvh1344769c  Tvh1344770c  Tvh1344773c  srts
    [Setup]  DefaultTestCaseSetup
    Verify SAML User Accessiblity Based User Role  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}
    Enable Externalauth Customer  ${SAML_GROUP_ROLE_GUEST}
    Verify SAML User Accessiblity Based User Role  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  ${sma_user_roles.GUEST}
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Verify Devops User Accessiblity
    [Teardown]  Test Case Teardown

Tvh1344771c
    [Documentation]  To verify tha local user able to access the spam quarantine from legacy UI if access\n
    ...  given for spam quarantine to locall users (based on user role can verify) otherwise\n
    ...  user does not have access to spam quarantine page..\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344771
    [Tags]  Tvh1344771c  srts
    [Setup]  DefaultTestCaseSetup
    Users Add User  ${LOCAL_USER_ADMIN}  AdminUser  ${USER_PASSWORD}
    Users Add User  ${LOCAL_USER_GUEST}  GuestUser  ${USER_PASSWORD}  ${sma_user_roles.GUEST}
    Commit Changes
    Log Out Of Dut
    Log Into DUT  user=${LOCAL_USER_ADMIN}  password=${USER_PASSWORD}
    Verify User With Admin Role Allowed To Enable And Disable Spam Quarantine Centralized Reporting And Tracking
    Log Out Of Dut
    Log Into DUT  user=${LOCAL_USER_GUEST}  password=${USER_PASSWORD}
    Verify Centralized Services Naviagtion Not Allowed For Guset Role
    [Teardown]  Tvh1344771c Teardown

Tvh1344271c
    [Documentation]  cutomer idp profile to be copied to euq by using "copy" in EUQ SAML config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344271\n
    [Tags]  Tvh1344271c   srts
    [Setup]  DefaultTestCaseSetup
    Navigate To  System Administration  SAML
    Click Button   ${EUQ_IDP_EDIT_BUTTON}
    Click Button   ${COPY_BUTTON}
    Click Button   ${SUBMIT_BUTTON}
    Commit Changes
    ${output}=  Saml Get Euq Details  euq_idp_profile
    Log  ${output}
    ${euq_idp}=  Get From Dictionary  ${output}  Identity Provider Settings
    Dictionary Should Contain Value  ${euq_idp}   ${TEST_IDP_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344777c
    [Documentation]  To verify the ldap euq workflow if spam quarantine method is ldap & saml is\n
    ...  configured for customer UI and devops then also check in another tab that saml and\n
    ...  devops external user able to access the legacy UI.\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344777
    [Tags]  Tvh1344777c   srts
    [Setup]  DefaultTestCaseSetup
    Enable Spam Qurantine for SAML/LDAP  LDAP
    Enable Externalauth for LDAP
    Go To Euq Gui  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}
    Run Keyword And Ignore Error  Capture Screenshot
    Close Browser
    SAML Selenium Setup
    Enable Externalauth Customer
    Log Out Of Dut
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Run Keyword And Ignore Error  Capture Screenshot
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Verify SSO Login for Devops User
    [Teardown]  Tvh1344777c Teardown

Tvh1344366c
    [Documentation]  Verify EUQ SAML flow with same IDP as that of SAML login\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344366
    ...  To verify the saml euq workflow and External user LDAP able to logged\n
    ...  in legacy if saml is configured for euq, customer UI and devops, spam quarantine\n
    ...  method is saml and external user is selected as LDAP.\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344779
    [Tags]  Tvh1344366c   Tvh1344779c  srts
    [Setup]  DefaultTestCaseSetup
    Enable Externalauth for LDAP
    Enable Spam Qurantine for SAML/LDAP  SAML 2.0
    Run Keyword And Ignore Error  Log Out Of Dut
    Log Into DUT  user=${LDAP_SMA_USER}  password=${LDAP_SMA_USER_PASS}
    Launch DUT Browser  https://${SMA}:83
    Do AZURE LOGIN TO DUT  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}
    [Teardown]  Tvh1344366c Teardown
