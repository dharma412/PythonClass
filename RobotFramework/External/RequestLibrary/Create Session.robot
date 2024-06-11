*** Settings ***
Library               RequestsLibrary

Suite Setup   Create Session    google    https://reqres.in/

*** Variables ***
${url}       https://reqres.in/
*** Test Cases ***
GetRespose
    ${response}=    GET On Session  google  url=${url}api/users?page=2
    log to console    ${response}
