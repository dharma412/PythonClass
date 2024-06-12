*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Get Dictionary Values Example
    ${values}=    Get Dictionary Values    ${MY DICTIONARY}
    Log Many    ${values}
