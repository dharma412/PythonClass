*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
CountFilesInDictionary
    ${count} =  count files in directory    dic
    log to console  ${count}