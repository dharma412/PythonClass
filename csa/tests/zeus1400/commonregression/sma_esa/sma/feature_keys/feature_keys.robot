# $Id: //prod/main/sarf_centos/tests/zeus1350/postel/regression/common/sma_general_functionalities/feature_keys/feature_keys/feature_keys.txt#1 $ $Date: 2019/11/13 $ $Author: sarukakk $

*** Settings ***
Resource  sma/feature_keys.txt

Suite Setup     DefaultRegressionSuiteSetup
Suite Teardown  DefaultRegressionSuiteTeardown
Test Setup      Feature Keys Test Setup
Test Teardown   Feature Keys Test Teardown
Force Tags  feature_keys.general

*** Keywords ***
Feature Keys Test Setup
    DefaultRegressionTestCaseSetup
    Selenium Login

Feature Keys Test Teardown
    DefaultRegressionTestCaseTeardown
    Selenium Close
    Restore Feature  ${sma_fkeys.CENTR_EMAIL_MSG_TRACKING}

*** Test Cases ***
Tvh569614c
    [Tags]  Tvh569614c  standard  invalid_not_applicable_for_smart_license
    [Documentation]   Verify that if feature key expires, the feature is
    ...  disabled
    ...  \n link:  http://tims.cisco.com/warp.cmd?ent=Tvh569614c
    ...  \n 1. Make message tracking feature key expired
    ...  \n 2. Navigate to Management Appliance > Centralized Services >
    ...        Centralized Message Tracking page
    ...  \n 3. Verify that if feature key expires, the feature is disabled

    Set Test Variable  ${Test_Id}  ${TEST NAME}

    ${key_2s}=  Generate Feature Key  ${sma_fkeys.CENTR_EMAIL_MSG_TRACKING}  2
    Feature Keys Submit  ${key_2s}
    Sleep  2s

    Navigate To  Management Appliance  Centralized Services
    ...  Centralized Message Tracking

    Page Should Not Contain Button  Enable...
    Page Should Contain  Feature Key Unavailable
    Page Should Contain
    ...  The feature key for this feature has expired or is unavailable.

Tvh569947c
    [Tags]  Tvh569947c  standard  invalid_not_applicable_for_smart_license
    [Documentation]   Verify that alerts are sent, when feature key are going
    ...  to be expired
    ...  \n link:  http://tims.cisco.com/warp.cmd?ent=Tvh569947c
    ...  \n 1. Generate 2 day and 2 minutes feature key
    ...  \n 2. Activate generated key
    ...  \n 3. Verify that alerts are sent, when feature key are going to be
    ...        expired

    Set Test Variable  ${Test_Id}  ${TEST NAME}

    Null Smtpd Start
    Alerts Add Recipient  testuser@${CLIENT_HOSTNAME}  all-all
    Alerts Edit Settings  ${None}  ${True}  30  60
    Commit Changes

    ${key}=  Generate Feature Key  ${sma_fkeys.CENTR_EMAIL_MSG_TRACKING}  86520
    Feature Key Activate  ${key}

    ${msg} =  Null Smtpd Next Message  timeout=180
    Null Smtpd Stop
    Should Match  "${msg}"
    ...  *Cisco IronPort Centralized Email Message Tracking" key will expire*

Tvh569827c
    [Tags]  Tvh569827c  extended  invalid_not_applicable_for_smart_license
    [Documentation]  Verify that feature key is downloaded from server specified in Update Settings
    ...  \n link:  http://tims.cisco.com/warp.cmd?ent=Tvh569827c
    ...  \n 1. Navigate to Management Appliance > System Administration > Update Settings page
    ...  \n 2. Specify qa10.qa server in Update Settings
    ...  \n 3. Click "Check for New Keys" button on feature keys page
    ...  \n Verify that feature key is downloaded from server specified in Update Settings

    Set Test Variable  ${Test_Id}  Tvh569827c

    ${key_2s}=  Generate Feature Key  ${sma_fkeys.CENTR_EMAIL_MSG_TRACKING}  2
    Feature Keys Submit  ${key_2s}
    Sleep  2s

    ${status} =  Get Feature Status  Cisco IronPort Centralized Email Message Tracking
    Should Be Equal  ${status}  ${fkey_status.EXPIRED}

    ${key}=  Generate Feature Key  ${sma_fkeys.CENTR_EMAIL_MSG_TRACKING}  86520
    Clear Feature Key Update File On Updates Server
    Add Feature Key Update On Updates Server  ${key}

    Update Config Setup
    ...  update_from=Use own
    ...  update_server=http://${FK_UPDATES_SERVER}
    Commit

    ${pending_feature_key}=  Feature Keys Check New Keys
    Should Contain  ${pending_feature_key}  ${sma_fkeys.CENTR_EMAIL_MSG_TRACKING}
    Feature Keys Submit  ${key}

    ${status} =  Get Feature Status  Cisco IronPort Centralized Email Message Tracking
    Should Be Equal  ${status}  ${fkey_status.ACTIVE}
