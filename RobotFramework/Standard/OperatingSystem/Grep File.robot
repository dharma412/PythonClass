*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
GetBINARYFILE
    ${content}=  grep file  dic/File2.txt   [a-z]*
    log to console  ${content}