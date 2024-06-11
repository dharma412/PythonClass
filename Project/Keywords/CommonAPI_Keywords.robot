*** Settings ***
Library    RequestsLibrary

*** Variables ***
*** Keywords ***
Set Header For API User
    [Documentation]
    [Arguments]    ${token}=${TOKEN}
    &{HEADERS}    Create Dictionary    Authorization=Bearer ${TOKEN}
    set global variable    ${HEADERS}

Create GIT_HUB Creation
    Create Session    endpoint    ${INPUT_URL}

GITHUB COMMON SETUP
    Set Header For API User
    Create GIT_HUB Creation
