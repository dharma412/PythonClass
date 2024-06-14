
*** Settings ***
Library  Collections

*** Test Cases ***
Keep Specific Keys In Dictionary
    # Define the initial dictionary
    ${my_dict}=    Create Dictionary    key1=value1    key5=value2    key3=value3    key4=value4

    keep in dictionary    ${my_dict}    key1     key5
    log to console    ${my_dict}

#    # Define the keys to keep
#    ${keys_to_keep}=    Create List    key1    key3
#    # Create a new dictionary with only the keys to keep
#    ${filtered_dict}=    Create Dictionary
#    FOR    ${key}    IN    @{keys_to_keep}
#        ${value}=    Get From Dictionary    ${my_dict}    ${key}
#        Keep in Dictionary    ${filtered_dict}    ${key}    ${value}
#    # Log the filtered dictionary to verify the result
#    END
#    Log To Console    ${filtered_dict}

