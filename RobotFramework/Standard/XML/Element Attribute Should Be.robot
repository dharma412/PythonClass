*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Element Attribute Should Be
    element attribute should be  output1.xml  id  1  .//first