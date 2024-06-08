*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
RunTest
     ${output} =	Run	ls -lhF /tmp
     log to console  ${output}