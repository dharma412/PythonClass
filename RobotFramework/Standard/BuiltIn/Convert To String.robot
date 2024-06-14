Convert To String
*** Settings ***
Library           BuiltIn

*** Test Cases ***
Convert Various Types To String
    ${number}       Set Variable     123
    ${list}         Create List      item1    item2    item3
    ${dictionary}   Create Dictionary    key1=value1    key2=value2

    log to console    ${dictionary}
    ${type1}=   Evaluate    type(${dictionary})
    log to console    ${type1}

    ${number_str}   Convert To String    ${number}
    ${list_str}     Convert To String    ${list}
    ${dict_str}     Convert To String    ${dictionary}

    Log To Console  Number as string: ${number_str}
    Log To Console  List as string: ${list_str}
    Log To Console  Dictionary as string: ${dict_str}

    ${type1}=   Evaluate    type(${list_str})
    log to console    ${type1}
