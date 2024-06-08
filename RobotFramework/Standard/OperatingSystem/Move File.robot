*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
LogEnvironmentalVariables
     Move File   Files2.txt   dic/