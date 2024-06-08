*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
GetBINARYFILE
    ${content}=  get file size  dic/file3.txt
    log to console  ${content}