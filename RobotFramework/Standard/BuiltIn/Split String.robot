*** Settings ***
Library    String
*** Variables ***
${string1}      This is python

*** Test Cases ***
SplitString
    @{words} =    split string    ${string1}
    log to console    ${words}
