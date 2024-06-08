*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
RemoveFiles
    Remove File   dic/File.txt