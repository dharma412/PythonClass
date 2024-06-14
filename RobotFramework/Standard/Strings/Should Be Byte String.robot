*** Settings ***
Library    String
*** Variables ***
${string1}       b'65 112 112 108 101'

*** Test Cases ***
SplitString
    ${words} =    should be byte string    ${string1}    msg=given string is not bytre string
    log to console    ${words}