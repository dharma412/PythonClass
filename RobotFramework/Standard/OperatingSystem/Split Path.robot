*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
SplitPathKeyword
    @{output} =  Split Path    dic/File232.txt
    log to console  ${output}