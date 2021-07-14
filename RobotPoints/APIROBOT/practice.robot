*** Keywords ***

*** Variables ***

${a}=    Set Variable   First
${b}=    Set Variable   Second

${c}=    Set Variable   ${a}${b}


*** Test Cases ***
VariableTest
    log to console    ${c}