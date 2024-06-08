*** Keywords ***
*** Variables ***
@{list1}     1    33    44    432    443    533

*** Test Cases ***
ExitforloopTestcase
    FOR	${var}	IN	@{list1}
    Run Keyword If	'${var}' == '44'	Exit For Loop
    log to console    	${var}
    END