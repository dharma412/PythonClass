*** Settings ***
Library  Collections

*** Variables ***
@{MY LIST}    item1    item2    item3    item1    item2    item1    item4

*** Test Cases ***
Get Matches Example
    ${matches1}=    Get Matches    ${MY LIST}    item1
    Log Many    ${matches1}  # Expected output: ['item1', 'item1', 'item1']

    ${matches2}=    Get Matches    ${MY LIST}    item2
    Log Many    ${matches2}  # Expected output: ['item2', 'item2']

    ${matches3}=    Get Matches    ${MY LIST}    item3
    Log Many    ${matches3}  # Expected output: ['item3']

    ${matches4}=    Get Matches    ${MY LIST}    item4
    Log Many    ${matches4}  # Expected output: ['item4']

    ${matches5}=    Get Matches    ${MY LIST}    item5
    Log Many    ${matches5}  # Expected output: []
