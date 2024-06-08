*** Keywords ***

*** Variables ***
${y} =    teja
*** Settings ***


*** Test Cases ***
GetVariableValueTestcase
    ${x} =    get variable value    ${y}    name
    log to console    ${x}
    ${x1} =    get variable value    ${z}    name
    log to console    ${x1}