*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Get Dictionary Items Example
    ${items}=    Get Dictionary Items    ${MY DICTIONARY}
    Log Many    ${items}
