# $Id: //prod/main/sarf_centos/tests/zeus1350/csdl/sec_web_id_3.txt#1 $
# $Date: 2020/06/10 $
# $Author: mrmohank $

*** Settings ***
Resource        csdlresource.txt
Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
@{set_cookie_attributes}    httponly  Path  SameSite  secure
${user_agent_ff}            Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0
${user_agent_chrome}        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36

*** Keywords ***
Verify Set Cookie contents in Response and Request Header
    [Arguments]  ${url}  ${user_agent}=${user_agent_ff}

    # Send request and get response and request header
    ${response_header}  ${request_header}=  Get header response and request  ${url}  ${user_agent}

    # Get request header session id
    ${request_header_session_id}=  Get From Dictionary  ${request_header}  Cookie

    # Get response header Set cookie attributes
    ${response_header_set_cookie_attributes}=  Get From Dictionary  ${response_header}  set-cookie

    # Verify cookie sid value in the Request Header matches the sid value generated in the Response header .
    Should Contain  ${response_header_set_cookie_attributes}  ${request_header_session_id}

    # Verify response header set cookie session attributes does not contain 'expires'
    Should Not Contain  ${response_header_set_cookie_attributes}  .*expires.*

    # Verify response set cookie contents contains  httponly, Path , SameSite , secure attributes
    : FOR  ${attribute}  IN  @{set_cookie_attributes}
    \  Should Contain  ${response_header_set_cookie_attributes}  ${attribute}

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
Tvh1305981c
    [Documentation]  Tvh1305981c-In Management Appliance>Centralized Services>System Status page verify the HTTP Request & response header
    [Tags]  Tvh1305981c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/system_status

Tvh1305982c
    [Documentation]  Tvh1305982c-In Management Appliance>Centralized Services>Security Appliance page verify the HTTP Request & response header
    [Tags]  Tvh1305982c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/security_appliances

Tvh1305983c
    [Documentation]  Tvh1305983c-In Management Appliance>Centralized Services>Spam Quarantine page verify the HTTP Request header
    [Tags]  Tvh1305983c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/email/spam_quarantine

Tvh1305984c
    [Documentation]  Tvh1305984c-In Management Appliance>Centralized Services>PVO Quarantine page verify the HTTP Request header
    [Tags]  Tvh1305984c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/email/policy_quarantines

Tvh1305985c
    [Documentation]  Tvh1305985c-In Management Appliance>Centralized Services>Email Centralized Reporting page verify the HTTP Request & response header
    [Tags]  Tvh1305985c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/email/centralized_reporting

Tvh1305986c
    [Documentation]  Tvh1305986c-In Management Appliance>Centralized Services>Email Centralized Tracking page verify the HTTP Request header
    [Tags]  Tvh1305986c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/email/centralized_tracking

Tvh1305987c
    [Documentation]  Tvh1305987c-In Management Appliance>Centralized Services>Web Centralized Reporting page verify the HTTP Request header
    [Tags]  Tvh1305987c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/centralized_configuration/centralized_web_reporting

Tvh1305988c
    [Documentation]  Tvh1305988c-In Management Appliance>Centralized Services>Web Centralized Configuration Manager page verify the HTTP Request header
    [Tags]  Tvh1305988c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/centralized_configuration/configuration

Tvh1305990c
    [Documentation]  Tvh1305990c-In Management Appliance>Centralized Services>Web Centralized Upgrade Manager page verify the HTTP Request & response header
    [Tags]  Tvh1305990c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/services/centralized_configuration/centralized_web_upgrades

Tvh1305991c
    [Documentation]  Tvh1305991c-In Management Appliance>Network ->IP Interfaces page verify the HTTP Request header
    [Tags]  Tvh1305991c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/network/ip_interfaces

Tvh1305992c
    [Documentation]  Tvh1305992c-In Management Appliance>Network ->SMTP Routes page verify the HTTP Request header
    [Tags]  Tvh1305992c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/network/smtp_routes

Tvh1305993c
    [Documentation]  Tvh1305993c-In Management Appliance>Network ->Routing page verify the HTTP Request header
    [Tags]  Tvh1305993c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/network/routing

Tvh1305994c
    [Documentation]  Tvh1305994c-In Management Appliance>Network ->DNS page verify the HTTP Request header
    [Tags]  Tvh1305994c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/network/dns

Tvh1305996c
    [Documentation]  Tvh1305996c-In Management Appliance>System Administration-> System Health page verify the HTTP Request header
    [Tags]  Tvh1305996c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/health

Tvh1305997c
    [Documentation]  Tvh1305997c-In Management Appliance>System Administration-> Alerts page verify the HTTP Request header
    [Tags]  Tvh1305997c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/alerts

Tvh1306004c
    [Documentation]  Tvh1306004c-In Management Appliance>System Administration-> Log Subscription page verify the HTTP Request heade
    [Tags]  Tvh1306004c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/log_subscriptions

Tvh1306005c
    [Documentation]  Tvh1306005c-In Management Appliance>System Administration-> Return Addresses page verify the HTTP Request and Response header
    [Tags]  Tvh1306005c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/return_address

Tvh1306006c
    [Documentation]  Tvh1306006c-In Management Appliance>System Administration-> SSL Configuration page verify the HTTP Request and Response header
    [Tags]  Tvh1306006c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/ssl_config

Tvh1306026c
    [Documentation]  Tvh1306026c-In Management Appliance->System Administration-> Users Verify the HTTP Request and Response header
    [Tags]  Tvh1306026c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/access/users

