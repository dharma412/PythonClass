
*** Settings ***
Library  Collections

*** Variables ***
@{MY LIST}    item1    item2    item3    item4

*** Test Cases ***
Set List Values Example
    # Original list
    Log Many    ${MY LIST}  # Expected output: ['item1', 'item2', 'item3', 'item4']

    # Set a new value at index 1
    Set List Value    ${MY LIST}    1    new_item2
    Log Many    ${MY LIST}  # Expected output: ['item1', 'new_item2', 'item3', 'item4']

    # Set a new value at index 3
    Set List Value    ${MY LIST}    3    new_item4
    Log Many    ${MY LIST}  # Expected output: ['item1', 'new_item2', 'item3', 'new_item4']

    # Set a new value at index 0
    Set List Value    ${MY LIST}    0    new_item1
    Log Many    ${MY LIST}  # Expected output: ['new_item1', 'new_item2', 'item3', 'new_item4']
