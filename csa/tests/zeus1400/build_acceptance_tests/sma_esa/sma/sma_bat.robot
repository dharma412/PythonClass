# $Id: //prod/main/sarf_centos/tests/zeus1350/build_acceptance_tests/sma_bat.txt#2 $
# $DateTime: 2020/01/15 23:08:52 $
# $Author: vsugumar $

*** Settings ***
Resource  sma/esasma.txt
Resource  sma/backdoor_snippets.txt
Library   OperatingSystem
Library   String

Suite Setup  Do Suite Setup
Suite Teardown  Do Suite Teardown

*** Variables ***
${DATA_UPDATE_TIMEOUT}=  5m
${RETRY_TIME}=  10s
${LOCKED_USERNAME} =   lockeduser
${EXPIRED_USERNAME} =  expireduser
${PWD_USERNAME} =      pwdtestuser
${SMA_VERSION} =  ${Empty}
${BUILD_PREFIX} =  zeus-
${PROFILE_NAME} =  sma_bat
${LICENSE_NAME}=  smalicense.xml

${VESA_LICENSE_FILE_ON_LOCAL}=  %{SARF_HOME}/tests/testdata/virtual/${LICENSE_NAME}
${VESA_LICENSE_FILE_ON_DUT}=  ${LICENSE_NAME}

*** Keywords ***
Do Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup
    Selenium Login
    Init BAT Common Variables

    Add LDAP Users
    ${ip} =  Get Host IP By Name  ${SMA2}
    Set Suite Variable  ${SMA2_IP}  ${ip}
    ${INITIAL_CONFIG}=  Save Config From DUT
    Set Suite Variable  ${INITIAL_CONFIG}
    Log Out Of Dut
    Log Into Dut
    Wait Until Keyword Succeeds  5 minutes  15 seconds
    ...  Start CLI Session If Not Open
    Set Host Name  ${SMA}
    Commit
    Library Order Sma2
    Run Keyword And Ignore Error  Passwd  ${DUT_ADMIN_PASSWORD}  ${DUT_ADMIN_SSW_PASSWORD}
    Commit
    Library Order Sma

Do Suite Teardown
    Run keyword and ignore error  Remove LDAP Users
    DefaultTestSuiteTeardown

Do Tvh544837c Setup
    DefaultTestCaseSetup
    Users Edit Password Rules  req_alpha=0
    ...  req_number=0  req_special_char=0  ban_username=0
    Commit Changes
    FOR  ${username}  IN  ${locked_username}  ${expired_username}
        Users Add User  ${username}  ${username}  ${RTESTER_PASSWORD}
    END
    Commit Changes
    Users Edit Password Rules  req_min_chars=10  req_alpha=1
    ...  req_number=1  req_special_char=1  ban_username=1
    Users Edit Account Locking  1
    Users Edit Reset Rules  admin_change=on
    Commit Changes

Do Tvh544837c Teardown
    Login As Admin
    Users Edit Reset Rules  admin_change=off
    Users Edit Account Locking  5
    Users Edit Account Locking  lock_failed_login=${False}
    Users Edit Password Rules  req_min_chars=8
    Commit Changes
    FOR  ${username}  IN  ${locked_username}  ${expired_username}
        Users Delete User  ${username}
    END
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh544850c Setup
    DefaultTestCaseSetup
    Wait For Backup Finish
    Sync Disk Quotas  SMA  SMA2

Do Tvh544850c Teardown
    Wait For Backup Finish
    DefaultTestCaseTeardown

Do Tvh544839c Setup
    DefaultTestCaseSetup
    SmaCliLibrary.Restart CLI Session

Do Tvh544839c Teardown
    SmaCliLibrary.Resume
    DefaultTestCaseTeardown

Do Tvh544816c Setup
    DefaultTestCaseSetup

Do Tvh544816c Teardown
    DefaultTestCaseTeardown

Login As
    [Arguments]  ${user_name}  ${password}
    Run Keyword And Ignore Error  Log Out Of DUT
    Login To DUT  ${user_name}  ${password}

Login As Admin
    Login As  admin  ${RTESTER_PASSWORD}

Verify Account Settings
    [Arguments]  ${user_name}  ${exp_status}=${EMPTY}  ${exp_expiration}=${EMPTY}
    [Documentation]
    ...  Verifies status and/or expiration field for
    ...  user ${user_name}
    ${users_info} =  Users Get List
    ${user_info} =  Get From Dictionary  ${users_info}  ${user_name}
    ${user_acc_status} =  Get From List  ${user_info}  2
    Run Keyword If  '${exp_status}' <> ''
    ...  Should Be Equal As Strings  ${user_acc_status}  ${exp_status}
    ${user_pass_status} =  Get From List  ${user_info}  3
    Run Keyword If  '${exp_expiration}' <> ''
    ...  Should Be Equal As Strings  ${user_pass_status}  ${exp_expiration}

