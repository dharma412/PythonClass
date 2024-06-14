*** Settings ***
Library  Collections

*** Test Cases ***
Verify List Does Not Contain Duplicates
    # Define the list
    ${my_list}=    Create List    1    2    3    4    5

    List Should Not Contain Duplicates    ${my_list}


