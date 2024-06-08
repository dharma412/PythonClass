*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
GetBINARYFILE
    Append To Environment Variable	NAME	first
    ${content}=  get environment variable  NAME
    log to console  ${content}