*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
AppendContentToFile
    append to file    File2.txt   This is new file content added
