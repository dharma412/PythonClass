# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/cli_saml_devops.txt#1 $
# $DateTime: 2019/11/13 21:45:18 $
# $Author: sarukakk $

*** Settings ***
Resource          sma/global_sma.txt
Variables         sma/saml_constants.py
Suite Setup       Test Suite Setup
Suite Teardown    Test Suite Teardown
Force Tags        invalid_not_applicable_for_smart_license

*** Keywords ***
Initialize Variables
    ${cert_file}=    OperatingSystem.Get File    ${CERT_FILE}
    Set Suite Variable  ${cert_file}
    ${cert_key}=    OperatingSystem.Get File    ${CERT_KEY}
    Set Suite Variable  ${cert_key}
    ${idp_metadata}=    OperatingSystem.Get File  ${IDP_METADATA}
    Set Suite Variable  ${idp_metadata}

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

Add Devops SAML Config
    Devops External Auth Config New
    ...  sp_profile_name=${TEST_NAME}
    ...  sp_entity_id=${SP_ENTITY_ID}
    ...  sp_certificate=${cert_file}
    ...  sp_certificate_key=${cert_key}
    ...  sp_certificate_passphrase=${CERTIFICATE_PASSPHRASE}
    ...  sp_sign_request=Y
    ...  sp_sign_assertion_request=Y
    ...  sp_technical_contact_id=${ORGANIZATION_TECHNICAL_CONTACT}
    ...  sp_organization_url=${ORGANIZATION_URL}
    ...  sp_organization_name=${ORGANIZATION_NAME}
    ...  sp_organization_display_name=${ORGANIZATION_DISPLAY_NAME}
    ...  idp_profile_name=${TEST_NAME}
    ...  idp_metadata_action=${IDP_METADATA_ACTION_ENTER}
    ...  idp_entity_id=${IDP_ENTITY_ID}
    ...  idp_sso_url=${SSO_URL}
    ...  idp_certificate=${cert_file}
    Commit

Delete/Clear Devops SMAL Config
    Devops External Auth Config Delete
    Commit

Test Case Teardown
    Delete/Clear Devops SMAL Config
    DefaultTestCaseTeardown

*** Test Cases ***
Tvh1344288c
    [Documentation]  Check GUI and CLI sync for SAML configuration\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344288
    [Tags]  Tvh1344288c   srts
    [Setup]  DefaultTestCaseSetup
    Add Devops SAML Config
    ${output}=  Saml Get Details  devops_sp_profile
    ${customer_sp}=  Get From Dictionary    ${output}  Service Provider Settings
    Dictionary Should Contain Value  ${customer_sp}   ${TEST_NAME}
    Dictionary Should Contain Value   ${customer_sp}  ${SP_ENTITY_ID}
    ${output}=  SAML Get Details    devops_idp_profile
    ${customer_idp}=  Get From Dictionary    ${output}       Identity Provider Settings
    Dictionary Should Contain Value   ${customer_idp}  ${IDP_ENTITY_ID}
    [Teardown]  Test Case Teardown

Tvh1344280c
    [Documentation]  To check if cli command "devopsexternalauthconfig"\n
    ...  shows option to configure "SAML UI" config\n
    ...  Check whether Add new SP and IDP configuration can be done\n
    ...  by uploading certificates,keys and metadata from cli\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344280
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344278
    [Tags]  Tvh1344280c  Tvh1344278c  srts
    [Setup]  DefaultTestCaseSetup
    Devops External Auth Config New
    ...  sp_profile_name=${TEST_NAME}
    ...  sp_entity_id=${SP_ENTITY_ID}
    ...  sp_certificate=${cert_file}
    ...  sp_certificate_key=${cert_key}
    ...  sp_certificate_passphrase=${CERTIFICATE_PASSPHRASE}
    ...  sp_sign_request=Y
    ...  sp_sign_assertion_request=Y
    ...  sp_technical_contact_id=${ORGANIZATION_TECHNICAL_CONTACT}
    ...  sp_organization_url=${ORGANIZATION_URL}
    ...  sp_organization_name=${ORGANIZATION_NAME}
    ...  sp_organization_display_name=${ORGANIZATION_DISPLAY_NAME}
    ...  idp_profile_name=${TEST_NAME}
    ...  idp_metadata_action=${IDP_METADATA_ACTION_PASTE}
    ...  idp_metadata_xml=${idp_metadata}
    [Teardown]  Test Case Teardown

Tvh1344290c
    [Documentation]  check by editing any parameters of SP /IDP in\n
    ...  SAML configuration and try submit from cli\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344290
    [Tags]  Tvh1344290c   srts
    [Setup]  DefaultTestCaseSetup
    ${new_sp_name}=   Catenate  ${TEST_NAME}  NEW
    ${new_idp_name}=  Catenate  ${TEST_NAME}  NEW_IDP
    ${new_idp_entity_id}=  Set Variable  New_entity_id
    ${new_sso_url}=  Set Variable  https://pingfed.com/ESA/NEW
    Add Devops SAML Config
    Devops External Auth Config Edit Sp
    ...  sp_profile_name=${new_sp_name}
    ...  sp_certificate_edit_option=USE
    Commit
    Devops External Auth Config Edit Idp
    ...  idp_profile_name=${new_idp_name}
    ...  idp_metadata_edit_action=${IDP_METADATA_ACTION_PASTE}
    ...  idp_metadata_xml=${idp_metadata}
    Commit
    [Teardown]  Test Case Teardown

Tvh1344289c
    [Documentation]  Confirm deletion happens for SP/IDP via cli\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344289
    [Tags]  Tvh1344289c   srts
    [Setup]  DefaultTestCaseSetup
    Add Devops SAML Config
    Delete/Clear Devops SMAL Config
    [Teardown]  DefaultTestCaseTeardown