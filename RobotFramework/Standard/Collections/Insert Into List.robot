
*** Settings ***
Library  Collections

*** Test Cases ***
Insert Element Into List
    # Define the initial list
    ${my_list}=  Create List  1  2  3  4  5
    # Insert an element into the list at a specific position
    Insert Into List  ${my_list}  2  new_element
    # Log the modified list to verify the insertion
    Log  ${my_list}    console=true
