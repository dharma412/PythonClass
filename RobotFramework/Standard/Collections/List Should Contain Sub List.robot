*** Settings ***
Library  Collections

*** Test Cases ***
Verify List Contains Sub List
    # Define the main list and the sub-list
    ${main_list}=    Create List    1    2    3    4    5    6
    ${sub_list}=     Create List    3    4

    # Verify that the main list contains the sub-list
    List Should Contain Sub List    ${main_list}    ${sub_list}

    # Log a message to indicate success
    Log To Console    The main list contains the sub-list
