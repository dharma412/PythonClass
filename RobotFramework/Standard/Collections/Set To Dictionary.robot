
*** Settings ***
Library  Collections

*** Variables ***
&{LIST AS PAIRS}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Set To Dictionary Example
    ${my_dict}=    Set To Dictionary    ${LIST AS PAIRS}
    Log    ${my_dict}  # Expected output: {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

    ${my_dict}=    Set To Dictionary    ${my_dict}     key4=value4
    Log To Console    ${my_dict}
