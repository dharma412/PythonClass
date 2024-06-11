*** Settings ***
Variables        Sample.py


*** Test Cases ***
LoginTest
   ${var}=   BuiltIn.Call Method    ${cal}   add    2    8
   log to console    ${var}