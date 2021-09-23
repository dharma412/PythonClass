# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_pwd_strength.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      String
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown
Test Setup      DefaultTestCaseSetup
Test Teardown   DefaultTestCaseTeardown


*** Variables ***
@{USER_PASSWORD}=                  Cisco123$  Cisco321$  Abctur115$  turZYX115$  CCCisco12$  Cisssssco12$  Cisco1222$  Cisco1####$  CcCisco12$  Cis${SPACE*3}co143$
@{GUEST_USER_VARIATION_PASSWORD}=  Guest124$  45Tuser%  78*estuS
@{ADMIN_USER_VARIATION_PASSWORD}=  45Admi@1  Dmin@143  Min@%368
${USER_NAME1}=                     testuser
${USER_NAME2}=                     guestuser
${SEQUENTIAL_PASSWORD}=            Cisco123$
${REPETATIVE_PASSWORD}=            CCCisco12$
${SEQUENTIAL_PASSWORD_1}=          Ccisco1234$
${SEQUENTIAL_PASSWORD_2}=          CisStUvco12$
${VARIATIONS_PASSWORD}=            Admintest@12
${SEQUENTIAL_ERROR}=               not contain three or more repetitive or sequential characters
${VARIATIONS_ERROR}=               not be a username or one of its variations
${GROUP_ADMINISTRATOR}=            Administrator
${GROUP_OPERATORS}=                Operators
${GROUP_RO_OPERATORS}=             Read-Only Operators
${GROUP_GUESTS}=                   Guests
${ERROR_MSG_MORELINK}=             //span[text()='more']
${ERROR_MESSAGE_MORE_POPUP}=       //*[@id='win']/div[2]
${HELP_MSG}=                       //th[contains(text(),'Passphrase:')]//span[@class='bubble-link-info']
${EDIT_BUTTON}=                    //input[@value='Edit Settings...']


*** Keywords ***
Verify Password Change Error Message In CLI
    [Arguments]  ${string}  ${error_message}
    ${error_tuple}=  Get Substring  ${string}  1
    ${tuple_to_str}=  Catenate  ${error_tuple}
    should contain   ${tuple_to_str}   ${error_message}

Verify Password Change Error Message
    [Arguments]  ${error_message}
    Sleep  1
    Click Element  ${error_message}
    ${text} =  Get Text  ${ERROR_MESSAGE_MORE_POPUP}
    [Return]  ${text}

Setup DUT with license and password after restore
    Start CLI Session If Not Open
    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Load License From File

Delete User and Change Passphrase Policy From CLI
    [Arguments]  ${user_name}
    Restart CLI Session
    User Config Delete  ${user_name}  confirm=yes
    User Config Policy Passwordstrength  sequential_chars=yes
    Commit

Delete User and Change Passphrase Policy From GUI
    [Arguments]  ${user_name}
    Users Delete User  ${user_name}
    Users Edit Password Rules  rep_sequential_char=on
    Commit Changes
    Log Out Of Dut

Do Tvh1468444c Setup
    Set Test Variable  ${TEST_ID}  Tvh1455409c
    ${CONFIG_FILE}=  Save Config  yes
    Set Test Variable   ${CONFIG_FILE}
    Suspend
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

Do Tvh1468444c Teardown
    Close Browser
    Selenium Login
    Log Out Of Dut
    Load Config From File   ${CONFIG_FILE}
    commit


*** Test Cases ***
Tvh1468438c
    [Documentation]  Verify 3 or more repetitive/sequential characters are not allowed
    ...  in passwords for any user through CLI - userconfig > new/edit option,
    ...  verify proper error message shown when such characters are used in passwords.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468438c
    [Tags]  Tvh1468438c
    [Teardown]  Delete User and Change Passphrase Policy From CLI  ${USER_NAME2}

    Set Test Variable  ${TEST_ID}    Tvh1455403c
    User Config New  ${USER_NAME2}  ${TEST_ID}  Cisco143$  group=${Group_Guests}
    Commit

    FOR  ${password}  IN  @{USER_PASSWORD}
       ${error_string}=  Run Keyword And Ignore Error  User Config New  ${USER_NAME1}
       ...  ${TEST_ID}  ${password}  ${Group_Guests}
       Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}
    END
    FOR  ${password}  IN  @{USER_PASSWORD}
       ${error_string}=  Run Keyword And Ignore Error  User Config Edit  ${USER_NAME2}
       ...  ${TEST_ID}  ${password}  ${Group_Guests}
        Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}
    END

