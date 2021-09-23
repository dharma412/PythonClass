# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/cli_saml_externalauth_devops.txt#1 $
# $DateTime: 2019/11/13 21:45:18 $
# $Author: sarukakk $

*** Settings ***
Resource          sma/global_sma.txt
Resource          sma/saml.txt
Variables         sma/saml_constants.py
Suite Setup       Test Suite Setup
Suite Teardown    Test Suite Teardown
Force Tags        invalid_not_applicable_for_smart_license

*** Keywords ***
Test Suite Setup
    DefaultTestSuiteSetup
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  cloud
    Restart CLI Session
    Initialize Variables

Test Suite Teardown
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Delete Key  cloud
    DefaultTestSuiteTeardown

Test Case Setup
    DefaultTestCaseSetup
    Add Devops SAML Config

Test Case Teardown
    Delete/Clear Devops SMAL Config
    DefaultTestCaseTeardown

Enable external auth for Devops
    Userconfig External Devopssetup
    ...  use_ext_auth=YES
    ...  cache_time=0
    ...  mechanism=saml
    ...  group_name=${SAML_GROUP}
    ...  role=1
    ...  group_attribute=${SAML_GROUP_ATTRIB}
    ...  sso_string=samluser,testuser
    Commit

Devops Groups Print
    ${devops_groups}=  Userconfig External Devopsgroups Print
    Log  ${devops_groups}

*** Test Cases ***
Tvh1344378c
    [Documentation]  verify if devopssetup can be opted for enabling external authentication\n
    ...  auth SAML is configured\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344378
    [Tags]  Tvh1344378c  srts
    [Setup]  Test Case Setup
    Enable external auth for Devops
    Userconfig External Devopssetup  use_ext_auth=NO
    [Teardown]  Test Case Teardown

Tvh1344332c
    [Documentation]  Check whether usergroups can be mapped\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344332
    [Tags]  Tvh1344332c  srts
    [Setup]  Test Case Setup
    Enable external auth for Devops
    Userconfig External Devopsgroups New
    ...  group_name=${SAML_GROUP_NEW}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    Commit
    ${devops_groups}=  Userconfig External Devopsgroups Print
    Log  ${devops_groups}
    Userconfig External Devopssetup  use_ext_auth=NO
    [Teardown]  Test Case Teardown

Tvh1344336c
    [Documentation]  Verify if user group mapping can be edited in "Groups"\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344336
    [Tags]  Tvh1344336c  srts
    [Setup]  Test Case Setup
    Enable external auth for Devops
    Userconfig External Devopsgroups New
    ...  group_name=${SAML_GROUP_NEW}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    Commit
    ${devops_groups}=  Userconfig External Devopsgroups Print
    Log  ${devops_groups}
    Userconfig External Devopsgroups Edit
    ...  group_name=${SAML_GROUP_NEW}
    ...  role=${SAML_GROUP_ROLE_OPERATOR}
    ${devops_groups}=  Userconfig External Devopsgroups Print
    Log  ${devops_groups}
    Userconfig External Devopssetup  use_ext_auth=NO
    [Teardown]  Test Case Teardown

Tvh1344350c
    [Documentation]  verify if user group mapping cab be cleared to create\n
    ...  new user group mapping\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344350
    [Tags]  Tvh1344350c  srts
    [Setup]  Test Case Setup
    Enable external auth for Devops
    Userconfig External Devopsgroups Delete
    ...  group_name=${SAML_GROUP}
    Commit
    Userconfig External Devopsgroups New
    ...  group_name=${SAML_GROUP_NEW}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    Commit
    Devops Groups Print
    Userconfig External Devopssetup  use_ext_auth=NO
    [Teardown]  Test Case Teardown

Tvh1344349c
    [Documentation]  Check if all configured user role mapping can be viewed in "print"\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344349
    [Tags]  Tvh1344349c  srts
    [Setup]  Test Case Setup
    enable external auth for Devops
    Userconfig External Devopsgroups New
    ...  group_name=${SAML_GROUP_NEW}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    Commit
    Devops Groups Print
    Userconfig External Devopssetup  use_ext_auth=NO
    [Teardown]  Test Case Teardown