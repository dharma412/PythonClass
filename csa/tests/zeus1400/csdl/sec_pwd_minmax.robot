# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_pwd_minmax.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Library      BuiltIn
Library      String
Resource     sma/global_sma.txt
Resource     sma/csdlresource.txt

Force Tags   csdl
Suite Setup   CSDL Suite Setup
#Suite Teardown  CSDL Suite Teardown

*** Variables ***
${required_password_length}  10
${default_password_length}  8
${password_with_upper_limit}  Cisco12new$
${password_below_expected_limit}  abc
${128_character_password}  &$Cisco12$$Cisco21$$Cisco34$$Cisco43$$Cisco56$$Cisco65$$Cisco78$$Cisco87$$Cisco90$$Cisco09$$Ciscoa1$$Cisco1a$$Cisco2a$$Ciscoa2$&
${greater_than_128_character_password}  greaterthan128&$Cisco12$$Cisco21$$Cisco34$$Cisco43$$Cisco56$$Cisco65$$Cisco78$$Cisco87$$Cisco90$$Cisco09$$Ciscoa1$$Cisco1a$$Cisco2a$$Ciscoa2$&
${cli_authentication_login_failure_message}  Too many authentication failures
${password_below_expected_limit_error}  Following criteria for passphrase are not met:\n- at least ${required_password_length} characters.\n- at least one upper (A-Z) and one lower (a-z) case letter.\n- at least one number (0-9).\n- at least one special character.
${syssetup_password_below_expected_limit_error}  Following criteria for passphrase are not met:\n- at least 8 characters.\n- at least one upper (A-Z) and one lower (a-z) case letter.\n- at least one number (0-9).\n- at least one special character.
${greater_than_128_char_password_error_msg}  Following criteria for passphrase are not met: - at most 128 characters.
${greater_than_128_char_password_error_msg_cli}  Following criteria for passphrase are not met:\\n- at most 128 characters.
${error_msg_morelink}  //span[text()='more']
${error_message_more_popup}  //div[@class='bd']
${header_logo}      //*[@id='header']//following::a

*** Keywords ***
Update password length
    [Arguments]  ${admin_user}  ${admin_password}  ${password_length}

    Run keyword and ignore error  Login To DUT  ${admin_user}  ${admin_password}
    Users Edit Password Rules  req_min_chars=${password_length}
    Commit Changes
    Run keyword and ignore error  Log Out Of Dut

Verify password change error message
    [Arguments]  ${error_message}

    Sleep  1
    Click Element  ${error_msg_morelink}
    ${text} =  Get Text  ${error_message_more_popup}
    should contain   ${text}  ${error_message}

Verify password change error message in CLI
    [Arguments]  ${string}  ${error_message}

    ${error_tuple}=  Get Substring  ${string}  1
    ${tuple_to_str}=  Catenate  ${error_tuple}
    should contain   ${tuple_to_str}   ${error_message}

Teardown System Setup Wizard
    Click Element  ${header_logo}

*** Test Cases ***
Tvh1210389c

    [Documentation]  Tvh1210389c-Verify the password change in CLI with less than 128 characters and greater than the characters set in Password settings field and verify the ability to login in both CLI and GUI
    ...  FLOW DETAILS
    ...  Precondition - Navigate to System Setup wizard-> Users-> Local User and password settings -> Edit settings and set the Minimum password length.
    ...  SMA CLI -> passwd
    ...  Change password to a password less than 128 characters and greater than password setting value
    ...  Verify sucessful password change
    ...  Verify login in CLI and GUI
    ...  Post condition - Reset password length to default value

    [Tags]  cli  Tvh1210389c
    [Setup]  Update password length  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}  ${required_password_length}
    [Teardown]  Run keywords  Update password length  ${DUT_ADMIN}  ${password_with_upper_limit}  ${default_password_length}
    ...  AND  Reset password to default  ${password_with_upper_limit}
    ...  AND  Set SSHLib Prompt  ${empty}

    Change password via CLI  ${DUT_ADMIN_SSW_PASSWORD}  ${password_with_upper_limit}
    Commit
    Login to DUT and check login is successful  ${DUT_ADMIN}   ${password_with_upper_limit}
    Connect to SMA  ${DUT_ADMIN}   ${password_with_upper_limit}

Tvh1210384c
    [Documentation]  Tvh1210384c-Verify in GUI that change password fields is not accepting the password greater than 128 characters
        ...  FLOW DETAILS
        ...  Check successful login to SMA via GUI
        ...  GUI--> Options-->Change passphrase
        ...  Try to change password to  greater than 128 character password.
        ...  Verify error message.

    [Tags]  gui  Tvh1210384c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run keyword and ignore error  Change password  ${DUT_ADMIN_SSW_PASSWORD}  ${greater_than_128_character_password}
    Verify password change error message   ${greater_than_128_char_password_error_msg}
    Log Out Of Dut

Tvh1210385c
    [Documentation]  Tvh1210385c-Verify in CLI that change password fields is not accepting the password greater than 128 characters
        ...  FLOW DETAILS
        ...  Check successful CLI
        ...  cli --> passwd
        ...  Try to change password to new greater than 128 character password.
        ...  Verify error message.

    [Tags]  cli  Tvh1210385c

    ${str1}=  Run keyword and ignore error  Change password via CLI  ${DUT_ADMIN_SSW_PASSWORD}  ${greater_than_128_character_password}
    Verify password change error message in CLI  ${str1}  ${greater_than_128_char_password_error_msg_cli}