Tvh1468439c
    [Documentation]  Verify 3 or more repetitive/sequential characters are not allowed
    ...  in passwords for any user through CLI - userconfig > passphrase > assign option,
    ...  verify proper error message shown when such characters are used in passwords.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1455404c
    [Tags]  Tvh1468439c

    FOR  ${password}  IN  @{USER_PASSWORD}
        ${error_string}=  Run Keyword And Ignore Error  User Config Password Assign  ${DUT_ADMIN}
        ...  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
        Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}
    END

Tvh1468440c
    [Documentation]  Verify 3 or more repetitive/sequential characters are not allowed
    ...  in passwords for any user through CLI - passphrase/passwd options, verify proper
    ...  error message shown when such characters are used in passwords.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468440c
    [Tags]  Tvh1468440c

    FOR  ${password}  IN  @{USER_PASSWORD}
       ${error_string}=  Run Keyword And Ignore Error  Change password via CLI  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
       Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}
       Restart CLI Session
    END

Tvh1468441c
    [Documentation]  Verify 3 or more repetitive/sequential characters are not allowed
    ...  in passwords for any user through GUI - System Admininstration > Users > Add User
    ...  option, verify proper error message shown when such characters are used in passwords.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1455406c
    [Tags]  Tvh1468441c
    Set Test Variable  ${TEST_ID}  Tvh1468441c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    FOR  ${password}  IN  @{USER_PASSWORD}
       Run Keyword And Ignore Error  Users Add User  ${USER_NAME1}
       ...  ${TEST_ID}  ${password}
       ...  ${sma_user_roles.OPERATOR}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${SEQUENTIAL_ERROR}
    END
    Log Out Of Dut

Tvh1468442c
    [Documentation]  Verify 3 or more repetitive/sequential characters are not allowed in passwords
    ...  for any user through GUI - Options > Account > Change Passphrase option,
    ...  verify proper error message shown when such characters are used in passwords.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468442c
    [Tags]  Tvh1468442c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    FOR  ${password}  IN  @{USER_PASSWORD}
       Run Keyword And Ignore Error  Change Password
       ...  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${SEQUENTIAL_ERROR}
    END
    Log Out Of Dut

Tvh1468444c
    [Documentation]  Verify 3 or more repetitive/sequential characters are not allowed
    ...  in passwords for admin through GUI - System Admininstration
    ...  System Setup > System Setup Wizard.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468444c
    [Tags]  Tvh1468444c
    [Setup]  Do Tvh1468444c Setup
    [Teardown]  Do Tvh1468444c Teardown

    FOR  ${password}  IN  @{USER_PASSWORD}
       System setup wizard run password change  ${EMAIL_ALERTS}  passwd=${password}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${SEQUENTIAL_ERROR}
    END
    FOR  ${password}  IN  @{ADMIN_USER_VARIATION_PASSWORD}
       System setup wizard run password change  ${EMAIL_ALERTS}  passwd=${password}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${VARIATIONS_ERROR}
    END

Tvh1468448c
    [Documentation]  Verify username variations (Having substrings from username and appending numbers
    ...  or special chars to it) cannot be used in passwords under CLI - userconfig, passphrase,passwd.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468448c
    [Tags]  Tvh1468448c
    Set Test Variable  ${TEST_ID}  Tvh1468448c

    FOR  ${password}  IN  @{GUEST_USER_VARIATION_PASSWORD}
       ${error_string}=  Run Keyword And Ignore Error  User Config New  ${USER_NAME2}
       ...  ${TEST_ID}  ${password}  ${Group_Guests}
       Verify Password Change Error Message In CLI  ${error_string}  ${VARIATIONS_ERROR}
    END

    FOR  ${password}  IN  @{ADMIN_USER_VARIATION_PASSWORD}
        ${error_string}=  Run Keyword And Ignore Error  User Config Password Assign  ${DUT_ADMIN}
        ...  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
        Verify Password Change Error Message In CLI  ${error_string}  ${VARIATIONS_ERROR}
        Restart CLI Session
    END

    FOR  ${password}  IN  @{ADMIN_USER_VARIATION_PASSWORD}
       ${error_string}=  Run Keyword And Ignore Error  Change password via CLI  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
       Verify Password Change Error Message In CLI  ${error_string}  ${VARIATIONS_ERROR}
       Restart CLI Session
    END

