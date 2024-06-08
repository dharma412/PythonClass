*** Settings ***

*** Variables ***
@{list1} =    1    2    3    76    67    79    77    93
*** Keywords ***
RunUnlessKeyword
    [Arguments]    ${name}    ${number}
    log to console    ${name}
    log to console    ${number}
    [Return]    ${name}

*** Test Cases ***
RunkeywordUnLessTestcase
    FOR    ${item}    IN    @{list1}
        ${output} =    run keyword and return if    '${item}'=='77'  RunUnlessKeyword   teja    45
        log to console    ${output}
    END