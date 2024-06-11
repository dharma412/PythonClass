*** Settings ***

*** Variables ***
@{list1} =    1    2    3    76    67    79    77    93
*** Keywords ***
RunKeywordIF1
    [Arguments]    ${name}    ${number}
    log to console    ${name}
    log to console    ${number}

*** Test Cases ***
RunkeywordIFTestcase
    FOR    ${item}    IN    @{list1}
        run keyword if  '${item}'=='77'     RunKeywordIF1   teja    45
    END

RunkeywordIFTestcase2
    FOR    ${item}    IN    @{list1}
        run keyword if  '${item}'=='77'  log to console   I am runing runif keyword
    END