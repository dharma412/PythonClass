*** Settings ***
Library    String
*** Variables ***
${string1}       python


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${words} =   encode string to bytes    ${string1}    UTF-8
    ${result}=    should be byte string    ${words}    msg="This is not byte string"
    log to console    ${result}