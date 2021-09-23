*** Settings ***
Resource    sma/reports_keywords.txt
Resource    sma/config_masters.txt


Suite Setup     CustomSuiteSetup
Test Setup      DefaultReportTestCaseSetup
Test Teardown   DefaultReportTestCaseTeardown
Suite Teardown  DefaultReportSuiteTeardown

*** Variables ***
${WEB_USER}      webuser
${FULL_NAME}     USER1
${WEB_USER_PWD}  Ironport@123

*** Keywords ***
CustomSuiteSetup
    DefaultRegressionSuiteSetup  reset_appliances=${False}
    Set CMs
    DefaultReportSuiteSetup  CM=${CM}

Delete User
    Run Keyword And Ignore Error  Log Out Of DUT
    Log Into DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Users Delete User  ${WEB_USER}
    Commit Changes

*** Test Cases ***

Tvh1251789c
    [Documentation]  Check ssh vulnerability after adding user.\n
    ...  http://tims/view-entity.cmd?ent=1251789
    ...  Add web user and log into dut
    ...  SSH to sma with admin
    ...  SSH to sma with rtestuser and check ssh version
    ...  SSH to sma with webuser
    ...  Log out of dut and login with admin
    ...  Delete web user

    [Tags]  srts  teacat  CSCvm69925  Tvh1251789c
    [Teardown]  Delete User

    Users Add user  ${WEB_USER}  ${FULL_NAME}  ${WEB_USER_PWD}  ${sma_user_roles.WEB_ADMIN}
    Commit Changes
    Log Out Of DUT
    Log Into DUT  ${WEB_USER}  ${WEB_USER_PWD}
    SSHLibrary.Open Connection  ${SMA}  prompt=>  timeout=30
    SSHLibrary.Login  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    SSHLibrary.Close Connection
    SSHLibrary.Open Connection  ${SMA}  prompt=]  timeout=30
    SSHLibrary.Login  ${RTESTUSER}  ${RTESTUSER_PASSWORD}
    SSHLibrary.Write  ssh -V
    ${out}=  Read Until Prompt
    SSHLibrary.Close Connection
    ${ssh_version}=  Evaluate  re.search('OpenSSH_(.*)p1', '''${out}''').group(1)  re
    ${ssh_version}=  Get Substring  ${ssh_version}  0  1
    Should Be True  ${ssh_version} >= 6
