*** Settings ***

*** Variables ***
${var1}    python
${var2}    python I am learning
*** Keywords ***

*** Test Cases ***
ShouldStratWithTestcase
    should start with    ${var1}    ${var2}
    should start with    ${var1}    ${var2}    string does not start with given word

