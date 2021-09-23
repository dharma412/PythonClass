*** Settings ***
Library            SmaGuiLibrary
Resource           selenium.txt
Suite Setup        Selenium Login
Suite Teardown     Selenium Close


*** Test Cases ***

Edit General Settings
    [Documentation]  Edit all General settings of SMA
    [Tags]  ut0
    Edit General Settings  edit_analytics= False ,edit_securex= False 
    Commit Changes

Enable Securex
    [Documentation]  Enable Cisco Securex on SMA
    [Tags]     ut1

    Edit Securex Settings
    Commit Changes

Disable Securex
    [Documentation]  Disable Cisco Securex on SMA
    [Tags]     ut2

    Edit Securex Settings  ${False}
    Commit Changes

Verify Securex Setting Status
   [Documentation]  Verify Securex Setting Status Enabled or Disabled
   [Tags]  ut3

   ${status}=  Get Securex Edit Setting Status
   Log  ${status}

   Run Keyword If  '${status}'== 'False'
   ...  Log  "Securex Disbaled"

Get General Setting Prefrences
   [Documentation]  Get General Setting Prefrences option and values
   [Tags]  ut4

   ${settings_prefrences}=  Get General Settings Preferences
   Log  ${settings_prefrences}


