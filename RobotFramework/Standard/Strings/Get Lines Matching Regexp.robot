*** Settings ***
Library    String
*** Variables ***
${string1}       python version 39\n
...              python is\n
...              pyt


*** Test Cases ***
SplitString
    set test variable    ${string1}
    ${result}=   get lines matching regexp    ${string1}    \\w{3}
    log to console    ${result}