Tvh1468449c
    [Documentation]  Verify username and its variations (Having substrings from username and appending
    ...  numbers or special chars to it) cannot be used in passwords under GUI - System Administration
    ...  Users, Options > Account > Change Passphrase, SSW options.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468449c
    [Tags]  Tvh1468449c
    Set Test Variable  ${TEST_ID}  Tvh1468449c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    FOR  ${password}  IN  @{GUEST_USER_VARIATION_PASSWORD}
       Run Keyword And Ignore Error  Users Add User  ${USER_NAME2}
       ...  ${TEST_ID}  ${password}
       ...  ${sma_user_roles.GUEST}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${VARIATIONS_ERROR}
    END

    FOR  ${password}  IN  @{ADMIN_USER_VARIATION_PASSWORD}
       Run Keyword And Ignore Error  Change Password
       ...  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${VARIATIONS_ERROR}
    END
    Log Out Of Dut

Tvh1468450c
    [Documentation]  Verify configuring password with 3 or more repetitive/sequential
    ...  characters are accepted when it is allowed by password policy settings (from CLI).\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468450c
    [Tags]  Tvh1468450c
    [Teardown]  Run keywords  Load Config From File  ${CONFIG_FILE}
    ...  AND  Commit
    Set Test Variable  ${TEST_ID}  Tvh1468450c

    ${CONFIG_FILE}=  Save Config  yes
    Set Test Variable   ${CONFIG_FILE}

    User Config Policy Passwordstrength  sequential_chars=no
    Commit

    # Verification on userconfig > new
    FOR  ${password}  IN  @{USER_PASSWORD}
        User Config New  ${USER_NAME1}  ${TEST_ID}  ${password}
        ...  group=${Group_RO_Operators}
        Commit
        Start Cli Session  ${USER_NAME1}  ${password}
        Restart CLI Session
        User Config Delete  ${USER_NAME1}  confirm=yes
        Commit
    END

    User Config New  ${USER_NAME2}  ${TEST_ID}  Cisco143$  group=${Group_Guests}
    Commit

    # Verification on userconfig > Edit
    FOR  ${password}  IN  @{USER_PASSWORD}
       User Config Edit  ${USER_NAME2}
       ...  ${TEST_ID}  ${password}  ${Group_Guests}
       Commit
       Start Cli Session  ${USER_NAME2}  ${password}
       Restart CLI Session
    END

    # Verification on userconfig > passphrase > assign
    User Config Password Assign  ${DUT_ADMIN}
    ...  ${DUT_ADMIN_SSW_PASSWORD}  ${SEQUENTIAL_PASSWORD}
    Commit
    Start Cli Session  ${DUT_ADMIN}  ${SEQUENTIAL_PASSWORD}

    # Verification on passwd/passphrase
    Change password via CLI  ${SEQUENTIAL_PASSWORD}  ${REPETATIVE_PASSWORD}
    Commit
    Start Cli Session  ${DUT_ADMIN}  ${REPETATIVE_PASSWORD}

Tvh1468451c
    [Documentation]  Verify configuring password with 3 or more repetitive/sequential characters are
    ...  accepted when it is allowed by password policy settings (from GUI).\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468451c
    [Tags]  Tvh1468451c
    [Teardown]  Run keywords  Load Config From File  ${CONFIG_FILE}
    ...  AND  Commit
    Set Test Variable  ${TEST_ID}  Tvh1468451c

    ${CONFIG_FILE}=  Save Config  yes
    #Set Test Variable   ${CONFIG_FILE}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    # Need to Commit password rules before add users
    Users Edit Password Rules  rep_sequential_char=off
    Commit Changes

    #System Administration > Users
    Users Add User  ${USER_NAME1}  ${TEST_ID}
    ...  ${SEQUENTIAL_PASSWORD}  ${sma_user_roles.OPERATOR}
    Commit Changes
    Login to SMA via GUI  ${USER_NAME1}  ${SEQUENTIAL_PASSWORD}
    Log Out Of Dut

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    #Options > Account > Change Passphrase
    Change Password  ${DUT_ADMIN_SSW_PASSWORD}  ${SEQUENTIAL_PASSWORD_1}
    Commit Changes
    Login to SMA via GUI  ${DUT_ADMIN}  ${SEQUENTIAL_PASSWORD_1}

    #SSW verification need to Resetconfiguraion and after restconf again need to uncheck password rule
    Suspend
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Users Edit Password Rules  rep_sequential_char=off
    Commit Changes

    System setup wizard run  ${EMAIL_ALERTS}  userpasswd=${SEQUENTIAL_PASSWORD_2}
    Login to SMA via GUI  ${DUT_ADMIN}  ${SEQUENTIAL_PASSWORD_2}

    Run Keyword And Ignore Error  Users Get Settings
    Click Button  ${EDIT_BUTTON}
    Checkbox Should Not Be Selected  password_no_rep_seq_chars

