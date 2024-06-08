*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
FileShouldNotBeEmpty
    file should not be empty  File2.txt