*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
CountItemsInDictionary
    ${count} =  count items in directory    dic
    log to console  ${count}