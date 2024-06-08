*** Settings ***

*** Variables ***
@{list1} =    1    2    3    76    67    79    77    93
*** Keywords ***
RunUnlessKeywordsKeyword
    [Arguments]    ${name}    ${number}
    log to console    ${name}
    log to console    ${number}

RunKeywordsKeyword
    [Arguments]    ${name}    ${number}
    log to console    ${name}
    log to console    ${number}

*** Test Cases ***
RunkeywordUnLessTestcase
    FOR    ${item}    IN    @{list1}
        run keywords    RunUnlessKeywordsKeyword     name=${item}    number=98
        ...    AND    RunKeywordsKeyword     name=${item}    number=77
    END