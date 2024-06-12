*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Get From Dictionary Example
    ${value1}=    Get From Dictionary    ${MY DICTIONARY}    key1
    Log    ${value1}  # Expected output: value1

    ${value2}=    Get From Dictionary    ${MY DICTIONARY}    key2
    Log    ${value2}  # Expected output: value2

    ${value3}=    Get From Dictionary    ${MY DICTIONARY}    key3
    Log    ${value3}  # Expected output: value3

    ${non_existent_value}=    Get From Dictionary    ${MY DICTIONARY}    key4    default_value
    Log    ${non_existent_value}  # Expected output: default_value
