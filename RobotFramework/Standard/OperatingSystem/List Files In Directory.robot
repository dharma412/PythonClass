*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
List Files In Directory
    @{content}=  List Files In Directory  dic
    log to console  ${content}