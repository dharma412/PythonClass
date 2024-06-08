*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Get Element Attributes
    ${attribute} =  Get Element Attributes  output1.xml  .//first
    log to console  ${attribute}