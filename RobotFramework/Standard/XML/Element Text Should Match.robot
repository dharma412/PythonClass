*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Element Attribute Should Match
    Element Attribute Should Match  output1.xml  id  1  .//first