*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
ListDirectoriesInDirectory
    @{content}=  List Directory  dic
    log to console  ${content}