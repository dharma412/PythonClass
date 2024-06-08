*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Keywords ***
SetModify
    Set Modified Time    dic/File232.txt  NOW

*** Test Cases ***
SetEnvironmenetVaribels
    SetModify
