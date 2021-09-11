*** Settings ***
Resource        regression/regression.robot

*** Variables ***
${user}                    ${ATLAS_NEWUSER_DATA.username}
${user_pass}               ${ATLAS_NEWUSER_DATA.password}
${atlas_url}               ${ATLAS_CONSTANTS['atlas_host_ip']}
${new_user_pass}           Ironport567!


*** Test Cases ***
Tvh1642647c
    [Documentation]
    ...     Verification of notification on creation new user
    [Tags]    usermanagement
    Atlasloginpage.open    ${atlas_url}
    Create Atlas User
    Newuser Permission    ${user}
    Atlasloginpage.Login To Atlas     username=${user}    password=${user_pass}

Tvh1642648c
    [Documentation]
    ...  Verify if we can change the admin user password
    [Tags]    usermanagement
    Atlasloginpage.Login To Atlas     username=${user}    password=${user_pass}
    change user password     ${user_pass}    ${new_user_pass}
    Atlasloginpage.Login To Atlas     username=${user}    password=${new_user_pass}