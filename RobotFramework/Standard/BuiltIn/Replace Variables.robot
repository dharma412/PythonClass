*** Settings ***
Library  OperatingSystem


*** Test Cases ***
ReplaceTest
    set test variable  ${name}  robot
    ${Contenet}    get file   textfile.txt
    log to console  ${Contenet}
    ${Contenet}  replace variables  ${Contenet}
    log to console  ${Contenet}

