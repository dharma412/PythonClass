# syntax to create ${variablename}
*** Settings ***
Library    Collections
Library    SeleniumLibrary

*** Variables ***
${value1}    23
${value2}    age is
*** Keywords ***

*** Test Cases ***
ScalarVariableContatenation
    LOG TO CONSOLE    ${value2} ${value1}

typeofVariable
    ${nested} =    Evaluate    [['a', 'b', 'c'], {'key': ['x', 'y']}]
    ${typeof} =    evaluate    type(${nested})
    log to console    ${typeof}
    log to console    @{nested}[0]         # Logs 'a', 'b' and 'c'.
    log to console    @{nested}[1][key]    # Logs 'x' and 'y'.

Example
    [Tags]    var
    ${list} =    Create List    first    second    third
    Length Should Be    ${list}    3
    #log to console    @{list}
    #log to console    ${TEMPDIR}
    # dispaly the testcase names
    log to console    ${TEST NAME}
    # display the tag names of the testcase
    log to console    @{TEST_TAGS}}

