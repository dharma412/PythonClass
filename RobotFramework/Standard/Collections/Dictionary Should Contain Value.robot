*** Settings ***
Library  Collections

*** Variables ***
&{MY DICTIONARY}    key1=value1    key2=value2    key3=value3

*** Test Cases ***
Dictionary Should Contain Value Example
#    ${values}=    Get Dictionary Values    ${MY DICTIONARY}
#    List Should Contain Value    ${values}    value1
#    List Should Contain Value    ${values}    value2
#    List Should Contain Value    ${values}    value3

    Dictionary Should Contain Value     ${MY DICTIONARY}    value1