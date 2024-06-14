*** Settings ***
Library    String
*** Variables ***
${string1}       python version 39


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=   replace string    ${string1}    39    45
    log to console    ${result}