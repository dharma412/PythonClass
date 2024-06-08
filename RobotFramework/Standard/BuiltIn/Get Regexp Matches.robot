*** Settings ***
Library    String
*** Variables ***
${string1}       python version 39


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=   get regexp matches    ${string1}    \\w
    log to console    ${result}