*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Get Element Text
    ${text} =  get element text   output1.xml   .//first
    log to console  ${text}