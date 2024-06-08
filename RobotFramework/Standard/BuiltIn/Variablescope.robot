*** Settings ***


*** Variables ***
${VARIABLE_GLOBAL}    This is gloal variable




*** Test Cases ***
GlobalVariableDemo
    ${TestcaseVariable} =    set variable    This is testcase variable
    log to console    ${TestcaseVariable}
    #log to console    ${VARIABLE_GLOBAL}

GlobalVariableDemo2
    log to console    ${VARIABLE_GLOBAL}

GlobalVariableDemo3
    this is keywordvariable demo

*** Keywords ***
this is keywordvariable demo
    [Arguments]    ${variable_global}=This is KEYWORD variable
    log to console    ${VARIABLE_GLOBAL}


# global variable recommended to write in Capital Letters.*** Keywords ***
