*** Keywords ***
*** Variables ***
@{list1}     1    33    44    432    443    533

*** Test Cases ***
ExitforloopTestcase
    FOR	${var}	IN	@{list1}
    EXIT FOR LOOP IF   '${var}' == '44'
    log to console    	${var}
    END