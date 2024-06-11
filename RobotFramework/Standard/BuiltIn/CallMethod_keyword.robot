*** Settings ***
Variables     Sample.py


*** Test Cases ***
LoginTest
   ${var}=   Call Method    ${cal}   add
   log to console    ${var}