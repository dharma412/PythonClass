*** Settings ***
Library    String
*** Variables ***
${string1}       python version 39


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=   replace string using regexp    ${string1}    \\d\\d    45
    log to console    ${result}