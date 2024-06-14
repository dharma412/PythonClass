*** Settings ***
Library    String

*** Test Cases ***
ConvertTitileCase
    ${output} =    convert to uppercase    	   .python
    log to console    ${output}