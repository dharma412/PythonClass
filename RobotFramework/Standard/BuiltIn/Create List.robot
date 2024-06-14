
# syntax to create dictionary  is  &{variablename}
*** Settings ***
Library    Collections
Library    SeleniumLibrary


*** Test Cases ***

CreateDictionarTestcase
    ${dic1} =    Create List    12    4    6    76    644    654    76
    log to console    ${dic1}


