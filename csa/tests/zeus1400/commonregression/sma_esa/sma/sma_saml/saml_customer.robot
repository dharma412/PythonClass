# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/sma_saml/saml_customer.txt#1 $
# $DateTime: 2019/11/13 21:45:18 $
# $Author: sarukakk $

*** Settings ***
Resource           sma/global_sma.txt
Resource           sma/reports_keywords.txt
Resource           sma/saml.txt
Variables          sma/saml_constants.py

Suite Setup         Test Suite Setup
Suite Teardown      DefaultTestSuiteTeardown

*** Variables ***
@{PASSPHRASES}                        lab123  @123*$  !saml_123
@{IDP_NAMES}                          idpsaml  IDPSAML  IDP_saml  IDP_SAML@
${ASSERTION_CONSUMER_URL}             http://${DUT}/acs

*** Keywords ***
Test Suite Setup
    DefaultTestSuiteSetup
    Setup Firefox Preferences

Tvh1344319c Testcase Teardown
    [Arguments]  ${sp_profile}=${TEST_SP_PROFILE}
    Delete SP IDP For Customer   ${TEST_SP_PROFILE_EDIT}  ${TEST_IDP_PROFILE_EDIT}
    ${download_file}   Catenate  SEPARATOR=  ${sp_profile}  _metadata.xml
    Log   ${download_file}
    OperatingSystem.Remove File                      %{SARF_HOME}/tmp/${download_file}
    OperatingSystem.File Should Not Exist            %{SARF_HOME}/tmp/${download_file}
    DefaultTestCaseTeardown

Verify Config Mode Manual Option And SSO Urls
    [Arguments]  ${config_mode}=${CONFIGURATION_MODE_MANUAL}  ${sso_url}=${SSO_URL}
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  Assertion Consumer URL             ${ASSERTION_CONSUMER_URL}
    ...  SP Certificate                     ${CERT_FILE}
    ...  Private Key                        ${CERT_KEY}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Sign Requests                      ${SIGN_REQUEST}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  IDP Entity ID                      ${IDP_ENTITY_ID}
    ...  Configuration Mode                 ${config_mode}
    ...  SSO URL                            ${sso_url}
    ...  Certificate                        ${CERT_FILE}
    [Return]  ${settings}

Test Extentions Of Metadata Certificate Certificate Key
    [Arguments]  ${certificate_file}=${CERT_FILE}  ${certificate_passphrase}=${CERTIFICATE_PASSPHRASE}\n
    ...  ${certificate_key}=${CERT_KEY}  ${metadata}=${IDP_METADATA}
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  Assertion Consumer URL             ${ASSERTION_CONSUMER_URL}
    ...  SP Certificate                     ${certificate_file}
    ...  Private Key                        ${certificate_key}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Sign Requests                      ${SIGN_REQUEST}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  IDP Entity ID                     ${IDP_ENTITY_ID}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${metadata}
    [Return]  ${settings}

Verify SP AND IDP Fields
    [Arguments]  ${sp_profile}  ${idp_profile}
    ${output}=  Saml Get Details  user_sp_profile
    ${customer_sp}=  Get From Dictionary    ${output}  Service Provider Settings
    Dictionary Should Contain Value  ${customer_sp}   ${sp_profile}
    Dictionary Should Contain Value   ${customer_sp}  ${SP_ENTITY_ID}
    Dictionary Should Contain Value   ${customer_sp}  ${ASSERTION_CONSUMER_URL}
    ${output_new}=  Saml Get Details  user_idp_profile
    ${customer_idp}=  Get From Dictionary  ${output_new}  Identity Provider Settings
    Dictionary Should Contain Value  ${customer_idp}      ${idp_profile}
    Dictionary Should Contain Value   ${customer_idp}   ${SSO_URL}
    Dictionary Should Contain Value   ${customer_idp}   ${IDP_ENTITY_ID}

Verify SP AND IDP Profile Names
    [Arguments]  ${sp_profile}  ${idp_profile}
    ${output}=  Saml Get Details  user_sp_profile
    ${customer_sp}=  Get From Dictionary    ${output}  Service Provider Settings
    Dictionary Should Contain Value  ${customer_sp}  ${sp_profile}
    ${output_new}=  Saml Get Details  user_idp_profile
    ${customer_idp}=  Get From Dictionary  ${output_new}  Identity Provider Settings
    Dictionary Should Contain Value  ${customer_idp}   ${idp_profile}

