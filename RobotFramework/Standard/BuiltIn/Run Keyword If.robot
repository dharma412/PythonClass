*** Settings ***

*** Variables ***
@{list1} =    1    2    3    76    67    79    77    93
*** Keywords ***
RunKeywordIF
    [Arguments]    ${name}    ${number}
    log to console    ${name}
    log to console    ${number}

*** Test Cases ***
RunkeywordIFTestcase
    FOR    ${item}    IN    @{list1}
        run keyword if  '${item}'=='77'  RunUnlessKeyword   teja    45
    END