Tvh1468452c
    [Documentation]  Verify users are restricted to use 3 or more repetitive/sequential
    ...  characters in passwords by default and it can be allowed through password
    ...  policy settings (from GUI).\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468452c
    [Tags]  Tvh1468452c
    [Teardown]  Run keywords  Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  AND  Delete User and Change Passphrase Policy From GUI  ${USER_NAME1}
    Set Test Variable  ${TEST_ID}  Tvh1468452c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Users Add User  ${USER_NAME1}
    ...  {TEST_ID}  ${SEQUENTIAL_PASSWORD}  ${sma_user_roles.OPERATOR}
    ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
    Should Contain   ${error_message}  ${SEQUENTIAL_ERROR}

    Users Edit Password Rules  rep_sequential_char=off
    Commit Changes

    Users Add User  ${USER_NAME1}  ${TEST_ID}
    ...  ${SEQUENTIAL_PASSWORD}  ${sma_user_roles.OPERATOR}
    Commit Changes

    Login to SMA via GUI  ${USER_NAME1}  ${SEQUENTIAL_PASSWORD}

Tvh1468453c
    [Documentation]  Verify users are restricted to use 3 or more repetitive/sequential
    ...  characters in passwords by default and it can be allowed through password
    ...   policy settings (from CLI).\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1455418c
    [Tags]  Tvh1468453c
    [Teardown]  Delete User and Change Passphrase Policy From CLI  administratores
    Set Test Variable  ${TEST_ID}  Tvh1468453c

    ${error_string}=  Run Keyword And Ignore Error  User Config New  administratores
    ...  ${TEST_ID}  ${SEQUENTIAL_PASSWORD}  ${GROUP_ADMINISTRATOR}
    Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}

    User Config Policy Passwordstrength  sequential_chars=no
    Commit

    User Config New  administratores  ${TEST_ID}
    ...  ${SEQUENTIAL_PASSWORD}  group=${GROUP_ADMINISTRATOR}
    Commit

    Start Cli Session  administratores  ${SEQUENTIAL_PASSWORD}

Tvh1468454c
    [Documentation]  Verify the password policy settings to allow/restrict the usage
    ...  of 3 or more repetitive/sequential characters in passwords is retained
    ...  after save, reset & load configuration.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468454c
    [Tags]  Tvh1468454c
    [Teardown]  Run keywords  Load Config From File  ${CONFIG_FILE}
    ...  AND  Commit

    Set Test Variable  ${TEST_ID}  Tvh1468454c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    #By default all passphrase rules Enabled and saved configuration
    ${CONFIG_FILE}=  Save Config  yes

    Users Edit Password Rules  rep_sequential_char=off
    Commit Changes

    Users Add User  administratores  ${TEST_ID}
    ...  ${SEQUENTIAL_PASSWORD}  ${sma_user_roles.ADMIN}
    Commit Changes

    #Load configuration file saved at step 5 and verify all rules are enabled
    Load Config From File  ${CONFIG_FILE}
    Commit

    Run Keyword And Ignore Error  Users Add User  ${USER_NAME2}
    ...  ${TEST_ID}  ${SEQUENTIAL_PASSWORD}
    ...  ${sma_user_roles.ADMIN}
    ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
    Should Contain   ${error_message}  ${SEQUENTIAL_ERROR}

    Run Keyword And Ignore Error  Users Get Settings
    Click Button  ${EDIT_BUTTON}
    Checkbox Should Be Selected  password_require_upper_lower
    Checkbox Should Be Selected  password_require_numeric_char
    Checkbox Should Be Selected  password_require_special_char
    Checkbox Should Be Selected  password_no_username_resemblance
    Checkbox Should Be Selected  password_no_rep_seq_chars

    #Disable all passphrase rules and save configuration
    Users Edit Password Rules  req_alpha=off
    ...  req_number=off
    ...  req_special_char=off
    ...  ban_username=off
    ...  rep_sequential_char=off
    Commit Changes

    ${DISABLE_RULES_CONFIG_FILE}=  Save Config  yes

    Load Config From File  ${DISABLE_RULES_CONFIG_FILE}
    Commit

    Run Keyword And Ignore Error  Users Get Settings
    Click Button  ${EDIT_BUTTON}
    Checkbox Should Not Be Selected  password_require_upper_lower
    Checkbox Should Not Be Selected  password_require_numeric_char
    Checkbox Should Not Be Selected  password_require_special_char
    Checkbox Should Not Be Selected  password_no_username_resemblance
    Checkbox Should Not Be Selected  password_no_rep_seq_chars

