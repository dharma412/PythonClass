# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/TEACATS/sma_esa/upgrade_suites.txt#11 $ $DateTime: 2020/05/27 01:05:46 $ $Author: sumitada $

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
    Set Suite Variable   ${LDAP_USER_NAME}   ldap_2
    Set Suite Variable   ${LDAP_PASSWORD}   ironport
    ${sma_version}=  Get Dut Build
    Set Suite Variable   ${sma_version}
    LDAP Client Connect  ${LDAP_AUTH_SERVER}
    ...  ldap_server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  basedn=${LDAP_BASEDN}
    ...  binddn=${LDAP_BINDDN}
    ...  password=${LDAP_PASSWORD}
    Run keyword And Ignore Error  Ldap Client Add User
    ...  uid=${LDAP_USER_NAME}
    ...  password=${LDAP_PASSWORD}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}
    ...  mail=${LDAP_USER_NAME}@${CLIENT}

    Set Suite Variable   ${LDAP_CLASS}   ldap_group1
    Run keyword And Ignore Error  Ldap Client Add Group
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
   Commit Changes

*** Test Cases ***

CSCvp82068
    [Documentation]  Reporting page fails to load page
    ...  when using LDAP External Authentication
    ...  1. Add ldap profile with ssl enable
    ...  2. Enable external user authentication
    ...  3. Check if ldap user is able to log in
    [Tags]  srts  teacat  upgrade  CSCvp82068

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

CSCvg91079
    [Documentation]  Raid_log_watch crashes on startup
    ...  http://tims/view-entity.cmd?ent=1157623
    [Tags]  srts  teacat  upgrade  CSCvg91079  Tvh1157623c

    Set Appliance Under Test To SMA
    ${output}=  Run on DUT  echo "test" | /data/bin/raid_log_watch
    Should Not Contain  ${output}  raid_log_watch
    ${output}=  Run on DUT  grep "syslogd" /var/log/messages
    Should Not Contain  ${output}  raid_log_watch

CSCvg91149
    [Documentation]  Checking ssh keys are not regenerated
    ...     and showlicense are working after upgrade
    ...     http://tims/view-entity.cmd?ent=1157624
    [Tags]  srts  teacat  upgrade  CSCvg91149  Tvh1157624c

    Set SSHLib Timeout  10 seconds
    Open Connection  ${CLIENT_HOSTNAME}  client
    Login  ${TESTUSER}  ${TESTUSER_PASSWORD}
    Write  ssh ${DUT_ADMIN}@${SMA}
    ${out}=  Read Until Regexp  .*\\(yes\\/no\\)\\?|.*assword\\:
    ${add_to_known_hosts}=  Set Variable If  '${out.find('yes')}' !='-1'  yes  ${EMPTY}
    Run Keyword If  '${add_to_known_hosts}' != '${EMPTY}'  Write  ${add_to_known_hosts}
    Sleep  3s
    ${is_dut_virtual}  Is DUT A Virtual Model
    Set Suite Variable  ${is_dut_virtual}
    Start Cli Session If Not Open
    SmaCliLibrary.Revert  ${sma_version}  continue_revert=Yes
    ...   confirm_revert=Yes
    Wait Until DUT Reboots  timeout=1200  wait_for_ports=80,443,22,8123
    Start Cli Session If Not Open
    Update Config Dynamichost  dynamic_host=${UPDATE_SERVER}
    Update Config Validate Certificates  validate_certificates=no
    Commit
    Upgrade And Wait  ${SMA_UPGRADE_VERSION}  timeout=1200
    Open Connection  ${CLIENT_HOSTNAME}  client
    Login  ${TESTUSER}  ${TESTUSER_PASSWORD}
    Write  ssh ${DUT_ADMIN}@${SMA}
    ${out}=  Read Until Regexp  .*\\(yes\\/no\\)\\?|.*assword\\:
    Run Keyword If  '${out.find('yes')}' !='-1'  Fail
    Sleep  3s
    Restart CLI Session
    ${license_status}=  Run Keyword If  ${is_dut_virtual} is ${TRUE}
    ...  ShowLicense
    Log  ${license_status}
    Run Keyword If  ${is_dut_virtual} is ${TRUE}
    ...  Should Contain  ${license_status}  license_version
