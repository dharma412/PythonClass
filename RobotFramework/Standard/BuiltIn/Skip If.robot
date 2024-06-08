*** Settings ***
*** Variables ***
@{list1}    2    4    5    6    8    10    14
*** Keywords ***
SkipKeyword1
    log to console    skipkeyword1

SkipKeyword2
    log to console    skipkeyword2
SkipKeyword3
    log to console    skipkeyword3
SkipKeyword4
    log to console    skipkeyword4

*** Test Cases ***
skipTestcase1
    FOR    ${ITEM}    IN    @{list1}
        skip if    '${ITEM}'=='8'
        skipkeyword1
        skipkeyword2
        skipkeyword3
    END
