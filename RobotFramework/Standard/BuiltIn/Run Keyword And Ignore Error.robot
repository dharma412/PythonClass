*** Keywords ***
RunKeywordExpectedErrorKeyword
    ${var} =    set variable    787
    ${var1}=    set variable    454
    ${total} =    evaluate    ${var}+${var1}
    [Return]    ${total}

*** Test Cases ***
RunKeywordANDExpectedErrir
    ${status} =    run keyword and ignore error    RunKeywordExpectedErrorKeyword
    log to console    ${status}

#This keyword returns two values, so that the first is either string PASS or FAIL, depending on the status of the executed keyword.
#The second value is either the return value of the keyword or the received error message.