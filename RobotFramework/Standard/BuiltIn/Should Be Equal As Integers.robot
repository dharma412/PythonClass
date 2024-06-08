*** Settings ***

*** Variables ***
${var1}    123
${var2}    123
*** Keywords ***

*** Test Cases ***
ShoudbeEqaulAsInteger
    should be equal as integers      ${var1}    ${var2}   They are not integers