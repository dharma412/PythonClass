*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.DateTime

*** Test Cases ***
ConvertTitileCase
    ${time} =  Add Time To Time	 1 minute	42
    log to console    ${time}