
*** Settings ***
Library  Collections

*** Test Cases ***
Verify Lists Are Equal
    # Define the first list
    ${list1}=    Create List    1    2    3    4    5

    # Define the second list
    ${list2}=    Create List    1    2    3    4    5

    # Verify that both lists are equal
    Lists Should Be Equal    ${list1}    ${list2}

    # Log a message to indicate success
    Log    The lists are equal
