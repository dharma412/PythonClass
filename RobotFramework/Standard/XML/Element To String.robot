*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Element To String
    ${value}=  Element To String   output1.xml   .//first
    log to console  ${value}