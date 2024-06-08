*** Settings ***

*** Variables ***
${var1}    123
${var2}    123.443.33
*** Keywords ***

*** Test Cases ***
ShoudbeEqaulAsNumber
    should be equal as numbers     ${var1}    ${var2}   They are not integers