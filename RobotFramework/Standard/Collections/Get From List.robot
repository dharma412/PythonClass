*** Settings ***
Library  Collections

*** Variables ***
@{MY LIST}    item1    item2    item3    item4

*** Test Cases ***
Get From List Example
    ${item0}=    Get From List    ${MY LIST}    0
    Log    ${item0}  # Expected output: item1

    ${item1}=    Get From List    ${MY LIST}    1
    Log    ${item1}  # Expected output: item2

    ${item2}=    Get From List    ${MY LIST}    2
    Log    ${item2}  # Expected output: item3

    ${item3}=    Get From List    ${MY LIST}    3
    Log    ${item3}  # Expected output: item4
