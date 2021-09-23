# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_pwd_chkchg.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Library      BuiltIn
Library      String
Resource     sma/global_sma.txt
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${required_password_length}             6
${new_required_password_length}         10
${default_password_length}              8
${test_user_admin_1}                    admin_pwd_chkchg_1
${test_user_admin_2}                    admin_pwd_chkchg_2
${test_user_name_1}                     test user1
${test_user_name_2}                     test user2
${test_user_admin_password}             Cisco12$
${test_user_group}                      Administrator
${less_than_criteria_password}          Cisco12@
${less_than_criteria_password_error}   .*at least ${new_required_password_length} characters.*

*** Keywords ***
Update password length
    [Arguments]  ${password_length}
    Users Edit Password Rules  req_min_chars=${password_length}
    Commit Changes

*** Test Cases ***
Tvh1340921c
    [Documentation]  Tvh1340921c-Restrict passphrases only at change time
        ...  FLOW DETAILS
        ...  Set password Strength to atleast 6 characters
        ...  Create two new users with password length as 8 characters
        ...  Set password strength to atleast 10 characters after new users creation
        ...  Verify user logins are successful after changing password strength and no errors thrown for new password length
        ...  Try changing pasword of user and user should be able to set password characters more than 10 only

    [Tags]  gui  cli  Tvh1340921c
    [Teardown]  Run Keywords  Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  AND  Users Delete User   ${test_user_admin_1}
    ...  AND  Users Delete User   ${test_user_admin_2}
    ...  AND  Update password length  ${default_password_length}

    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Update password length  ${required_password_length}
    User Config New  ${test_user_admin_1}  ${test_user_name_1}  ${test_user_admin_password}  ${test_user_group}
    User Config New  ${test_user_admin_2}  ${test_user_name_2}  ${test_user_admin_password}  ${test_user_group}
    Commit
    Update password length  ${new_required_password_length}
    Login to SMA via GUI  ${test_user_admin_1}  ${test_user_admin_password}
    Log Out Of Dut
    Login to SMA via GUI  ${test_user_admin_2}  ${test_user_admin_password}
    Run keyword and ignore error  Change password  ${test_user_admin_password}  ${less_than_criteria_password}
    Verify password change error message   ${less_than_criteria_password_error}