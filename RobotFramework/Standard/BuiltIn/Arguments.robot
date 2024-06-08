*** Settings ***

*** Variables ***

*** Test Cases ***
Arguments demo keyword1
    Arguments demo keyword    teja    dharma
    Arguments demo keyword    teja1

*** Keywords ***
Arguments demo keyword
    [Arguments]    ${arg1}    ${arg2}= name
    log to console    ${arg1}
    log to console    ${arg2}
    log to console    ${true}
    log to console    ${false}


