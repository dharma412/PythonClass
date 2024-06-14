*** Settings ***
*** Variables ***

${value}    1

*** Keywords ***

Keyword1

    log to console  This is keyword1

    RETURN    This is Return



*** Test Cases ***

Testcase1

    ${type string}=     Evaluate    type(${value})

    log to console   ${type string}

    run keyword if  ${value}=='1'  Keyword1
