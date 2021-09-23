# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/saml_extauth_enable_devops.txt#3 $
# $DateTime: 2020/04/29 03:11:36 $
# $Author: sumitada $

*** Settings ***
Resource         sma/saml.txt
Force Tags       invalid_not_applicable_for_smart_license

Suite Setup      Test Suite Setup
Suite Teardown   DefaultTestSuiteTeardown

*** Variables  ***
${no_saml_message}  No SAML profiles configured.

*** Keywords ***
Test Suite Setup
    DefaultTestSuiteSetup
    Set Feature Key

Set Feature Key
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  cloud
    Restart CLI Session

TestCase Setup
    DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}

Enable External Auth Devops
     [Arguments]  ${user_role}=Administrator   ${group_name}=test_group
     ${devops_group_mappings}=  Create Dictionary
     ...  ${group_name}  ${user_role}
     ${enable_devops_ext_auth_settings}=  Create Dictionary
     ...  Authentication Type  SAML
     ...  External Authentication Attribute Name Map  mail
     ...  Customize Strings to View Devops SSO Login  testsaml,samluser,testuser
     ...  Group Mapping   ${devops_group_mappings}
     Users External Auth Devops Enable  ${enable_devops_ext_auth_settings}
     Commit Changes

TestCase Teardown
    Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    DefaultTestCaseTeardown

*** Test Cases ***
Tvh1344332c
    [Documentation]  Check whether usergroups can be mapped\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344332
    [Tags]  Tvh1344332c  srts
    [Setup]  TestCase Setup
    Enable External Auth Devops
    ${enabled_saml}  Users External Auth Devops Is Enabled
    Log   ${enabled_saml}
    Users External Auth Devops Disable
    Commit Changes
    [Teardown]  TestCase Teardown

Tvh1344333c
    [Documentation]  check whether wihout user groups , external auth cannot be mapped to SAML\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344333
    [Tags]  Tvh1344333c  srts
    [Setup]  TestCase Setup
    Run Keyword And Expect Error  GuiValueError: *  Enable External Auth Devops  group_name=${Empty}
    [Teardown]  TestCase Teardown

Tvh1344343c
     [Documentation]  IF SAML in external auth is elected,verify no SAML summary\n
     ...  is shown when devops SAML is not configured\n
     ...  http://tims.cisco.com/view-entity.cmd?ent=1344343
     [Tags]  Tvh1344343c  srts
     [Setup]  DefaultTestCaseSetup
     Run Keyword And Expect Error   GuiValueError: *  Enable External Auth Devops
     Page Should Contain  ${no_saml_message}
     [Teardown]  DefaultTestCaseTeardown

Tvh1344351c
    [Documentation]  While deleting SAML configured,verify the warning as\n
    ...  "in external auth SAML is configured and cannot be deleted"\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344351
    ...  Could not delete devops SAML SP/IDP when external auth SAML is configured\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344379
    [Tags]  Tvh1344351c  Tvh1344379c  srts
    [Setup]  TestCase Setup
    Enable External Auth Devops
    ${enabled_saml}  Users External Auth Devops Is Enabled
    Log   ${enabled_saml}
    Run Keyword And Expect Error  ConfigError: *  Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Users External Auth Devops Disable
    Commit Changes
    [Teardown]  TestCase Teardown

Tvh1344381c
    [Documentation]  Verify whether proper submit of devops saml profile with user role being mapped in Externalauth\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344381
    ...  Even when SAML summary is chosen ,verify external auth without submitting user role\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344357
    [Tags]  Tvh1344381c  Tvh1344357c srts
    [Setup]  TestCase Setup
    Enable External Auth Devops
    ${enabled_saml}  Users External Auth Devops Is Enabled
    Log   ${enabled_saml}
    Users External Auth Devops Disable
    Commit Changes
    Delete SP IDP For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    SAML Add SP And IDP Profile For Devops  ${TEST_SP_DEVOPS_PROFILE}  ${TEST_IDP_DEVOPS_PROFILE}
    Enable External Auth Devops  user_role=${Empty}
    SmaGuiLibrary.Users External Auth Devops Disable
    Commit Changes
    [Teardown]  TestCase Teardown
