*** Settings ***
Library  Collections

*** Variables ***
&{ORIGINAL DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Copy Dictionary Example
    ${copied_dict}=    Copy Dictionary    ${ORIGINAL DICTIONARY}
    Log    ${copied_dict}    console=True
