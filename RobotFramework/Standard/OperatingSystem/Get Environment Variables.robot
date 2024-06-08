*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem



*** Test Cases ***
GetBINARYFILE
    Append To Environment Variable	NAME	first  dharma
    ${content}=  get environment variables
    log to console  ${content}