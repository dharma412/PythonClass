*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Add Element In XML
    element text should be   output1.xml   text   .//first
    ${text} =  get element text   output1.xml   .//first
    log to console  ${text}