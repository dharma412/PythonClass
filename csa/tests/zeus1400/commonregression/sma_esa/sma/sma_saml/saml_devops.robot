# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/saml_devops.txt#1 $
# $DateTime: 2019/11/13 21:45:18 $
# $Author: sarukakk $

*** Settings ***
Resource         sma/global_sma.txt
Resource     	 sma/reports_keywords.txt
Resource         sma/saml.txt
Variables        sma/saml_constants.py
Force Tags       invalid_not_applicable_for_smart_license

Suite Setup      Test Suite Setup
Suite Teardown   DefaultTestSuiteTeardown

*** Variables ***
${ASSERTION_CONSUMER_URL_DEVOPS}             http://${DUT}/devops_sso
@{PASSPHRASES}                               lab123  @123*$  !saml_123

*** Keywords ***
Set Feature Key
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  cloud
    Restart CLI Session

Verify SP AND IDP Fields
    [Arguments]  ${sp_profile}  ${idp_profile}
    ${output}=  Saml Get Details  devops_sp_profile
    ${devops_sp}=  Get From Dictionary    ${output}  Service Provider Settings
    Dictionary Should Contain Value  ${devops_sp}   ${sp_profile}
    Dictionary Should Contain Value   ${devops_sp}  ${SP_ENTITY_ID}
    Dictionary Should Contain Value   ${devops_sp}  ${ASSERTION_CONSUMER_URL_DEVOPS}
    ${output_new}=  Saml Get Details  devops_idp_profile
    ${devops_idp}=  Get From Dictionary  ${output_new}  Identity Provider Settings
    Dictionary Should Contain Value  ${devops_idp}     ${idp_profile}
    Dictionary Should Contain Value   ${devops_idp}   ${SSO_URL}
    Dictionary Should Contain Value   ${devops_idp}   ${IDP_ENTITY_ID}

Verify SP AND IDP Profile Names
    [Arguments]  ${sp_profile}  ${idp_profile}
    ${output}=  Saml Get Details  devops_sp_profile
    ${devops_sp}=  Get From Dictionary    ${output}  Service Provider Settings
    Dictionary Should Contain Value  ${devops_sp}   ${sp_profile}
    ${output_new}=  Saml Get Details  devops_idp_profile
    ${devops_idp}=  Get From Dictionary  ${output_new}  Identity Provider Settings
    Dictionary Should Contain Value  ${devops_idp}  ${idp_profile}

SAML Add SP And IDP Profile with Import IDP Metadata For Devops
    [Arguments]  ${user_role}  ${sp_profile}  ${idp_profile}
    ${settings}=  Create Dictionary
    ...  User Role                          ${user_role}
    ...  SP Profile Name                    ${sp_profile}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  Assertion Consumer URL             ${ASSERTION_CONSUMER_URL_DEVOPS}
    ...  SP Certificate                     ${CERT_FILE}
    ...  Private Key                        ${CERT_KEY}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Sign Requests                      ${SIGN_REQUEST}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  IDP Profile Name                   ${idp_profile}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_METADATA}
    [Return]  ${settings}

Test Suite Setup
    DefaultTestSuiteSetup
    Set Feature Key
    Setup Firefox Preferences

*** Test Cases ***
Tvh1344294c
    [Documentation]  To verify if delete option in SP config deletes SP config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344294
    ...  To verify if delete option in IDP config deletes IDP  config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344295
    [Tags]  Tvh1344294c  Tvh1344295c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Verify SP AND IDP Profile Names   ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Delete SP For Devops  ${TEST_SP_DEVOPS_PROFILE}
    Page Should Not Contain Link  xpath=//a[contains(text(),'${TEST_SP_DEVOPS_PROFILE}')]
    Delete IDP For Devops  ${TEST_IDP_DEVOPS_PROFILE}
    Page Should Not Contain Link  xpath=//a[contains(text(),'${TEST_IDP_DEVOPS_PROFILE}')]
    [Teardown]  DefaultTestCaseTeardown

