# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/TEACATS/sma_esa/CSCvm25115_legacy.txt#2 $ $DateTime: 2020/03/25 09:24:08 $ $Author: thariram $

*** Settings ***
Library           SmaGuiLibrary
Library           Collections
Resource          sma/global_sma.txt
Resource          regression.txt

Suite Setup   Run Keywords
              ...  Set Aliases For Appliance Libraries
              ...  Set Appliance Under Test to SMA
              ...  global_sma.DefaultTestSuiteSetup
              ...  Do Suite Setup

Suite Teardown   Run Keywords
                 ...  Do Suite Teardown
                 ...  global_sma.DefaultTestSuiteTeardown

*** Variables ***
${PAGE_EMAIL_REPORTING}  Cisco Content Security Management Appliance ${SMA_MODEL} (${DUT}) - Centralized Services > Email > Centralized Reporting
${PAGE_TRACKING}  Cisco Content Security Management Appliance ${SMA_MODEL} (${DUT}) - Centralized Services > Email > Centralized Message Tracking

** Keywords ***
Do Suite Setup
    Set Suite Variable   ${LDAP_USER_NAME}   ldap_1
    Set Suite Variable   ${LDAP_PASSWORD}   ironport
    LDAP Client Connect  ${LDAP_AUTH_SERVER}
    ...  ldap_server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  basedn=${LDAP_BASEDN}
    ...  binddn=${LDAP_BINDDN}
    ...  password=${LDAP_PASSWORD}
    Ldap Client Add User
    ...  uid=${LDAP_USER_NAME}
    ...  password=${LDAP_PASSWORD}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}
    ...  mail=${LDAP_USER_NAME}@${CLIENT}

    Set Suite Variable   ${LDAP_CLASS}   ldap_group
    Ldap Client Add Group
    ...  ${LDAP_CLASS}
    ...  members=${LDAP_USER_NAME}
    ...  basedn=${LDAP_BASEDN}

    Set Suite Variable   ${LDAP_PROFILE_NAME}   mainldapprofile
    Set Suite Variable   ${LDAP_EXT_QUERY}   externalauth
    Selenium Login

    LDAP Add Server Profile
    ...  ${LDAP_PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}
    ...  anonymous
    ...  OpenLDAP
    ...  ${LDAP_AUTH_PORT}
    ...  ${LDAP_BASE_DN}

    LDAP Edit External Authentication Queries
    ...  ${LDAP_PROFILE_NAME}
    ...  ${LDAP_EXT_QUERY}
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Commit Changes

Do Suite Teardown
   Selenium Close
   Selenium Login
   Ldap Client Delete Group   ${LDAP_CLASS}
   Ldap Client Delete User   ${LDAP_USER_NAME}
   Ldap Client Disconnect
   Ldap Delete Server Profile  ${LDAP_PROFILE_NAME}
   Commit Changes

Should Have Access To
    [Arguments]  ${page}  ${expected_title}
    Go To  ${page}
    ${current_title} =  Get Title
    Should Be Equal  ${current_title}  ${expected_title}

Assign Page Virtual
    Set TestVariable  ${PAGE_EMAIL_REPORTING}  Cisco Content Security Management Virtual Appliance ${SMA_MODEL} (${DUT}) - Centralized Services > Email > Centralized Reporting
    Set TestVariable  ${PAGE_TRACKING}  Cisco Content Security Management Virtual Appliance ${SMA_MODEL} (${DUT}) - Centralized Services > Email > Centralized Message Tracking

Close SSH connection
   Set SSHLib Prompt  ${Empty}
   SSHLibrary.Close Connection

*** Test Cases ***

Tvh1231016c
    [Documentation]  Reporting page fails to load page
    ...  when using LDAP External Authentication
    ...  1. Add ldap profile and enable external user authentication
    ...  2. Check if ldap user have access to reporting and tracking page
    ...  http://tims/view-entity.cmd?ent=1231016
    [Tags]  srts  teacat  CSCvm25115  Tvh1231016c

    Set Test Variable  ${TEST_ID}  Tvh1231016c
    Run Keyword And Ignore Error  Log Out Of DUT
    Log Into DUT
    Users Edit External Authentication
    ...  LDAP
    ...  ldap_query=${LDAP_EXT_QUERY}
    ...  auth_cache_timeout=20
    ...  group_mapping=${LDAP_CLASS}:Administrator
    Commit Changes

    ${ldap_enabled}=  Users Get External Authentication
    Should Not Be Empty   ${ldap_enabled}
    Log Out Of DUT
    Log Into DUT  ${LDAP_USER_NAME}  ${LDAP_PASSWORD}
    ${is_dut_virtual}=  Is DUT A Virtual Model
    Set Suite Variable  ${is_dut_virtual}
    Run Keyword If  ${is_dut_virtual}  Assign Page Virtual
    Should Have Access To  https://${SMA}/services/email/centralized_reporting  ${PAGE_EMAIL_REPORTING}
    Should Have Access To  https://${SMA}/services/email/centralized_tracking  ${PAGE_TRACKING}
