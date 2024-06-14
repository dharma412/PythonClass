*** Settings ***
Library    String

*** Test Cases ***
ConvertLower
    ${output} =    convert to lowercase    .PYTHON
    log to console    ${output}

