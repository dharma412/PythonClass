*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
CountDirectoriesInDirectory
    ${count} =  count directories in directory    dic
    log to console  ${count}