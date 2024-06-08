*** Settings ***

*** Variables ***
@{list1} =    1    2    3    76    67    79    77    93

*** Keywords ***
RunKeywordExpectedErrorKeyword
    ${var} =    set variable    787
    ${var1}=    set variable    3ffdfd
    ${total} =    evaluate    ${var}+${var1}
    [Return]    ${total}

*** Test Cases ***
RunKeywordANDExpectedErrir
    ${output}=    wait until keyword succeeds   2 min    3s    RunKeywordExpectedErrorKeyword
    ${output}=    wait until keyword succeeds   10x    3s    RunKeywordExpectedErrorKeyword
    log to console    ${output}