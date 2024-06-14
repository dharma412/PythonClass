*** Settings ***
Library    Collections

*** Variables ***
#${Test}      this is robot

*** Test Cases ***
LoginTest
    [Documentation]    Login Test
    [Tags]    regression
    log to console    ${Test}
    log to console    ${Test2}
    log to console    ${Test4}
    log to console    ${Test5}
