*** Settings ***
Library  Collections

*** Variables ***
@{MY LIST}    item1    item2    item3    item1    item2    item1     ThisisPython

*** Test Cases ***
Get Match Count Example
    ${count1}=    Get Match Count    ${MY LIST}    *Python
    Log    ${count1}  # Expected output: 3

    ${count2}=    Get Match Count    ${MY LIST}    item2
    Log    ${count2}  # Expected output: 2

    ${count3}=    Get Match Count    ${MY LIST}    item3
    Log    ${count3}  # Expected output: 1

    ${count4}=    Get Match Count    ${MY LIST}    item4
    Log    ${count4}  # Expected output: 0
