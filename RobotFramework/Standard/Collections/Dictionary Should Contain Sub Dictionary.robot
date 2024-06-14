*** Settings ***
Library  Collections

*** Variables ***
&{SUPER DICTIONARY}    key1=value1    key2=value2    key3=value3    key4=value4
&{SUB DICTIONARY}      key1=value1    key3=value3

*** Test Cases ***
Dictionary Should Contain Sub Dictionary
    Dictionary Should Contain Sub Dictionary    ${SUPER DICTIONARY}    ${SUB DICTIONARY}
