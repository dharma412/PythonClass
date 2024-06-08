*** Settings ***

*** Variables ***
@{list1}    1    33    44    432    443    533

*** Test Cases ***

continueforloopIfTest
    FOR	${var}	IN	@{list1}
        Continue For Loop If	'${var}' == '44'
        log to console    	${var}
    END