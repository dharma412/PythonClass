*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    String

*** Variables ***
${var1}    name
@{list}    12    12    778    988    98
&{dictionary}    name=value    name2=value2    name3=value4

*** Keywords ***
RegistartionKeyword
    [Arguments]    ${value1}    ${value2}    ${value3}
    click button
    input text   xpath:   ${value1}
    input text   xpath    ${value2}
    input text   xpath:   ${value3}
    click button

*** Test Cases ***
Test1
    RegistartionKeyword    teja     tejach@gmail.com    0098098