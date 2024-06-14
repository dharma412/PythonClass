*** Settings ***
Library  Collections

*** Variables ***
@{MY LIST}    apple    banana    cherry    date

*** Test Cases ***
Should Contain Match Example
    # Check if the list contains an item matching the pattern 'a*'
    Should Contain Match    ${MY LIST}    a*
    # Expected output: Passes because 'apple' and 'banana' match the pattern

    # Check if the list contains an item matching the pattern 'b*'
    Should Contain Match    ${MY LIST}    b*
    # Expected output: Passes because 'banana' matches the pattern

    # Check if the list contains an item matching the pattern '*e'
    Should Contain Match    ${MY LIST}    *e
    # Expected output: Passes because 'apple', 'date', and 'cherry' match the pattern

    # Check if the list contains an item matching the pattern 'x*'
    Should Contain Match    ${MY LIST}    x*
    # Expected output: Fails because no item matches the pattern 'x*'
