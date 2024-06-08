*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
ConvertTitileCase
    ENVIRONMENT VARIABLE SHOULD NOT BE SET  	NAME