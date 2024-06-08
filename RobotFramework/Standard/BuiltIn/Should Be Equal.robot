*** Settings ***

*** Variables ***
#${var1}    123
${var2}    python
*** Keywords ***

*** Test Cases ***
ShoudbeEqaultestcase
    should be equal    python    ${var2}    string does not start with given word

