*** Settings ***

*** Variables ***
@{list1} =    1    2    3    76    67    79    77    93

*** Keywords ***
RunKeywordExpectedErrorKeyword
    ${var} =    set variable    787
    ${var1}=    set variable    333
    ${total} =    evaluate    ${var}+${var1}
    [Return]        ${total}

*** Test Cases ***
RunKeywordANDExpectedErrir
    run keyword and return    RunKeywordExpectedErrorKeyword