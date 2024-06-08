*** Settings ***
*** Variables ***

@{mxrecord}    mx1.hc3-25.auto-dev1.nap5.ironport.com    mx2.hc3-25.auto-dev1.nap5.ironport.com    obj1.hc3-25.auto-dev1.nap5.ironport.com
*** Keywords ***


*** Test Cases ***
RegularExpression
    FOR    ${attemp}    IN    @{mxrecord}
        log to console    ${attemp}
        should match regexp    ${attemp}    [[a-z]]*[1-2].
    END

