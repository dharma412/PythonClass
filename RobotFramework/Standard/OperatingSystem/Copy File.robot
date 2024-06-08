*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
CopyFileTestCase
    copy file    dic/File.txt   ..//DateTime