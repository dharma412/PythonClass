# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/saml_sso_ui_login.txt#1 $
# $DateTime: 2020/01/09 22:36:26 $
# $Author: amanikaj $

*** Settings ***
Resource           sma/global_sma.txt
Resource           sma/saml.txt
Variables          sma/saml_constants.py
Suite Setup        Test Suite Setup
Suite Teardown     Test Suite Teardown
Force Tags         sso_login

*** Variables ***
${SSO_FAIL_MSG}=               Single Sign On Authentication Request Failed! Please contact your administrator.
${SSO_LINK}=                   //a[@id='sso_link']

*** Keywords ***
Test Suite Setup
    DefaultTestSuiteSetup
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  cloud
    Restart CLI Session
    Add Customer/Devops SAML Config Azure  ${USER_ROLE}
    Enable Externalauth Customer
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Add Customer/Devops SAML Config Azure  ${USER_ROLE_DEVOPS}
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Enable external auth for Devops

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
    DefaultTestSuiteTeardown

SAML Selenium Setup
    Set Up Selenium Environment
    Launch DUT Browser
    Log Into DUT

SAML Selenium Close
    Log Out Of Dut
    Selenium Close

Enable Externalauth Customer
    Userconfig External Setup Saml
    ...  cache_time=0
    ...  group_name=${SAML_GROUP_Azure}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    Commit

Enable external auth for Devops
    Userconfig External Devopssetup
    ...  use_ext_auth=YES
    ...  cache_time=0
    ...  mechanism=saml
    ...  group_name=${SAML_GROUP_Azure}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
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

*** Test Cases ***
Tvh1344363c
    [Documentation]  Check SAVE/LOAD config when logged in as SAML user\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344363\n
    ...  To check for redirection to IDP when single sign on is clicked\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344282
    ...  To verify the redirected IDP URL is same as that configured in SAML config page\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344364
    [Tags]  Tvh1344363c   Tvh1344282c  Tvh1344364c  srts
    [Setup]  DefaultTestCaseSetup
    Log Out Of Dut
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    ${config_file} =  Configuration File Save Config
    Configuration File Load Config  ${config_file}
    Commit Changes
    [Teardown]  DefaultTestCaseTeardown

Tvh1344365c
    [Documentation]  Check if logout/Access denied seen after disabling\n
    ...  external auth when logged in as SAML user\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344365
    [Tags]  Tvh1344365c   srts
    [Setup]  DefaultTestCaseSetup
    SAML Selenium Close
    SAML Selenium Setup
    Log Out Of Dut
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    User Config External Setup Disable
    Commit
    Navigate To  Centralized Services  Spam Quarantine
    Log Into DUT
    Enable Externalauth Customer
    [Teardown]  DefaultTestCaseTeardown

Tvh1344772c
    [Documentation]  To verify that user able to logged in as devops in legacy \n
    ...  UI by giving configured keyword and sso-login tab got enabled, after \n
    ...  logged in check the spam quarantine, reporting and tracking based on\n
    ...  the user role given to devops user\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344772\n
    ...  To verify the redirected IDP URL is same as that configured in SAML config page
    ...  for devops\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344344\n
    ...  To check for redirection to IDP when single sign on is clicked\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344347\n
    [Tags]  Tvh1344772c   Tvh1344344c  Tvh1344347c  srts  invalid_not_applicable_for_smart_license
    [Setup]  DefaultTestCaseSetup
    SAML Selenium Close
    SAML Selenium Setup
    Log Out Of Dut
    SSO Log Into Dut    ${USER_ROLE_DEVOPS}    ${SAML_AZUR_USER}     ${SAML_AZUR_USER_PASSWORD}  azure   samluser
    Spam Quarantine Enable
    Centralized Email Reporting Enable
    Commit Changes
    [Teardown]  DefaultTestCaseTeardown

Tvh1344369c
    [Documentation]  Check for Authorization failure -(by issuing IDP conflict credentials)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344369
    [Tags]  Tvh1344369c   srts
    [Setup]  DefaultTestCaseSetup
    SAML Selenium Close
    SAML Selenium Setup
    Log Out Of Dut
    Run Keyword And Expect Error
    ...   *Duo Login Failed:*
    ...   SSO Log Into Dut    customer    user1@gmail.com     123456789
    [Teardown]  DefaultTestCaseTeardown

Tvh1344367c
    [Documentation]  Check  when customer IDP is down or not reachable\n
    ...  and external auth is mapped to SAML\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344367
    ...  verify for singlesign on request failed message\n
    ...  for improper SAML config if any\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344370
    [Tags]  Tvh1344367c   Tvh1344370c  srts
    [Setup]  DefaultTestCaseSetup
    Close Browser
    SAML Selenium Setup
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID_Azure}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE_MANUAL}
    ...  IDP Entity ID                      ${IDP_ENTITY_ID}
    ...  SSO URL                            ${SSO_URL}
    ...  Certificate                        ${CERT_FILE}
    SAML EDIT SP AND IDP    ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes
    Log Out Of Dut
    Run Keyword And Expect Error
    ...   *  SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Go To  https://${DUT}
    Run On DUT  rm /data/third_party/external_auth/saml20/metadata/user_sp/private-key-raw.pem
    Click Element  ${SSO_LINK}
    Page Should Contain   ${SSO_FAIL_MSG}
    [Teardown]  DefaultTestCaseTeardown