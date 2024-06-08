*** Settings ***
Library    String
*** Variables ***
${string1}       python


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${words} =   encode string to bytes    ${string1}    UTF-8
    ${result}=    should be byte string    ${words}    msg="This is not byte string"
    ${words1} =   decode bytes to string    ${words}    UTF-8
    ${result} =  should be string    ${words1}
    log to console    ${result}