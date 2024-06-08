*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
ConvertTitileCase
    Append To Environment Variable	NAME	first
    ENVIRONMENT VARIABLE SHOULD BE SET  	NAME