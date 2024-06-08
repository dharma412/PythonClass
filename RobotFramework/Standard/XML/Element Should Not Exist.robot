*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test Element Should Not Exist
    Element Should Not Exist  output1.xml  .//first1