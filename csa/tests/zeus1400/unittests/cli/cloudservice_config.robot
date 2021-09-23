*** Settings ***
Library         SmaCliLibrary
Suite Setup     Restart CLI Session

*** Keywords ***
Verify Cloudservice Config Status
    ${status}=   Cloudservice Config Status
    Should Be Equal    ${status}      REGISTERED

*** Test Cases ***
Cloud Service Config Enable
    [Documentation]  Cloud Service Config Enable
    [Tags]    ut1
    Cloudservice Config Enable    APJC
    Commit

Cloud Service Config Status
    [Documentation]  To Get the  Cloud Service Config Status
    [Tags]    ut2
    Wait Until Keyword Succeeds  2 min  10 sec   Verify Cloudservice Config Status

Cloud Service Config Disable
    [Documentation]  Cloud Service Config Disable
    [Tags]    ut3
    Cloudservice Config Disable
    Commit
    ${status}=     Cloudservice Config Status
    Should Be Equal    ${status}      DISABLED

Cloud Service Config Fetch Talos Certificate
    [Documentation]  Cloud Service Config Fetch Talos Certificate
    [Tags]    ut4
    ${output}=  Cloud Service Config Fetch Certificate
    Log  ${output}