Tvh1344296c
    [Documentation]  Confirm if SAML config cannot be submitted unless the required fields are filled\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344296
    [Tags]  Tvh1344296c  srts
    [Setup]  DefaultTestCaseSetup
    ${settings}  Test Extentions Of Metadata Certificate Certificate Key  user_role=${USER_ROLE}  certificate_file=${EMPTY}
    Run Keyword And Expect Error  GuiValueError: Errors have occurred*
    ...  SAML Add SP And IDP  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}  ${settings}
    Page Should Contain  Errors have occurred. Please see below for details.
    [Teardown]  DefaultTestCaseTeardown

Tvh1344297c
    [Documentation]  To check if configured SP details  can be submitted with all required fields\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344297
    [Tags]  Tvh1344297c  erts
    [Setup]  DefaultTestCaseSetup
    ${settings}  SAML Add SP And IDP Profile with Import IDP Metadata For Devops  ${USER_ROLE_DEVOPS}  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    SAML Add SP And IDP  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}  ${settings}
    Verify SP AND IDP Profile Names   ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344300c
    [Documentation]  Confirm whether configure keys manually can be opted in IDP config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344300
    ...  confirm Entity ID,SSO Url are mandatory when configure keys are opted in IDP configuration\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344301
    [Tags]  Tvh1344300c  Tvh1344301c  srts
    [Setup]  DefaultTestCaseSetup
    ${settings_sso}  Verify Config Mode Manual Option  user_role=${USER_ROLE_DEVOPS}  assertion_url=${ASSERTION_CONSUMER_URL_DEVOPS}
    SAML Add SP And IDP  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}  ${settings_sso}
    Commit Changes
    Log  configure keys manully can be opted.
    Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344303c
    [Documentation]  To check if any passphrase is accepted in submitting SP config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344303
    [Tags]  Tvh1344303c  srts
    [Setup]  DefaultTestCaseSetup
    :FOR  ${i}  IN  @{PASSPHRASES}
    \  ${settings}  Test Extentions Of Metadata Certificate Certificate Key  user_role=${USER_ROLE_DEVOPS}  certificate_passphrase=${i}
    \  SAML Add SP And IDP  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}  ${settings}
    \  Commit Changes
    \  Verify SP AND IDP Profile Names  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    \  Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344304c
    [Documentation]  Try editing SP config and verify submit\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344304
    ...  Try editing IDP config and verify submit\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344305
    [Tags]  Tvh1344304c  Tvh1344305c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Verify SP AND IDP Profile Names  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    SAML Edit SP And IDP Profile For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}  user_role=${USER_ROLE_DEVOPS}
    Verify SP AND IDP Profile Names  ${TEST_SP_PROFILE_EDIT}  ${TEST_IDP_PROFILE_EDIT}
    Delete SP IDP For Devops   ${TEST_SP_PROFILE_EDIT}  ${TEST_IDP_PROFILE_EDIT}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344306c
    [Documentation]  Confirm if SP metadata  can be viewed from the SAML summary page\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344306
    [Tags]  Tvh1344306c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    ${metadata}=  SAML View IDP Metadata  ${USER_ROLE_DEVOPS}
    Log  ${metadata}
    Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344327c
    [Documentation]   To check if SP and IDP details can be added by clicking\n
    ...  Add Service and Identity provider for devops login
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344327
    [Tags]  Tvh1344327c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Verify SP AND IDP Profile Names   ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344307c
    [Documentation]  Confirm  if metadata of IDP is hyperlink and can be\n
    ...  downloaded from the SAML summary page\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344307
    [Tags]  Tvh1344307c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Close Browser
    Selenium Login With Autodownload Enabled  %{SARF_HOME}/tmp  text/xml
    Download Metadata  sp_profile=${TEST_SP_DEVOPS_PROFILE}  user_role=${USER_ROLE_DEVOPS}
    Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    [Teardown]  Testcase Teardown
