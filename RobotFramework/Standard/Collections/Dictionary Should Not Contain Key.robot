*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Dictionary Should Not Contain Key Example
    Dictionary Should Not Contain Key    ${MY DICTIONARY}    key4
    Dictionary Should Not Contain Key    ${MY DICTIONARY}    key5
