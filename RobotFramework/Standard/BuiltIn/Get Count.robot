*** Keywords ***
*** Variables ***
@{list1}     1    33    44    432    443    533    1    1    1    1

*** Test Cases ***
GetCountTestcase
    ${count} =  get count    ${list1}    1
    log to console    ${count}
    should be equal as integers    ${count}    5