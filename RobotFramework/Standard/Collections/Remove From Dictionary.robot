*** Settings ***
Library  Collections

*** Test Cases ***
Remove Item From Dictionary
    # Define the dictionary
    ${my_dict}=    Create Dictionary    key1=value1    key2=value2    key3=value3

    # Remove an item from the dictionary
    Remove From Dictionary    ${my_dict}    key2

    # Log the modified dictionary
    Log Dictionary    ${my_dict}

