*** Settings ***
Library    String
*** Variables ***
${programming}      python
${version}          3.9
${year}             2021

*** Test Cases ***
SplitString
    ${words} =    format string    To:{} and {}     ${programming}    ${version}
    log to console    ${words}