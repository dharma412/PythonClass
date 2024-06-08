*** Settings ***

*** Variables ***

*** Keywords ***

*** Test Cases ***
evaluatetestcase
    ${nested} =    Evaluate    [['a', 'b', 'c'], {'key': ['x', 'y']}]
    ${typeof} =    evaluate    type(${nested})
    log to console    ${typeof}
    log to console    @{nested}[0]         # Logs 'a', 'b' and 'c'.
    log to console    @{nested}[1][key]    # Logs 'x' and 'y'.

