*** Settings ***
Library    DateTime

Suite Setup    Keyword1    Thususpthon


*** Variables ***
${country}    India

*** Keywords ***
Keyword1
    [Arguments]    ${text3}    ${text2}=name
    log to console    ${text3}


*** Test Cases ***
Testcase1
    [Tags]      Smoke
    ${date}    Get Current Date
    Keyword1   thisispython
    log to console    ${date}

Testcase2
    [Tags]     Sanity    Regression
    ${date}    Get Current Date
    Keyword1   thisispython
    log to console    ${date}

Testcase3
    [Tags]     Smoke    Regression
    ${date}    Get Current Date
    Keyword1   thisispython
    log to console    ${date}

Testcase4
    log to console      ${country}