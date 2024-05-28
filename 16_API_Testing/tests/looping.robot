*** Settings ***
Library     String
*** Keywords ***
[Arguments]  ${Eleemt}
Start Element
    log    ${Eleemt}

*** Variables ***

*** Test Cases ***
Example
    FOR    ${element}    IN    @{ELEMENTS}
        Start Element    ${element}
    END





