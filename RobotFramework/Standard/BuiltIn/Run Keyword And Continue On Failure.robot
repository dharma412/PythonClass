*** Settings ***

*** Variables ***
@{list1} =    1    2    3    76    67    79    77    93
*** Keywords ***
RunKeywordContinueOnFailure
    [Arguments]    ${number}
    log to console    ${number}
    [Return]     ${number}


*** Test Cases ***
RunkeywordIFTestcase
    FOR    ${item}    IN    @{list1}
        ${out}=    RunKeywordContinueOnFailure    ${item}
        run keyword and continue on failure    should contain    ${item}    ${out}
    END