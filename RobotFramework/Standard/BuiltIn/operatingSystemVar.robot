*** Settings ***
Library    Collections

*** Variables ***
${value1}    23
${value2}    age is
*** Keywords ***

*** Test Cases ***
operatingSystemVariable
    log to console    ${CURDIR}
    log to console    ${TEMPDIR}
    log to console    ${EXECDIR}
    log to console    ${/}
    log to console    ${:}
    log to console    ${\n}