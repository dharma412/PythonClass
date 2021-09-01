*** Variables ***

${MYGLOBAL}=    Set Varible  some information

*** Test Cases ***
Create and log var
    ${var1} =   set variable  some information
    log     ${MYGLOBAL}

Create and log var2
    log     ${MYGLOBAL}