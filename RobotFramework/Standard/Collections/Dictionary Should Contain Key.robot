*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Dictionary Should Contain Key Example
    Dictionary Should Contain Key    ${MY DICTIONARY}    key1
    Dictionary Should Contain Key    ${MY DICTIONARY}    key2
    Dictionary Should Contain Key    ${MY DICTIONARY}    key3
