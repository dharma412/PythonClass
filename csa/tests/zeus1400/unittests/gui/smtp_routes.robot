*** Settings ***
Library            SmaGuiLibrary
Resource           selenium.txt
Suite Setup        Selenium Login
Suite Teardown     Selenium Close


*** Test Cases ***
Delete All SMTP Routes
    [Documentation]  Delete all the SMTP Routes
    [Tags]  ut1

    Smtp Routes Add
    ...  ironport.com
    ...  smtp.mysite.com:25

    Smtp Routes Delete  ironport.com
    Smtp Routes Delete   ALL 



