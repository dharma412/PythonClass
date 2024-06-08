*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
RemoveFiles
    Remove Files   dic/file3.txt   dic/Files2.txt