*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
GetBINARYFILE
    ${content}=  get file  dic/File2.txt
    log to console  ${content}