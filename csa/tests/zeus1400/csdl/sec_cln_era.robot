# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_cln_era.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/global_sma.txt
Resource     sma/saml.txt
Resource     regression.txt
Resource     sma/csdlresource.txt

Force Tags   csdl
Suite Setup   CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${test_user_admin}  admin_cln_era
${test_user_name}  test user
${test_user_admin_password}  Cisco12$
${new_password_after_reboot}  Cisco12new$
${inactivity_timeout}  10
${default_inactivity_timeout}  30
${core_files_list_command}  cd /data/cores/ && ls -lrt

*** Keywords ***
Setup to create user data
    Run keyword and ignore error  Log Out Of Dut
    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Users Add User  ${test_user_admin}  ${test_user_name}  ${test_user_admin_password}  ${sma_user_roles.ADMIN}
    Network Access Edit Settings  timeout=${inactivity_timeout}
    Edit General Settings
    Commit Changes

Teardown to delete user data
    Run keyword and ignore error  Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Users Delete User   ${test_user_admin}
    Delete SP IDP For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Commit Changes

Setup DUT with license and password after restore
    Start CLI Session If Not Open
    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_TMP_PASSWORD}
    Load License From File

*** Test Cases ***
Tvh1217419c
   [Documentation]  Tvh1217419c-Verify erasure of physical storage to enter clean state using WIPEDATA
        ...  Tvh1217423c-Verify option is provided to wipe data with diagnostic command
        ...  Tvh1217434c-Verify status option of wipedata command
        ...  Tvh1217435c  Verify coredump option of wipedata command
        ...  FLOW DETAILS
        ...  Pre-condition: Create core files in /data/cores
        ...  cli->wipedata
        ...  Check wipedata options
        ...  Enter option -> Coredump
        ...  Verify wipedata status
        ...  Verify erasure of physical storage to enter clean state using WIPEDATA
        ...  Verify that core files are removed in data/cores

    [Tags]  cli  Tvh1217419c  Tvh1217423c  Tvh1217434c  Tvh1217435c
    [Setup]  Run On DUT  cd /data/cores/ && touch test.core

    ${core_files_before_wipedata}=  Run On DUT  ${core_files_list_command}
    ${wipedata_coredump}=  Wipedata coredump
    Should contain  ${wipedata_coredump}  wipedata: In progress
    ${wipedata_status}=  Wipedata status
    ${wipe_command_status}=  Run keyword and return status  should contain  ${wipedata_status}  Last wipedata status: Successful
    Run keyword if  '${wipe_command_status}'=='False'   Should contain  ${wipedata_status}  Last wipedata status: Fail
    ${core_files_after_wipedata}=  Run On DUT  ${core_files_list_command}
    Should contain  ${core_files_after_wipedata}  total 0
    Should not be equal  ${core_files_before_wipedata}  ${core_files_after_wipedata}

Tvh1217432c
    [Documentation]  Tvh1217432c-Verify after performing wipe operation through reload user is able to configure system
        ...  Tvh1217431c-Verify erasure of physical storage security when performed with wipe data of diagnostic-> Reload command
        ...  FLOW DETAILS
        ...  Pre-Condition: Configure User data and other data.
        ...  cli -> Diagnostic --> Reload
        ...  Enter ""Y"" for want to continue and really wants to continue
        ...  Do you want to wipe also?[N] --> Y
        ...  Verify system goes to reboot
        ...  Once system comes up perform SSW, User Creation, Change password and other operations.
        ...  Check : User is able to configure system once after wipe performed through reload.
        ...  Verify that all the data is removed and all the configurations are set to default

    [Tags]  cli  gui Tvh1217431c  Tvh1217432c
    [Setup]  Setup to create user data
    [Teardown]   Run keywords  Reset password to default  ${new_password_after_reboot}
    ...  AND  Teardown to delete user data

    ${before_reboot_gui_timeout}=  Network access get gui timeout
    Diagnostic Reload  confirm=yes  wipedata=yes
    Wait until DUT Is Accessible    wait_for_ports=${DUT_PORT}    timeout=360
    Setup DUT with license and password after restore
    Selenium Login
    System setup wizard run  testuser@mail.qa
    SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Users Add User  ${test_user_admin}  ${test_user_name}  ${test_user_admin_password}  ${sma_user_roles.ADMIN}
    ${after_reboot_gui_timeout}=  Network access get gui timeout
    Should not be equal   ${after_reboot_gui_timeout}  ${before_reboot_gui_timeout}
    Should be equal  ${after_reboot_gui_timeout}  ${default_inactivity_timeout}
    Commit Changes
    Change password via CLI  ${DUT_ADMIN_SSW_PASSWORD}  ${new_password_after_reboot}

Tvh1217430c
    [Documentation]  Tvh1217430c-Verify erasure of physical storage to enter clean state using DIAGNOSTIC
        ...  FLOW DETAILS
        ...  Pre-Condition: Configure User data and other data.
        ...  cli -> Diagnostic --> Reload
        ...  Enter ""Y"" for want to continue and really wants to continue
        ...  Do you want to wipe also?[N] --> N
        ...  Verify system goes to reboot
        ...  Verify device is now in clean state - all options are in default state
    [Tags]  cli  gui Tvh1217430c
    [Setup]  Setup to create user data
    [Teardown]  Teardown to delete user data

    ${before_reboot_gui_timeout}=  Network access get gui timeout
    Diagnostic Reload  confirm=yes
    Wait until DUT Is Accessible    wait_for_ports=${DUT_PORT}    timeout=360
    Setup DUT with license and password after restore
    Selenium Login
    System setup wizard run  testuser@mail.qa
    ${after_reboot_gui_timeout}=  Network access get gui timeout
    Should be equal  ${after_reboot_gui_timeout}  ${default_inactivity_timeout}
    Should not be equal   ${after_reboot_gui_timeout}  ${before_reboot_gui_timeout}
    ${analytics_after_reboot}=  Get general analytics setting status
    Should be True   ${analytics_after_reboot}
    ${saml_status}=  Run keyword and return status  SAML Add SP And IDP Profile For Customer  ${TEST_NAME}  ${TEST_IDP_PROFILE}
    Should be True  ${saml_status}
    ${user_add_status}=  Run keyword and return status  Users Add User  ${test_user_admin}  ${test_user_name}  ${DUT_ADMIN_SSW_PASSWORD}  ${sma_user_roles.ADMIN}
    Should be True  ${user_add_status}
    Commit Changes
