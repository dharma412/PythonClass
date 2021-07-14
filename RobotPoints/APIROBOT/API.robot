*** Settings ***
Library    RequestsLibrary


*** Variables ***
${base_url}    http://restapi.demoqa.com/utilities/weather/city/Delhi
${city}     Delhi

*** Test Cases ***
GetwatherInfo
    create session  mysession   ${base_url}
    ${responce} =    GET On Session    mysession    /utilities/weather/city/${city}
    ${responce.status_code}
    log to console    ${responce.status_code}
    log to console    ${responce.content}
    log to console    ${responce.headers}

    #validations
    ${statuscode} =   convert to string    ${responce.status_code}
    should be equal    ${statuscode}    200
    should be equal    ${responce.content}
