*** Settings ***
Library    String
*** Variables ***
${string1}      $$$$python version is 3.9$$$

*** Test Cases ***
SplitString
    @{words} =    split string to characters    ${string1}
    log to console    ${words}
