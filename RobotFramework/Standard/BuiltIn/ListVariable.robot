# syntax to create list is  @{variablename}
*** Settings ***
Library    Collections

*** Variables ***
${value1}    23
@{value2}    23    25    23
*** Test Cases ***
ListDIsplay
    log to console    ${value2}[1]
    log to console    ${value2}[1]