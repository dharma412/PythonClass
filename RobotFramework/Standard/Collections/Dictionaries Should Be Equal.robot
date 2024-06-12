*** Settings ***
Library  Collections

*** Variables ***
&{DICTIONARY 1}    key1=value1    key2=value2    key3=value3
&{DICTIONARY 2}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Dictionaries Should Be Equal Using Custom Library
    Dictionaries Should Be Equal    ${DICTIONARY 1}    ${DICTIONARY 2}
