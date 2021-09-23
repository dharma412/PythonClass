# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/saml_extauth_enable_customer.txt#2 $
# $DateTime: 2020/04/17 06:10:54 $
# $Author: sarukakk $

*** Settings ***
Resource         sma/saml.txt

Suite Setup       DefaultTestSuiteSetup
Suite Teardown    DefaultTestSuiteTeardown

*** Variables ***
${check_cust_saml}           xpath=//th[contains(text(),'Authentication Type:')]/following-sibling::td[contains(text(),'SAML')]
${no_saml_message}           No SAML profiles configured.

*** Keywords ***
TestCase Setup
    DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}

TestCase Teardown
     Users Disable External Authentication
     Commit Changes
     Delete SP IDP For Customer   ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}
     DefaultTestCaseTeardown

Tvh1344263c TestCase Teardown
     Delete SP IDP For Customer   ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}
     DefaultTestCaseTeardown

*** Test Cases ***
Tvh1344262c
    [Documentation]  Check whether usergroups can be mapped\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344262
    ...  Check configured SAML external auth is shown in User page itself\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344279
    [Tags]  Tvh1344262c   Tvh1344279c  srts
    [Setup]  TestCase Setup
    Users Edit External Authentication  SAML
    ...  extauth_attribute_name_map=sample_attribute
    ...  group_mapping=my_group:Administrator
    Commit Changes
    Navigate To  System Administration  Users
    Page Should Contain Element  ${check_cust_saml}
    [Teardown]  TestCase Teardown

Tvh1344263c
    [Documentation]  check whether wihout user groups,external auth cannot be mapped to SAML
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344263
    ...  Even when SAML summary is chosen ,verify external auth without submitting user role\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344277
    [Tags]  Tvh1344263c   Tvh1344277c  srts
    [Setup]  TestCase Setup
    Run Keyword And Expect Error  GuiValueError: *   Users Edit External Authentication  SAML
    ...  extauth_attribute_name_map=sample_attribute
    ...  group_mapping=${Empty}:Administrator
    Navigate To  System Administration  Users
    Page Should Not Contain Element  ${check_cust_saml}
    [Teardown]  Tvh1344263c TestCase Teardown

Tvh1344266c
    [Documentation]  Verify if SAML selected in externalauth and it shows no SAML config\n
    ...  when SAML is not configured in SAML config page already\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344266
    [Tags]  Tvh1344266c  srts
    [Setup]  DefaultTestCaseSetup
    Run Keyword And Expect Error  GuiValueError: *  Users Edit External Authentication  SAML
    ...  extauth_attribute_name_map=sample_attribute
    ...  group_mapping=my_group:Administrator
    Page Should Contain   ${no_saml_message}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344287c
    [Documentation]  While deleting SAML configured,verify the warning as\n
    ...  "in external auth SAML is configured and cannot be deleted"
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344287
    [Tags]  Tvh1344287c  srts
    [Setup]  TestCase Setup
    Users Edit External Authentication  SAML
    ...  extauth_attribute_name_map=sample_attribute
    ...  group_mapping=my_group:Administrator
    Commit Changes
    Navigate To  System Administration  Users
    Page Should Contain Element  ${check_cust_saml}
    Run Keyword And Expect Error  ConfigError: *  Delete SP IDP For Customer   ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}
    [Teardown]  TestCase Teardown
