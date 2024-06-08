*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
CopyFilesTestCase
    copy files    File*.txt  dic