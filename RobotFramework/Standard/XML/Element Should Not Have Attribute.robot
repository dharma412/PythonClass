*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Element Should Not Have Attribute
    Element Should Not Have Attribute  output1.xml  id1  .//first