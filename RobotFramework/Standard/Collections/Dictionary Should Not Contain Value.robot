*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Dictionary Should Not Contain Value Using Custom Library
    Dictionary Should Not Contain Value    ${MY DICTIONARY}    value4
    Dictionary Should Not Contain Value    ${MY DICTIONARY}    value5
