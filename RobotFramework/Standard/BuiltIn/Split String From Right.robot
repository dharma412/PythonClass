*** Settings ***
Library    String
*** Variables ***
${string1}      python version is 3.9

*** Test Cases ***
SplitString
    #@{words} =    split string    ${string1}
    @{words} =    split string from right    ${string1}
    log to console    ${words}
