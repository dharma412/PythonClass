*** Settings ***

*** Keywords ***

*** Variables ***
${var}      1
*** Test Cases ***
runifkeyword
    run keyword if   ${var}==1
    ...    log to console    passedteset
    ...    log to console    passedtest2
    ...    ELSE       log to console    failed
