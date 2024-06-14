*** Keywords ***
*** Variables ***


*** Test Cases ***
GetCountTestcase
    ${length} =	Get Length	Hello, world!
    Should Be Equal As Integers	${length}	13