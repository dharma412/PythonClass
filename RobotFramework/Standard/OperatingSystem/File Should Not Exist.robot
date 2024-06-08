*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
FileShouldNotExist
    file should not exist  File3452.txt