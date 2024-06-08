*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
GetBINARYFILE
    ${content}=  get binary file  dic/file3.txt
    log to console  ${content}