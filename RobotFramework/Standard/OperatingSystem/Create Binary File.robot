*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
CreateBinaryFile
    create binary file    dic/file3.txt   \x01\x00\xe4\x00