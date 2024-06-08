*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
LogEnvironmentalVariables
    @{content}=  Log Environment Variables   level=INFO
    log to console  ${content}