*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${username}    teja@gami.com
${password}    jdjhjdjd

*** Test Cases ***
Testcase
    open browser    https://www.facebook.com/login/   Chrome
    #close browser



