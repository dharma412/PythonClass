# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_dsp_proc.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
@{tcp_services_system_process_details}  ftpd.main - The FTP daemon
    ...   ginetd - The INET daemon
    ...   interface - The interface controller for inter-process communication
    ...   ipfw - The IP firewall
    ...   sntpd - The SNTP daemon
    ...   sshd - The SSH daemon
    ...   syslogd - The system logging daemon
    ...   winbindd - The Samba Name Service Switch daemon
@{tcp_services_feature_process_details}  Feature Processes
    ...  euq_webui - GUI for ISQ
    ...  gui - GUI process
    ...  hermes - Mail server for sending alerts, etc.
    ...  java - Processes for storing and querying Web Tracking data
    ...  splunkd - Processes for storing and querying Email Tracking data
@{tcp_services_ip_details}  interface .* IPv4 TCP .*:.*
    ...  nginx .* IPv4 TCP .*:.*
    ...  nginx .* IPv4 TCP .*:*
    ...  euq_webui .* IPv4 TCP .*:.*
    ...  gui .* IPv4 TCP .*:.*
    ...  splunkd .* IPv4 TCP .*:.*
@{status_details}  Status as of: .*
    ...  Appliance available from: .*
    ...  System Uptime: .*
    ...  Last counter reset: .*
    ...  System status: *
    ...  Oldest Message: .*
    ...  Counters: .* .* .*
    ...  Messages Received .* .* .*
    ...  Recipients Received .* .* .*
    ...  Gen. Bounce Recipients .* .* .*
    ...  Rejected Recipients .* .* .*
    ...  Dropped Messages .* .* .*
    ...  Soft Bounced Events .* .* .*
    ...  Completed Recipients .* .* .*
    ...  Hard Bounced Recipients .* .* .*
    ...  Delivered Recipients .* .* .*
    ...  Deleted Recipients .* .* .*
    ...  DomainKeys Signed Msgs .* .* .*
    ...  Gauges: Current
    ...  RAM Utilization
    ...  CPU Utilization
    ...  Quarantine Service
    ...  Reporting Service
    ...  Tracking Service
    ...  Disk I/O Utilization
    ...  Resource Conservation
    ...  Logging Disk Usage
    ...  Logging Disk Available

*** Keywords ***
Verify tcpservices and status command output
    [Arguments]  ${actual_cli_output}  @{expected_cli_output}

    @{actual_cli_output_split_lines}=  Create List
    @{actual_cli_output_split_lines}=  Split To Lines  ${actual_cli_output}
    ${actual_cli_output_list}=  Create list
    FOR  ${value}  IN  @{actual_cli_output_split_lines}
      ${newval}  Replace string using regexp  ${value}   ${SPACE}+    ${SPACE}
      Append to list  ${actual_cli_output_list}  ${newval.strip()}
    END
    Log  ${actual_cli_output_list}
    FOR  ${exp_value}  IN  @{expected_cli_output}
       ${actual_cli}  Convert To String  ${actual_cli_output_list}
       Should match regexp  ${actual_cli}  ${exp_value}
    END

Diagnostic services status check
    [Arguments]  ${diagnostic_service}  ${diagnostic_status_message}
    ${diagnostic_services_status}=  Run keyword  Diagnostic services ${diagnostic_service}  operation=status
    @{diagnostic_service_output} =	Split String	${diagnostic_status_message}  has
    ${status}=  Run keyword and return status  Should match regexp  ${diagnostic_services_status}   ${diagnostic_status_message}
    Run keyword if  '${status}'=='False'  Should match regexp  ${diagnostic_services_status}   @{diagnostic_service_output}[0]is down

Precondition Tvh1340568c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ${sl_is_enabled}=  Smart License Is Enabled
    Run Keyword If  not ${sl_is_enabled}  Smart License Enable
    Centralized Web Reporting Enable
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Pvo Quarantines Enable
    Spam Quarantine Enable
    Commit Changes
    Trailblazer config enable

*** Test Cases ***
Tvh1340568c
    [Documentation]  Tvh1340568c-Display active TCP/IP services (incl. Open ports)
        ...  Tvh1340820c-Verify customer is able to see important customer visible processes using cli command-tcpservices

    [Tags]  cli  Tvh1340568c  Tvh1340820c  smart_license
    [Setup]  Precondition Tvh1340568c
    [Teardown]   Run Keywords  Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  AND  Centralized Web Reporting Disable
    ...  AND  Centralized Email Reporting Disable
    ...  AND  Centralized Email Message Tracking Disable
    ...  AND  Pvo Quarantines Disable
    ...  AND  Spam Quarantine Disable
    ...  AND  Commit Changes

     # Step 1.  cli -> tcpservices
     # Step 2 . Verify All TCP related information with details of feature processes, system processes, etc.,
     ${cli_tcpservices_output}=  Tcp Services
     Verify tcpservices and status command output  ${cli_tcpservices_output}  @{tcp_services_system_process_details}
     Verify tcpservices and status command output  ${cli_tcpservices_output}  @{tcp_services_feature_process_details}
     Verify tcpservices and status command output  ${cli_tcpservices_output}  @{tcp_services_ip_details}

     # Step 3.cli -> status
     # Step 4.Verify status details
     Restart CLI Session
     ${cli_status_output}=  Status
     Verify tcpservices and status command output  ${cli_status_output}  @{status_details}

     # Step 5.cli -> diagnostics ->DISK_USAGE
     Diagnostic Services Reporting  operation=restart
     Diagnostic services status check  reporting  Reporting has been up for *

     # Step 6.cli -> diagnostics ->NETWORK
     Diagnostic Services Tracking  operation=restart
     Diagnostic services status check  tracking  Tracking has been up for *

     # Step 7.cli -> diagnostics ->REPORTING
     Diagnostic Services Euqweb  operation=restart
     Diagnostic services status check  euqweb  End User Quarantine UI has been up for *

     # Step 8.cli -> diagnostics ->TRACKING
     Diagnostic Services Webui  operation=restart
     Diagnostic services status check  webui  Web UI has been up for *

     # Step 9. cli -> diagnostics ->SERVICES
     Diagnostic Services Smartlicense  operation=restart
     Diagnostic services status check  smartlicense   Smart Licensing Agent has been up for *