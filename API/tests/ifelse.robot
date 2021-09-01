*** Settings ***
Library    Selenium2Library


*** Variables ***
${var} =  200

*** Test Cases ***
If condition test
    run keyword  if ${var} =200     keyword1

If else condition test
    run keyword  if ${var} >200     keyword1
    ...  ELSE  keyword2
If condition else if else test
    run keyword  if ${var}>200      keyword1
    ...  ELSE IF     ${VAR}==10     Keyword2
    ...  ELSE  Keyword3


*** Keywords ***
Keyword1
    log  True
    open browser
    cli

Keyword2
    log  False

Keyword3
    log  False