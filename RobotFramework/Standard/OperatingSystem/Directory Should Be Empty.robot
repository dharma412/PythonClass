*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
DirectoryShouldBeEmpty
    directory should be empty  dic