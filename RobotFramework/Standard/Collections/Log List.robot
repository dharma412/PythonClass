*** Settings ***
Library  Collections

*** Test Cases ***
Log Dictionary Contents
    # Define the dictionary
    ${my_dict}=    Create List    key1    value1    key2=    value2    key3    =value3

    # Log the dictionary
    Log List    ${my_dict}
