*** Keywords ***

*** Variables ***
${y} =    teja



*** Test Cases ***
GetVariableValueTestcase
    ${x} =    get variable value    ${y}    name
    log to console    ${x}
    ${x1} =    get variable value    ${z}    name
    log to console    ${x1}