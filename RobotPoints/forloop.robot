
*** Settings ***
Library    Collections

*** Variables ***
@{list1}        create list    a    b    c
&{dic}          name=teja    age=27    place=narasaraopet
*** Settings ***

*** Test Cases ***
forloop
    FOR  ${attempt}  IN    @{list1}
        log to console    ${attempt}
    END
forloop1
    ${keys} =   get dictionary keys    ${dic}
    ${key1} = Eva
    log to console    ${keys}
    FOR    ${att}    IN    @{keys}
        log to console    ${dic[${att}]}
    END