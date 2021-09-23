# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/TEACATS/sma_esa/CSCvp82068.txt#1 $ $DateTime: 2019/11/13 21:45:18 $ $Author: sarukakk $

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
    ...  use_ssl=${TRUE}

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

*** Test Cases ***

CSCvp82068
    [Documentation]  Reporting page fails to load page
    ...  when using LDAP External Authentication
    ...  1. Add ldap profile with ssl enable
    ...  2. Enable external user authentication
    ...  3. Check if ldap user is able to log in
    [Tags]  srts  teacat  CSCvp82068

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
    Run keyword And Ignore Error  Log Into DUT  ${LDAP_USER_NAME}  ${LDAP_PASSWORD}
    Run keyword And Ignore Error  Log Out Of DUT
    Start Cli Session If Not Open
    Update Config Dynamichost  dynamic_host=${UPDATE_SERVER}
    Update Config Validate Certificates  validate_certificates=no
    Commit
    Upgrade And Wait  ${SMA_UPGRADE_VERSION}  timeout=1200
    Log Into DUT  ${LDAP_USER_NAME}  ${LDAP_PASSWORD}
