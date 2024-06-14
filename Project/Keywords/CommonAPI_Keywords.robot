*** Settings ***
Library    RequestsLibrary

*** Variables ***
*** Keywords ***
Set Header For API User
    [Documentation]    This keyword is to set headers
    [Arguments]    ${token}=${TOKEN}
    &{HEADERS}    Create Dictionary    Authorization=Bearer ${TOKEN}
    set global variable    ${HEADERS}

Create GIT_HUB Creation
    Create Session    endpoint    ${INPUT_URL}

GITHUB COMMON SETUP
    Set Header For API User
    Create GIT_HUB Creation

SampleKeyword
    log to console    This is sample keyword
    log to console    This is another one