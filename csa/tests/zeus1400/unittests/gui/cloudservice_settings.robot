*** Settings ***
Library            SmaGuiLibrary
Resource           selenium.txt
Suite Setup        Selenium Login
Suite Teardown     Selenium Close

*** Keywords ***
Verify Registration Status
    ${status}=  Is Appliance Registered In Cloud
    Should Be True  ${status}

*** Test Cases ***
Cloud Service Enable
    [Documentation]  Enable Cisco Cloud Service on SMA
    [Tags]     ut1

    Enable Cloud Service     APJC (api.apj.sse.itd.cisco.com)
    Commit Changes

    ${status}=    Get Cloud_ Service Status
    Should Be Equal    ${status}    Enabled

    ${settings}=      Get Cloud Service Settings
    LogMany      ${settings}


Disable Cloud Service
    [Documentation]  Disable Cloud service status
    [Tags]     ut2

    Disable Cloud Service
    Commit Changes

    ${status}=    Get Cloud_ Service Status
    Should Be Equal    ${status}    Disabled

Cloud Service Settings
    [Documentation]  Get Cloud Service Settings on SMA
    [Tags]     ut3

    ${settings}=      Get Cloud Service Settings
    LogMany      ${settings}

Register Cloud Service
    [Documentation]  Register Cloud Service Settings on SMA
    [Tags]     ut4

    Enable Cloud Service     NAM (api-sse.cisco.com)
    Commit Changes

    Register Cloud  86230e0cbe69d4355cc0146f79671f11
    Commit Changes

Verif Cloud Registration Status
    [Documentation]    Get Registeration status
    [Tags]     ut5

    Wait Until Keyword Succeeds  2 min  10 sec   Verify Registration Status


Deregister Cloud Service
   [Documentation]  Deregister Cloud Service Settings
   [Tags]     ut6


   Deregister Cloud
   Commit Changes

   ${status}=  Is Appliance Registered In Cloud
   Should Not Be True  ${status}