Tvh1210386c
    [Documentation]  Tvh1210386c-Verify by changing the password in GUI with 128 characters and able to login with new password In both CLI and GUI
        ...  FLOW DETAILS
        ...  Check successful login to SMA via GUI and change password.
        ...  SMA GUI-> Change Passphrase
        ...  Change password to new 128 character password.
        ...  Login to CLI with new password and user should be able to login successfully.
        ...  Login to GUI with new password and user should be able to login successfully.

    [Tags]  gui  cli  Tvh1210386c
    [Teardown]  Run keywords  Reset password to default  ${128_character_password}
    ...  AND  Set SSHLib Prompt  ${empty}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Change password  ${DUT_ADMIN_SSW_PASSWORD}  ${128_character_password}
    Commit Changes
    Log Out Of Dut
    Login to DUT and check login is successful  ${DUT_ADMIN}  ${128_character_password}
    Connect to SMA  ${DUT_ADMIN}  ${128_character_password}

Tvh1210387c
    [Documentation]  Tvh1210387c-Verify by changing the password in CLI with 128 characters and able to login with new password in both CLI and GUI
        ...  FLOW DETAILS
        ...  Connect to SMA and change password.
        ...  cli --> passwd
        ...  Change password to new 128 character password.
        ...  Login to CLI with new password and user should be able to login successfully.
        ...  Login to GUI with new password and user should be able to login successfully.

    [Tags]  gui  cli  Tvh1210387c
    [Teardown]  Run keywords  Reset password to default  ${128_character_password}
    ...  AND  Set SSHLib Prompt  ${empty}

    Change password via CLI  ${DUT_ADMIN_SSW_PASSWORD}  ${128_character_password}
    Commit
    Connect to SMA  ${DUT_ADMIN}  ${128_character_password}
    Login to DUT and check login is successful  ${DUT_ADMIN}  ${128_character_password}

Tvh1210379c
    [Documentation]  Tvh1210379c-Verify that password field is not accepting the password less than that is set in Password settings field in GUI
        ...  FLOW DETAILS
        ...  Precondition - Navigate to System Setup wizard-> Users-> Local User and password settings -> Edit settings and set the Minimum password length.
        ...  Management Appliance -> System Administration -> System setup wizard
        ...  Accept the license, Go next.
        ...  In the password field give some password less than which we have set in password settings field and try to Go next
        ...  Check error message in GUI
        ...  Post condition - Reset password length to default value

    [Tags]  gui  Tvh1210379c
    [Setup]  Update password length  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}  ${required_password_length}
    [Teardown]  Run keywords  Teardown System Setup Wizard
    ...  AND  Update password length  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}  ${default_password_length}
    ...  AND  Reset password to default  ${DUT_ADMIN_TMP_PASSWORD}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    System setup wizard run password change  testuser@mail.qa
    ...  passwd=${password_below_expected_limit}
    Verify password change error message  ${syssetup_password_below_expected_limit_error}

Tvh1210380c
    [Documentation]  Tvh1210380c-Verify that password field is not accepting the password greater than 128 characters while Setting
        ...  FLOW DETAILS
        ...  Check successful login to SMA via GUI and change password.
        ...  Management Appliance -> System Administration -> System setup wizard
        ...  Accept the license, Go next.
        ...  Enter Password greater than 128 characters
        ...  Verify error

    [Tags]  gui  Tvh1210380c
    [Teardown]  Run keywords  Teardown System Setup Wizard
    ...  AND  Run keyword and ignore error  Reset password to default  ${DUT_ADMIN_TMP_PASSWORD}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    System setup wizard run password change  testuser@mail.qa
    ...  passwd=${greater_than_128_character_password}
    Verify password change error message  Following criteria for passphrase are not met:\n- at most 128 characters.

Tvh1210388c

    [Documentation]  Tvh1210388c-Verify the password change in GUI with less than 128 characters and greater than the characters set in Password settings field and verify the ability to login in both CLI and GUI.
    ...  FLOW DETAILS
    ...  Precondition - Navigate to System Setup wizard-> Users-> Local User and password settings -> Edit settings and set the Minimum password length.
    ...  Navigate to Options -> Change password in the top right corner
    ...  Change password to a password less than 128 characters and greater than password setting value
    ...  Verify sucessful password change
    ...  Verify login in CLI and GUI
    ...  Post condition - Reset password length to default value

    [Tags]  gui  cli  Tvh1210388c
    [Setup]  Update password length  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}  ${required_password_length}
    [Teardown]  Run keywords  Update password length  ${DUT_ADMIN}  ${password_with_upper_limit}  ${default_password_length}
    ...  AND  Reset password to default  ${password_with_upper_limit}
    ...  AND  Set SSHLib Prompt  ${empty}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Change password  ${DUT_ADMIN_SSW_PASSWORD}  ${password_with_upper_limit}
    Commit Changes
    Log Out Of Dut
    Login to DUT and check login is successful  ${DUT_ADMIN}   ${password_with_upper_limit}
    Connect to SMA  ${DUT_ADMIN}   ${password_with_upper_limit}

Tvh1210381c
    [Documentation]  Tvh1210381c-Verify that Password field is accepting the password with 128 characters and able to login in GUI and CLI
        ...  FLOW DETAILS
        ...  Check successful login to SMA via GUI and change password.
        ...  Management Appliance -> System Administration -> System setup wizard
        ...  Accept the license, Go next.
        ...  Enter Password with 128 characters and complete registration
        ...  Check sucessful login in GUI and CLI

    [Tags]  gui  cli  Tvh1210381c
    [Teardown]  Run keywords  Reset password to default  ${128_character_password}
    ...  AND  Set SSHLib Prompt  ${empty}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    System setup wizard run  testuser@mail.qa
    ...  userpasswd=${128_character_password}
    Log Out Of Dut
    Login to DUT and check login is successful  ${DUT_ADMIN}  ${128_character_password}
    Connect to SMA  ${DUT_ADMIN}  ${128_character_password}