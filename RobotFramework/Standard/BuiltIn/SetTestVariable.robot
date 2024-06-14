*** Settings ***

Suite Setup    Set Global Variable    ${Header1}   8
Test Setup     Set Test Variable     ${header2}    10
*** Variables ***
${Testcase1_value}      45


*** Test Cases ***
Testcase1
    Set Suite Variable    ${my_suite_var}    15
    Set Global Variable    ${my_global_var}    1

Testcase2

    ${my_suite_var}=    evaluate    ${my_suite_var}+${Testcase1_value}
    Set global variable    ${my_suite_var}

    ${my_global_var}=    evaluate    ${my_global_var}+${Testcase1_value}
    log to console    ${my_global_var}
    Set Global Variable    ${my_global_var}
    #Set Global Variable    ${my_global_var}

Testcase3
    log to console
    log to console    ${my_global_var}


