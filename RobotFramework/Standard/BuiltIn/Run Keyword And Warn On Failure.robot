*** Keywords ***
RunKeywordExpectedErrorKeyword
    ${var} =    set variable    787
    ${var1}=    set variable    trr
    ${total} =    evaluate    ${var}+${var1}
    [Return]    ${total}

*** Test Cases ***
RunKeywordANDExpectedErrir
    ${status} =    run keyword and warn on failure    RunKeywordExpectedErrorKeyword
    log to console    ${status}