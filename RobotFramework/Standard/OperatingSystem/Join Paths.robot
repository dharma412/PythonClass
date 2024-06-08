*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
JoinPaths
    @{content}=  Join Paths  ${CURDIR}   dic  dic2
    log to console  ${content}