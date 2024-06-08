*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
ListDirectoriesInDirectory
    @{content}=  List Directories In Directory   dic
    log to console  ${content}