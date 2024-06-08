*** Settings ***
Library    String
*** Variables ***
${string1}       python version 39


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=   remove string using regexp    ${string1}    \\d\\d
    log to console    ${result}