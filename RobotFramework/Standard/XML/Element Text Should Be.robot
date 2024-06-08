*** Settings ***
Library  XML
Library  OperatingSystem

*** Test Cases ***
Test element text should be
    element text should be   output1.xml   text   .//first