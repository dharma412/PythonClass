# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_cln_usr.txt#1 $
# $Date: 2020/05/27 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     csdlresource.txt

Force Tags   csdl
Suite Setup   CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${reboot_timeout}  360
@{all_feature_keys}  1
    ...  2
    ...  3

*** Keywords ***
Get all available feature keys
    @{all_feature_keys}=  Feature keys get all keys
    get length  Feature keys get all keys
    ${all_feature_keys_list}=  Create list
    FOR  ${license}  IN  @{all_feature_keys}
        Append to list  ${all_feature_keys_list}  ${license}
    END
    Log list  ${all_feature_keys_list}
    [Return]   ${all_feature_keys_list}

*** Test Cases ***
Tvh1340560c
    [Documentation]  Tvh1340560c-Erase user data to enter clean state  ID
        ...  FLOW DETAILS
        ...  Pre-Condition: Configure User data
        ...  cli -> Diagnostic --> Reload
        ...  Enter ""Y"" for want to continue and really wants to continue
        ...  Do you want to wipe also?[N] --> Y
        ...  Verify system goes to reboot
        ...  Verify command has removed all user settings and reset the entire device.
        ...  If Virtual device- All feature keys have been removed,and the license must be reapplied.

    [Tags]  cli  gui Tvh1340560c

    Run keyword and ignore error  Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Get all available feature keys
    ${feature_keys}=  Get all available feature keys
    Should not be empty  ${feature_keys}
    Diagnostic Reload  confirm=yes  wipedata=yes
    Wait until DUT Is Accessible    wait_for_ports=${DUT_PORT}    timeout=${reboot_timeout}
    Start CLI Session If Not Open
    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_TMP_PASSWORD}
    Selenium Login
    Navigate To  System Administration  Feature Keys
    ${feature_keys_after_reboot}=   Get all available feature keys
    Should be empty  ${feature_keys_after_reboot}
    Load License From File
    ${feature_keys_after_loadlicense}=  Get all available feature keys
    Should not be empty  ${feature_keys_after_loadlicense}