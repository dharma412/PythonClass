*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Element Should Exist
    Element Should Exist  output1.xml  .//first