SAML Edit SP And IDP Profile For Customer
    [Arguments]  ${sp_profile}  ${idp_profile}
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Profile Name                    ${TEST_SP_PROFILE_EDIT}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  Assertion Consumer URL             ${ASSERTION_CONSUMER_URL}
    ...  SP Certificate                     ${CERT_FILE}
    ...  Private Key                        ${CERT_KEY}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Sign Requests                      ${SIGN_REQUEST}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  IDP Profile Name                   ${TEST_IDP_PROFILE_EDIT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_METADATA}
    SAML EDIT SP AND IDP  ${sp_profile}  ${idp_profile}  ${settings}
    Commit Changes

*** Test Cases ***
Tvh1344315c
    [Documentation]  Try editing IDP config and verify submit\n
    ...  can be view from the SAML summary page\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344315
    ...  Confirm if SP metadata  can be viewed from the SAML summary page\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344317
    [Tags]  Tvh1344315c  Tvh1344317c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    SAML Edit SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Verify SP AND IDP Profile Names   ${TEST_SP_PROFILE_EDIT}  ${TEST_IDP_PROFILE_EDIT}
    Delete SP IDP For Customer   ${TEST_SP_PROFILE_EDIT}  ${TEST_IDP_PROFILE_EDIT}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344318c
    [Documentation]  Check if profile name of both SP and IDP are the hyperlink\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344318
    [Tags]  Tvh1344318c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Page Should Contain Link  xpath=//a[contains(text(),'${TEST_NAME}')]
    Page Should Contain Link  xpath=//a[contains(text(),'${TEST_IDP_PROFILE}')]
    Log   yes, entered profile names of both SP and IDP are the hyperlinks.
    Delete SP IDP For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344321c
    [Documentation]  confirm Entity ID,SSO Url are mandatory when configure keys\n
    ...  are opted in IDP configuration\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344321
    [Tags]  Tvh1344321c  srts
    [Setup]  DefaultTestCaseSetup
    ${settings}  Verify Config Mode Manual Option And SSO Urls
    SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}   ${settings}
    Commit Changes
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Delete SP IDP For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344322c
    [Documentation]  Verify the configured profile for IDP and SP can be viewed in\n
    ...  SAML configuration page with profilename,Entity ID,assertion URL and Metadata\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344322
    [Tags]  Tvh1344322c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Delete SP IDP For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344323c
    [Documentation]  Verify whether metadata can be uploaded and is mandatory for either\n
    ...  of IDP configuration\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344323
    [Tags]  Tvh1344323c  erts
    [Setup]  DefaultTestCaseSetup
    ${meta_xml}=  Test Extentions Of Metadata Certificate Certificate Key  metadata=${IDP_METADATA}
    SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${meta_xml}
    Commit Changes
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Delete SP IDP For Customer   ${TEST_NAME}   ${TEST_IDP_PROFILE}
    ${meta_txt}=  Test Extentions Of Metadata Certificate Certificate Key  metadata=${IDP_METADATA_OTH_FORMAT}
    Run Keyword And Expect Error  GuiValueError: Errors have occurred. Please see below for details.*
    ...  SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${meta_txt}
    Page Should Contain  Errors have occurred. Please see below for details.
    Commit Changes
    SAML Delete SP IDP  sp_name=${TEST_NAME}
    Commit Changes
    [Teardown]  DefaultTestCaseTeardown

Tvh1344335c
    [Documentation]  To check if SP and IDP details can be added by clicking\n
    ...  Add Service and Identity provider for customer login
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344335
    [Tags]  Tvh1344335c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Delete SP IDP For Customer    ${TEST_NAME}  ${TEST_IDP_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344341c
    [Documentation]  To Verify if SP certificate can be browsed and uploaded\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344341
    [Tags]  Tvh1344341c  erts
    [Setup]  DefaultTestCaseSetup
    ${settings}  Test Extentions Of Metadata Certificate Certificate Key  certificate_file=${CERT_FILE}
    SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Delete SP IDP For Customer   ${TEST_NAME}  ${TEST_IDP_PROFILE}
    ${settings}  Test Extentions Of Metadata Certificate Certificate Key  certificate_file=${EMPTY}
    Run Keyword And Expect Error  GuiValueError: Errors have occurred*
    ...  SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344354c
    [Documentation]  Confirm whether configure keys manually can be opted in IDP config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344354
    [Tags]  Tvh1344354c  erts
    [Setup]  DefaultTestCaseSetup
    ${settings_sso}  Verify Config Mode Manual Option And SSO Urls
    SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings_sso}
    Commit Changes
    Log  configure keys manully can be opted.
    Delete SP IDP For Customer   ${TEST_NAME}  ${TEST_IDP_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344358c
    [Documentation]  Check whether "Import DATA" cannot be submitted unless\n
    ...  metadata is exported in IDP config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344358
    [Tags]  Tvh1344358c  srts
    [Setup]  DefaultTestCaseSetup
    ${settings}  Test Extentions Of Metadata Certificate Certificate Key  metadata=${Empty}
    Run Keyword And Expect Error  GuiValueError: Errors have occurred*
    ...  SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings}
    SAML Delete SP IDP  sp_name=${TEST_NAME}
    Commit Changes
    [Teardown]  DefaultTestCaseTeardown

