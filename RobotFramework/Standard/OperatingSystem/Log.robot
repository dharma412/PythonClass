*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
LogEnvironmentalVariables
    Log  dic/LogFiles34.txt   level=INFO
    ${getcontent} =  Get File  dic/LogFiles34.txt
    log to console  ${getcontent}