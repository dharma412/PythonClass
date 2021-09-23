# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/sec_web_id3_suite1.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown
Test Template   Verify Set Cookie contents in Response and Request Header

*** Test Cases ***
Tvh1305981c
    [Documentation]  Tvh1305981c-In Management Appliance>Centralized Services>System Status page verify the HTTP Request & response header
    [Tags]  Tvh1305981c

    https://${dut}/services/system_status

Tvh1305982c
    [Documentation]  Tvh1305982c-In Management Appliance>Centralized Services>Security Appliance page verify the HTTP Request & response header
    [Tags]  Tvh1305982c

    https://${dut}/services/security_appliances

Tvh1305983c
    [Documentation]  Tvh1305983c-In Management Appliance>Centralized Services>Spam Quarantine page verify the HTTP Request header
    [Tags]  Tvh1305983c

    https://${dut}/services/email/spam_quarantine

Tvh1305984c
    [Documentation]  Tvh1305984c-In Management Appliance>Centralized Services>PVO Quarantine page verify the HTTP Request header
    [Tags]  Tvh1305984c

    https://${dut}/services/email/policy_quarantines

Tvh1305985c
    [Documentation]  Tvh1305985c-In Management Appliance>Centralized Services>Email Centralized Reporting page verify the HTTP Request & response header
    [Tags]  Tvh1305985c

    https://${dut}/services/email/centralized_reporting

Tvh1305986c
    [Documentation]  Tvh1305986c-In Management Appliance>Centralized Services>Email Centralized Tracking page verify the HTTP Request header
    [Tags]  Tvh1305986c

    https://${dut}/services/email/centralized_tracking

Tvh1305987c
    [Documentation]  Tvh1305987c-In Management Appliance>Centralized Services>Web Centralized Reporting page verify the HTTP Request header
    [Tags]  Tvh1305987c

    https://${dut}/services/centralized_configuration/centralized_web_reporting

Tvh1305988c
    [Documentation]  Tvh1305988c-In Management Appliance>Centralized Services>Web Centralized Configuration Manager page verify the HTTP Request header
    [Tags]  Tvh1305988c

    https://${dut}/services/centralized_configuration/configuration

Tvh1305990c
    [Documentation]  Tvh1305990c-In Management Appliance>Centralized Services>Web Centralized Upgrade Manager page verify the HTTP Request & response header
    [Tags]  Tvh1305990c

    https://${dut}/services/centralized_configuration/centralized_web_upgrades

Tvh1305991c
    [Documentation]  Tvh1305991c-In Management Appliance>Network ->IP Interfaces page verify the HTTP Request header
    [Tags]  Tvh1305991c

    https://${dut}/network/ip_interfaces

Tvh1305992c
    [Documentation]  Tvh1305992c-In Management Appliance>Network ->SMTP Routes page verify the HTTP Request header
    [Tags]  Tvh1305992c

    https://${dut}/network/smtp_routes

Tvh1305993c
    [Documentation]  Tvh1305993c-In Management Appliance>Network ->Routing page verify the HTTP Request header
    [Tags]  Tvh1305993c

    https://${dut}/network/routing

Tvh1305994c
    [Documentation]  Tvh1305994c-In Management Appliance>Network ->DNS page verify the HTTP Request header
    [Tags]  Tvh1305994c

    https://${dut}/network/dns

Tvh1305995c
    [Documentation]  Tvh1305995c-In Management Appliance-> Network ->Cloud Service Settings page verify the HTTP Request header
    [Tags]  Tvh1305995c

    https://${dut}/network/cloud_service_settings

Tvh1305996c
    [Documentation]  Tvh1305996c-In Management Appliance>System Administration-> System Health page verify the HTTP Request header
    [Tags]  Tvh1305996c

    https://${dut}/system_administration/health

Tvh1305997c
    [Documentation]  Tvh1305997c-In Management Appliance>System Administration-> Alerts page verify the HTTP Request header
    [Tags]  Tvh1305997c

    https://${dut}/system_administration/alerts

Tvh1306004c
    [Documentation]  Tvh1306004c-In Management Appliance>System Administration-> Log Subscription page verify the HTTP Request heade
    [Tags]  Tvh1306004c

    https://${dut}/system_administration/log_subscriptions

Tvh1306005c
    [Documentation]  Tvh1306005c-In Management Appliance>System Administration-> Return Addresses page verify the HTTP Request and Response header
    [Tags]  Tvh1306005c

    https://${dut}/system_administration/return_address

Tvh1306006c
    [Documentation]  Tvh1306006c-In Management Appliance>System Administration-> SSL Configuration page verify the HTTP Request and Response header
    [Tags]  Tvh1306006c

    https://${dut}/system_administration/ssl_config

Tvh1306026c
    [Documentation]  Tvh1306026c-In Management Appliance->System Administration-> Users Verify the HTTP Request and Response header
    [Tags]  Tvh1306026c

    https://${dut}/system_administration/access/users

Tvh1306027c
    [Documentation]  Tvh1306027c-In Management Appliance->System Administration-> User Roles page , verify the HTTP Request & response headers
    [Tags]  Tvh1306027c

    https://${dut}/system_administration/access/custom_roles

