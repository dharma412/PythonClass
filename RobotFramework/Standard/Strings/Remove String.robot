*** Settings ***
Library    String
*** Variables ***
${string1}       python version 39


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=   remove string    ${string1}    39
    log to console    ${result}