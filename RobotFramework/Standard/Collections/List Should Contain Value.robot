*** Settings ***
Library  Collections

*** Test Cases ***
Verify List Contains Value
    # Define the list
    ${my_list}=    Create List    1    2    3    4    5

    # Verify that the list contains the value 3
    List Should Contain Value    ${my_list}    3

    # Log a message to indicate success
    Log    The list contains the value 3