Tvh1306027c
    [Documentation]  Tvh1306027c-In Management Appliance->System Administration-> User Roles page , verify the HTTP Request & response headers
    [Tags]  Tvh1306027c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/access/custom_roles

Tvh1306028c
    [Documentation]  Tvh1306028c-In Management Appliance->System Administration-> Network Access page Verify the HTTP Request & response header
    [Tags]  Tvh1306028c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/access/network_access

Tvh1306029c
    [Documentation]  Tvh1306029c-In Management Appliance->System Administration->LDAP verify the HTTP Request & response header
    [Tags]  Tvh1306029c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/ldap

Tvh1306030c
    [Documentation]  Tvh1306030c-In Management Appliance->System Administration->SAML page  Verify the HTTP Request & response header
    [Tags]  Tvh1306030c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/saml

Tvh1306031c
    [Documentation]  Tvh1306031c-In Management Appliance->System Administration->Disk Management page Verify the HTTP Request & response header
    [Tags]  Tvh1306031c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/disk_management

Tvh1306034c
    [Documentation]  Tvh1306034c-In Management Appliance->System Administration->Time Settings page  Verify the HTTP Request header
    [Tags]  Tvh1306034c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/system_time/time_settings

Tvh1306047c
    [Documentation]  Tvh1306047c-In Management Appliance->System Administration->Shutdown/ Reboot  page  Verify the HTTP Request header
    [Tags]  Tvh1306047c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/system_administration/shutdown_reboot

Tvh1306048c
    [Documentation]  Tvh1306048c-In Email->Reporting ->My Reports page Verify the HTTP Request header
    [Tags]  Tvh1306048c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email/user_report

Tvh1306049c
    [Documentation]  Tvh1306049c-In Email->Reporting -> Overview page Verify the HTTP Request header
    [Tags]  Tvh1306049c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email/mail_reports/overview

Tvh1306050c
    [Documentation]  Tvh1306050c-In Email->Reporting -> Incoming Mail page Verify the HTTP Request header
    [Tags]  Tvh1306050c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email/mail_reports/incoming_mail

Tvh1306051c
    [Documentation]  Tvh1306051c-In Email->Reporting -> Content Filters page Verify the HTTP Request header
    [Tags]  Tvh1306051c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email/mail_reports/content_filters

Tvh1306052c
    [Documentation]  Tvh1306052c-In Email->Reporting -> Scheduled Reports page  Verify the HTTP Request header
    [Tags]  Tvh1306052c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email/email_reports/scheduled_reports

Tvh1306053c
    [Documentation]  Tvh1306053c-In Email->Reporting->Outgoing Destinations  page  Verify the HTTP Request header
    [Tags]  Tvh1306053c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email/mail_reports/destination_domains

Tvh1306055c
    [Documentation]  Tvh1306055c-In Email->Message Quarantine >Spam Quarantine page Verify the HTTP Request header
    [Tags]  Tvh1306055c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email_quarantine/spam_quarantine_search

Tvh1306056c
    [Documentation]  Tvh1306056c-In Email->Message Quarantine >PVO Quarantine  page  Verify the HTTP Request header
    [Tags]  Tvh1306056c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email_quarantine/local_quarantines

Tvh1306057c
    [Documentation]  Tvh1306057c-In Email->Message Tracking  -> Message Tracking page  Verify the HTTP Request header
    [Tags]  Tvh1306057c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_email_tracking/message_tracking

Tvh1306058c
    [Documentation]  Tvh1306058c-In Web->Reporting -> Overview page  Verify the HTTP Request header
    [Tags]  Tvh1306058c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_web/monitor_overview

Tvh1306059c
    [Documentation]  Tvh1306059c-In Web->Reporting -> Scheduled Reports page  Verify the HTTP Request header
    [Tags]  Tvh1306059c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_web/reporting_services/scheduled_reports

Tvh1306060c
    [Documentation]  Tvh1306060c-In Web>Reporting ->My Reports page  Verify the HTTP Request header
    [Tags]  Tvh1306060c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/monitor_web/wsa_user_report

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

Tvh1306063c
    [Documentation]  Tvh1306063c-In Web->Utilities-> Web Appliance Status page  Verify the HTTP Request header
    [Tags]  Tvh1306063c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/web_utilities/appliance_status

Tvh1306064c
    [Documentation]  Tvh1306064c-In Web->Utilities>Security Services Display page  Verify the HTTP Request header
    [Tags]  Tvh1306064c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/web_utilities/display_settings

Tvh1306065c
    [Documentation]  Tvh1306065c-In Web>Utilities >Configuration Masters page  Verify the HTTP Request header
    [Tags]  Tvh1306065c

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/web_utilities/centralized_configuration/configuration_masters

Tvh1306066c
    [Documentation]  Tvh1306066c-In Web->CM-> Identification Profile page  Verify the HTTP Request header
    [Tags]  Tvh1306066c  Tvh1306067c
    [Setup]  Run Keywords  Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  AND  Centralized Web Configuration Manager Enable
    ...  AND  Configuration Masters Initialize    ${sma_config_masters.CM117}  {True}
    ...  AND  Commit Changes

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/prod/web/11_7/web_security_manager/authentication/identities

    Verify Set Cookie contents in Response and Request Header
    ...  https://${SMA}/web_utilities/centralized_configuration/publish

Tvh1306068c
    [Documentation]  Tvh1306068c- In Web>Utilities >Centralized Upgrade page  Verify the HTTP Request header
    [Tags]  Tvh1306068c

     Verify Set Cookie contents in Response and Request Header
     ...  https://${SMA}/web_utilities/centralized_upgrade/centralized_upgrade_manager