Verify Password Requirements
    [Arguments]  ${user_name}
    [Documentation]
    ...  Verifies strong passwords \n
    ...  policies for ${user_name}
    @{weak_passwords} =  Create List  1234567
    ...  ${user_name}  1234567890a  qwertyASDFG
    ...  qwerASDF12  ~?!@#$%^&*-_  $%^qweqwe12313
    ...  $%^$%^werewASDASD  1231312$%^&$%^$%^
    FOR  ${password}  IN  @{weak_passwords}
        Run Keyword And Expect Error  *  Users Add User  ${user_name}  ${user_name}  ${password}
    END

Verify Account Locking
    [Arguments]  ${user_name}  ${password}
    [Documentation]
    ...  Verifies if particular account \n
    ...  ${user_name} can be sucessfully locked
    # Log in with incorrect password for the first time
    Login As  ${user_name}  wrong password
    Current Frame Should Contain  Error
    Login As Admin
    Verify Account Settings  ${user_name}  Locked
    Login As  ${user_name}  ${password}
    # Now account is locked and can not be logged even with correct password
    Current Frame Should Contain  Error
    Login As Admin

Verify Account Expiration
    [Arguments]  ${user_name}
    [Documentation]
    ...  Verifies if particular account \n
    ...  ${user_name} can be successfully expired
    ${new_password} =  Set Variable  123454323Aa$
    Users Edit User  ${user_name}  password=${new_password}
    Commit Changes
    Verify Account Settings  ${user_name}  ${EMPTY}  Expired
    Login As  ${user_name}  ${new_password}
    ${current_title} =  Get Title
    Should Contain  '${current_title}'  Change Password
    Login As Admin

Do Tvh544835c Setup
    DefaultTestCaseSetup

Do Tvh544835c Teardown
    Login As  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  timeout=30
    Commit Changes
#    Go To  /
    DefaultTestCaseTeardown

Create User
    [Arguments]  ${user_name}  ${pwd_user_name}
    Users Add User  ${user_name}  ${user_name}  ${pwd_user_name}
    Commit Changes

Get SMA Version
    ${_build_installed} =  Version
    Log  ${_build_installed}
    ${_sma_version} =  Evaluate
    ...  re.search('Version: ([0-9]+\.[0-9]+\.[0-9]+-[0-9]+)', '''${_build_installed}''').group(1)
    ...  re
    Log  ${_sma_version}
    [Return]  ${_sma_version}

Check If User Exists
    [Arguments]  ${user_name}
    ${users_info} =  Users Get List
    Log  ${users_info}
    Dictionary Should Contain Key  ${users_info}  ${user_name}

Check If User Does Not Exist
    [Arguments]  ${user_name}
    ${users_info} =  Users Get List
    Log  ${users_info}
    Dictionary Should Not Contain Key  ${users_info}  ${user_name}

Suspend Reset Load and Resume DUT
    [Arguments]  ${config_file}
    [Documentation]  Suspend, reset and resume DUT
    Suspend  10
    Reset Config  yes
    Wait Until Keyword Succeeds  5 minutes  15 seconds
    ...  Start CLI Session If Not Open
    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Resume
    Load Config On DUT  ${config_file}
    Restart CLI Session
    Commit  comment=${DUT} reset.

Check Backup In Log
    [Arguments]  ${name}  ${ip}  ${timeout}
    [Documentation]  Search log for strings to verify backup steps
    @{result} =  Log Search
    ...  BACKUP: Starting the backup\\(${name}\\) to ${ip}  search_path=/data/pub/backup_logs  timeout=${timeout}
    ${result_len} =  Get From List  ${result}  0
    Should Be True  ${result_len} > 0
    @{result} =  Log Search
    ...  BACKUP: COMPLETED: Backup job\\(${name}\\) for ${SMA} scheduled to start at.*?to ${ip} successfully completed
    ...  search_path=/data/pub/backup_logs  timeout=${timeout}
    ${result_len} =  Get From List  ${result}  0
    Should Be True  ${result_len} > 0

Is Backup Finished
    ${out} =  Backup Config View
    ${no_backups} =  Evaluate
    ...  '''${out}'''.find('No scheduled backups.') >= 0
    Should Be True  ${no_backups}

Wait For Backup Finish
    [Documentation]  Waiting for previous log operations finish, so it will
    ...  be possible to start new backup immediately
    Wait Until Keyword Succeeds  30 minutes  20 seconds
    ...  Is Backup Finished

