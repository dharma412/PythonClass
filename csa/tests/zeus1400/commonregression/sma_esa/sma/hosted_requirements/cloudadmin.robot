# $Id: //prod/main/sarf_centos/tests/zeus1350/feature_acceptance_tests/hosted_requirements/cloudadmin.txt#2 $ $DateTime: 2020/07/19 23:09:50 $ $Author: vsugumar $

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

** Keywords ***
Do Suite Setup
    Set Suite Variable   ${FEATUREKEY}   cloud
    Feature Key Set Key  ${FEATUREKEY}
    Radius Client Connect   ${RADIUS_SERVER}
    ...  default_secret_str=${RADIUS_SECRET}
    Set Suite Variable   ${LOCAL_ROLE_CLOUDADMINS}   Cloud Administrator
    Set Suite Variable   ${RADIUS_GROUP_CLOUDADMINS}   radCloudadmins
    Set Suite Variable   ${RADIUS_PORT}   1812
    Set Suite Variable   ${RADIUS_USERNAME}
    ...  radius-1
    Set Suite Variable   ${RADIUS_PASSWORD}   ironport
    Radius Client Update Basic User    ${RADIUS_USERNAME}
    ...  ${RADIUS_PASSWORD}  ${RADIUS_GROUP_CLOUDADMINS}

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

    Set Suite Variable   ${LDAP_CLASS}   ldap_cloud_group
    Ldap Client Add Group
    ...  ${LDAP_CLASS}
    ...  members=${LDAP_USER_NAME}
    ...  basedn=${LDAP_BASEDN}

    Set Suite Variable   ${LDAP_PROFILE_NAME}   mainldapprofile
    Set Suite Variable   ${LDAP_EXT_QUERY}   externalauth

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

    Set Suite Variable   ${USERNAME}   cloud
    Set Suite Variable   ${FULL_NAME}   Cloud Administrator
    Set Suite Variable   ${PASSWORD}   ${DUT_ADMIN_SSW_PASSWORD}
    Users Add User   ${USERNAME}   ${FULL_NAME}
    ...  ${PASSWORD}  ${sma_user_roles.CLOUD_ADMIN}
    Commit Changes

Do Suite Teardown
   Selenium Close
   Selenium Login
   Radius Client Delete User   ${RADIUS_USERNAME}
   Radius Client Disconnect
   Ldap Client Delete Group   ${LDAP_CLASS}
   Ldap Client Delete User   ${LDAP_USER_NAME}
   Ldap Client Disconnect
   Ldap Delete Server Profile  ${LDAP_PROFILE_NAME}
   Users Delete User   ${USERNAME}
   Commit Changes
   Feature Key Delete Key   ${FEATUREKEY}

Do Common Testcase Setup
    DefaultTestCaseSetup
    Run Keyword And Ignore Error
    ...  Log Out Of DUT

Verify GUI Login OK
    [Arguments]  ${username}  ${password}
    Log Out Of DUT
    Log Into DUT  ${username}  ${password}
    ${title}=  Get Title
    Should Not Contain  ${title}  Welcome

Do Tvh701788c Setup
    Do Common Testcase Setup
    Log Into DUT  ${USERNAME}  ${PASSWORD}

    Users Edit External Authentication   RADIUS
    ...  radius_servers=${RADIUS_SERVER}:${RADIUS_PORT}:${RADIUS_SECRET}:10
    ...  auth_cache_timeout=20
    ...  group_mapping=${RADIUS_GROUP_CLOUDADMINS}:${LOCAL_ROLE_CLOUDADMINS}
    Commit Changes

Do Tvh701788c Teardown
   User Config External Setup Delete  ${RADIUS_SERVER}
   Commit Changes
   UserConfig External Setup Disable
   Commit
   DefaultTestCaseTeardown

Do Tvh701898c Setup
     Do Common Testcase Setup
     Log Into DUT  ${USERNAME}  ${PASSWORD}

     Users Edit External Authentication
     ...  LDAP
     ...  ldap_query=${LDAP_EXT_QUERY}
     ...  auth_cache_timeout=20
     ...  group_mapping=${LDAP_CLASS}:Cloud Administrator
     Commit Changes

Do Tvh701971c Teardown
     Centralized Email Reporting Disable
     Centralized Email Message Tracking Disable
     Commit Changes

Do Tvh703868c Setup
     Do Common Testcase Setup
     Log Into DUT  ${USERNAME}  ${PASSWORD}

     UserConfig External Setup LDAP
     ...  ldap_query=${LDAP_EXT_QUERY}
     ...  ext_group=${LDAP_CLASS}
     ...  role=Cloud Administrators
     Commit

