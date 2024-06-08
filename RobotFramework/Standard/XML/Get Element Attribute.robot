*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Get Element Attribute
    ${attribute} =  Get Element Attribute  output1.xml  id  .//first
    log to console  ${attribute}