Do Tvh544847c Setup
    DefaultTestCaseSetup
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Spam Quarantine Enable  interface=Management  port=6025
    Spam Quarantine Edit EndUser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=LDAP
    Spam Quarantine SLBL Enable
    Ldap Add Server Profile
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}
    ...  base_dn=${LDAP_BASEDN}
    ...  auth_method=anonymous
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    Ldap Edit Isq End User Authentication Query
    ...  ${PROFILE_NAME}
    ...  query_name=${PROFILE_NAME}.isq_auth
    ...  query_string=(uid={u})
    ...  email_attrs=mail
    ...  activate=${True}
    Commit Changes  ${SMA} configured.
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Go To Euq Gui  ${isq_user}@${CLIENT}  ${RTESTER_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete

Do Tvh544847c Teardown
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To Main Gui
#    LDAP Delete Server Profile  ${PROFILE_NAME}
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh544842c Setup
    DefaultTestCaseSetup

Do Tvh544842c Teardown
    DefaultTestCaseTeardown

Do Load License
    ${license_content}=  OperatingSystem.Get File  ${VESA_LICENSE_FILE_ON_LOCAL}
    ${license_paste_return}=  SMACliLibrary.Load License  conf=paste_via_cli  paste_conf=${license_content}

*** Test Cases ***
Tvh544847c
    [Documentation]  Verify that you can specify email address in IPv4 and IPv6
    ...  format in blocklist
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544847c
    [Tags]  autobat  Tvh544847c
    [Setup]  Do Tvh544847c Setup
    [Teardown]  Do Tvh544847c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544847c

    Turn SLBL Entries  Add
    @{blocklist_entries} =  BlockList Get
    Log  ${blocklist_entries}
    Turn SLBL Entries  Delete
    @{blocklist_entries} =  BlockList Get
    Log  ${blocklist_entries}

Tvh544835c
    [Tags]  Tvh544835c  autobat
    [Documentation]  Verify that GUI Timeout feature
    ...  works properly for SMA web interface
    [Setup]  Do Tvh544835c Setup
    [Teardown]  Do Tvh544835c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544835c

    ${timeout} =  Set Variable  5
    ${default_timeout} =  Network Access Get Gui Timeout
    Should Be Equal As Integers  ${default_timeout}  30
    Network Access Edit Settings  timeout=${timeout}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Commit Changes
    Sleep  ${timeout} minutes 1 second
    Run Keyword And Ignore Error  Navigate To  Web  Utilities  Publish to Web Appliances
    Page Should Contain  Username:
    Page Should Contain  Passphrase:
    Log Into Dut

Tvh544837c
    [Tags]  Tvh544837c  skip_autobat
    [Documentation]  Verify that Strong Password Controls are
    ...  working properly\n
    ...  Test case fails due to the bug CSCuw57763
    [Setup]  Do Tvh544837c Setup
    [Teardown]  Do Tvh544837c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544837c

    Verify Account Settings  ${LOCKED_USERNAME}  Active  n/a
    Verify Password Requirements  ${PWD_USERNAME}
    Verify Account Locking  ${LOCKED_USERNAME}  ${RTESTER_PASSWORD}
    Verify Account Expiration  ${EXPIRED_USERNAME}

Tvh544850c
    [Documentation]  Verify that users can choose single features for backups
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh544850c\n
    ...  Testcase teardown section fails due to the bug CSCul10478
    [Tags]  Tvh544850c  autobat
    [Setup]  Do Tvh544850c Setup
    [Teardown]  Do Tvh544850c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544850c
    Set Test Variable  ${passwd}  ${DUT_ADMIN_SSW_PASSWORD}

    Roll Over Now
    Backup Config Schedule  job_name=backup_job  backup_type=now  ip=${SMA2_IP}
    ...  name=dst_sma  user=admin  passwd=${passwd}  backup_all=no  backup_isq=yes
    ...  backup_email_tracking=no  backup_reporting=no  backup_reporting=no
    ...  backup_slbl=no  backup_web_tracking=no  backup_policy_quarantine=no
    Wait For Backup Finish
    Check Backup In Log  backup_job  ${SMA2_IP}  30

    Backup Config Schedule  job_name=backup_job  backup_type=now  ip=${SMA2_IP}
    ...  name=dst_sma  user=admin  passwd=${passwd}  backup_all=no  backup_isq=no
    ...  backup_email_tracking=yes  backup_reporting=no  backup_reporting=no
    ...  backup_slbl=no  backup_web_tracking=no  backup_policy_quarantine=no
    Wait For Backup Finish
    Check Backup In Log  backup_job  ${SMA2_IP}  30

    Backup Config Schedule  job_name=backup_job  backup_type=now  ip=${SMA2_IP}
    ...  name=dst_sma  user=admin  passwd=${passwd}  backup_all=no  backup_isq=no
    ...  backup_email_tracking=no  backup_reporting=yes
    ...  backup_slbl=no  backup_web_tracking=no  backup_policy_quarantine=no
    Wait For Backup Finish
    Check Backup In Log  backup_job  ${SMA2_IP}  30

    Backup Config Schedule  job_name=backup_job  backup_type=now  ip=${SMA2_IP}
    ...  name=dst_sma  user=admin  passwd=${passwd}  backup_all=no  backup_isq=no
    ...  backup_email_tracking=no  backup_reporting=no
    ...  backup_slbl=yes  backup_web_tracking=no  backup_policy_quarantine=no
    Wait For Backup Finish
    Check Backup In Log  backup_job  ${SMA2_IP}  30

    Set Test Variable  ${name}  test2-1
    Backup Config Schedule  job_name=${name}  backup_type=now
    ...  ip=${SMA2_IP}  name=dst_sma  user=admin  passwd=${passwd}
    ...  backup_all=no  backup_isq=yes  backup_email_tracking=yes
    ...  backup_reporting=no  backup_slbl=no  backup_web_tracking=no
    ...  backup_policy_quarantine=no
    Wait For Backup Finish
    Check Backup In Log  ${name}  ${SMA2_IP}  5

    Set Test Variable  ${name}  test2-2
    Backup Config Schedule  job_name=${name}  backup_type=now
    ...  ip=${SMA2_IP}  name=dst_sma  user=admin  passwd=${passwd}
    ...  backup_all=no  backup_reporting=yes  backup_email_tracking=yes
    ...  backup_slbl=no  backup_web_tracking=no  backup_isq=no
    ...  backup_policy_quarantine=no
    Wait For Backup Finish
    Check Backup In Log  ${name}  ${SMA2_IP}  5

    Set Test Variable  ${name}  backup-all
    Backup Config Schedule  job_name=${name}  backup_type=now
    ...  ip=${SMA2_IP}  name=dst_sma  user=admin  passwd=${passwd}  backup_all=yes
    Wait For Backup Finish
    Check Backup In Log  ${name}  ${SMA2_IP}  5

Tvh544839c
    [Tags]  Tvh544839c  autobat
    [Documentation]
    ...  Verify that configuration can be saved
    ...  and restored using save/loadconfig\n
    ...  Testcase teardown section fails due to the bug CSCur50771
    [Setup]  Do Tvh544839c Setup
    [Teardown]  Do Tvh544839c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544839c

    ${sma_config_file} =  Save Config From DUT
    Log  ${sma_config_file}
    Suspend Reset Load and Resume DUT  ${sma_config_file}

Tvh544816c
    [Tags]  Tvh544816c  autobat
    [Documentation]  Netinstall SMA and run default SSW
    ...  Runs on the specified build ${SMA_VERSION}
    ...  If fails, cancels the execution \n
    ...  Testcase teardown section fails due to the bug CSCur50771
    [Setup]  Do Tvh544816c Setup
    [Teardown]  Do Tvh544816c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544816c

    ${SMA_VERSION}  Get Dut Build
    ${_build} =  Evaluate  re.match('[^0-9]*' + "(.*)", '${SMA_VERSION}').group(1)  re
    Netinstall  build_id_regex=${BUILD_PREFIX}.*${_build}  wait_for_ports=80,443,22
    Start CLI Session If Not Open
    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Do Load License
    Suspend  10
    Reset Config  yes
    global_sma.Configure SSL For GUI
    Selenium Login
    Go To Main Gui
    System Setup Wizard Run  ${ALERT_RCPT}  hostname=${SMA}

Tvh544842c
    [Tags]  Tvh544842c  autobat
    [Documentation]
    ...  Verify if machine can be reverted to the same build\n
    ...  Testcase teardown section fails due to the bug CSCur50771
    [Setup]  Do Tvh544842c Setup
    [Teardown]  Do Tvh544842c Teardown
    Set Test Variable  ${TEST_ID}  Tvh544842c

    Create User  ${PWD_USERNAME}  ${DUT_ADMIN_SSW_PASSWORD}
    Check If User Exists  ${PWD_USERNAME}
    ${current_sma_version} =  Get SMA Version

    Revert
    ...  version=${current_sma_version}
    ...  continue_revert=yes
    ...  confirm_revert=yes
    Wait Until DUT Reboots  timeout=1200  wait_for_ports=80,443,22,8123
    Start CLI Session

    global_sma.Configure SSL For GUI
    Selenium Login
    Check If User Does Not Exist  ${PWD_USERNAME}
    ${post_revert_sma_version} =  Get SMA Version
    Should Be Equal As Strings  ${current_sma_version}  ${post_revert_sma_version}
