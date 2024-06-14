*** Settings ***
Library  Collections

*** Test Cases ***
Remove Duplicates From List
    # Define the list with duplicates
    ${my_list}=    Create List    1    2    2    3    4    4    5

    # Remove duplicates by converting the list to a set and back to a list
    ${unique_list}    remove duplicates    ${my_list}

    # Log the modified list
    Log    ${unique_list}

