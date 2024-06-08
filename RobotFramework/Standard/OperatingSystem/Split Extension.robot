*** Settings ***
Library    String
Library    BuiltIn
Library    robot.libraries.OperatingSystem

*** Test Cases ***
SplitExtensionKeyword
    @{output} =  Split Extension    dic/File232.txt
    log to console  ${output}