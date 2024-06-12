*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Dictionary Should Contain Item Example
    Dictionary Should Contain Item    ${MY DICTIONARY}    key1=value1
    Dictionary Should Contain Item    ${MY DICTIONARY}    key2=value2
    Dictionary Should Contain Item    ${MY DICTIONARY}    key3=value3
