*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
LogEnvironmentalVariables
     ${path} =  Normalize Path   ${CURDIR}/../Resource/sample.xml
     log to console  ${path}
     log to console  ${CURDIR}
     log to console  ${path}