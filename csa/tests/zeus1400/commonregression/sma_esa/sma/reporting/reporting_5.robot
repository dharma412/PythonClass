# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/reporting/reporting_5.txt#12 $
# $DateTime: 2020/06/07 21:40:56 $
# $Author: sumitada $

*** Settings ***
Resource     esa/global.txt
Resource     sma/global_sma.txt
Resource     sma/esasma.txt
Resource     esa/injector.txt
Resource     sma/reports_keywords.txt
Resource     regression.txt
Resource     esa/logs_parsing_snippets.txt
Variables    sma/constants.py

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Initialize Suite
Suite Teardown  Finalize Suite

*** Variables ***
${DATA_UPDATE_TIMEOUT}=              20m
${NO_DATA_IMAGE_MD5}=                5432ae167562581bff63ba0f6d615143
${RETRY_TIME}=                       20s
${DEFAULT_SSL_METHOD}=               SSL v3 and TLS v1
${DEFAULT_SSL_CIPHER}=               RC4-SHA:RC4-MD5:ALL
${REPORTING_GROUP_NAME}=             test_group
${REPORTING_GROUP}=                  testgroup
${DOMAIN_BASED_REPORT_TITLE}=        domain_based_report
${INCOMING_MAIL_REPORT_TITLE}=       incoming_mail_report
${REPORT_RECIPIENT}=                 testuser@cisco.com
${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  4
${firefox_prefs_browser.download.dir}=                          %{SARF_HOME}/tmp
${firefox_prefs_browser.download.folderList}=                   2
${firefox_prefs_browser.download.manager.showWhenStarting}=     false
${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=        application/pdf,text/csv,application/csv
${SESSION_TIMEOUT}                   1440
${PDF2TXT_PATH}                      /usr/bin/pdf2txt.py


*** Keywords ***
Initialize Suite
    Set Appliance Under Test To ESA
    global.DefaultTestSuiteSetup  should_revert_to_initial=${False}
    ${PUBLIC_LISTENER}=  Get ESA Listener
    ${PRIVATE_LISTENER} =  Get ESA Listener  scope=Private
    Set Suite Variable  ${PUBLIC_LISTENER}
    Set Suite Variable  ${PRIVATE_LISTENER}
    ${ESA_PUBLIC_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUBLIC_LISTENER_IP}
    ${ESA_PRIVATE_LISTENER_IP}=  Get ESA Private IP
    Set Suite Variable  ${ESA_PRIVATE_LISTENER_IP}
    ${settings}=  Create Dictionary  Web UI Inactivity Timeout  60
    Network Access Edit  ${settings}
    Commit Changes
    Admin Access Config Timeout   timeout_webui=1440  timeout_cli=1440
    Commit
    Diagnostic Reporting Delete DB  confirm=yes
    Reporting Config Setup  enable=yes
    Commit

    Set Appliance Under Test To SMA
    global_sma.DefaultTestSuiteSetup
    Close Browser
    Selenium Login With Autodownload Enabled  ${firefox_prefs_browser.download.dir}  ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  c_rep_processing  duration=2592000
    Commit Changes
    Admin Access Config Timeout   timeout_webui=1440  timeout_cli=1440
    Commit
    Diagnostic Reporting Delete DB  confirm=yes
    Centralized Email Reporting Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  ${SESSION_TIMEOUT}
    Commit Changes

    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp(dir="%{SARF_HOME}/tmp")  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}

Finalize Suite
    Remove Directory  ${SUITE_TMP_DIR}  recursive=${True}
    ${fpath}=  Catenate  SEPARATOR=/  %{SARF_HOME}  tmp
    Run  sudo rm -rf ${fpath}/*.pdf
    Switch To ESA
    Diagnostic Reporting Delete DB  confirm=yes
    Reporting Config Setup  enable=no
    Commit
    global.DefaultTestSuiteTeardown

    Switch To SMA
    Diagnostic Reporting Delete DB  confirm=yes
    Security Appliances Delete Email Appliance  ${ESA}
    Centralized Email Reporting Disable
    Network Access Edit Settings  60
    Commit Changes
    global_sma.DefaultTestSuiteTeardown

Enable Reporting on ESA
    Reporting Config Setup  enable=yes
    Commit

Enable Reporting on SMA
    Centralized Email Reporting Enable
    Commit Changes

General Test Case Setup
    FOR  ${dut_type}  IN  ESA  SMA
      Switch To ${dut_type}
      Run Keyword And Ignore Error  Start CLI Session If Not Open
      Diagnostic Reporting Delete DB  confirm=yes
      Run Keyword If  '${dut_type}' == 'ESA'
      ...  Enable Reporting on ESA
      Run Keyword If  '${dut_type}' == 'SMA'
      ...  Enable Reporting on SMA
      Set Appliance Under Test To ${dut_type}
      DefaultTestCaseSetup
    END

General Test Case Teardown
	Select Window  MAIN
    OperatingSystem.Empty Directory  ${SUITE_TMP_DIR}
    Log  ${CLIENT_HOSTNAME}
    @{files}=  OperatingSystem.List Files In Directory  %{SARF_HOME}/tmp  *.csv  absolute
    Log  ${files}

    @{files1}=  OperatingSystem.List Files In Directory  %{SARF_HOME}/tmp  *.pdf  absolute
    Log  ${files1}

    ${len_files}=  Get Length  ${files}
    Run Keyword If  '${len_files}' != '0'
    ...  Cleanup Files  @{files}

    ${len_files}=  Get Length  ${files1}
    Run Keyword If  '${len_files}' != '0'
    ...  Cleanup Files  @{files1}

    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Sync Appliances Datetime  ${SMA}  ${ESA}
    FOR  ${dut_type}  IN  SMA  ESA
      Switch To ${dut_type}
      DefaultTestCaseTeardown
    END

Cleanup Files
   [Arguments]  @{files}
   FOR  ${file}  IN  @{files}
      Remove File  ${file}
   END

Switch To ${dut}
    Set Appliance Under Test To ${dut}
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Execute JavaScript  window.focus()
    Run Keyword And Ignore Error  Log Into DUT

Prepare TXT File With Domain IP
    [Arguments]  ${ip_addr}=${CLIENT_IP}
    ${rand_str}=  Generate Random String
    ${fname}=  Catenate  SEPARATOR=.  ${rand_str}  txt
    ${fpath}=  Catenate  SEPARATOR=/  %{SARF_HOME}  tmp  ${fname}
    OperatingSystem.Create File  ${fpath}
    Append To File  ${fpath}  ${ip_addr}
    Copy File To DUT  ${fpath}  /data/pub/
    OperatingSystem.Remove File  ${fpath}
    [Return]  ${fname}

Set Mail Flow Policies To TLS ${value}
    ${policy_settings}=  Mail Flow Policies Create Settings
    ...  TLS  ${value}
    ...  Verify Client Certificate  ${False}
    Mail Flow Policies Edit  ${PUBLIC_LISTENER.name}  default  ${policy_settings}

Set Destination Controls To TLS Support ${value}
    ${dest_controls_settings}=  Create Dictionary  TLS Support  ${value}
    Destination Controls Edit  default  ${dest_controls_settings}

Inject ${count} Clean Messages To ${type} Listener With TLS Option ${option}
    Inject Messages
    ...  rcpt-host-list=${CLIENT_HOSTNAME}
    ...  num-msgs=${count}
    ...  inject-host=${${type.upper()}_LISTENER.ipv4}
    ...  tls=${option}

Chart ${name} Should Not Be Empty
    ${chart_md5}=  Email Reporting Charts Get Md5 Hash  ${name}  password=${DUT_ADMIN_SSW_PASSWORD}
    Log  ${chart_md5}
    ${result}  ${msg}=  Run Keyword And Ignore Error
    ...  Should Not Be Equal As Strings  ${chart_md5}  ${NO_DATA_IMAGE_MD5}
    # add screenshot into log if checksum of empty chart and existing one aren't equal
    Run Keyword If  '${result}' == 'FAIL'  Capture Screenshot
    Run Keyword If  '${result}' == 'FAIL'  Fail  ${msg}

Verify TLS Reporting On SMA
    [Arguments]  ${connection_type}  ${period}=Day
    ...  ${successful_required}=0  ${successful_preferred}=0
    ...  ${failed_required}=0  ${failed_preferred}=0  ${unencrypted}=0
    ...  ${domain}=${None}  ${last_tls_status}=${None}
    ${total_tls_encrypted}=  Evaluate
    ...  str(${successful_required} + ${successful_preferred})
    ${total_successful}=  Evaluate  str(${total_tls_encrypted} + ${unencrypted})
    ${total_tls}=  Evaluate
    ...  str(${total_tls_encrypted} + ${failed_required} + ${failed_preferred})
    ${total_connections}=  Evaluate  str(${total_tls} + ${unencrypted})
    @{expected_summary_table}=  Create List
    ...  ${successful_required}  ${successful_preferred}  ${failed_required}
    ...  ${failed_preferred}  ${unencrypted}  ${total_connections}
    @{expected_messages_summary_table}=  Create List
    ...  ${total_tls_encrypted}  ${unencrypted}  ${total_successful}

    # verify summary tables
    FOR  ${table_name}  ${column}  ${expected_table}  IN
    ...  ${connection_type} TLS Connections Summary  Connections
    ...  ${expected_summary_table}
    ...  ${connection_type} TLS Messages Summary  Messages
    ...  ${expected_messages_summary_table}
      ${table_params}=  Email Report Table Create Parameters
      ...  ${table_name}  period=${period}
      ${table}=  Wait Until Keyword Succeeds
      ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
      ...  Email Report Table Get Data  ${table_name}
           ...  table_parameters=${table_params}
      Lists Should Be Equal
      ...  ${table['${column}']}  ${expected_table}
    END
    # verify details table
    ${details_table_name}=  Set Variable
    ...  ${connection_type} TLS Connections Details
    ${details_table_params}=  Email Report Table Create Parameters
    ...  ${details_table_name}  period=${period}
    ${details_table}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  ${details_table_name}
         ...  table_parameters=${details_table_params}
    FOR  ${column}  ${value}  IN
    ...  TLS Req. Success         ${successful_required}
    ...  TLS Req. Failed          ${failed_required}
    ...  TLS Pref. Success        ${successful_preferred}
    ...  TLS Pref. Failed         ${failed_preferred}
    ...  Total TLS Connections    ${total_tls}
    ...  Unencrypted Connections  ${unencrypted}
    ...  Messages by TLS          ${total_tls_encrypted}
      Should Be Equal As Strings  ${details_table['${column}'][0]}  ${value}
    END
    Run Keyword If  '${domain}' != '${None}'
    ...  Should Be Equal As Strings  ${details_table['Domain'][0]}  ${domain}
    Run Keyword If  '${last_tls_status}' != '${None}'
    ...  Should Be Equal As Strings
         ...  ${details_table['Last TLS Status'][0]}  ${last_tls_status}

    # verify chart
    ${chart_name}=  Set Variable  ${connection_type} TLS Connections Graph
    Email Reporting Check Chart Presence  ${chart_name}

Generate Incomming TLS Reporting On ESA
    [Arguments]  ${connections_per_category}
    FOR  ${change_policy}  ${setting}  ${tls}  IN
    ...  ${True}   Off        ${False}
    ...  ${True}   Required   ${True}
    ...  ${False}  Required   ${False}
    ...  ${True}   Preferred  ${True}
    ...  ${False}  Preferred  ${False}
      Run Keyword If  ${change_policy}
      ...  Run Keywords
           ...  Set Mail Flow Policies To TLS ${setting}
           ...  Commit Changes
      Inject ${connections_per_category} Clean Messages To Public Listener With TLS Option ${tls}
    END
    ${command}=  Catenate  openssl s_client -no_tls1 -ssl3 -starttls smtp
    ...  -host ${PUBLIC_LISTENER.ipv4} -port 25
    Operating System.Run  ${command}

Generate Outgoing TLS Reporting On ESA
    [Arguments]  ${connections_per_category}
    Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT_HOSTNAME}
    Commit
    Deleterecipients All
    FOR  ${change_policy}  ${setting}  ${tls}  ${tls_fail}  IN
    ...  ${True}   Required   ${True}   ${False}
    ...  ${False}  Required   ${False}  ${True}
    ...  ${True}   Preferred  ${True}   ${False}
    ...  ${False}  Preferred  ${False}  ${False}
      Run Keyword If  ${change_policy}
      ...  Run Keywords
           ...  Set Destination Controls To TLS Support ${setting}
           ...  Commit Changes
      Null Smtpd Start  bind-ip=${CLIENT_IP}  tls=${tls}  tls-fail2=${tls_fail}
      Sleep  5s  Wait until drain will be started
      Inject ${connections_per_category} Clean Messages To Private Listener With TLS Option ${False}
      Deliver Now All
      Sleep  5s  Wait until messages will be delivered
      Run Keyword And Ignore Error  Null Smtpd Stop
      Deleterecipients All
    END
    Smtp Routes Delete  .${NETWORK}
    Commit Changes

Generate Overview Reporting For Specified Time Ranges
    [Arguments]  @{time_ranges}
    ${current_time}=  Set Time
    FOR  ${period}  IN  @{time_ranges}
      Shift ESA Datetime By Days  ${period}  cur_time=${current_time}
      Generate Generic Email Reporting Data
    END
    Sync Appliances Datetime  ${SMA}  ${ESA}

Save And Reload Config
    ${saved_conf}=  Save Config
    Suspend
    Reset Config  yes
    Load Config From File  ${saved_conf}
    Commit
    [Return]  ${saved_conf}

Shedule Domain Based Reporting
    [Arguments]  ${outgoing_domain}=server
    Email Scheduled Reports Add Domain Based Report
    ...  title=${DOMAIN_BASED_REPORT_TITLE}
    ...  report_generation=individual
    ...  domains=${CLIENT_HOSTNAME}
    ...  email_to=${REPORT_RECIPIENT}
    ...  outgoing_domain=${outgoing_domain}

SMA Should Contain System Capacity Report
    Navigate To  Email  Reporting  System Capacity
    Page Should Contain Element  xpath=//table[@class='chart_container']//img

Verify System Capacity Report On SMA For ${appliance}
    Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain System Capacity Report
    Select From List
    ...  xpath=//select[@id='host_id']  ${appliance}
    # do not reload page if '${appliance}' option is already selected
    Run Keyword And Ignore Error  Wait Until Page Loaded
    FOR  ${chart_name}  IN
    ...  Average Time Spent in Work Queue
    ...  Average Messages in Work Queue
    ...  Maximum Messages in Work Queue
      Email Reporting Check Chart Presence  ${chart_name}
    END

${enable_disable} Consolidated Reporting On SMA
    Switch To SMA
    SSHLibrary.Open Connection  ${SMA_IP}  prompt=>  timeout=30
    SSHLibrary.Login  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    SSHLibrary.Write  reportingconfig
    SSHLibrary.Read Until Prompt
    SSHLibrary.Write  complete_consolidated_reports
    SSHLibrary.Read Until Prompt

    @{enable_commands_list}=  Create List  Y
    @{disable_commands_list}=  Create List  N  Y
    FOR  ${command}  IN  @{${enable_disable.lower()}_commands_list}
      SSHLibrary.Write  ${command}
      SSHLibrary.Read Until Prompt
    END
    SSHLibrary.Write  \n
    SSHLibrary.Close Connection

Verify Mail Summary Reporting On SMA
    [Arguments]  ${connection_type}=Incoming  ${column_index_to_check}=0
    ...  ${expected_column_value}=0  ${view_data_for}=All Email Appliances
    ${table_name}=  Set Variable  ${connection_type} Mail Summary
    ${table_params}=  Email Report Table Create Parameters  ${table_name}
    ...  view_data_for=${view_data_for}
    ${table_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  ${table_name}
         ...  table_parameters=${table_params}
    Log  ${table_data}
    ${actual_column_value}=  Set Variable
    ...  ${table_data['Messages'][${column_index_to_check}]}
    Should Be Equal As Integers
    ...  ${expected_column_value}  ${actual_column_value}
    # verify chart
    ${chart_name}=  Set Variable  ${connection_type} Mail Graph
    Email Reporting Check Chart Presence  ${chart_name}

SMA Table Column Value Should Be Equal
    [Arguments]  ${table}  ${column}  ${expected_data}
    ${table_params}=  Email Report Table Create Parameters  ${table}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  ${RETRY_TIME}
    ...  Email Report Table Get Data  ${table}  ${table_params}
    Should Be Equal As Integers  ${reporting_data['${column}'][0]}  ${expected_data}

Verify Headers In Message
    [Arguments]  @{varargs}
    [Documentation]  Accepts multiple named arguments.\n
    ...  Argument is header name to get value from.\n
    ...  Value is expected header's value.
    ...  This keyword gets drained message, gets headers and compares values.
    Message Unload
    ${msg}=  Null Smtpd Next Message  timeout=60
    Message Load  ${msg}
    ${headers}=  Message Items
    Log Dictionary  ${headers}
    FOR  ${arg}  IN  @{varargs}
      ${k}  ${v}=  Split String  ${arg}  =  1
      ${header_value}=  Message Get  ${k}
      Should Be Equal As Strings  ${header_value}  ${v}
    END

Append Payload To File
    [Arguments]  ${file}
    ${payload}=  Message Get Payload  decode=${True}
    Log  ${payload}
    OperatingSystem.Append To File  ${file}  ${payload}

Initialize TLS Reporting Test
    Switch To ESA
    Roll Over Now  logname=mail_logs
    Ssl Config Inbound  method=TLS v1  cipher=${DEFAULT_SSL_CIPHER}
    Commit

Finalize TLS Reporting Test
    Run Keyword And Ignore Error  Null Smtpd Stop
    Switch To ESA
    Ssl Config Inbound
    ...  method=${DEFAULT_SSL_METHOD}
    ...  cipher=${DEFAULT_SSL_CIPHER}
    Commit
    Run Keyword And Ignore Error  Smtp Routes Delete  .${NETWORK}
    Set Destination Controls To TLS Support None
    Set Mail Flow Policies To TLS Off
    Commit Changes

Process Mail And Extract Attachment Into ${dest_dir}
    @{params}=  Create List
    ...  From  "Cisco Reporting" <reporting@${SMA}>
    ${msg}=  Verify And Wait For Mail In Drain  reporting@${SMA}  @{params}
    Log  ${msg}
    Message Load  ${msg}
    ${generator}=  Message Walk
    Message Unload
    @{parts}=  Convert To List  ${generator}
    Message Load  @{parts}[-1]
    ${payload}=  Message Get Payload  ${None}  ${True}
    Log  ${payload}
    ${attachment_file_name}=  Message Get Filename
    # some file names contains '\n\t' symbols
    ${file_name}=  Run Keyword If  """${attachment_file_name}""" != '${None}'
    ...  Replace String  ${attachment_file_name}  \n\t  ${SPACE}
    ${file_name}=  Replace String  ${file_name}  ${SPACE}  _
    ${file_path}=  Join Path  ${dest_dir}  ${file_name}
    ${path}  ${ext}=  Split Extension  ${file_path}
    Run Keyword If  '${ext}' == 'csv'
    ...  OperatingSystem.Create File  ${file_path}  ${payload}
    Message Unload

Process Archived Mails And Extract CSV Reports Into ${dest_dir}
    # read 4 mails with CSV reports delivered to drain from SMA
    FOR  ${index}  IN RANGE  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
      Process Mail And Extract Attachment Into ${dest_dir}
    END

Find And Verify CSV Report
    [Arguments]  ${dir}  ${file_pattern}  @{key_value_pairs}
    ${file_names}=  OperatingSystem.List Files In Directory
    ...  ${dir}  ${file_pattern}
    Log  ${file_names}
    ${csv_report_file_path}=  OperatingSystem.Join Path
    ...  ${dir}  ${file_names[0]}
    ${csv_data}=  Csv Parser Get Data  ${csv_report_file_path}
    Log  ${csv_data}
    FOR  ${key}  ${value}  IN  @{key_value_pairs}
      List Should Contain Value  ${csv_data['${key}']}  ${value}
    END

Verify Executive Summary CSV Reporting
    [Arguments]  ${messages}=0  ${summary_messages}=0
    FOR  ${connection_type}  IN  Incoming  Outgoing
      Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${connection_type}*Graph*
      ...  Clean Messages  ${messages}
    END
    @{summary_clean_messages}=  Create List
    ...  Clean Messages  ${summary_messages}
    Find And Verify CSV Report  ${SUITE_TMP_DIR}  *Incoming*Summary*
    ...  @{summary_clean_messages}
    ...  Total Attempted Messages  ${summary_messages}
    Find And Verify CSV Report  ${SUITE_TMP_DIR}  *Outgoing*Summary*
    ...  @{summary_clean_messages}
    ...  Total Messages Processed  ${summary_messages}

Generate Domain Based Reporting
    [Documentation]  Generates Incoming and Outgoing Domain-Based Report Data
    [Arguments]  ${messages_count}  ${ip}=${CLIENT_IP}
    ${file_name}=  Prepare TXT File With Domain IP  ${ip}
    FOR  ${listener}  IN  PUBLIC_LISTENER  PRIVATE_LISTENER
      Smtp Session Spoof Enable  ${${listener}.name}  ${file_name}
      Generate Email Reporting Data
      ...  rcpt-host-list=${CLIENT_HOSTNAME}
      ...  inject-host=${${listener}.ipv4}
      ...  ${CLEAN}=${messages_count}
      Smtp Session Spoof Disable
    END

Generate Domain Reporting For Different Periods
    [Arguments]  ${ip_addr}=  ${msg_count}=1
    ${current_time} =  Set Time
    @{time_periods}=  Create List  1  7  20  360
    FOR  ${period}  IN  @{time_periods}
      ${datetime_to_set}=  Calculate Shifted Datetime  ${period}  cur_time=${current_time}
      Set Time  ${datetime_to_set}
      Generate Domain Based Reporting  ${msg_count}  ${ip_addr}
    END
    Sync Appliances Datetime  ${SMA}  ${ESA}

Wait Until Reporting Data Gets SMA
    Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Incoming Mail Summary

Verify Table Column Value
    [Documentation]  Verifies that particular column value\n
    ...  from given table is equal to ${expected_val}
    [Arguments]  ${table_name}  ${col_name}  ${expected_val}
    ...  ${table_params}=${None}  ${should_navigate_to_table}=${True}
    ${table_data} =  Email Report Table Get Data  ${table_name}
    ...  table_parameters=${table_params}
    ...  should_navigate_to_table=${should_navigate_to_table}
    ${col_values} =  Get From Dictionary  ${table_data}  ${col_name}
    ${value} =  Get From List  ${col_values}  0
    Should Be Equal As Integers  ${value}  ${expected_val}

Verify Tracking Data
    [Documentation]  Verifies that message tracking contains data\n
    [Arguments]  ${sender_name}  ${count}
    ${result_list} =  Email Message Tracking Search
    ...  sender_data=${sender_name}
    ${result_count} =  Email Message Tracking Get Total Result Count
    ...  ${result_list}
    Should Be True  ${result_count} == ${count}

Initialize Tvh663967c
    ${connections_per_category}=  Set Variable  1
    Generate Incomming TLS Reporting On ESA  ${connections_per_category}
    Generate Outgoing TLS Reporting On ESA  ${connections_per_category}

Initialize Tvh663287c
    ${connections_per_category}=  Set Variable  1
    ${current_time}=  Set Time
    @{time_ranges}=  Create List  365  90  30  7  1
    FOR  ${period}  IN  @{time_ranges}
      Shift ESA Datetime By Days  ${period}  cur_time=${current_time}
      Generate Incomming TLS Reporting On ESA  ${connections_per_category}
      Generate Outgoing TLS Reporting On ESA  ${connections_per_category}
    END
    Sync Appliances Datetime  ${SMA}  ${ESA}

Initialize Tvh663323c
    Switch To ESA
    Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT_HOSTNAME}
    Commit
    Set Destination Controls To TLS Support Required
    Commit Changes
    Null Smtpd Start  bind-ip=${CLIENT_IP}  tls=${True}
    Set Test Variable  ${CONNECTIONS}  1
    Inject ${CONNECTIONS} Clean Messages To Private Listener With TLS Option ${True}

Initialize Tvh664051c
    Switch To SMA
    Centralized Email Reporting Group Add  ${REPORTING_GROUP_NAME}  ${ESA}
    Commit Changes
    @{time_ranges}=  Create List  30  7  1
    Generate Overview Reporting For Specified Time Ranges  @{time_ranges}

Finalize Tvh664051c
    Switch To SMA
    Centralized Email Reporting Group Delete  ${REPORTING_GROUP_NAME}
    Commit Changes

Initialize Tvh663051c
    Switch To ESA
    ${messages_count}=  Set Variable  1
    Generate Domain Based Reporting  ${messages_count}

Finalize Tvh663051c
    Switch To ESA
    Run Keyword And Ignore Error  Smtp Session Spoof Disable
    Switch To SMA
    Email Scheduled Reports Delete Report  ${DOMAIN_BASED_REPORT_TITLE}
    Commit Changes

Initialize Tvh663008c
    Set Test Variable  ${MESSAGES}  1
    Switch To ESA
    ${current_time}=  Set Time
    @{time_ranges}=  Create List  365  90  30  7  1
    FOR  ${period}  IN  @{time_ranges}
      Shift ESA Datetime By Days  ${period}  cur_time=${current_time}
      Generate Domain Based Reporting  ${MESSAGES}
    END
    Sync Appliances Datetime  ${SMA}  ${ESA}

Finalize Tvh663008c
    Switch To ESA
    Run Keyword And Ignore Error  Smtp Session Spoof Disable

Initialize Tvh663908c
    Switch To ESA
    ${messages_count}=  Set Variable  1
    Generate Domain Based Reporting  ${messages_count}
    Switch To SMA
    Shedule Domain Based Reporting  outgoing_domain=server
    Commit Changes
    ${sma_conf}=  Save And Reload Config
    Set Test Variable  ${SMA_CONF}  ${sma_conf}

Finalize Domain Based Reporting Test With Reseting Config
    Switch To SMA
    Run Keyword If Test Failed  Load Config From File  ${SMA_CONF}
    Run Keyword If Test Failed  Commit
    Email Scheduled Reports Delete Report  ${DOMAIN_BASED_REPORT_TITLE}
    Commit Changes

Initialize Tvh662939c
    Switch To ESA
    ${messages_count}=  Set Variable  1
    Generate Domain Based Reporting  ${messages_count}
    Switch To SMA
    Shedule Domain Based Reporting  outgoing_domain=email_address
    Commit Changes
    ${sma_conf}=  Save And Reload Config
    Set Test Variable  ${SMA_CONF}  ${sma_conf}

Initialize Tvh663320c
    Switch To ESA
    Roll Over Now  mail_logs
    Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT_HOSTNAME}
    Commit
    Switch To SMA
    Roll Over Now  logname=mail_logs
    Inject Messages
    ...  mbox-filename=${VOF_ALL}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}

Finalize Tvh663320c
    Switch To ESA
    Smtp Routes Clear
    Commit
    Switch To SMA

Initialize Tvh664203c
    Switch To ESA
    Roll Over Now  mail_logs
    Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT_HOSTNAME}
    Commit
    Switch To SMA

Finalize Tvh664203c
    Email Scheduled Reports Delete Report  ${TEST_NAME}
    Commit Changes
    Sync Time
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Switch To ESA
    Smtp Routes Clear
    Commit

Initialize Tvh663486c
    Switch To SMA
    Security Appliances Delete Email Appliance  ${ESA}
    Commit Changes

Finalize Tvh663486c
    Switch To SMA
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes

Initialize Tvh664304c
    Inject Messages
    ...  mbox-filename=${VOF_ALL}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}

Initialize Email Reporting Group Test
    Switch To SMA
    Centralized Email Reporting Group Add  ${REPORTING_GROUP_NAME}  ${ESA}
    Commit Changes
    Set Test Variable  ${MESSAGES_COUNT}  1
    FOR  ${listener_ip}  IN
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${ESA_PRIVATE_LISTENER_IP}
      Inject Messages
      ...  num-msgs=${MESSAGES_COUNT}
      ...  inject-host=${listener_ip}
      ...  rcpt-host-list=${CLIENT}
    END

Finalize Email Reporting Group Test
    Switch To SMA
    Centralized Email Reporting Group Delete  ${REPORTING_GROUP_NAME}
    Commit Changes

Initialize Tvh664200c
    Inject Messages
    ...  mbox-filename=${VOF_ALL}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}

Initialize Tvh663970c
    Switch To ESA
    Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT}
    Commit

    ${msgs_count}=  Set Variable  1
    Null Smtpd Start  bind-ip=${CLIENT_IP}
    Inject Messages
    ...  num-msgs=${msgs_count}
    ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}

    Switch To SMA
    ${table_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Outgoing Destinations Detail
    Log  ${table_data}
    Should Be Equal As Integers
    ...  ${table_data['Total Processed'][0]}  ${msgs_count}

Finalize Tvh663970c
    Run Keyword And Ignore Error  Null Smtpd Stop

    Switch To ESA
    Smtp Routes Clear
    Commit

Initialize Tvh662988c
    General Test Case Setup
    Set Test Variable  ${REPORT_VALUE}  Content Filters
    Email Scheduled Reports Add Report  ${REPORT_VALUE}  title=${TEST_NAME}  language=deutsch
    Commit Changes
    ${CONFIG_FILE}=  Save And Reload Config
    Set Test Variable  ${CONFIG_FILE}

Finalize Tvh662988c
    Email Scheduled Reports Delete Report  ${TEST_NAME}
    Commit Changes
    General Test Case Teardown

Initialize Tvh663067c
    Set Test Variable  ${DLP_POLICY_NAME}  All-Compressed
    General Test Case Setup
    Switch To ESA
    Roll Over Now  mail_logs

    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable
    DLP Policy New  Custom Policy  Custom Policy
    ...  change_policy_name=${DLP_POLICY_NAME}  submit=${False}
    @{all_compressed}=  Create List  All Compressed
    ${attachment_category}=  Create Dictionary  Compressed  ${all_compressed}
    DLP Policy Configure Filter Attachments  attachment_category=${attachment_category}
    ...  apply_if=Is  submit=${True}
    DLP Message Action Edit  Default Action  msg_action=Drop
    ${policy_settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  ${DLP_POLICY_NAME}  ${True}
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    Commit Changes

Finalize Tvh663067c
    Switch To ESA
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes
    General Test Case Teardown

Initialize Tvh663406c
    General Test Case Setup
    Inject Messages
    ...  num-msgs=5
    ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}

    Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  ${RETRY_TIME}
    ...  Email Report Table Get Data  User Mail Flow Details

    FOR  ${time_range}  IN  last day  last week  last month
    ...                      last year  num days:10  num months:3
      Email Archived Reports Add Report
      ...  ${sma_email_reports.INT_USERS}
      ...  time_range=${time_range}
    END

Finalize Tvh663406c
    Email Archived Reports Delete All Reports
    General Test Case Teardown

Initialize Tvh663380c
    Set Test Variable  ${EXECUTIVE_SUMMARY_REPORT_TITLE}  executive_summary_report
    Set Test Variable  ${MESSAGES_COUNT}  1

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    @{time_periods}=  Create List  300  20  7  1
    FOR  ${period}  IN  @{time_periods}
      ${datetime_to_set}=  Calculate Shifted Datetime
      ...  ${period}  cur_time=${first_day_of_curr_month}
      EsaCliLibrary.Set Time  ${datetime_to_set}
      Inject ${MESSAGES_COUNT} Clean Messages To Public Listener With TLS Option ${False}
      Inject ${MESSAGES_COUNT} Clean Messages To Private Listener With TLS Option ${False}
    END
    Sync Appliances Datetime  ${SMA}  ${ESA}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit
    Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Incoming Mail Summary

Finalize Tvh663380c
    Switch To ESA
    Sync Time
    OperatingSystem.Empty Directory  ${SUITE_TMP_DIR}
    Run Keyword And Ignore Error  Null Smtpd Stop

    Switch To SMA
    Sync Time
    Smtp Routes Clear
    Commit
    Run Keyword If Test Failed
    ...  Email Archived Reports Delete Report  ${EXECUTIVE_SUMMARY_REPORT_TITLE}
    Run Keyword If Test Failed  Commit Changes

Initialize Tvh663031c
    ${CLIENT_MNGMT_IP}=  Get Host IP By Name  ${CLIENT}
    Set Test Variable  ${CLIENT_MNGMT_IP}
    Set Test Variable  ${RECIPIENT}  ${TEST_NAME}@${CLIENT}
    Set Test Variable  ${MESSAGES_COUNT}  1

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Switch To ESA
    Generate Domain Reporting For Different Periods  ${CLIENT_MNGMT_IP}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit
    Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Incoming Mail Summary

Initialize Tvh663798c
    Set Test Variable  ${REPORT_RCPT}  user@${CLIENT}
    Set Test Variable  ${MESSAGES_COUNT}  1
    Null Smtpd Start  bind-ip=${CLIENT_IP}
    Switch To ESA
    Roll Over Now  mail_logs
    Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT_HOSTNAME}
    Commit
    Shift ESA Datetime  sec_offset=-3600*24
    Generate Domain Based Reporting  ${MESSAGES_COUNT}
    Switch To SMA
    Sync Appliances Datetime  ${SMA}  ${ESA}

Finalize Tvh663798c
    Switch To ESA
    Smtp Routes Clear
    Commit
    Null Smtpd Stop

Verify CSV Data
    [Arguments]  ${query}  ${control_header}  @{expected_results}
    # First check header value to ensure we got expected message
    Wait Until Keyword Succeeds
    ...  3 min
    ...  30 sec
    ...  Verify Headers In Message
         ...  ${control_header}
    ${rnd}=  String.Generate Random String
    ${payload_file}=  Join Path  ${SUITE_TMP_DIR}  ${rnd}.txt
    OperatingSystem.Create File  ${payload_file}
    ${headers}=  Message Items
    Log Dictionary  ${headers}

    ${is_multipart}=  Message Is Multipart
    Log  ${is_multipart}
    Should Be True  ${is_multipart}

    # Message Load  ${msg}
    ${generator}=  Message Walk
    @{parts}=  Convert To List  ${generator}
    Message Unload
    # walk through message parts to get csv attachment
    # and write to file when found
    FOR  ${part}  IN  @{parts}
      Message Load  ${part}
      ${ct}=  Message Get Content Type
      Log  ${ct}
      Run Keyword If  '${ct}' == 'application/csv'  Append Payload To File  ${payload_file}
      Message Unload
    END
    ${data_dict}=  CSV Parser Get Data  ${payload_file}
    Log Dictionary  ${data_dict}
    @{result}=  CSV Parser Query  ${payload_file}  ${query}
    Log List  ${result}
    FOR  ${expected_res}  IN  @{expected_results}
      List Should Contain Value  ${result}  ${expected_res}
    END

Verify Message Data
    [Arguments]  ${control_header}  ${expected_data}
    Wait Until Keyword Succeeds
    ...  3 min
    ...  30 sec
    ...  Verify Headers In Message
         ...  ${control_header}
    ${headers}=  Message Items
    Log Dictionary  ${headers}
    ${is_multipart}=  Message Is Multipart
    Log  ${is_multipart}
    Should Be True  ${is_multipart}
    ${generator}=  Message Walk
    @{parts}=  Convert To List  ${generator}
    Message Unload
    # 8|16 is re.M|re.DOTALL, seems much easier than
    # ${re}=  Evaluate  re  modules=re
    # then Call Method to compile pattern etc.
    FOR  ${part}  IN  @{parts}
      Message Load  ${part}
      ${ct}=  Message Get Content Type
      Message Unload
      Log  ${ct}
      ${mo}=  Evaluate  re.search('${expected_data}', """${part}""", 8|16)  modules=re
      Run Keyword If  '${ct}' == 'application/csv'  Should Be True  ${mo}
      Run Keyword If  '${ct}' == 'application/csv'  Exit For Loop
    END

Create MBOX With Attachments
    [Arguments]  ${mbox_path}  ${subject}  ${text}  @{files_to_attach}
    ${msg}=  Message Builder Create MIMEMultipart
    Message Builder Add Headers  ${msg}
    ...  From=me@${CLIENT}
    ...  To=you@${CLIENT}
    ...  Subject=${subject}
    ${textobj}=  Message Builder Create MIMEText  ${text}
    Message Load   ${msg}
    Message Attach  ${textobj}
    Message Unload

    FOR  ${file_path}  IN  @{files_to_attach}
      ${mime_type}  ${mime_subtype}  Evaluate
      ...  tuple(mimetypes.guess_type('${file_path}')[0].split('/'))  mimetypes
      ${content}=  Get Binary File  ${file_path}
      ${charset_param}=  Run Keyword If  '${mime_type}' == 'text'
      ...  Get Attachment Charset  ${content}
      ${empty_dict}=  Create Dictionary
      ${charset_param}=  Set Variable If  """${charset_param}""" == 'None'
      ...  ${empty_dict}  ${charset_param}
      ${part}=  Message Builder Create MIMEBase  ${mime_type}  ${mime_subtype}  ${charset_param}
      Message Load   ${part}
      Message Set Payload  ${content}
      Message Unload
      Message Builder Encode Base64   ${part}
      ${filename}=  Evaluate  os.path.basename("""${file_path}""")  os
      Message Builder Add Headers  ${part}
      ...  Content-Disposition=attachment; filename="${filename}"
      Message Load   ${msg}
      Message Attach  ${part}
      Message Unload
    END
    Create MBOX Containing Message  ${mbox_path}  ${msg}

Initialize Tvh662979c
   General Test Case Setup
   Switch To SMA
   Security Appliances Add Email Appliance
    ...  ${ESA2}
    ...  ${ESA2_IP}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Centralized Email Reporting Group Add  ${TEST_NAME}  ${ESA2}
    Commit Changes
    Generate Incoming Email Reporting Data

Finalize Tvh662979c
   Switch To SMA
   Centralized Email Reporting Group Delete  ${TEST_NAME}
   Security Appliances Delete Email Appliance  ${ESA2}
   Commit Changes
   General Test Case Teardown

Initialize Tvh663308c
    Set Test Variable  ${CLEAN_MSGS_COUNT}  1
    Set Test Variable  ${SPAM_MSGS_COUNT}  1
    ${mboxes_dict}=  Create Dictionary
    ...  ${CLEAN}  ${CLEAN_MSGS_COUNT}
    ...  ${SPAM}  ${SPAM_MSGS_COUNT}
    Generate Incoming Email Reporting Data
    ...  incoming_dictionary=${mboxes_dict}

Initialize Tvh662881c
    ${current_time}=  EsaCliLibrary.Set Time
    Set Test Variable  ${MESSAGES_COUNT}  1
    ${mboxes_dict}=  Create Dictionary
    ...  ${CLEAN}  ${MESSAGES_COUNT}
    ...  ${SPAM}  ${MESSAGES_COUNT}
    FOR  ${period}  IN  300  80  20  7  1
      ${datetime_to_set}=  Calculate Shifted Datetime
      ...  ${period}  cur_time=${current_time}
      EsaCliLibrary.Set Time  ${datetime_to_set}
      Generate Incoming Email Reporting Data
      ...  incoming_dictionary=${mboxes_dict}
    END
    Sync Appliances Datetime  ${SMA}  ${ESA}

Initialize Outgoing Destinations Reporting Test Case
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Spam Scanning  Use IronPort Anti-Spam service
    Mail Policies Edit Antispam  outgoing  default  ${settings}
    ${settings}=    Mail Flow Policies Create Settings
    ...  Spam Detection  On
    Mail Flow Policies Edit  ${PRIVATE_LISTENER.name}  RELAYED  ${settings}
    Commit Changes

Finalize Outgoing Destinations Reporting Test Case
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Switch To ESA
    ${settings}=    Mail Flow Policies Create Settings
    ...  Spam Detection  Off
    Mail Flow Policies Edit  ${PRIVATE_LISTENER.name}  RELAYED  ${settings}
    Commit Changes
    Policyconfig Edit Antispam Disable  Outgoing  DEFAULT
    Commit

Initialize Tvh663284c
    Set Test Variable  ${CLEAN_MSGS_COUNT}  1
    Set Test Variable  ${SPAM_MSGS_COUNT}  1
    ${mboxes_dict}=  Create Dictionary
    ...  ${CLEAN}  ${CLEAN_MSGS_COUNT}
    ...  ${SPAM}  ${SPAM_MSGS_COUNT}
    Generate Outgoing Email Reporting Data
    ...  listener_ip=${ESA_PRIVATE_LISTENER_IP}
    ...  outgoing_dictionary=${mboxes_dict}

Initialize Tvh663895c
    Set Test Variable  ${CLEAN_MSGS_COUNT}  1
    Set Test Variable  ${SPAM_MSGS_COUNT}  1
    ${mboxes_dict}=  Create Dictionary
    ...  ${CLEAN}  ${CLEAN_MSGS_COUNT}
    ...  ${SPAM}  ${SPAM_MSGS_COUNT}
    ${current_time}=  EsaCliLibrary.Set Time
    FOR  ${period}  IN  300  80  20  7  1
      ${datetime_to_set}=  Calculate Shifted Datetime
      ...  ${period}  cur_time=${current_time}
      EsaCliLibrary.Set Time  ${datetime_to_set}
      Generate Outgoing Email Reporting Data
      ...  listener_ip=${ESA_PRIVATE_LISTENER_IP}
      ...  outgoing_dictionary=${mboxes_dict}
    END
    Sync Appliances Datetime  ${SMA}  ${ESA}

Verify Mail Reporting On SMA
    [Arguments]  ${table_name}=${None}  ${expected_columns}=${None}
    ...  ${left_chart}=${None}  ${right_chart}=${None}  ${time_period}=Day
    Switch To SMA
    ${table_params}=  Email Report Table Create Parameters
    ...  ${table_name}  period=${time_period}
    ${table_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  ${table_name}
         ...  table_parameters=${table_params}
    Log  ${table_data}
    # verify table
    @{columns}=  Convert To List  ${expected_columns}
    FOR  ${name}  ${value}  IN  @{columns}
      Should Be Equal As Strings  ${table_data['${name}'][0]}  ${value}
    END
    # verify charts
    FOR  ${chart_name}  IN  ${left_chart}  ${right_chart}
      Run Keyword If  '${chart_name}' != '${None}'
      ...  Email Reporting Check Chart Presence  ${chart_name}
    END

Apply Single Content Filter
    [Arguments]  ${name}  ${conditions}  ${actions}  ${dest_policy}
    Content Filter Add  ${dest_policy}  ${name}  ${name}
    ...  ${actions}  ${conditions}
    @{filters_to_enable}=  Create List  ${name}
    Mailpolicy Edit Contentfilters  ${dest_policy}  Default Policy  custom
    ...  enable_filter_names=@{filters_to_enable}
    Commit Changes

Initialize Tvh663115c
    Null Smtpd Start  bind-ip=${CLIENT_IP}
    Switch To ESA
    Roll Over Now  mail_logs
    Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT_HOSTNAME}
    Commit
    Switch To SMA

Finalize Tvh663115c
    Email Scheduled Reports Delete Report  ${TEST_NAME}
    Commit Changes
    Sync Time
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Switch To ESA
    Smtp Routes Clear
    Commit
    Null Smtpd Stop

Initialize Tvh663788c
    Null Smtpd Start  bind-ip=${CLIENT_IP}
    Switch To ESA
    Roll Over Now  mail_logs
    Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT_HOSTNAME}
    Commit
    Switch To SMA

Finalize Tvh663788c
    Email Scheduled Reports Delete Report  ${TEST_NAME}
    Commit Changes
    Sync Time
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Switch To ESA
    Smtp Routes Clear
    Commit
    Null Smtpd Stop

Initialize Tvh662949c
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  Yes
    ...  Use Sophos Anti-Virus  ${True}
    Mail Policies Edit Antivirus  outgoing  default  ${settings}
    Commit Changes

    Set Test Variable  ${PUB_LISTENER_MSGS}  1
    Set Test Variable  ${PR_LISTENER_MSGS}  1
    FOR  ${listener_ip}  ${msgs_cnt}  IN
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${PUB_LISTENER_MSGS}
    ...  ${ESA_PRIVATE_LISTENER_IP}  ${PR_LISTENER_MSGS}
      Inject Messages
      ...  mbox-filename=${EICAR_COM_ZIP}
      ...  num-msgs=${msgs_cnt}
      ...  inject-host=${listener_ip}
      ...  rcpt-host-list=${CLIENT}
      Deliver Now All
      Sleep  5s  Wait until messages will be delivered
    END

Finalize Tvh662949c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  outgoing  default  ${settings}
    Commit Changes

Initialize Tvh664215c
    Set Test Variable  ${VIRUS_MSGS_COUNT}  1
    Inject Messages
    ...  mbox-filename=${VOF_ALL}
    ...  num-msgs=${VIRUS_MSGS_COUNT}
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}

Verify Pdf Report User
    [Arguments]  ${msg}
    Sleep  10s
    ${start_time}=  Get Time
    Wait Until Keyword Succeeds  1m  10s
    ...  Click Element  xpath=//td[@id='report_toolbar']/a  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=600
    ...  download_directory=%{SARF_HOME}/tmp
    Set Test Variable  ${path}
    Log  ${path}
    ${out}=  Run  ${PDF2TXT_PATH}  ${path}
    Log  ${out}
    ${out}=  Replace String  ${out}  \\n  ${EMPTY}
    Should match regexp  ${out}  .*${msg}.*
    Log  ${out}
    Remove File  ${path}

Verify Pdf Report
    [Arguments]  ${msg}
    Sleep  10s
    ${start_time}=  Get Time
    Wait Until Keyword Succeeds  1m  10s
    ...  Click Element  xpath=//td[@id='report_toolbar']/a  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=600
    ...  download_directory=%{SARF_HOME}/tmp
    Set Test Variable  ${path}
    Log  ${path}
    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    Log  ${out}
    Should match regexp  ${out}  .*${msg}.*
    Remove File  ${path}

Do SMA System Capacity Verification
    Chart Average Time Spent in Work Queue Should Not Be Empty
    Chart Average Messages in Work Queue Should Not Be Empty
    Chart Maximum Messages in Work Queue Should Not Be Empty
    Chart Total Incoming Connections Should Not Be Empty
    Chart Total Incoming Messages Should Not Be Empty
    Chart Average Incoming Message Size (Bytes) Should Not Be Empty
    Chart Total Incoming Message Size (Bytes) Should Not Be Empty
    Chart Total Outgoing Connections Should Not Be Empty
    Chart Total Outgoing Messages Should Not Be Empty
    Chart Average Outgoing Message Size (Bytes) Should Not Be Empty
    Chart Total Outgoing Message Size (Bytes) Should Not Be Empty
    Chart Overall CPU Usage Should Not Be Empty
    Chart CPU by Function Should Not Be Empty
    Chart Memory Page Swapping Should Not Be Empty

    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

Initialize Tvh663133c
    Set Test Variable  ${CLEAN_MSGS_COUNT}  1
    Set Test Variable  ${SPAM_MSGS_COUNT}  1
    ${mboxes_dict}=  Create Dictionary
    ...  ${CLEAN}  ${CLEAN_MSGS_COUNT}
    ...  ${SPAM}  ${SPAM_MSGS_COUNT}
    Generate Outgoing Email Reporting Data
    ...  listener_ip=${ESA_PRIVATE_LISTENER_IP}
    ...  outgoing_dictionary=${mboxes_dict}

Initialize Tvh664204c
    Switch To ESA
    Set Test Variable  ${Tvh664204c_FILTER_NAME}  drop-by-filetype
    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is executables
    ${conditions}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Executables
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info   ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}
    Apply Single Content Filter  ${Tvh664204c_FILTER_NAME}  ${conditions}  ${actions}  Incoming

    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is executables
    ${conditions}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Executables
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info   ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}
    Apply Single Content Filter  ${Tvh664204c_FILTER_NAME}  ${conditions}  ${actions}  Outgoing

Finalize Tvh664204c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Switch To ESA
    @{filters_to_disable}=  Create List  ${${TEST_NAME}_FILTER_NAME}
    Mailpolicy Edit Contentfilters  incoming  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Incoming  ${${TEST_NAME}_FILTER_NAME}
    Commit Changes

    @{filters_to_disable}=  Create List  ${${TEST_NAME}_FILTER_NAME}
    Mailpolicy Edit Contentfilters  outgoing  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Outgoing  ${${TEST_NAME}_FILTER_NAME}
    Commit Changes

Initialize Tvh663810c
    Set Test Variable  ${DLP_POLICY_NAME}  All-Compressed
    Switch To ESA
    Roll Over Now  mail_logs

    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable
    DLP Policy New  Custom Policy  Custom Policy
    ...  change_policy_name=${DLP_POLICY_NAME}  submit=${False}
    @{all_compressed}=  Create List  All Compressed
    ${attachment_category}=  Create Dictionary  Compressed  ${all_compressed}
    DLP Policy Configure Filter Attachments  attachment_category=${attachment_category}
    ...  apply_if=Is  submit=${True}
    DLP Message Action Edit  Default Action  msg_action=Drop
    ${policy_settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  ${DLP_POLICY_NAME}  ${True}
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    Commit Changes

Finalize Tvh663810c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Switch To ESA
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes

Initialize Tvh664182c
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  Yes
    ...  Use Sophos Anti-Virus  ${True}
    Mail Policies Edit Antivirus  outgoing  default  ${settings}
    Commit Changes

    ${mboxes_dict}=  Create Dictionary
    ...  ${CLEAN}  1
    ...  ${SPAM}  1
    Generate Outgoing Email Reporting Data
    ...  listener_ip=${ESA_PRIVATE_LISTENER_IP}
    ...  outgoing_dictionary=${mboxes_dict}

Finalize Tvh664182c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  outgoing  default  ${settings}
    Commit Changes

Initialize Tvh663071c
    Set Test Variable  ${DLP_POLICY_NAME}  All-Compressed
    Switch To ESA
    Roll Over Now  mail_logs

    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable
    DLP Policy New  Custom Policy  Custom Policy
    ...  change_policy_name=${DLP_POLICY_NAME}  submit=${False}
    @{all_compressed}=  Create List  All Compressed
    ${attachment_category}=  Create Dictionary  Compressed  ${all_compressed}
    DLP Policy Configure Filter Attachments  attachment_category=${attachment_category}
    ...  apply_if=Is  submit=${True}
    DLP Message Action Edit  Default Action  msg_action=Drop
    ${policy_settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  ${DLP_POLICY_NAME}  ${True}
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    Commit Changes

Finalize Tvh663071c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Switch To ESA
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes

Initialize Tvh663921c
    Switch To ESA
    FOR  ${mbox}  IN  ${CLEAN}  ${SPAM}
      Inject Messages
      ...  mbox-filename=${mbox}
      ...  num-msgs=1
      ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    END

Finalize Tvh663921c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  outgoing  default  ${settings}
    Commit Changes

Initialize Tvh663215c
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  Yes
    ...  Use Sophos Anti-Virus  ${True}
    Mail Policies Edit Antivirus  outgoing  default  ${settings}
    Commit Changes

    FOR  ${mbox}  IN  ${CLEAN}  ${SPAM}
      Inject Messages
      ...  mbox-filename=${mbox}
      ...  num-msgs=1
      ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    END

Finalize Tvh663215c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Switch To ESA
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  outgoing  default  ${settings}
    Commit Changes

Initialize Tvh662978c
    Switch To SMA
    Centralized Email Reporting Group Add  ${REPORTING_GROUP}  ${ESA}
    Commit Changes

Finalize Tvh662978c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Switch To SMA
    Centralized Email Reporting Group Delete  ${REPORTING_GROUP}
    Commit Changes

Initialize Tvh663681c
    Switch To SMA
    Centralized Email Reporting Group Add  ${REPORTING_GROUP_NAME}  ${ESA}
    Commit Changes

Finalize Tvh663681c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Switch To SMA
    Centralized Email Reporting Group Delete  ${REPORTING_GROUP_NAME}
    Commit Changes

Initialize Tvh662868c
    Switch To SMA
    Initialize Email Reporting Group Test
    Disable Consolidated Reporting On SMA

Finalize Tvh662868c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Switch To SMA
    Finalize Email Reporting Group Test

Initialize Tvh663622c
    Initialize Email Reporting Group Test
    Enable Consolidated Reporting On SMA

Finalize Tvh663622c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Disable Consolidated Reporting On SMA
    Finalize Email Reporting Group Test

Do Tvh663629c Verification
    Chart Average Time Spent in Work Queue Should Not Be Empty
    Chart Average Messages in Work Queue Should Not Be Empty
    Chart Maximum Messages in Work Queue Should Not Be Empty
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

Initialize Tvh664007c
    Set Test Variable  ${DLP_POLICY_NAME}  All-Compressed
    Switch To ESA
    Roll Over Now  mail_logs
    Feature Key Set Key  rsadlp

    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable
    DLP Policy New  Custom Policy  Custom Policy
    ...  change_policy_name=${DLP_POLICY_NAME}  submit=${False}
    @{all_compressed}=  Create List  All Compressed
    ${attachment_category}=  Create Dictionary  Compressed  ${all_compressed}
    DLP Policy Configure Filter Attachments  attachment_category=${attachment_category}
    ...  apply_if=Is  submit=${True}
    DLP Message Action Edit  Default Action  msg_action=Drop
    ${policy_settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  ${DLP_POLICY_NAME}  ${True}
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    Commit Changes

Finalize Tvh664007c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes

Initialize Tvh664306c
    Set Test Variable  ${CLEAN_MSGS_COUNT}  2
    ${mboxes_dict}=  Create Dictionary
    ...  ${CLEAN}  ${CLEAN_MSGS_COUNT}
    Generate Outgoing Email Reporting Data
    ...  listener_ip=${ESA_PRIVATE_LISTENER_IP}
    ...  outgoing_dictionary=${mboxes_dict}

Initialize Tvh664192c
    Switch To ESA
    Set Test Variable  ${Tvh664192c_FILTER_NAME}  drop-by-filetype
    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is executables
    ${conditions}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Executables
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info   ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}
    Apply Single Content Filter  ${Tvh664192c_FILTER_NAME}  ${conditions}  ${actions}  Incoming

    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is executables
    ${conditions}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Executables
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info   ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}
    Apply Single Content Filter  ${Tvh664192c_FILTER_NAME}  ${conditions}  ${actions}  Outgoing

Finalize Tvh664192c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    @{filters_to_disable}=  Create List  ${${TEST_NAME}_FILTER_NAME}
    Mailpolicy Edit Contentfilters  incoming  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Incoming  ${${TEST_NAME}_FILTER_NAME}
    Commit Changes

    @{filters_to_disable}=  Create List  ${${TEST_NAME}_FILTER_NAME}
    Mailpolicy Edit Contentfilters  outgoing  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Outgoing  ${${TEST_NAME}_FILTER_NAME}
    Commit Changes

Initialize Tvh663077c
    Switch To ESA
    ${messages_count}=  Set Variable  1
    Generate Domain Based Reporting  ${messages_count}
    Switch To SMA
    Shedule Domain Based Reporting  outgoing_domain=email_address
    Commit Changes

Finalize Tvh663077c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Switch To SMA
    Email Scheduled Reports Delete Report  ${DOMAIN_BASED_REPORT_TITLE}
    Commit Changes

Initialize Tvh663514c
    Switch To ESA
    ${messages_count}=  Set Variable  1
    Generate Domain Based Reporting  ${messages_count}
    Commit Changes

Initialize Tvh663509c
    Set Test Variable  ${DLP_POLICY_NAME}  All-Compressed
    General Test Case Setup
    Switch To ESA
    Roll Over Now  mail_logs

    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable
    DLP Policy New  Custom Policy  Custom Policy
    ...  change_policy_name=${DLP_POLICY_NAME}  submit=${False}
    @{all_compressed}=  Create List  All Compressed
    ${attachment_category}=  Create Dictionary  Compressed  ${all_compressed}
    DLP Policy Configure Filter Attachments  attachment_category=${attachment_category}
    ...  apply_if=Is  submit=${True}
    DLP Message Action Edit  Default Action  msg_action=Drop
    ${policy_settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  ${DLP_POLICY_NAME}  ${True}
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    Commit Changes

Finalize Tvh663509c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Switch To ESA
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes
    General Test Case Teardown

Initialize Tvh663986c
    Switch To ESA
    Set Test Variable  ${Tvh663986c_FILTER_NAME}  drop-by-filetype
    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is executables
    ${conditions}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Executables
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info   ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}
    Apply Single Content Filter  ${Tvh663986c_FILTER_NAME}  ${conditions}  ${actions}  Incoming

    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is executables
    ${conditions}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Executables
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info   ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}
    Apply Single Content Filter  ${Tvh663986c_FILTER_NAME}  ${conditions}  ${actions}  Outgoing

Finalize Tvh663986c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Switch To ESA
    @{filters_to_disable}=  Create List  ${${TEST_NAME}_FILTER_NAME}
    Mailpolicy Edit Contentfilters  incoming  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Incoming  ${${TEST_NAME}_FILTER_NAME}
    Commit Changes

    @{filters_to_disable}=  Create List  ${${TEST_NAME}_FILTER_NAME}
    Mailpolicy Edit Contentfilters  outgoing  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Outgoing  ${${TEST_NAME}_FILTER_NAME}
    Commit Changes

Finalize Tvh663146c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Run Keyword And Ignore Error  Null Smtpd Stop
    Switch To ESA
    Run Keyword And Ignore Error  Smtp Routes Delete  .${NETWORK}
    Set Destination Controls To TLS Support None
    Set Mail Flow Policies To TLS Off
    Commit Changes

Initialize Tvh663149c
    Initialize Outgoing Destinations Reporting Test Case
    Initialize Tvh664182c

Finalize Tvh663149c
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

    Finalize Tvh664182c
    Finalize Outgoing Destinations Reporting Test Case

Verify Export Data For Charts
    @{files_skipped}=  Create List
    ...  Maximum_Messages
    ...  Outgoing_Connections
    ...  Outgoing_Messages
    ...  Outgoing_Message_Size
    ...  Outgoing_Message_Size_Bytes
    ...  Overall_CPU_Usage
    ...  CPU_by_Function

    FOR  ${chart_id}  IN  @{chart_ids}
        ${start_time}=  Get Time
        Sleep  5s
        Click Element  xpath=//td[@id='${chart_id}']/span  don't wait
        ${path}=  Wait Until Keyword Succeeds  10m  10s
        ...  Wait For Download  .csv  start_time=${start_time}  timeout=180
             ...  download_directory=%{SARF_HOME}/tmp
        Set Test Variable  ${path}
        Log  ${path}
        ${file_pattern}=  Get From List  ${pattern}  ${num}
        Log  ${file_pattern}
        ${index}=  Get Index From List  ${files_skipped}  ${file_pattern}
        Log  ${index}
        Run Keyword If  '${index}'=='-1'
        ...  Find And Verify CSV Report  %{SARF_HOME}/tmp  *${file_pattern}*
             ...  @{expected_value${num}}
        Remove File  ${path}
        ${num}=  Evaluate  ${num} + 1
    END

Verify Export Data For Table ${table_name}
    ${path}=   Reports Export  page=Email, Reporting, ${type}
    ...  name=${table_name}   password=${DUT_ADMIN_SSW_PASSWORD}
    OperatingSystem.File Should Exist  ${path}
    ${dir}  ${filename}=  Split Path  ${path}
    Find And Verify CSV Report  ${dir}  ${file_name}  @{expected_value}
    Remove File  ${path}

Enable Antispam on Incoming Policy
    ${spam_dict}=  Spam Params Get  use_ipas=YES
    ...  action_spam=IRONPORT QUARANTINE
    ${suspected_spam_dict}=  Suspected Spam Params Get
    ...  action_spam_suspected=IRONPORT QUARANTINE

    Policyconfig Edit Antispam Edit  Incoming
    ...  DEFAULT
    ...  ${spam_dict}
    ...  ${suspected_spam_dict}
    Commit

Enable Antispam On Outgoing Policy
    ${spam_dict}=  Spam Params Get  use_ipas=YES
    ...  action_spam=IRONPORT QUARANTINE
    ${suspected_spam_dict}=  Suspected Spam Params Get
    ...  action_spam_suspected=IRONPORT QUARANTINE

    Policyconfig Edit Antispam Enable  Outgoing
    ...  DEFAULT
    ...  ${spam_dict}
    ...  ${suspected_spam_dict}
    Commit

Enable Antivirus on Mail Policy
    [Arguments]  ${policy_name}

    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  Yes
    ...  Use Sophos Anti-Virus  ${True}

    Mail Policies Edit Antivirus  ${policy_name}  default  ${settings}
    Commit Changes

SMA Should Contain ${type} Chart For ${range}
    Navigate To  Email  Reporting  ${type}
    Select From List  xpath=//select[@id='date_range']  ${range}
    Run Keyword If  '${type}'=='System Capacity'
    ...  Page Should Contain Element  xpath=//table[@class='chart_container']//img
    Run Keyword If  '${type}'!='System Capacity'
    ...  Page Should Contain Element  xpath=//td[@id='ss_0_0_0-links']/span

Initialize Tvh662871c
    Switch To ESA
    Enable Antispam On Incoming Policy
    Enable Antispam On Outgoing Policy
    @{policy_list}=  Create List
    ...  Incoming
    ...  Outgoing

    FOR  ${policy}  IN  @{policy_list}
        Enable Antivirus on Mail Policy  ${policy}
    END
    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is documents
    ${conditions}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Documents
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info  ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}

    Apply Single Content Filter  myFilter  ${conditions}  ${actions}  Incoming

Inject Messages For Incoming Mail Report

    @{mbox_list}=  Create List
    ...  ${CLEAN}  ${SPAM}  ${TESTVIRUS}  ${SPAM_SUSPECT}
    ...  ${MARKETING}  ${MSOFFICEDOCATTACH}

    FOR  ${mbox}  IN  @{mbox_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${mbox}
        ...  num-msgs=${msg_count}
        ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END
    ${addr_file}=  Join Path  ${SUITE_TMP_DIR}  ${TEST_ID}_1.txt
    Set Test Variable  ${addr_file}
    OperatingSystem.Create File  ${addr_file}
    OperatingSystem.Append to File  ${addr_file}  testmail@testsuite.test\n

    ${mbox}=  Get From List  ${mbox_list}  0

    Inject Messages
    \  ...  mail-from=${TEST_ID}@${CLIENT}
    \  ...  mbox-filename=${mbox}
    \  ...  num-msgs=1
    \  ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    \  ...  address-list=${addr_file}
    Deliver Now All
    Sleep  5s  Wait until messages will be delivered

    Inject Messages
    \  ...  mail-from=m1_clean_message@test.com
    \  ...  mbox-filename=${mbox}
    \  ...  num-msgs=${msg_count}
    \  ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    \  ...  rcpt-host-list=${CLIENT}
    Deliver Now All
    Sleep  5s  Wait until messages will be delivered

    ${hat_dict}=  Create Dictionary
    ...  enable_mrpes  yes
    ...  mrpes  1

    Listenerconfig Edit Hostaccess Default  ${PUBLIC_LISTENER.name}  ${hat_dict}
    Commit

    Inject Messages
    \  ...  mail-from=${TEST_ID}@${CLIENT}
    \  ...  mbox-filename=${mbox}
    \  ...  num-msgs=${msg_count}
    \  ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    Deliver Now All
    Sleep  5s  Wait until messages will be delivered

    ${hat_dict}=  Create Dictionary
    ...  enable_mrpes  no

    Listenerconfig Edit Hostaccess Default  ${PUBLIC_LISTENER.name}  ${hat_dict}
    Commit

Finalize Tvh662871c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Policyconfig Edit Antispam Disable  Outgoing  DEFAULT
    Commit
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  Outgoing  default  ${settings}
    Commit Changes
    @{filters_to_disable}=  Create List  myFilter
    Mailpolicy Edit Contentfilters  incoming  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Incoming  myFilter
    Commit Changes

Initialize Tvh662817c
    Switch To ESA
    Enable Antispam On Incoming Policy
    Enable Antispam On Outgoing Policy
    @{policy_list}=  Create List
    ...  Incoming
    ...  Outgoing

    ${settings}=  Create Dictionary
    ...  Anti-Spam Scanning  Use IronPort Anti-Spam service
    Mail Policies Edit Antispam  outgoing  default  ${settings}
    ${settings}=    Mail Flow Policies Create Settings
    ...  Spam Detection  On
    Mail Flow Policies Edit  ${PRIVATE_LISTENER.name}  RELAYED  ${settings}
    Commit Changes

    FOR  ${policy}  IN  @{policy_list}
        Enable Antivirus On Mail Policy  ${policy}
    END
    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is documents
    ${conditions}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Documents
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info  ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}

    Apply Single Content Filter  myFilter  ${conditions}  ${actions}  Outgoing

Finalize Tvh662817c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    ${settings}=    Mail Flow Policies Create Settings
    ...  Spam Detection  Off
    Mail Flow Policies Edit  ${PRIVATE_LISTENER.name}  RELAYED  ${settings}
    Commit Changes
    Policyconfig Edit Antispam Disable  Outgoing  DEFAULT
    Commit

    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  Outgoing  default  ${settings}
    Commit Changes

    @{filters_to_disable}=  Create List  myFilter
    Mailpolicy Edit Contentfilters  Outgoing  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Outgoing  myFilter
    Commit Changes

Inject Messages For Content Filters Report
    @{mbox_listener_list}=  Create List
    ...  ${CLEAN}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MARKETING}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MSOFFICEXLSATTACH}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${CLEAN}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MARKETING}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MSOFFICEXLSATTACH}  ${ESA_PRIVATE_LISTENER_IP}

    FOR  ${mbox}  ${inject_host}  IN  @{mbox_listener_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${mbox}
        ...  num-msgs=${msg_count}
        ...  inject-host=${inject_host}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END

    ${PLAIN_TEXT_MATCH_MBOX}=  Join Path
    ...  ${SUITE_TMP_DIR}  plain_text_match.mbox
    Create Plain Text MBOX  ${PLAIN_TEXT_MATCH_MBOX}
    ...  Testing  mango
    ${PLAIN_TEXT_MATCH1_MBOX}=  Join Path
    ...  ${SUITE_TMP_DIR}  plain_text_match1.mbox
    Create Plain Text MBOX  ${PLAIN_TEXT_MATCH1_MBOX}
    ...  Testing  orange

    @{mbox_list}=  Create List
    ...  ${PLAIN_TEXT_MATCH_MBOX}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${PLAIN_TEXT_MATCH1_MBOX}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${PLAIN_TEXT_MATCH_MBOX}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${PLAIN_TEXT_MATCH1_MBOX}  ${ESA_PRIVATE_LISTENER_IP}

    FOR  ${mbox}  ${inject_host}  IN  @{mbox_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${mbox}
        ...  num-msgs=${msg_count}
        ...  inject-host=${inject_host}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END

Initialize Tvh664000c
    Switch To ESA
    Enable Antispam On Incoming Policy
    Enable Antispam On Outgoing Policy

    ${settings}=  Create Dictionary
    ...  Anti-Spam Scanning  Use IronPort Anti-Spam service
    Mail Policies Edit Antispam  outgoing  default  ${settings}
    ${settings}=    Mail Flow Policies Create Settings
    ...  Spam Detection  On
    Mail Flow Policies Edit  ${PRIVATE_LISTENER.name}  RELAYED  ${settings}
    Commit Changes

    @{policy_list}=  Create List
    ...  Incoming
    ...  Outgoing

    Set Test Variable  @{policy_list}

    FOR  ${policy}  IN  @{policy_list}
        Enable Antivirus on Mail Policy  ${policy}
    END
    ${attach_info_cond}=  Create Dictionary
    ...  File type is  Is documents
    ${attach_msg_cond1}=  Create Dictionary
    ...  Contains text  mango
    ${conditions1}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ...  Message Body  ${attach_msg_cond1}

    ${attach_msg_cond2}=  Create Dictionary
    ...  Contains text  orange
    ${conditions2}=  Content Filter Create Conditions
    ...  Attachment File Info  ${attach_info_cond}
    ...  Message Body  ${attach_msg_cond2}

    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${strip_attachment_by_fileinfo_action}=  Create Dictionary
    ...  File type is  Documents
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info  ${strip_attachment_by_fileinfo_action}
    ...  Drop (Final Action)  ${drop_action}

    FOR  ${policy}  IN  @{policy_list}
        Content Filter Add  ${policy}  myFilter1  myFilter1
        ...  ${actions}  ${conditions1}
        Content Filter Add  ${policy}  myFilter2  myFilter2
        ...  ${actions}  ${conditions2}
        @{filters_to_enable}=  Create List  myFilter1  myFilter2
        Mailpolicy Edit Contentfilters  ${policy}  Default Policy  custom
        ...  enable_filter_names=@{filters_to_enable}
        Commit Changes
    END

Finalize Tvh664000c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    ${settings}=    Mail Flow Policies Create Settings
    ...  Spam Detection  Off
    Mail Flow Policies Edit  ${PRIVATE_LISTENER.name}  RELAYED  ${settings}
    Commit Changes
    Policyconfig Edit Antispam Disable  Outgoing  DEFAULT
    Commit

    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  Outgoing  default  ${settings}
    Commit Changes

    @{filters_to_disable}=  Create List  myFilter1  myFilter2
    FOR  ${policy}  IN  @{policy_list}
        Mailpolicy Edit Contentfilters  ${policy}  Default Policy  custom
        ...  disable_filter_names=@{filters_to_disable}
        Content Filter Delete  ${policy}  myFilter1
        Content Filter Delete  ${policy}  myFilter2
        Commit Changes
    END

Initialize Tvh663499c
    Switch To ESA
    Enable Antispam On Incoming Policy
    Enable Antispam On Outgoing Policy

    ${settings}=  Create Dictionary
    ...  Anti-Spam Scanning  Use IronPort Anti-Spam service
    Mail Policies Edit Antispam  outgoing  default  ${settings}
    ${settings}=    Mail Flow Policies Create Settings
    ...  Spam Detection  On
    Mail Flow Policies Edit  ${PRIVATE_LISTENER.name}  RELAYED  ${settings}
    Commit Changes

    @{policy_list}=  Create List
    ...  Incoming
    ...  Outgoing

    Set Test Variable  @{policy_list}

    FOR  ${policy}  IN  @{policy_list}
        Enable Antivirus on Mail Policy  ${policy}
    END
    Outbreak Config Setup
    ...  use=yes  alerts=no  use_heuristics=no
    Commit

    FOR  ${policy}  IN  @{policy_list}
        Run Keyword And Ignore Error  Policyconfig Edit Outbreak Enable  ${policy}  DEFAULT
    END
    Commit

Finalize Tvh663499c
    Switch to ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    ${settings}=    Mail Flow Policies Create Settings
    ...  Spam Detection  Off
    Mail Flow Policies Edit  ${PRIVATE_LISTENER.name}  RELAYED  ${settings}
    Mail Policies Edit Antispam  outgoing  default  ${settings}
    Commit Changes
    Policyconfig Edit Antispam Disable  Outgoing  DEFAULT
    Commit

    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  Outgoing  default  ${settings}
    Commit Changes

    Outbreak Config Setup
    ...  use=no
    Commit
    FOR  ${policy}  IN  @{policy_list}
        Policyconfig Edit Outbreak Disable  ${policy}  DEFAULT
    END
    Commit

Initialize Tvh664017c
    Switch To ESA
    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh664017c

    Inject Messages
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${CLEAN}
    ...  num-msgs=${msg_count}
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}
    Deliver Now All
    Sleep  5s  Wait until messages will be delivered

    Inject Messages
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${CLEAN}
    ...  num-msgs=${msg_count}
    ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}
    Deliver Now All
    Sleep  5s  Wait until messages will be delivered

Initialize Tvh663925c
    Set Appliance Under Test To ESA
    Set Test Variable  ${WORD_MATCH}  orange
    Set Test Variable  ${WORD_WEIGHT}  100
    Set Test Variable  ${WORD_MAX_SCORE}  10000

    Dlp Enable
    Message Tracking Enable  track_info_for_rej_conn=${True}
    Commit Changes
    Dlp Edit Settings  enable_matched_content_logging=${True}
    Commit Changes

    Dlp Message Action Add  name=quarantine_ma
    ...  msg_action=Quarantine

    Dlp Policy New
    ...  Custom Policy
    ...  Custom Policy
    ...  change_policy_name=DLP_POLICY_0
    ...  submit=${False}

    ${rule1}=  Create Dictionary
    ...  rule_type  Words or Phrases
    ...  words_phrases  ${WORD_MATCH}
    ...  weight  ${WORD_WEIGHT}
    ...  max_score  ${WORD_MAX_SCORE}

    ${rule1}=  Evaluate
    ...  ','.join(map(lambda x: x[0] + ':' + x[1], ${rule1}.iteritems()))
    @{rules}=  Create List  ${rule1}

    Dlp Policy Create classifier  blade_name=myclassifier  description=cust classifier  rules=${rules}  submit=${True}
    Dlp Policy Configure Content Matching Classifier  DLP_POLICY_0  enable_classifiers=myclassifier  submit=${True}
    ${settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  DLP_POLICY_0  ${True}
    Mail Policies Edit Dlp
    ...  outgoing
    ...  default
    ...  ${settings}
    Commit Changes

    ${PLAIN_TEXT_MATCH_MBOX}=  Join Path
    ...  ${SUITE_TMP_DIR}  plain_text_match.mbox
    Create Plain Text MBOX  ${PLAIN_TEXT_MATCH_MBOX}
    ...  Testing  orange

    Set Test Variable  ${TEST_ID}  Tvh663925c
    Inject Messages
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${PLAIN_TEXT_MATCH_MBOX}
    ...  num-msgs=20
    ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}
    Deliver Now All
    Sleep  5s  Wait until messages will be delivered

Finalize Tvh663925c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Dlp Policy Delete  DLP_POLICY_0
    Dlp Message Action Delete  quarantine_ma
    Dlp Custom Classifier Delete  myclassifier
    Message Tracking Disable
    Dlp Disable
    Commit Changes

Initialize Tvh663914c
    Switch To ESA
    Enable Antivirus on Mail Policy  Outgoing

Finalize Tvh663914c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    ${settings}=  Create Dictionary
    ...  Anti-Virus Scanning  No
    Mail Policies Edit Antivirus  outgoing  default  ${settings}
    Commit Changes

Common Cleanup For Archive Reports
    Switch To SMA
    Email Archived Reports Delete All Reports
    Smtp Routes Clear
    Commit Changes
    Sync Time
    Switch To ESA
    Sync Time

Initialize Tvh664307c
    Set Appliance Under Test To ESA
    Set Test Variable  ${WORD_MATCH}  orange
    Set Test Variable  ${WORD_WEIGHT}  100
    Set Test Variable  ${WORD_MAX_SCORE}  10000

    Dlp Enable
    Message Tracking Enable  track_info_for_rej_conn=${True}
    Commit Changes
    Dlp Edit Settings  enable_matched_content_logging=${True}
    Commit Changes

    Dlp Message Action Add  name=quarantine_ma
    ...  msg_action=Quarantine

    Dlp Policy New
    ...  Custom Policy
    ...  Custom Policy
    ...  change_policy_name=DLP_POLICY_0
    ...  submit=${False}

    ${rule1}=  Create Dictionary
    ...  rule_type  Words or Phrases
    ...  words_phrases  ${WORD_MATCH}
    ...  weight  ${WORD_WEIGHT}
    ...  max_score  ${WORD_MAX_SCORE}

    ${rule1}=  Evaluate
    ...  ','.join(map(lambda x: x[0] + ':' + x[1], ${rule1}.iteritems()))
    @{rules}=  Create List  ${rule1}

    Dlp Policy Create classifier  blade_name=myclassifier  description=cust classifier  rules=${rules}  submit=${True}
    Dlp Policy Configure Content Matching Classifier  DLP_POLICY_0  enable_classifiers=myclassifier  submit=${True}
    ${settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  DLP_POLICY_0  ${True}
    Mail Policies Edit Dlp
    ...  outgoing
    ...  default
    ...  ${settings}
    Commit Changes

    ${PLAIN_TEXT_MATCH_MBOX}=  Join Path
    ...  ${SUITE_TMP_DIR}  plain_text_match.mbox
    Create Plain Text MBOX  ${PLAIN_TEXT_MATCH_MBOX}
    ...  Testing  orange

    Set Test Variable  ${TEST_ID}  Tvh664307c

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    Set Test Variable  ${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  10  cur_time=${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${datetime_to_set}

    Inject Messages
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${PLAIN_TEXT_MATCH_MBOX}
    ...  num-msgs=20
    ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}
    Deliver Now All
    Sleep  5s  Wait until messages will be delivered

    Sync Appliances Datetime  ${SMA}  ${ESA}
    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

Common Cleanup For Schedule Reports
    Switch To SMA
    Email Archived Reports Delete All Reports
    Smtp Routes Clear
    Commit Changes
    Sync Time
    Close All Browsers
    Selenium Login
    Switch To ESA
    Sync Time
    Close All Browsers
    Selenium Login

Initialize Tvh662995c
    Set Appliance Under Test To ESA
    Set Test Variable  ${WORD_MATCH}  orange
    Set Test Variable  ${WORD_WEIGHT}  100
    Set Test Variable  ${WORD_MAX_SCORE}  10000

    Dlp Enable
    Message Tracking Enable  track_info_for_rej_conn=${True}
    Commit Changes
    Dlp Edit Settings  enable_matched_content_logging=${True}
    Commit Changes

    Dlp Message Action Add  name=quarantine_ma
    ...  msg_action=Quarantine

    Dlp Policy New
    ...  Custom Policy
    ...  Custom Policy
    ...  change_policy_name=DLP_POLICY_0
    ...  submit=${False}

    ${rule1}=  Create Dictionary
    ...  rule_type  Words or Phrases
    ...  words_phrases  ${WORD_MATCH}
    ...  weight  ${WORD_WEIGHT}
    ...  max_score  ${WORD_MAX_SCORE}

    ${rule1}=  Evaluate
    ...  ','.join(map(lambda x: x[0] + ':' + x[1], ${rule1}.iteritems()))
    @{rules}=  Create List  ${rule1}

    Dlp Policy Create classifier  blade_name=myclassifier  description=cust classifier  rules=${rules}  submit=${True}
    Dlp Policy Configure Content Matching Classifier  DLP_POLICY_0  enable_classifiers=myclassifier  submit=${True}
    ${settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  DLP_POLICY_0  ${True}
    Mail Policies Edit Dlp
    ...  outgoing
    ...  default
    ...  ${settings}
    Commit Changes

    ${PLAIN_TEXT_MATCH_MBOX}=  Join Path
    ...  ${SUITE_TMP_DIR}  plain_text_match.mbox
    Create Plain Text MBOX  ${PLAIN_TEXT_MATCH_MBOX}
    ...  Testing  orange

    Set Test Variable  ${TEST_ID}  Tvh662995c

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    Set Test Variable  ${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  10  cur_time=${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${datetime_to_set}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Switch To ESA

    Inject Messages
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${PLAIN_TEXT_MATCH_MBOX}
    ...  num-msgs=20
    ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}
    Deliver Now All
    Sleep  5s  Wait until messages will be delivered

    Sync Appliances Datetime  ${SMA}  ${ESA}

Finalize Tvh663296c
    Centralized Email Reporting Group Delete  ${REPORTING_GROUP_NAME}
    Centralized Email Reporting Group Delete  ${Reporting_group_name2}
    Commit Changes
    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

*** Test Cases ***

Tvh663681c
    [Documentation]  When some e-mail groups are configured
    ...  and ungrouped appliances Verify Incoming
    ...  Mail: Domains page can be viewed for individual e-mail groups\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663681c
    [Tags]  srts  wsrts  Tvh663681c
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663681c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663681c
    ...  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh663681c
    Set Appliance Under Test To SMA
    Close All Browsers
    Selenium Close
    Selenium Login
    Navigate To  Email  Reporting  Incoming Mail
    Select From List  //select[@id='host_id']  Group: ${REPORTING_GROUP_NAME}
    Sleep  30s
    Page Should Contain Element  //option[contains(text(),'Group: ${REPORTING_GROUP_NAME}')]

Tvh662746c
    [Documentation]  When no e-mail group is configured,
    ...  Verify Incoming Mail: Domains page can be viewed
    ...  without "View Data For" option\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662746c
    [Tags]  srts  Tvh662746c  wsrts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662746c
    Set Appliance Under Test To SMA
    Close All Browsers
    Selenium Close
    Selenium Login
    Navigate To  Email  Reporting  Incoming Mail
    Page Should Not Contain Element  //td[contains(text(),'View Data for:')]/select

Tvh663462c
    [Documentation]  When no e-mail group is configured Verify Overview
    ...  page can be viewed for All Email Appliances\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663462c
    [Tags]  srts  Tvh663462c  wsrts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh663462c
    Set Appliance Under Test To SMA
    Close All Browsers
    Selenium Close
    Selenium Login
    Navigate To  Email  Reporting  Overview
    Page Should Contain Element  //option[contains(text(),'All Email Appliances')]
    Page Should Not Contain Element  //option[contains(text(),'Group: ${REPORTING_GROUP_NAME}')]

    Switch TO ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open

Tvh663553c
    [Documentation]  When no e-mail group is configured Verify
    ...  Overview page can be viewed for individual Appliances\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663553c
    [Tags]  srts  Tvh663553c  wsrts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh663553c
    Set Appliance Under Test To SMA
    Close All Browsers
    Selenium Close
    Selenium Login
    Navigate To  Email  Reporting  Overview
    Page Should Contain Element  //td[contains(text(),'View Data for:')]
    Page Should Not Contain Element  //option[contains(text(),'Group: ${REPORTING_GROUP_NAME}')]

Tvh662868c
    [Documentation]  When no e-mail group is configured
    ...  Verify Overview page can be viewed for individual Appliances\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662868c
    [Tags]  srts  Tvh662868c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662868c
    [Teardown]  Run Keywords
    ...  Enable Consolidated Reporting On SMA
    ...  Finalize Tvh662868c
    ...  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662868c
    Switch To SMA
    Navigate To  Email  Reporting  Overview
    Select From List  //select[@id='host_id']  Group: ${REPORTING_GROUP_NAME}
    Sleep  30s
    Page Should Contain Element  //option[contains(text(),'Group: ${REPORTING_GROUP_NAME}')]
    Page Should Contain Element  //option[contains(text(),'Machine: ${ESA}')]

Tvh664135c
    [Documentation]  Verify that CSV report contains correct value
    ...  for counter TOTAL_DLP_INCIDENTS\n
    ...  Verify that CSV report contains correct value for
    ...  counter TOTAL_RECIPIENTS_PROCESSED\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664135c
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664057c
    [Tags]  srts  wsrts  Tvh664135c  Tvh664057c
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663810c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663810c
    ...  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh664135c

    Set Test Variable  ${DLP_MSGS_COUNT}  10
    ${log_pattern}=  Set Variable  Dropped by DLP
    Switch TO ESA
    Inject Messages
    ...  mbox-filename=${ZIP_ATTACHMENT_WITH_EXCELFILE}
    ...  num-msgs=${DLP_MSGS_COUNT}
    ...  inject-host=${ESA_PRIVATE_LISTENER_IP}

    Verify And Wait For Log Records  ${log_pattern} >= ${DLP_MSGS_COUNT}

    Switch TO SMA
    ${expected_columns}=  Create List
    ...  High      ${DLP_MSGS_COUNT}
    ...  Total     ${DLP_MSGS_COUNT}
    Verify Mail Reporting On SMA
    ...  table_name=DLP Incident Details
    ...  expected_columns=${expected_columns}
    ...  left_chart=Top Incidents by Severity
    ...  right_chart=Top DLP Policy Matches
    ...  time_period=Day

    Navigate To  Email  Reporting  Outgoing Senders
    Click Link  xpath=//*[@id='report_title']/div/a
    ${start_time}=  Get Time
	Click Element  xpath=//td[@id='ss_0_1_0-links']/span[2]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .csv  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Set Test Variable  ${path}
    Log  ${path}
    ${csv_data}=  Csv Parser Get Data  ${path}
    Log List  ${csv_data}
    List Should Contain Value  ${csv_data['Total Messages']}  10
    List Should Contain Value  ${csv_data['Stopped by DLP']}  ${DLP_MSGS_COUNT}
    Remove File  ${path}

Tvh663142c
    [Documentation]  Verify user is able to generate pdf reports, and
    ...  reports contatin appropriate Virus Types data\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663142c
    [Tags]  Tvh663142c  srts  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    [Teardown]  Run Keywords
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh663142c

    Set Test Variable  ${total_msgs_count}  10
    Switch TO ESA
    Inject Messages
    ...  mbox-filename=${EICAR_COM_ZIP}
    ...  num-msgs=${total_msgs_count}
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}

    Switch TO SMA
    FOR  ${time_period}  IN
    ...  Day
    ...  Year
      ${expected_columns}=  Create List
      ...  Incoming Messages         ${total_msgs_count}
      ...  Total Infected Messages   ${total_msgs_count}
      Verify Mail Reporting On SMA
      ...  table_name=Virus Types Detail
      ...  expected_columns=${expected_columns}
      ...  time_period=${time_period}
      Verify Pdf Report  EICAR-AV-Test
    END

Tvh662861c
    [Documentation]  Verify user is able to generate pdf reports, and
    ...  reports contatin appropriate Incoming Mail data\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662861c
    [Tags]  srts  wsrts  Tvh662861c
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662881c
    [Teardown]  General Test Case Teardown
	Set Test Variable  ${TEST_ID}  Tvh662861c

    ${clean_messages_count}=  Set Variable  0
    ${spam_messages_count}=  Set Variable  0
    ${total_messages_count}=  Set Variable  0
    ${clean_messages_count}=  Evaluate  ${clean_messages_count} + 1
    ${spam_messages_count}=  Evaluate  ${spam_messages_count} + 1
    ${total_messages_count}=  Evaluate
    ...  ${clean_messages_count} + ${spam_messages_count}
    ${expected_columns}=  Create List
    ...  Clean            ${clean_messages_count}
    ...  Spam Detected    ${spam_messages_count}
    ...  Total Threat     ${spam_messages_count}
    ...  Total Attempted  ${total_messages_count}
    Verify Mail Reporting On SMA
    ...  table_name=Incoming Mail Details
    ...  expected_columns=${expected_columns}
    ...  left_chart=Top Senders by Total Threat Messages
    ...  right_chart=Top Senders by Clean Messages
    ...  time_period=Day
    Verify Pdf Report  Sender Domain

Tvh663297c
    [Documentation]  Verify export functionality for Internal Users Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663297c
    [Tags]  srts  Tvh663297c  wsrts
    [Setup]  Run Keyword
    ...  General Test Case Setup
    [Teardown]  Run Keyword
    ...  General Test Case Teardown

    Set Appliance Under Test To ESA
    Set Test Variable  ${TEST_ID}  Tvh663297c
    Set Test Variable  ${PUB_LISTENER_MSGS}  1

    @{listeners_list}=  Create List
    ...  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${ESA_PRIVATE_LISTENER_IP}

    FOR  ${listener}  IN  @{listeners_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${CLEAN}
        ...  num-msgs=${PUB_LISTENER_MSGS}
        ...  inject-host=${listener}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END

    @{range_list}=  Create List
    ...  Day
    ...  Week

    @{chart_ids}=  Create List
    ...  ss_0_0_0-links  ss_0_0_1-links

    Set Test Variable  @{chart_ids}

    @{pattern}=  Create List
	...  Incoming
    ...  Outgoing

    Set Test Variable  @{pattern}
    Set Test Variable  ${type}  Internal Users
    Set Test Variable  ${num_clean}  1

    @{expected_table_detail}=  Create List
    ...  Incoming Spam Detected    0
    ...  Incoming Virus Detected   0
    ...  Incoming Content Filter Matches   0
    ...  Incoming Stopped by Content Filter   0
    ...  Incoming Clean   1
    ...  Outgoing Spam Detected   0
    ...  Outgoing Virus Detected   0
    ...  Outgoing Content Filter Matches   0
    ...  Outgoing Stopped by Content Filter   0
    ...  Outgoing Clean   0
    ...  Incoming Detected by Advanced Malware Protection   0

   Set Test Variable  @{expected_table_detail}

   Set Appliance Under Test To SMA

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        ${table_params}=  Email Report Table Create Parameters
        ...  User Mail Flow Details
        ...  period=${range}
        ${reporting_data}=  Wait Until Keyword Succeeds
        ...  ${DATA_UPDATE_TIMEOUT}
        ...  10 sec
        ...  Email Report Table Get Data
          ...  User Mail Flow Details
          ...  ${table_params}
        @{expected_value0}=  Create List
        ...  Clean Messages  ${num_clean}
        @{expected_value1}=  Copy List  ${expected_value0}
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
	    Verify Export Data For Charts
        @{expected_value}=  Create List
        ...  @{expected_table_detail}
        Set suite variable  @{expected_value}
        Set Test Variable  ${table_name}  User Mail Flow Details
        Verify Export Data For Table ${table_name}
    END
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
