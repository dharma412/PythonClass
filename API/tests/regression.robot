
*** Variables ***

${vari1} =  Teja
${var2} =  thsi is second var
@{Listvar} =  teja  dharma  ch
@{ListVar2} =  Create


*** Test Cases ***
Variable Demostration
    Log     ${var2}

Variable Demostarion2
    Log     ${vari1}

Set variable in Tetscase
    ${MyNewVar} =  set variable  this is calss varibale
    log  ${MyNewVar}

Display List Variables
    log  @{Listvar}[0]

Display List Varible2
    @{Listvar2} =   set variable  item1  item2  ietm3
    log  @{listvar2}[0]
    log  @{listvar2}[1]
    log  @{listvar2}[2]

Display List varibale3
    @{LIstvar3} =   create list  item1  item2   item2
    log  @{LIstvar3}[0]
    log  @{LIstvar3}[1]
    log  @{LIstvar3}[2]





# Gloval varibale -access form all test and *** keywords ***
#Suite

