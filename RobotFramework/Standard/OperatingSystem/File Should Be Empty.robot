*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
FileShouldbeEmpty
    file should be empty  File.txt
