*** Settings ***
Library    String
*** Variables ***
${programming}      python is lang and version is , 3.9
${version}          3.9
${year}             2021

*** Test Cases ***
SplitString
    ${words} =  fetch from left    ${programming}    ,
    log to console    ${words}