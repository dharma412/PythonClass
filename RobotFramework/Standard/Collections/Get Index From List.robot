*** Settings ***
Library  Collections

*** Variables ***
@{MY LIST}    item1    item2    item3    item4

*** Test Cases ***
Get Index From List Example
    ${index1}=    Get Index From List    ${MY LIST}    item1
    Log    ${index1}  # Expected output: 0

    ${index2}=    Get Index From List    ${MY LIST}    item2
    Log    ${index2}  # Expected output: 1

    ${index3}=    Get Index From List    ${MY LIST}    item3
    Log    ${index3}  # Expected output: 2

    ${index4}=    Get Index From List    ${MY LIST}    item4
    Log    ${index4}  # Expected output: 3
