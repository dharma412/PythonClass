*** Settings ***
Library    String
*** Variables ***
${string1}       \u00E9


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=    should be unicode string    ${string1}    msg="This is not byte string"
    log to console    ${result}