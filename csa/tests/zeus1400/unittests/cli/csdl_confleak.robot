*** Settings ***
Resource        sma/csdlresource.txt
Suite Setup     Do Suite Setup
Suite Teardown  DefaultTestSuiteTeardown


*** Keywords ***

Do Suite Setup
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup

Setup DUT after Reboot
    Start CLI Session If Not Open
    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_TMP_PASSWORD}
    Load License From File

*** Test Cases ***
Enable Adming Access Encrypt Config
    [Documentation]  Checking Encryption Status. If it is dsalbe \n
    ...  enabling encryption \n
    [Tags]  ut1
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    ${status}=  Admin Access Config Encryptconfig Status
    Log  ${status}

    Run Keyword If  '${status}'== 'Disabled'
    ...  Admin Access Config Encryptconfig  enable=${True}
    Wait until DUT Is Accessible    wait_for_ports=${DUT_PORT}    timeout=360
    Setup DUT after Reboot

    ${status}=  Admin Access Config Encryptconfig Status
    Log  ${status}
    Should Be Equal  ${status}  Enabled

Disable Admin Access Encrypt Config
    [Documentation]  Checking Encryption Status. If it is Enabled \n
    ...  disabling encryption \n
    [Tags]  ut2
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    ${status}=  Admin Access Config Encryptconfig Status
    Log  ${status}

    Run Keyword If  '${status}'== 'Enabled'
    ...  Admin Access Config Encryptconfig  enable=${False}
    Wait until DUT Is Accessible    wait_for_ports=${DUT_PORT}    timeout=360
    Setup DUT after Reboot

    ${status}=  Admin Access Config Encryptconfig Status
    Log  ${status}
    Should Be Equal  ${status}  Disabled