Tvh1468445c
    [Documentation]  Verify that help message includes the restriction of repetitive/sequential
    ...  characters in password while configuring user's password through GUI
    ...  System Administration> Users > Add User/ Edit User  (By clicking on user).\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1468445c
    [Tags]  Tvh1468445c
    Set Test Variable  ${TEST_ID}  Tvh1468445c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Users Add User  ${USER_NAME2}
    ...  ${TEST_ID}  ${SEQUENTIAL_PASSWORD}
    ...  ${sma_user_roles.GUEST}
    ${help_message}=  Verify Password Change Error Message  ${HELP_MSG}
    Should Contain   ${help_message}  ${SEQUENTIAL_ERROR}

    Run Keyword And Ignore Error  Users Edit User  ${DUT_ADMIN}
    ...  ${SEQUENTIAL_PASSWORD}
    ${help_message}=  Verify Password Change Error Message  ${HELP_MSG}
    Should Contain   ${help_message}  ${SEQUENTIAL_ERROR}
    Log Out Of Dut

Tvh1473577c
    [Documentation]  Verify creating new user with username which has
    ...  3 or 4 same words sequentially and check whether it is allowed.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1472693c
    [Tags]  Tvh1473577c
    [Teardown]  Delete User and Change Passphrase Policy From CLI  testttuser
    Set Test Variable  ${TEST_ID}  Tvh1473577c

    User Config New  testttuser  ${TEST_ID}  ${VARIATIONS_PASSWORD}  ${GROUP_ADMINISTRATOR}
    Commit
    Start Cli Session   testttuser  ${VARIATIONS_PASSWORD}

    Login to SMA via GUI  testttuser  ${VARIATIONS_PASSWORD}
    Log Out Of Dut

Tvh1473578c
    [Documentation]  Verify after executing diagnostic >> reload, create a new user
    ...  with a password which breaks new password rule and make sure it is not allowed.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1473578c
    [Tags]  Tvh1473578c

    Set Test Variable  ${TEST_ID}  Tvh1473578c

    Diagnostic Reload  confirm=yes  wipedata=yes
    Wait until DUT Is Accessible    wait_for_ports=${DUT_PORT}    timeout=360
    Setup DUT with license and password after restore

    User Config New  ${USER_NAME2}  ${TEST_ID}  Cisco143$  group=${Group_Guests}
    Commit

    FOR  ${password}  IN  @{USER_PASSWORD}
       ${error_string}=  Run Keyword And Ignore Error  User Config New  ${USER_NAME1}
       ...  ${TEST_ID}  ${password}  ${Group_Guests}
       Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}
    END

    FOR  ${password}  IN  @{USER_PASSWORD}
       ${error_string}=  Run Keyword And Ignore Error  User Config Edit  ${USER_NAME2}
       ...  ${TEST_ID}  ${password}  ${Group_Guests}
        Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}
    END

    Restart CLI Session
    FOR  ${password}  IN  @{USER_PASSWORD}
       ${error_string}=  Run Keyword And Ignore Error  Change password via CLI  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
       Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}
       Restart CLI Session
    END

    FOR  ${password}  IN  @{USER_PASSWORD}
        ${error_string}=  Run Keyword And Ignore Error  User Config Password Assign  ${DUT_ADMIN}
        ...  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
        Verify Password Change Error Message In CLI  ${error_string}  ${SEQUENTIAL_ERROR}
    END

    User Config Delete  ${USER_NAME2}  confirm=yes
    Commit

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    FOR  ${password}  IN  @{USER_PASSWORD}
       Run Keyword And Ignore Error  Users Add User  ${USER_NAME1}
       ...  ${TEST_ID}  ${password}
       ...  ${sma_user_roles.ADMIN}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${SEQUENTIAL_ERROR}
    END

    FOR  ${password}  IN  @{USER_PASSWORD}
       Run Keyword And Ignore Error  Change Password
       ...  ${DUT_ADMIN_SSW_PASSWORD}  ${password}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${SEQUENTIAL_ERROR}
    END
    FOR  ${password}  IN  @{USER_PASSWORD}
       System setup wizard run password change  ${EMAIL_ALERTS}  passwd=${password}
       ${error_message}=  Verify Password Change Error Message  ${ERROR_MSG_MORELINK}
       Should Contain   ${error_message}  ${SEQUENTIAL_ERROR}
    END