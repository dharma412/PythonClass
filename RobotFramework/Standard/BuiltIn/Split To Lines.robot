*** Settings ***
Library    String
*** Variables ***
${string1}      python version is 3.9\n
...             we are learning it now \n
...             we are learning  \n
...             we are learning it\n
...             we are  \n

*** Test Cases ***
SplitString
    #@{words} =    split string    ${string1}
    @{words} =    split to lines    ${string1}    -1
    log to console    ${words}