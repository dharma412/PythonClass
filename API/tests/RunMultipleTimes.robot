*** Variables ***

*** Keywords ***
Multiple
    log  first run
    log  secod run
*** Test Cases ***
Execute Multiple Times
    repeat keyword  2 times  Multiple

