*** Settings ***
Library    String
*** Variables ***
${string1}      PYTHONwee

*** Test Cases ***
SplitString
    ${words} =    should be uppercase    ${string1}    msg=given string is not upper case
    log to console    ${words}