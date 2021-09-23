# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/sec_web_id3_suite2.txt#3 $
# $Date: 2020/09/07 $
# $Author: mrmohank $

*** Settings ***
Resource    sma/csdlresource.txt
Resource    sma/config_masters.txt
Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Keywords ***
Get Session id from response header
    [Arguments]  ${url}  ${user_agent}

    # Get response header values
    ${response_header}=  Get header response  ${url}  ${user_agent}

    # Get response header Set cookie attribute
    ${response_header_set_cookie_attributes}=  Get From Dictionary  ${response_header}  set-cookie

    # Split the set cookie attributes to individual values and store in list
    @{response_set_cookies}=  Split string  ${response_header_set_cookie_attributes}  ;

    # Check for SID value and return the sid value
    FOR  ${set_cookie_value}  IN   @{response_set_cookies}
      ${sid_value_match}=  Run keyword and return status  Should match regexp  ${set_cookie_value}  .*sid=.*
      Return From Keyword If    '${sid_value_match}' == 'True'    ${set_cookie_value}
      Exit For Loop If   '${sid_value_match}' == 'True'
    END

*** Test Cases ***
Tvh1306061c
    [Documentation]  Tvh1306061c- To verify if a new Session id is created whenever a new session is started.
    [Tags]  Tvh1306061c

    # Step 1. Get sid in set-cookie function in the response header for firefox browser
    ${firefox_header_response_sessionid}=  Get Session id from response header  https://${SMA}/services/system_status  ${user_agent_ff}

    # Step 2. Get sid in set-cookie function in the response header for chrome browser
    ${chrome_header_response_sessionid}=  Get Session id from response header  https://${SMA}/services/system_status  ${user_agent_chrome}

    # Step 3. Check SID values from different browsers are not same
    Should not be equal  ${firefox_header_response_sessionid}  ${chrome_header_response_sessionid}

Tvh1306062c
    [Documentation]  Tvh1306062c- Open a new SMA session and verify if the sid is different from the previous one.
     [Tags]  Tvh1306062c

     # Step 1. Log into DUT and get Session id
     Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
     ${page_url}=  Get Location
     ${header_response_sessionid}=  Get Session id from response header  ${page_url}  ${user_agent_ff}

     # Step 2. Log out of DUT
     Log Out Of Dut

     # Step 3. Log into DUT again and get Session id
     Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
     ${relogin_page_url}=  Get Location
     ${relogin_header_response_sessionid}=  Get Session id from response header  ${relogin_page_url}  ${user_agent_ff}

     # Step 4. Check SID values for different logins are not same
     Should not be equal  ${header_response_sessionid}   ${relogin_header_response_sessionid}

Tvh1306066c
    [Documentation]  Tvh1306066c-In Web->CM-> Identification Profile page  Verify the HTTP Request header
    ...  Tvh1306067c-Web->Utilities>Publish to web Appliances page   Verify the HTTP Request heade
    [Tags]  Tvh1306066c  Tvh1306067c
    [Setup]  Run Keywords  Centralized Web Configuration Manager Enable
    ...  AND  Commit Changes
    ...  AND  Set CMs
    ...  AND  Configuration Masters Initialize    ${sma_config_masters.${CM}}  {True}
    ...  AND  Commit Changes

    Navigate To  Web   ${sma_config_masters.${CM}}  Identification Profiles
    ${configuration_manager_identification_url} =  Get Location
    Verify Set Cookie contents in Response and Request Header   ${configuration_manager_identification_url}

    Navigate To  Web   Utilities  Publish to Web Appliances
    ${publish_to_web_url} =  Get Location
    Verify Set Cookie contents in Response and Request Header    ${publish_to_web_url}

