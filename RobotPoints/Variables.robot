*** Keywords ***

*** Variables ***

# 4 tyep of variables 1.scalr 2.list 3.dictionary 4.environment
${scalar}     teja
${scalar}    set vari
@{list1}
&{dic}
%{var} - environment variable
@{list1}        create list    a    b    c




*** Keywords ***
AssignVariable
    ${scalar}       set variable    hello world.
    log to console    ${scalar}
    @{list1}        create list    a    b    c
    &{dic}          create dictionary    name=teja      age=25
    %{var}
    ${scalar}    evaluate    datetime.date.today()

*** Test Cases ***
VariableTest
    log to console    ${scalar}