Tvh1344360c
    [Documentation]  To check if configured SP details  can be submitted with\n
    ...  all required fields\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344360
    [Tags]  Tvh1344360c  erts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Log  SP details can be submitted with all required fields
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Delete SP IDP For Customer   ${TEST_NAME}  ${TEST_IDP_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344368c
    [Documentation]  To verify if without SP private key upload\n
    ...  IDP config can't be submitted\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344368
    [Tags]  Tvh1344368c  srts
    [Setup]  DefaultTestCaseSetup
    ${settings}  Test Extentions Of Metadata Certificate Certificate Key  certificate_key=${EMPTY}
    ${msg}   Run Keyword And Expect Error  GuiValueError: Errors have occurred*
    ...  SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings}
    Page Should Contain  Errors have occurred. Please see below for details.
    [Teardown]  DefaultTestCaseTeardown

Tvh1344372c
    [Documentation]  Confirm if SAML config cannot be submitted unless the required\n
    ...  fields are filled\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344372
    [Tags]  Tvh1344372c  srts
    [Setup]  DefaultTestCaseSetup
    ${settings}  Test Extentions Of Metadata Certificate Certificate Key  certificate_file=${EMPTY}
    Run Keyword And Expect Error  GuiValueError: Errors have occurred*
    ...  SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings}
    Page Should Contain  Errors have occurred. Please see below for details.
    [Teardown]  DefaultTestCaseTeardown

Tvh1344373c
    [Documentation]  To verify if delete option in IDP config deletes IDP  config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344373
    ...  To verify if delete option in SP config deletes SP  config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344374
    [Tags]  Tvh1344373c  Tvh1344374c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Delete IDP For Customer   ${TEST_IDP_PROFILE}
    Page Should Not Contain Link  xpath=//a[contains(text(),'${TEST_IDP_PROFILE}')]
    Delete SP For Customer   ${TEST_NAME}
    Page Should Not Contain Link  xpath=//a[contains(text(),'${TEST_NAME}')]
    Log  yes able to delete sp and idp profiles for customer
    [Teardown]  DefaultTestCaseTeardown

Tvh1344376c
    [Documentation]  To check if any passphrase is accepted in submitting SP config\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344376
    [Tags]  Tvh1344376c  erts
    [Setup]  DefaultTestCaseSetup
    :FOR  ${any_passphrase}  IN  @{PASSPHRASES}
    \  ${settings}  Test Extentions Of Metadata Certificate Certificate Key  certificate_passphrase=${any_passphrase}
    \  SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings}
    \  Commit Changes
    \  Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    \  Delete SP IDP For Customer   ${TEST_NAME}  ${TEST_IDP_PROFILE}
    [Teardown]  DefaultTestCaseTeardown

Tvh1344319c
    [Documentation]  Try editing SP config and verify submit\n
    ...  can be downloaded from the SAML summary page
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344319
    ...  Confirm  if metadata of IDP is hyperlink and\n
    ...  can be downloaded from the SAML summary page
    ...  http://tims.cisco.com/view-entity.cmd?ent=1344320
    [Tags]  Tvh1344319c  Tvh1344320c  srts
    [Setup]  DefaultTestCaseSetup
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Verify SP AND IDP Profile Names  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    SAML Edit SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Close Browser
    Selenium Login With Autodownload Enabled  %{SARF_HOME}/tmp  text/xml
    Download Metadata  ${TEST_SP_PROFILE_EDIT}
    [Teardown]  Tvh1344319c Testcase Teardown   ${TEST_SP_PROFILE_EDIT}
