# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/cli_saml_externalauth_customer.txt#1 $
# $DateTime: 2019/11/13 21:45:18 $
# $Author: sarukakk $

*** Settings ***
Resource          sma/global_sma.txt
Resource          sma/saml.txt
Variables         sma/saml_constants.py
Suite Setup       Test Suite Setup
Suite Teardown    DefaultTestSuiteTeardown

*** Keywords ***
Test Case Setup
    DefaultTestCaseSetup
    Add Customer SAML Config

Test Case Teardown
    Delete/Clear Customer SMAL Config
    DefaultTestCaseTeardown

External Auth Enable For Customer
    [Arguments]  ${customer_role}=${SAML_GROUP_ROLE_ADMIN}
    Userconfig External Setup Saml
    ...  cache_time=5
    ...  group_name=${SAML_GROUP}
    ...  role=${customer_role}
    ...  group_attribute=${SAML_GROUP_ATTRIB}
    Commit

***Test Cases ***
Tvh1344291c
    [Documentation]  Check if all configured user role mapping can be viewed in "print"\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344291
    ...  Check whether SAML is listed If External auth is enabled in userconfig
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344265
    [Tags]  Tvh1344378c  Tvh1344265c  srts
    [Setup]  Test Case Setup
    External Auth Enable For Customer
    ${out}=  User Config External Groups Print
    Log  ${out}
    User Config External Setup Disable
    Commit
    [Teardown]  Test Case Teardown

Tvh1344292c
    [Documentation]  verify if user group mapping can be cleared to create new user group mapping\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344292
    [Setup]  Test Case Setup
    [Tags]  Tvh1344292c  srts
    External Auth Enable For Customer
    ${out}=  User Config External Groups Print
    Should Contain  ${out}  ${SAML_GROUP} -> Administrator
    UserConfig External Groups Delete
    ...  group_name=${SAML_GROUP}
    Commit
    User Config External Groups New  ${SAML_GROUP_NEW}  mapping_type=Operators
    Commit
    ${out}=  User Config External Groups Print
    Should Contain  ${out}  ${SAML_GROUP_NEW} -> Operators
    User Config External Setup Disable
    Commit
    [Teardown]  Test Case Teardown

Tvh1344293c
    [Documentation]  Verify if user group mapping can be edited in "Groups"\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344293c
    [Tags]  Tvh1344293c  srts
    [Setup]  Test Case Setup
    External Auth Enable For Customer
    User Config External Groups Edit  ${SAML_GROUP}  mapping_type=Operators
    Commit
    ${out}=  User Config External Groups Print
    Should Contain  ${out}  ${SAML_GROUP} -> Operators
    User Config External Setup Disable
    Commit
    [Teardown]  Test Case Teardown

Tvh1344277c
    [Documentation]  Even when SAML summary is chosen ,verify external auth without submitting user role\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344291
    [Tags]  Tvh1344277  srts
    [Setup]  Test Case Setup
    ${msg}=  Run Keyword And Expect Error  *  External Auth Enable For Customer  customer_role=DUMMY_TO_BE_FILLED
    Log  ${msg}
    [Teardown]  Test Case Teardown