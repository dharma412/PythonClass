*** Settings ***

*** Variables ***
@{list1}    1    33    44    432    443    533

*** Keywords ***
continueforloopkeyword
    log to console    contineloop

*** Test Cases ***
continueforloopTest
    FOR	${var}	IN	@{list1}
        #log to console    ${var}
        Run Keyword If	'${var}'=='44'  continue for loop
        log to console    	${var}
    END

