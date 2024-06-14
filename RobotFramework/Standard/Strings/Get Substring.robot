*** Settings ***
Library    String
*** Variables ***
${string1}       python version 39


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=   get substring    ${string1}    4    10
    log to console    ${result}