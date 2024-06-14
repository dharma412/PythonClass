
*** Settings ***
Library  Collections

*** Test Cases ***
Pop Item From Dictionary
    # Define the dictionary
    ${my_dict}=    Create Dictionary    key1=value1    key2=value2    key3=value3

    # Pop an item from the dictionary
    ${value}=    Pop From Dictionary    ${my_dict}    key2

    # Log the value that was popped
    Log    The value of key2 is ${value}

    # Log the modified dictionary
    Log Dictionary    ${my_dict}
