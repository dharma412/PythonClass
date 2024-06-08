*** Settings ***


*** Test Cases ***
Test Set Variable
    ${VARIABLES} =  set variable  hello teja
    ${VARIABLES1} =  create list  hello  teja  python
    ${VARIABLES2} =  set variable   ${VARIABLES1}
    log to console    ${VARIABLES2}
