*** Settings ***
Library         SmaCliLibrary
Test Setup     Restart CLI Session

*** Test Cases ***
Enable Securex
    [Documentation]  Enable Securex
    [Tags]    ut1

    Generalconfig Enable Securex
    Commit

    ${status}=   Generalconfig Securex Status
    Should Be Equal  ${status}  ENABLED

Disable Securex
    [Documentation]  Disable Securex
    [Tags]    ut2

    Generalconfig Disable Securex
    Commit

    ${status}=   Generalconfig Securex Status
    Should Be Equal  ${status}  DISABLED
