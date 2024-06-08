*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.DateTime

*** Test Cases ***
ConvertTitileCase
    ${output} =  Add Time To Date   2014-05-28 12:05:03.111	7 days
    log to console    ${output}