*** Settings ***
Library    Collections

*** Variables ***

*** Test Cases ***
ConvertToDicTest
    &{HEADERS}    Convert To Dictionary     Authorization=Bearer
    log to console    ${HEADERS}