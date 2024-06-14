# syntax to create dictionary  is  &{variablename}
*** Settings ***
Library    Collections
Library    SeleniumLibrary


*** Variables ***
${type}    Test
@{list}    12    4    6    76    644    654    76
&{url}    Test=https://www.w3schools.com/default.asp    Test1=https://www.youtube.com/watch?v=P8lpTs7j3Vw    Test2=https://www.guru99.com/
*** Test Cases ***
ListDIsplay
    log to console    ${url.Test}
    log to console    ${url}[Test]

ExecuteBrowsers
    open browser    ${url.${type}}    chrome

CreateDictionarTestcase
    &{dic1} =    create dictionary    name=dharma    mble=8008461613
    log to console    ${dic1}
    &{dic2} =    create dictionary    name  dhama    mobile    7075046314
    log to console    ${dic2}
    Should Be True	${dic1} == {'name': 'dharma','mble': '8008461613'}



