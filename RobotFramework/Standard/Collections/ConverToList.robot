*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3
${MY STRING}    This is a string
@{MY SET}    ${1}    ${2}    ${3}    ${4}
@{MY TUPLE}    (1, 2, 3, 4)

*** Test Cases ***
Convert Using BuiltIn Library
    ${list_from_dict}=    Convert To List    ${MY DICTIONARY}
    Log    ${list_from_dict}

    ${list_from_string}=    Convert To List    ${MY STRING}
    Log    ${list_from_string}    console=True

    ${list_from_set}=    Convert To List    ${MY SET}
    Log    ${list_from_set}    console=True

    ${list_from_tuple}=    Convert To List    ${MY TUPLE}
    Log    ${list_from_tuple}    console=True
