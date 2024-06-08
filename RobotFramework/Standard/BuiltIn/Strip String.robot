*** Settings ***
Library    String
*** Variables ***
${string1}      $$$$python version is 3.9$$$

*** Test Cases ***
SplitString
    #@{words} =    split string    ${string1}
    ${words} =    strip string    ${string1}    mode=right    characters=$
    log to console    ${words}
