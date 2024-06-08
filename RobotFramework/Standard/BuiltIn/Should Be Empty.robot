*** Settings ***

*** Variables ***
${var1}    python
${var2}    python I am learning
@{list1}   1    2    3    4    8    7    9    20
*** Keywords ***

*** Test Cases ***
ShouldStratWithTestcase
    ${len} =    get length    ${list1}
    ${len} =    set variable  0
    should be empty        ${len}


