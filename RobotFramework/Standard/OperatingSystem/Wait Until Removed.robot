*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
WaitUntilRemoveKeyword
     Wait Until Removed   dic/dic2