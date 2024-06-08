*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
GetBINARYFILE
    ${content}=  get modified time  dic/File232.txt
    log to console  ${content}