*** Settings ***
Library    String
*** Variables ***
${string1}      898

*** Test Cases ***
SplitString
    ${integer} =    convert to integer    ${string1}
    ${words} =    should not be string    ${integer}
    log to console    ${words}
