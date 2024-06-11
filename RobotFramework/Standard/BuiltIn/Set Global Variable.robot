*** Settings ***
Resource    SetTestVariable.robot


*** Test Cases ***
Testcase1
    log to console    ${Testcase1_value}
    log to console    ${Header1}
