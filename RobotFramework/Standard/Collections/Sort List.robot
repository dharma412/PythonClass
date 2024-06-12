*** Settings ***
Library  Collections

*** Variables ***
@{MY_LIST}    banana    apple    cherry    date

*** Test Cases ***
Sort List Example

    # Sort the list in descending order
    Sort List    ${MY LIST}
    Log To Console    ${MY LIST}  # Expected output: ['date', 'cherry', 'banana', 'apple']

