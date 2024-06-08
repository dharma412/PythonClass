*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
RemoveEnvironmentVaribles
    Append To Environment Variable	NAME	first
    Remove Environment Variable   NAME