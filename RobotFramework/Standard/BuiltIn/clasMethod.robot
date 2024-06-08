*** Settings ***

*** Variables ***
${a} =    dharma
${b} =    teja
*** Keywords ***

CallMethod1
    [Arguments]    ${value} ${value2}
    log to console    ${value}
    log to console    ${value2}

*** Test Cases ***
CallMethodTestcase

    ${output} =    call method  callmethod1   ${a}
    log to console    ${output}