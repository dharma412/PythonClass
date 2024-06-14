*** Settings ***


*** Test Cases ***
catenateMethod
    ${str1} =	Catenate	Python    Version
    log to console    ${str1}
    ${str2} =	Catenate	SEPARATOR=---	Python	Version
    log to console    ${str2}
    ${str3} =	Catenate	SEPARATOR=	Python	Version
    log to console    ${str3}