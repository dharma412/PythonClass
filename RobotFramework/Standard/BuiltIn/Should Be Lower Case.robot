*** Settings ***
Library    String
*** Variables ***
${string1}       pytho


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=    should be lowercase    ${string1}
    log to console    ${result}