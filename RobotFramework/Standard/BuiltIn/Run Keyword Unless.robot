*** Settings ***

*** Variables ***
@{list1} =    1    2    3    76    67    79    77    93
*** Keywords ***
RunUnlessKeyword
    [Arguments]    ${name}    ${number}
    log to console    ${name}
    log to console    ${number}

*** Test Cases ***
RunkeywordUnLessTestcase
    FOR    ${item}    IN    @{list1}
        run keyword unless    '${item}'=='77'  RunUnlessKeyword   teja    45
    END