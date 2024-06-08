*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
JoinPath
    ${content}=  Join Path  ${CURDIR}   dic
    log to console  ${content}