Tvh1306028c
    [Documentation]  Tvh1306028c-In Management Appliance->System Administration-> Network Access page Verify the HTTP Request & response header
    [Tags]  Tvh1306028c

    https://${dut}/system_administration/access/network_access

Tvh1306029c
    [Documentation]  Tvh1306029c-In Management Appliance->System Administration->LDAP verify the HTTP Request & response header
    [Tags]  Tvh1306029c

    https://${dut}/system_administration/ldap

Tvh1306030c
    [Documentation]  Tvh1306030c-In Management Appliance->System Administration->SAML page  Verify the HTTP Request & response header
    [Tags]  Tvh1306030c

    https://${dut}/system_administration/saml

Tvh1306031c
    [Documentation]  Tvh1306031c-In Management Appliance->System Administration->Disk Management page Verify the HTTP Request & response header
    [Tags]  Tvh1306031c

    https://${dut}/system_administration/disk_management

Tvh1306034c
    [Documentation]  Tvh1306034c-In Management Appliance->System Administration->Time Settings page  Verify the HTTP Request header
    [Tags]  Tvh1306034c

    https://${dut}/system_administration/system_time/time_settings

Tvh1306047c
    [Documentation]  Tvh1306047c-In Management Appliance->System Administration->Shutdown/ Reboot  page  Verify the HTTP Request header
    [Tags]  Tvh1306047c

    https://${dut}/system_administration/shutdown_reboot

Tvh1306048c
    [Documentation]  Tvh1306048c-In Email->Reporting ->My Reports page Verify the HTTP Request header
    [Tags]  Tvh1306048c

    https://${dut}/monitor_email/user_report

Tvh1306049c
    [Documentation]  Tvh1306049c-In Email->Reporting -> Overview page Verify the HTTP Request header
    [Tags]  Tvh1306049c

    https://${dut}/monitor_email/mail_reports/overview

Tvh1306050c
    [Documentation]  Tvh1306050c-In Email->Reporting -> Incoming Mail page Verify the HTTP Request header
    [Tags]  Tvh1306050c

    https://${dut}/monitor_email/mail_reports/incoming_mail

Tvh1306051c
    [Documentation]  Tvh1306051c-In Email->Reporting -> Content Filters page Verify the HTTP Request header
    [Tags]  Tvh1306051c

    https://${dut}/monitor_email/mail_reports/content_filters

Tvh1306052c
    [Documentation]  Tvh1306052c-In Email->Reporting -> Scheduled Reports page  Verify the HTTP Request header
    [Tags]  Tvh1306052c

    https://${dut}/monitor_email/email_reports/scheduled_reports

Tvh1306053c
    [Documentation]  Tvh1306053c-In Email->Reporting->Outgoing Destinations  page  Verify the HTTP Request header
    [Tags]  Tvh1306053c

    https://${dut}/monitor_email/mail_reports/destination_domains

Tvh1306055c
    [Documentation]  Tvh1306055c-In Email->Message Quarantine >Spam Quarantine page Verify the HTTP Request header
    [Tags]  Tvh1306055c

    https://${dut}/monitor_email_quarantine/spam_quarantine_search

Tvh1306056c
    [Documentation]  Tvh1306056c-In Email->Message Quarantine >PVO Quarantine  page  Verify the HTTP Request header
    [Tags]  Tvh1306056c

    https://${dut}/monitor_email_quarantine/local_quarantines

Tvh1306057c
    [Documentation]  Tvh1306057c-In Email->Message Tracking  -> Message Tracking page  Verify the HTTP Request header
    [Tags]  Tvh1306057c

    https://${dut}/monitor_email_tracking/message_tracking

Tvh1306058c
    [Documentation]  Tvh1306058c-In Web->Reporting -> Overview page  Verify the HTTP Request header
    [Tags]  Tvh1306058c

    https://${dut}/monitor_web/monitor_overview

Tvh1306059c
    [Documentation]  Tvh1306059c-In Web->Reporting -> Scheduled Reports page  Verify the HTTP Request header
    [Tags]  Tvh1306059c

    https://${dut}/monitor_web/reporting_services/scheduled_reports

Tvh1306060c
    [Documentation]  Tvh1306060c-In Web>Reporting ->My Reports page  Verify the HTTP Request header
    [Tags]  Tvh1306060c

    https://${dut}/monitor_web/wsa_user_report

Tvh1306063c
    [Documentation]  Tvh1306063c-In Web->Utilities-> Web Appliance Status page  Verify the HTTP Request header
    [Tags]  Tvh1306063c

    https://${dut}/web_utilities/appliance_status

Tvh1306064c
    [Documentation]  Tvh1306064c-In Web->Utilities>Security Services Display page  Verify the HTTP Request header
    [Tags]  Tvh1306064c

    https://${dut}/web_utilities/display_settings

Tvh1306065c
    [Documentation]  Tvh1306065c-In Web>Utilities >Configuration Masters page  Verify the HTTP Request header
    [Tags]  Tvh1306065c

    https://${dut}/web_utilities/centralized_configuration/configuration_masters

Tvh1306068c
    [Documentation]  Tvh1306068c- In Web>Utilities >Centralized Upgrade page  Verify the HTTP Request header
    [Tags]  Tvh1306068c

     https://${dut}/web_utilities/centralized_upgrade/centralized_upgrade_manager