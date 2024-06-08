*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
ShouldNotExist
    Should Not Exist    dic/File232.txt