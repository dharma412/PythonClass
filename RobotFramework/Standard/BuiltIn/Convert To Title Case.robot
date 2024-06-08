*** Settings ***
Library    String
Library    BuiltIn

*** Test Cases ***
ConvertTitileCase
    ${output} =    convert to title case	   .PYTHON
    log to console    ${output}