Do Tvh703868c Teardown
    UserConfig External Setup Disable
    Commit
    DefaultTestCaseTeardown

Do Tvh703867c Setup
     Do Common Testcase Setup
     Log Into DUT  ${USERNAME}  ${PASSWORD}

     User Config External Setup New
     ...  ${RADIUS_SERVER}
     ...  ${RADIUS_SECRET}
     ...  reply_timeout=15
     ...  auth_type=PAP
     ...  create_mapping=yes
     ...  group_name=${RADIUS_GROUP_CLOUDADMINS}
     ...  role=Cloud Administrators
     Commit

Do Tvh703912c Setup
    Do Common Testcase Setup
#   Enable exteranl authentication using Admin user
    Log Into DUT

    Users Edit External Authentication   RADIUS
    ...  radius_servers=${RADIUS_SERVER}:${RADIUS_PORT}:${RADIUS_SECRET}:10
    ...  auth_cache_timeout=20
    ...  group_mapping=${RADIUS_GROUP_CLOUDADMINS}:${LOCAL_ROLE_CLOUDADMINS}
    Commit Changes

*** Test Cases ***
Tvh701788c
    [Documentation]  Cloud Admin - Enable External Authentication type with RADIUS User
    [Tags]  Tvh701788c  fat
    [Setup]  Do Tvh701788c Setup
    [Teardown]  Do Tvh701788c Teardown
    Set Test Variable  ${TEST_ID}  Tvh701788c

    ${radius_enabled}=  Users Get External Authentication
    Should Not Be Empty   ${radius_enabled}
    Verify GUI Login OK   ${RADIUS_USERNAME}   ${RADIUS_PASSWORD}

Tvh701898c
    [Documentation]  Cloud Admin - Enable External Authentication type with LDAP User
    [Tags]  Tvh701898c  fat
    [Setup]  Do Tvh701898c Setup
    [Teardown]  Do Tvh703868c Teardown
    Set Test Variable  ${TEST_ID}  Tvh701898c

    ${ldap_enabled}=  Users Get External Authentication
    Should Not Be Empty   ${ldap_enabled}
    Verify GUI Login OK   ${LDAP_USER_NAME}   ${LDAP_PASSWORD}

Tvh701971c
    [Documentation]  Cloud Admin - Enable and disable Centralized Reporting and Message tracking
    [Tags]  Tvh701971c  fat
    [Teardown]  Do Tvh701971c Teardown
    Set Test Variable  ${TEST_ID}  Tvh701971c

    Log Out Of Dut
    Log Into DUT   ${USERNAME}    ${PASSWORD}
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Commit Changes

Tvh703868c
    [Documentation]  Cloud Admin - Enable External Authentication as LDAP through CLI
    [Tags]  Tvh703868c  srts
    [Setup]  Do Tvh703868c Setup
    [Teardown]  Do Tvh703868c Teardown
    Set Test Variable  ${TEST_ID}  Tvh703868c

    ${ldap_enabled}=  Users Get External Authentication
    Should Not Be Empty   ${ldap_enabled}
    Verify GUI Login OK   ${LDAP_USER_NAME}   ${LDAP_PASSWORD}

Tvh703867c
    [Documentation]  Cloud Admin - Enable External Authentication type as RADIUS through CLI
    [Tags]  Tvh703867c  srts
    [Setup]  Do Tvh703867c Setup
    [Teardown]  Do Tvh701788c Teardown
    Set Test Variable  ${TEST_ID}  Tvh703867c

    ${radius_enabled}=  Users Get External Authentication
    Should Not Be Empty   ${radius_enabled}
    Verify GUI Login OK   ${RADIUS_USERNAME}   ${RADIUS_PASSWORD}

Tvh703912c
    [Documentation]  Cloud Admin - Modify external authentication from RADIUS to LDAP
    [Tags]  Tvh703912c  srts
    [Setup]  Do Tvh703912c Setup
    [Teardown]  Do Tvh703868c Teardown
    Set Test Variable  ${TEST_ID}  Tvh703912c

    ${radius_enabled}=  Users Get External Authentication
    Should Not Be Empty   ${radius_enabled}
    Verify GUI Login OK   ${RADIUS_USERNAME}   ${RADIUS_PASSWORD}

#   Now login using Cloud admin and modify RADIUS to LDAP Auth.type
    Log Out Of Dut
    Log Into DUT

    Users Edit External Authentication
    ...  LDAP
    ...  ldap_query=${LDAP_EXT_QUERY}
    ...  auth_cache_timeout=20
    ...  group_mapping=${LDAP_CLASS}:Cloud Administrator
    Commit Changes

    Verify GUI Login OK   ${LDAP_USER_NAME}   ${LDAP_PASSWORD}
