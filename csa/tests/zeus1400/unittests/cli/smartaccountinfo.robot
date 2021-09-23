*** Settings ***
Library         SmaCliLibrary
Suite Setup     Restart CLI Session

*** Keywords ***

*** Test Cases ***
Get Smart Account Details
    [Documentation]  Smart Account Details
    [Tags]    ut1
    ${smart_account_info}=  Smart Account Details
    Log  ${smart_account_info}
