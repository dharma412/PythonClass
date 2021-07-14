*** Settings ***
Library    Collections
*** Variables ***
&{dictionary}    name=python    version=3.9   IDE=pycharm    work=USTglobal


*** Test Cases ***
DictionaryTestcase
    ${sorted} =    get dictionary items    ${dictionary}
    log to console    ${sorted}
    ${typeof} =     evaluate    type(${sorted})
    log to console    ${typeof}
    FOR    ${i}    IN    ${dictionary.keys()}
        ${val}=    get from dictionary    ${dictionary}   ${i}
    END
    log to console    ${val}

ExitloopTestcase
    FOR    ${att}    IN RANGE    5
        log to console    ${att}
        exit for loop if    ${att} == 2
    END