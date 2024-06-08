*** Settings ***
Library    RequestsLibrary

*** Test Cases ***
Quick Get Request Test
    ${response}=    GET  https://reqres.in/api/users?page=2
    log to console    ${response}