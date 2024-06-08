*** Settings ***


*** Test Cases ***
catenateMethod
    ${str1} =	Catenate	Hello	world
    log to console    ${str1}
    ${str2} =	Catenate	SEPARATOR=---	Hello	world
    log to console    ${str2}
    ${str3} =	Catenate	SEPARATOR=	Hello	world
    log to console    ${str3}