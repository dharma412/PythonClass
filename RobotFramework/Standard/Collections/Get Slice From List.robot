*** Settings ***
Library  Collections

*** Variables ***
@{MY LIST}    item1    item2    item3    item4    item5    item6

*** Test Cases ***
Get Slice From List Example
    ${slice1}=    Get Slice From List    ${MY LIST}    0    2
    Log Many    ${slice1}  # Expected output: ['item1', 'item2']

    ${slice2}=    Get Slice From List    ${MY LIST}    2    5
    Log Many    ${slice2}  # Expected output: ['item3', 'item4', 'item5']

    ${slice3}=    Get Slice From List    ${MY LIST}    1    4
    Log Many    ${slice3}  # Expected output: ['item2', 'item3', 'item4']

    ${slice4}=    Get Slice From List    ${MY LIST}    3    6
    Log Many    ${slice4}  # Expected output: ['item4', 'item5', 'item6']

    ${slice5}=    Get Slice From List    ${MY LIST}    -3    -1
    Log Many    ${slice5}  # Expected output: ['item4', 'item5']
