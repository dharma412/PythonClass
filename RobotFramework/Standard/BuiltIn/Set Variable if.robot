*** Settings ***

*** Variables ***
${count}   23
*** Test Cases ***
Test Set Variable if
    ${count1}  set variable   12
    ${count2}  set variable   23
    ${VARIABLES} =  set variable if  ${count1}==12   helloteja   hellodharma