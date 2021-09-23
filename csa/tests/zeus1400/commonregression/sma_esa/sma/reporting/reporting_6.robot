# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/reporting/reporting_6.txt#8 $
# $DateTime: 2020/06/05 03:57:43 $
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
${DATA_UPDATE_TIMEOUT}=              30m
${RETRY_TIME}=                       20s
${REPORTING_GROUP_NAME}=             test_group
${REPORTING_GROUP}=                  testgroup
${firefox_prefs_browser.download.dir}=                          %{SARF_HOME}/tmp
${firefox_prefs_browser.download.folderList}=                   2
${firefox_prefs_browser.download.manager.showWhenStarting}=     false
${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=        application/pdf,text/csv,application/csv,application/xml,text/xml
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
    Selenium Login With Autodownload Enabled  ${firefox_prefs_browser.download.dir}  ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  c_rep_processing  duration=2592000
    Commit Changes
    Set Host Name  ${SMA}
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
    Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Delete Email Appliance  ${ESA}
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
    OperatingSystem.Empty Directory  ${SUITE_TMP_DIR}
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
    ...  Replace String  ${attachment_file_name}  \n  ${EMPTY}
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
       Run Keyword If  '${key}' != 'Pages Swapped'  List Should Contain Value  ${csv_data['${key}']}  ${value}
       ${data} =  Get From List  ${csv_data['${key}']}  0
       ${status}  ${data}=  Run Keyword and Ignore Error  Convert To Number  ${data}
       Run Keyword If  '${key}' == 'Pages Swapped'  Should Be True  ${data} < 30.0
    END

Apply Single Content Filter
    [Arguments]  ${name}  ${conditions}  ${actions}  ${dest_policy}
    Content Filter Add  ${dest_policy}  ${name}  ${name}
    ...  ${actions}  ${conditions}
    @{filters_to_enable}=  Create List  ${name}
    Wait Until Keyword Succeeds  1m  10s
    ...  Mailpolicy Edit Contentfilters  ${dest_policy}  Default Policy  custom
    ...  enable_filter_names=@{filters_to_enable}
    Commit Changes

Initialize Tvh663254c
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

Finalize Tvh663254c
    Switch To ESA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
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
    ${path}=   Wait Until Keyword Succeeds  2m  5s  Reports Export  page=Email, Reporting, ${type}
    ...  name=${table_name}   password=${DUT_ADMIN_SSW_PASSWORD}
    OperatingSystem.File Should Exist  ${path}
    ${dir}  ${filename}=  Split Path  ${path}
    Find And Verify CSV Report  ${dir}  ${file_name}  @{expected_value}
    Remove File  ${path}

Enable Antispam on Incoming Policy
    ${spam_dict}=  Spam Params Get
    ...  action_spam=IRONPORT QUARANTINE
    ${suspected_spam_dict}=  Suspected Spam Params Get
    ...  action_spam_suspected=IRONPORT QUARANTINE

    Policyconfig Edit Antispam Edit  Incoming
    ...  DEFAULT
    ...  ${spam_dict}
    ...  ${suspected_spam_dict}
    Commit

Enable Antispam On Outgoing Policy
    ${spam_dict}=  Spam Params Get
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
    Run Keyword And Ignore Error  Start CLI Session If Not Open
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
    Log Out Of Dut
    Sync Time
    Log into DUT
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

*** Test Cases ***

 Tvh663914c
    [Documentation]  Verify Virus Types archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663914c
    [Tags]  erts  Tvh663914c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663914c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663914c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh663914c

    Shift ESA Datetime  sec_offset=-3600*24

    @{listeners_list}=  Create List
    ...  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${ESA_PRIVATE_LISTENER_IP}

    FOR  ${listener}  IN  @{listeners_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${EICAR_COM_ZIP}
        ...  num-msgs=${msg_count}
        ...  inject-host=${listener}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  80s  Wait until messages will be delivered
    END

    Sync Appliances Datetime  ${SMA}  ${ESA}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Virus Types
    Set Test Variable  ${range}  Yesterday (00:00 to 23:59)

    @{pattern}=  Create List
    ...  Incoming
    ...  Outgoing
    ...  Detail

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Messages   1
    ...  Virus Type    EICAR-AV-Test

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Copy List  ${expected_value0}
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Incoming Messages  1
    ...  Total Infected Messages  2
    ...  Outgoing Messages  1
    ...  Virus Type  EICAR-AV-Test

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Incoming Messages  Outgoing Messages  Total  Infected Messages  1  1  2

    Set Test Variable  @{expected_value3}

    ${table_params}=  Email Report Table Create Parameters
    ...  Virus Types Detail
    ...  period=${range}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  20 sec
    ...  Email Report Table Get Data
         ...  Virus Types Detail
         ...  ${table_params}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  3  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Email Archived Reports Add Report
       ...  ${sma_email_reports.VIRUS_TYPES}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=last day
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       ${num}=  Evaluate  ${num} + 1
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  3
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value3}
        Should Contain  ${out}  ${entry}
    END

Tvh664275c
    [Documentation]  Verify Outgoing Destinations archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664275c
    [Tags]  erts  Tvh664275c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662817c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662817c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh664275c

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'

    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  7  cur_time=${first_day_of_curr_month}

    SmaCliLibrary.Set Time Set  ${datetime_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    @{mbox_list}=  Create List
    ...  ${CLEAN}  ${SPAM}  ${FLASHPLA_EXE}
    ...  ${SPAM_SUSPECT}  ${MARKETING}  ${MSOFFICEDOCATTACH}

    FOR  ${mbox}  IN  @{mbox_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${mbox}
        ...  num-msgs=${msg_count}
        ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  85s  Wait until messages will be delivered
    END

    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Outgoing Destinations
    Set Test Variable  ${range}  Week
    Set Test Variable  ${num_threats}  4
    Set Test Variable  ${num_clean}  2

    @{pattern}=  Create List
    ...  Threat
    ...  Clean
    ...  Detail

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Threat Messages  ${num_threats}
    ...  Domain  ${CLIENT}
    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Clean Messages  ${num_clean}
    ...  Domain  ${CLIENT}
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Clean            2
    ...  Spam Detected    2
    ...  Total Threat     4
    ...  Stopped by Content Filter   1
    ...  Virus Detected   1
    ...  Total Processed   6
    ...  Hard Bounced   0
    ...  Delivered   0
    ...  Total Messages Delivered   0
    ...  Destination Domain   ${CLIENT}

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Destination  ${CLIENT}  Spam  Detected  Virus  Detected
    ...  Messages  Stopped by Content Filter  Total Threat  Clean
    ...  Total  Processed  Hard  Bounced  Delivered  Total  Messages Delivered
    ...  2  1  1  4  2  6  0  0  0

    Set Test Variable  @{expected_value3}

    Navigate To  Email  Reporting  Outgoing Destinations
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  3  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Email Archived Reports Add Report
       ...  ${sma_email_reports.OUT_DESTINATIONS}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=last week
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ...  num_of_rows=20
       ...  sort_col=virus
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  3
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value3}
        Should Contain  ${out}  ${entry}
    END

Tvh664039c
    [Documentation]  Verify Content Filters archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664039c
    [Tags]  srts  Tvh664039c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664000c
    [Teardown]  Run Keywords
    ...  Finalize Tvh664000c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh664039c
    Set Test Variable  ${msg_count}  1
    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  150  cur_time=${first_day_of_curr_month}
    SmaCliLibrary.Set Time Set  ${datetime_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    Inject Messages For Content Filters Report

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Content Filters
    Set Test Variable  ${range}  Year

    Sleep  20s  Wait until all messages delivered
    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}
    Sleep  40s  Wait until all messages delivered

    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    @{pattern}=  Create List
    ...  ${TEST_ID}_Top_Incoming
    ...  ${TEST_ID}_Top_Outgoing
    ...  ${TEST_ID}_Incoming
    ...  ${TEST_ID}_Outgoing

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Messages  3
    ...  Messages  1
    ...  Content Filter  myFilter1
    ...  Content Filter  myFilter2

    Set Test Variable  @{expected_value0}
    @{expected_value1}=  Copy List  ${expected_Value0}
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Messages  3
    ...  Messages  1
    ...  Messages  4
    ...  Content Filter  myFilter1
    ...  Content Filter  myFilter2
    Set Test Variable  @{expected_value2}
    @{expected_value3}=  Copy List  ${expected_value2}
    Set Test Variable  @{expected_value3}

    @{expected_value4}=  Copy List  ${expected_value2}
    Set Test Variable  @{expected_value4}

    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  4  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    Set Test Variable  ${time_range}  num months:5
    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Wait Until Keyword Succeeds  5m  20s
       ...  Email Archived Reports Add Report
       ...  ${sma_email_reports.FILTERS}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=${time_range}
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    Log  ${out}
    Convert To String  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value4}
        Should Contain  ${out}  ${entry}
    END

Tvh664021c
    [Documentation]  Verify Outgoing mail summary archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664021c
    [Tags]  srts  Tvh664021c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664000c
    [Teardown]  Run Keywords
    ...  Finalize Tvh664000c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh664021c
    Set Test Variable  ${msg_count}  1

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  30  cur_time=${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${datetime_to_set}

    Inject Messages For Content Filters Report

    Sync Appliances Datetime  ${SMA}  ${ESA}
    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Content Filters
    Set Test Variable  ${range}  30 days

    @{pattern}=  Create List
    ...  Over
    ...  Graph
    ...  Threat
    ...  Clean

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Virus Detected  0
    ...  Stopped by Content Filter  4
    ...  Spam Detected  1
    ...  Clean Messages  2

    Set Test Variable  @{expected_value0}
    @{expected_value1}=  Create List
    ...  Virus Detected  0
    ...  Stopped by Content Filter  4
    ...  Spam Detected  1
    ...  Clean  2

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Domain  ${CLIENT}
    ...  Matches  4

    Set Test Variable  @{expected_value2}
    @{expected_value3}=  Create List
    ...  Domain  ${CLIENT}
    ...  Clean Messages  2
    Set Test Variable  @{expected_value3}

    @{expected_value4}=  Create List
    ...  Spam Detected   Virus Detected
    ...  Stopped by Content Filter   Clean Messages
    ...  Total Messages Processed:   Total Messages Delivered:
    ...  1  0  4  2  7  1
    Set Test Variable  @{expected_value4}

    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  4  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    Set Test Variable  ${time_range}  last month
    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Email Archived Reports Add Report
       ...  ${sma_email_reports.OUT_MAIL}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=${time_range}
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    Convert To String  ${out}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value4}
        Should Contain  ${out}  ${entry}
    END

Tvh663212c
    [Documentation]  Verify Sender Groups archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663212c
    [Tags]  erts  Tvh663212c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664000c
    [Teardown]  Run Keywords
    ...  Finalize Tvh664000c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh663212c
    Set Test Variable  ${msg_count}  1

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  210  cur_time=${first_day_of_curr_month}

    SmaCliLibrary.Set Time Set  ${datetime_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    Inject Messages For Content Filters Report

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Sender Groups
    Set Test Variable  ${range}  Year


    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}


    @{pattern}=  Create List
    ...  Sender_Group
    ...  Mail_Flow

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Total Connections  7
    ...  Sender Group  UNKNOWNLIST
    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Relay  0
    ...  TCP Refuse  0
    ...  Accept  7
    ...  Reject  0

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Sender Group  UNKNOWNLIST
    ...  Accept (100.0%)   7
    ...  Total Incoming Connections:  7

    Set Test Variable  @{expected_value2}

    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  2  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    Set Test Variable  ${time_range}  num months:7
    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Wait Until Keyword Succeeds  5m  20s
       ...  Email Archived Reports Add Report
       ...  ${sma_email_reports.SENDER_GROUPS}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=${time_range}
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  2
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Split String  ${out}  \\n
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value2}
        Should Contain  ${out}  ${entry}
    END

Tvh664307c
    [Documentation]  Verify DLP Incidents Summary archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664307c
    [Tags]  srts  Tvh664307c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664307c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663925c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown


    Set Test Variable  ${type}  DLP Incidents
    Set Test Variable  ${range}  30 days

    @{pattern}=  Create List
    ...  Details
    ...  Summary
    ...  Top_DLP
    ...  Top_Incidents

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Medium  20
    ...  DLP Policy   DLP_POLICY_0
    ...  High  0
    ...  Critical  0
    ...  Low   0
    ...  Total  20
    ...  Delivered (encrypted)  0
    ...  Delivered (clear)  20

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  High   0.0
    ...  High   0
    ...  Critical  0.0
    ...  Critical   0
    ...  Total   20
    ...  Medium  100.0
    ...  Medium  20
    ...  Low   0.0
    ...  Low   0

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  DLP Policy Matches  DLP_POLICY_0
    ...  Messages  20

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  High   0
    ...  Critical   0
    ...  Medium   20
    ...  Low    0

    Set Test Variable  @{expected_value3}

    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  4  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Email Archived Reports Add Report
       ...  ${sma_email_reports.DLP_INCIDENT}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=num days:10
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ...  num_of_rows=20
       ...  sort_col=medium
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END

    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    Convert To String  ${out}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value0}
        Should Contain  ${out}  ${entry}
    END

Tvh663043c
    [Documentation]  Verify Outgoing Senders: Domains archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663043c
    [Tags]  erts  Tvh663043c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662817c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662817c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh663043c

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  30  cur_time=${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${datetime_to_set}

    @{mbox_list}=  Create List
    ...  ${CLEAN}  ${SPAM}  ${FLASHPLA_EXE}  ${SPAM_SUSPECT}
    ...  ${MARKETING}  ${MSOFFICEDOCATTACH}

    FOR  ${mbox}  IN  @{mbox_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${mbox}
        ...  num-msgs=${msg_count}
        ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END

    Sync Appliances Datetime  ${SMA}  ${ESA}
    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Outgoing Senders
    Set Test Variable  ${range}  30 days

    @{pattern}=  Create List
    ...  Threat
    ...  Clean
    ...  Details

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Domain   ${CLIENT_HOSTNAME}
    ...  Threat Messages  4

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Domain   ${CLIENT_HOSTNAME}

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Sender Domain  ${CLIENT_HOSTNAME}
    ...  Virus Detected  1
    ...  Total Threat  4
    ...  Total Messages  6
    ...  Spam Detected  2
    ...  Clean  2
    ...  Stopped by Content Filter  1

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Sender Domain  ${CLIENT_HOSTNAME}
    ...  Virus  Detected  1
    ...  Total  Threat  4
    ...  Total  Messages  6
    ...  Spam  Detected  2
    ...  Clean  2
    ...  Stopped  by  Content  Filter  1

    Set Test Variable  @{expected_value3}

    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}


    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  3  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Email Archived Reports Add Report
       ...  ${sma_email_reports.OUT_DOMAIN_SENDERS}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=last month
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ...  num_of_rows=20
       ...  sort_col=clean
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  3
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Split String  ${out}  \\n
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value3}
        Should Contain  ${out}  ${entry}
    END

Tvh662753c
    [Documentation]  Verify Virus Types schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662753c
    [Tags]  erts  Tvh662753c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663914c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663914c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh662753c

    Shift ESA Datetime  sec_offset=-3600*24

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Switch To ESA

    @{listeners_list}=  Create List
    ...  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${ESA_PRIVATE_LISTENER_IP}

    FOR  ${listener}  IN  @{listeners_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${EICAR_COM_ZIP}
        ...  num-msgs=${msg_count}
        ...  inject-host=${listener}
       ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END

    Sync Appliances Datetime  ${SMA}  ${ESA}

    Set Test Variable  ${type}  Virus Types
    Set Test Variable  ${range}  Yesterday (00:00 to 23:59)

    @{pattern}=  Create List
    ...  Incoming
    ...  Outgoing
    ...  Detail

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Messages   1
    ...  Virus Type    EICAR-AV-Test

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Copy List  ${expected_value0}
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Incoming Messages  1
    ...  Total Infected Messages  2
    ...  Outgoing Messages  1
    ...  Virus Type  EICAR-AV-Test

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Incoming Messages  Outgoing Messages  Total  Infected Messages  1  1  2

    Set Test Variable  @{expected_value3}

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    ${table_params}=  Email Report Table Create Parameters
    ...  Virus Types Detail
    ...  period=${range}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  10 sec
    ...  Email Report Table Get Data
         ...  Virus Types Detail
         ...  ${table_params}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  3  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${current_time}=  Set Time Get
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  1  cur_time=${current_time}
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=1
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
       Email Scheduled Reports Add Report
        ...  ${sma_email_reports.VIRUS_TYPES}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=last day
        ...  schedule=daily:${hour_for_report}
        ...  email_to=user@${CLIENT}
        Commit Changes
        Set Time Set  ${time_to_set}
        ${flag}=  Get From List  ${flg_list}  ${num}
        ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
        Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
        ${num}=  Evaluate  ${num} + 1
        Verify Log Contains Records
        ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
        ...  timeout=180
        Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
        Null Smtpd Stop
        Email Scheduled Reports Delete Report  ${TEST_NAME}
        Commit Changes
    END
    FOR  ${index}  IN RANGE  0  3
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value3}
        Should Contain  ${out}  ${entry}
    END

Tvh663848c
    [Documentation]  Verify Outgoing mail summary schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663848c
    [Tags]  srts  Tvh663848c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664000c
    [Teardown]  Run Keywords
    ...  Finalize Tvh664000c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh663848c
    Set Test Variable  ${msg_count}  1

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  30  cur_time=${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${datetime_to_set}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Switch To ESA
    Inject Messages For Content Filters Report

    Sync Appliances Datetime  ${SMA}  ${ESA}

    Set Test Variable  ${type}  Content Filters
    Set Test Variable  ${range}  30 days

    @{pattern}=  Create List
    ...  Over
    ...  Graph
    ...  Threat
    ...  Clean

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Virus Detected  0
    ...  Stopped by Content Filter  4
    ...  Spam Detected  1
    ...  Clean Messages  2

    Set Test Variable  @{expected_value0}
    @{expected_value1}=  Create List
    ...  Virus Detected  0
    ...  Stopped by Content Filter  4
    ...  Spam Detected  1
    ...  Clean  2

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Domain  ${CLIENT}
    ...  Matches  4

    Set Test Variable  @{expected_value2}
    @{expected_value3}=  Create List
    ...  Domain  ${CLIENT}
    ...  Clean Messages  2
    Set Test Variable  @{expected_value3}

    @{expected_value4}=  Create List
    ...  Spam Detected   Virus Detected
    ...  Stopped by Content Filter   Clean Messages
    ...  Total Messages Processed:   Total Messages Delivered:
    ...  1  0  4  2  7  1
    Set Test Variable  @{expected_value4}

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  4  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    Set Test Variable  ${time_range}  last month
    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  30  cur_time=${first_day_of_curr_month}
        Run Keyword And Ignore Error  Start CLI Session If Not Open
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
       Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=30
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
       Email Scheduled Reports Add Report
        ...  ${sma_email_reports.OUT_MAIL}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=last month
        ...  schedule=monthly:${hour_for_report}
        ...  email_to=user@${CLIENT}
        Commit Changes
        Set Time Set  ${time_to_set}
        ${flag}=  Get From List  ${flg_list}  ${num}
        ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
        Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
        ${num}=  Evaluate  ${num} + 1
        Verify Log Contains Records
        ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
        ...  timeout=180
        Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
        Null Smtpd Stop
        Email Scheduled Reports Delete Report  ${TEST_NAME}
        Commit Changes
    END

    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    Convert To String  ${out}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value4}
        Should Contain  ${out}  ${entry}
    END

Tvh662995c
    [Documentation]  Verify DLP Incidents Summary schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662995c
    [Tags]  erts  Tvh662995c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662995c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663925c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${type}  DLP Incidents
    Set Test Variable  ${range}  30 days

    @{pattern}=  Create List
    ...  Details
    ...  Summary
    ...  Top_DLP
    ...  Top_Incidents

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Medium  20
    ...  DLP Policy   DLP_POLICY_0
    ...  High  0
    ...  Critical  0
    ...  Low   0
    ...  Total  20
    ...  Delivered (encrypted)  0
    ...  Delivered (clear)  20

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  High   0.0
    ...  High   0
    ...  Critical  0.0
    ...  Critical   0
    ...  Total   20
    ...  Medium  100.0
    ...  Medium  20
    ...  Low   0.0
    ...  Low   0

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  DLP Policy Matches  DLP_POLICY_0
    ...  Messages  20

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  High   0
    ...  Critical   0
    ...  Medium   20
    ...  Low    0

    Set Test Variable  @{expected_value3}

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  4  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  10  cur_time=${first_day_of_curr_month}
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
       ${current_time}=  Set Time Get
        @{day_to_set}=  Split String  ${current_time}
        ${day}=  Get From List  ${day_to_set}  0
        ${dict_days}=  Create Dictionary  Sun  Sunday  Mon  Monday
        ...  Tue  Tuesday  Wed  Wednesday  Thu  Thursday  Fri  Friday  Sat  Saturday
       ${day_final}=  Get From Dictionary  ${dict_days}  ${day}
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=7
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
        Email Scheduled Reports Add Report
        ...  ${sma_email_reports.DLP_INCIDENT}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=num days:10
        ...  schedule=weekly:${hour_for_report}:${day_final}
        ...  email_to=user@${CLIENT}
        ...  num_of_rows=20
        ...  sort_col=medium
       Commit Changes
       Set Time Set  ${time_to_set}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Verify Log Contains Records
       ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
       ...  timeout=180
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
       Email Scheduled Reports Delete Report  ${TEST_NAME}
       Commit Changes
    END

    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END

    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Split String  ${out}  \\n
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value0}
        Should Contain  ${out}  ${entry}
    END

Tvh664184c
    [Documentation]  Verify Outgoing Destinations schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664184c
    [Tags]  erts  Tvh664184c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662817c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662817c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh664184c

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  7  cur_time=${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${datetime_to_set}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Switch To ESA

    @{mbox_list}=  Create List
    ...  ${CLEAN}  ${SPAM}  ${FLASHPLA_EXE}
    ...  ${SPAM_SUSPECT}  ${MARKETING}  ${MSOFFICEDOCATTACH}


    FOR  ${mbox}  IN  @{mbox_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${mbox}
        ...  num-msgs=${msg_count}
        ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END

    Sync Appliances Datetime  ${SMA}  ${ESA}

    Set Test Variable  ${type}  Outgoing Destinations
    Set Test Variable  ${range}  Week
    Set Test Variable  ${num_threats}  4
    Set Test Variable  ${num_clean}  2

    @{pattern}=  Create List
    ...  Threat
    ...  Clean
    ...  Detail

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Threat Messages  ${num_threats}
    ...  Domain  ${CLIENT}
    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Clean Messages  ${num_clean}
    ...  Domain  ${CLIENT}
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Clean            2
    ...  Spam Detected    2
    ...  Total Threat     4
    ...  Stopped by Content Filter   1
    ...  Virus Detected   1
    ...  Total Processed   6
    ...  Hard Bounced   0
    ...  Delivered   0
    ...  Total Messages Delivered   0
    ...  Destination Domain   ${CLIENT}

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Destination  ${CLIENT}  Spam  Detected  Virus  Detected
    ...  Messages  Stopped by Content Filter  Total Threat  Clean
    ...  Total  Processed  Hard  Bounced  Delivered  Total  Messages Delivered
    ...  2  1  1  4  2  6  0  0  0

    Set Test Variable  @{expected_value3}

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    Navigate To  Email  Reporting  Outgoing Destinations
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  3  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  7  cur_time=${first_day_of_curr_month}
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        @{day_to_set}=  Split String  ${current_time}
        ${day}=  Get From List  ${day_to_set}  0
        ${dict_days}=  Create Dictionary  Sun  Sunday  Mon  Monday
        ...  Tue  Tuesday  Wed  Wednesday  Thu  Thursday  Fri  Friday  Sat  Saturday
        ${day_final}=  Get From Dictionary  ${dict_days}  ${day}
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=7
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
        Email Scheduled Reports Add Report
        ...  ${sma_email_reports.OUT_DESTINATIONS}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=last week
        ...  schedule=weekly:${hour_for_report}:${day_final}
        ...  email_to=user@${CLIENT}
        ...  num_of_rows=20
        ...  sort_col=virus
       Commit Changes
       Set Time Set  ${time_to_set}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Verify Log Contains Records
       ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
       ...  timeout=180
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
       Email Scheduled Reports Delete Report  ${TEST_NAME}
       Commit Changes
    END
    FOR  ${index}  IN RANGE  0  3
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value3}
        Should Contain  ${out}  ${entry}
    END

Tvh663515c
    [Documentation]  Verify Outgoing Senders: Domains schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663515c
    [Tags]  srts  Tvh663515c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662817c
    ...  Switch To SMA
    ...  Commit Changes
    [Teardown]  Run Keywords
    ...  Finalize Tvh662817c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh663515c
    Run keyword and ignore error  Smtp Routes Clear
    Commit changes

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  30  cur_time=${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${datetime_to_set}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Switch To ESA

    @{mbox_list}=  Create List
    ...  ${CLEAN}  ${SPAM}  ${FLASHPLA_EXE}  ${SPAM_SUSPECT}
    ...  ${MARKETING}  ${MSOFFICEDOCATTACH}

    FOR  ${mbox}  IN  @{mbox_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${mbox}
        ...  num-msgs=${msg_count}
        ...  inject-host=${ESA_PRIVATE_LISTENER_IP}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END

    Sync Appliances Datetime  ${SMA}  ${ESA}


    Set Test Variable  ${type}  Outgoing Senders
    Set Test Variable  ${range}  30 days

    @{pattern}=  Create List
    ...  Threat
    ...  Clean
    ...  Details

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Domain   ${CLIENT_HOSTNAME}
    ...  Threat Messages  4

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Domain   ${CLIENT_HOSTNAME}

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Sender Domain  ${CLIENT_HOSTNAME}
    ...  Virus Detected  1
    ...  Total Threat  4
    ...  Total Messages  6
    ...  Spam Detected  2
    ...  Clean  2
    ...  Stopped by Content Filter  1

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Sender Domain  ${CLIENT_HOSTNAME}
    ...  Virus  Detected  1
    ...  Total  Threat  4
    ...  Total  Messages  6
    ...  Spam  Detected  2
    ...  Clean  2
    ...  Stopped  by  Content  Filter  1

    Set Test Variable  @{expected_value3}

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  3  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  30  cur_time=${first_day_of_curr_month}
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=30
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
        Email Scheduled Reports Add Report
        ...  ${sma_email_reports.OUT_DOMAIN_SENDERS}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=last month
        ...  schedule=monthly:${hour_for_report}
        ...  email_to=user@${CLIENT}
        ...  num_of_rows=20
       ...  sort_col=clean
       Commit Changes
       Set Time Set  ${time_to_set}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Verify Log Contains Records
       ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
       ...  timeout=180
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
       Email Scheduled Reports Delete Report  ${TEST_NAME}
       Commit Changes
    END
    FOR  ${index}  IN RANGE  0  3
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    Convert To String  ${out}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value3}
        Should Contain  ${out}  ${entry}
    END

Tvh664245c
    [Documentation]  Verify Incoming Mail Summary archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664245c
    [Tags]  srts  Tvh664245c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662871c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662871c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh664245c
    Set Test Variable  ${msg_count}  10


    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'

    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  1  cur_time=${first_day_of_curr_month}
    SmaCliLibrary.Set Time Set  ${datetime_to_set}

    Sync Appliances Datetime  ${SMA}  ${ESA}
    Inject Messages For Incoming Mail Report

    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${range}  Yesterday (00:00 to 23:59)
    @{pattern}=  Create List
    ...  Threat
    ...  Clean
    ...  Summary
    ...  Graph
    ...  Over

    Set Test Variable  @{pattern}
    Set Test Variable  ${num_threats}  50
    Set Test Variable  ${num_clean}  31

    @{expected_value0}=  Create List
    ...  Threat Messages  ${num_threats}
    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Clean Messages  ${num_clean}
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Clean Messages   31
    ...  Spam Detected    20
    ...  Total Threat Messages  50
    ...  Total Attempted Messages  81
    ...  Stopped by Reputation Filtering  9
    ...  Stopped as Invalid Recipients  1
    ...  Stopped by Content Filter  10
    ...  Virus Detected  10
    ...  Marketing Messages  0
    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Clean   31
    ...  Marketing   0
    ...  Reputation Filters   9
    ...  Invalid Recipients   1
    ...  Stopped by Content Filter   10
    ...  Spam Detected   20
    ...  Virus Detected  10
    Set Test Variable  @{expected_value3}

    @{expected_value4}=  Copy List  ${expected_value2}
    Set Test Variable  @{expected_value4}

    Set List Value  ${expected_value4}  4
    ...  Total Threat Messages:

    Set List Value  ${expected_value4}  6
    ...  Total Attempted Messages:

    Run Keyword And Ignore Error  Log Into DUT
    ${table_params}=  Email Report Table Create Parameters
    ...  Incoming Mail Details
    ...  period=${range}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  10 sec
    ...  Email Report Table Get Data
    ...  Incoming Mail Details
    ...  ${table_params}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  5  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Email Archived Reports Add Report
       ...  ${sma_email_reports.IN_MAIL}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=last day
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    Convert To String  ${out}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value4}
        Should Contain  ${out}  ${entry}
    END

Tvh663544c
    [Documentation]  Verify Incoming Mail Summary schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663544c
    [Tags]  srts  Tvh663544c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662871c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662871c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh663544c
    Set Test Variable  ${msg_count}  10

    Shift ESA Datetime  sec_offset=-3600*24

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Switch To ESA
    Inject Messages For Incoming Mail Report

    Sync Appliances Datetime  ${SMA}  ${ESA}

    Set Test Variable  ${range}  Yesterday (00:00 to 23:59)

    @{pattern}=  Create List
    ...  Threat
    ...  Clean
    ...  Summary
    ...  Graph
    ...  Over

    Set Test Variable  @{pattern}
    Set Test Variable  ${num_threats}  50
    Set Test Variable  ${num_clean}  31

    @{expected_value0}=  Create List
    ...  Threat Messages  ${num_threats}
    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Clean Messages  ${num_clean}
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Clean Messages   31
    ...  Spam Detected    20
    ...  Total Threat Messages  50
    ...  Total Attempted Messages  81
    ...  Stopped by Reputation Filtering  9
    ...  Stopped as Invalid Recipients  1
    ...  Stopped by Content Filter  10
    ...  Virus Detected  10
    ...  Marketing Messages  0
    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Clean   31
    ...  Marketing   0
    ...  Reputation Filters   9
    ...  Invalid Recipients   1
    ...  Stopped by Content Filter   10
    ...  Spam Detected   20
    ...  Virus Detected  10
    Set Test Variable  @{expected_value3}

    @{expected_value4}=  Copy List  ${expected_value2}
    Set Test Variable  @{expected_value4}

    Set List Value  ${expected_value4}  4
    ...  Total Threat Messages:

    Set List Value  ${expected_value4}  6
    ...  Total Attempted Messages:

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    ${table_params}=  Email Report Table Create Parameters
    ...  Incoming Mail Details
    ...  period=${range}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  10 sec
    ...  Email Report Table Get Data
    ...  Incoming Mail Details
    ...  ${table_params}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  5  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
    	Switch To SMA
        Start CLI Session
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${current_time}=  Set Time Get
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  1  cur_time=${current_time}
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=1
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
        Email Scheduled Reports Add Report
        ...  ${sma_email_reports.IN_MAIL}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=last day
        ...  schedule=daily:${hour_for_report}
        ...  email_to=user@${CLIENT}
        Commit Changes
        Set Time Set  ${time_to_set}
        ${flag}=  Get From List  ${flg_list}  ${num}
        ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
        Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
        ${num}=  Evaluate  ${num} + 1
        Verify Log Contains Records
        ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
        ...  timeout=180
        Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
        Null Smtpd Stop
        Email Scheduled Reports Delete Report  ${TEST_NAME}
        Commit Changes
    END
    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    Convert To String  ${out}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value4}
        Should Contain  ${out}  ${entry}
    END

Tvh664034c
    [Documentation]  Verify Internal Users archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664034c
    [Tags]  erts  Tvh664034c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662817c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662817c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh664034c

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  150  cur_time=${first_day_of_curr_month}

    SmaCliLibrary.Set Time Set  ${datetime_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    @{mbox_listener_list}=  Create List
    ...  ${CLEAN}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM_SUSPECT}
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${MARKETING}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${CLEAN}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM_SUSPECT}
    ...  ${ESA_PRIVATE_LISTENER_IP}  ${MARKETING}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PRIVATE_LISTENER_IP}

    FOR  ${mbox}  ${inject_host}  IN  @{mbox_listener_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${mbox}
        ...  num-msgs=${msg_count}
        ...  inject-host=${inject_host}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  50s  Wait until messages will be delivered
    END
    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Internal Users
    Set Test Variable  ${range}  Year

    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}
    Sleep  40s  Wait for all mails to deliver

    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    @{pattern}=  Create List
    ...  ${TEST_ID}_Summary_Information_for_Incoming
    ...  ${TEST_ID}_Summary_Information_for_Internal_Users_-_Incoming_Mail
    ...  ${TEST_ID}_Summary_Information_for_Outgoing
    ...  ${TEST_ID}_Summary_Information_for_Internal_Users_-_Outgoing_Mail
    ...  ${TEST_ID}_Top_Users_by_Clean_Messages_Received
    ...  ${TEST_ID}_Top_Users_by_Virus_Messages_Sent
    ...  ${TEST_ID}_Top_Users_by_Clean_Messages_Sent
    ...  ${TEST_ID}_Top_Users_by_Threat_Messages_Received

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Total Attempted Messages  6
    ...  Virus Detected  1
    ...  Spam Detected  2
    ...  Marketing Messages  0
    ...  Stopped by Content Filter  0
    ...  Clean Messages  3

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Virus Detected  1
    ...  Spam Detected  2
    ...  Marketing  0
    ...  Stopped by Content Filter  0
    ...  Clean  3

    Set Test Variable  @{expected_value1}

     @{expected_value2}=  Create List
    ...  Total Attempted Messages   6
    ...  Virus Detected   1
    ...  Spam Detected   2
    ...  Stopped by Content Filter  1
    ...  Clean Messages  2

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Virus Detected   1
    ...  Spam Detected   2
    ...  Stopped by Content Filter  1
    ...  Clean  2

    Set Test Variable  @{expected_value3}

    @{expected_value4}=  Create List
    ...  Clean Messages   1
    ...  Clean Messages   1

    Set Test Variable  @{expected_value4}

    @{expected_value5}=  Create List
    ...  Virus   1
    Set Test Variable  @{expected_value5}

    @{expected_value6}=  Create List
    ...  Clean Messages   2
    Set Test Variable  @{expected_value6}

    @{expected_value7}=  Create List
    ...  Threat Messages   1
    ...  Threat Messages   1
    ...  Threat Messages   1

    Set Test Variable  @{expected_value7}

    @{expected_value8}=  Create List
    ...  Spam Detected   Virus Detected   Stopped by Content Filter
    ...  Marketing Messages  Clean Messages   Total Attempted Messages:
    ...  2   1   0   1   2   6
    Set Test Variable  @{expected_value8}


    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  9  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
       Clean Up Delivery Queue
       Roll Over Now  mail_logs
       Null Smtpd Start  bind-ip=${CLIENT_IP}
       Email Archived Reports Add Report
       ...  ${sma_email_reports.INT_USERS}
       ...  title=${TEST_NAME}
       ...  report_format=${report}
       ...  time_range=last year
       ...  email_to=testuser@${CLIENT_HOSTNAME}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  8
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value8}
        Should Contain  ${out}  ${entry}
    END

Tvh662971c
    [Documentation]  Verify Internal Users Summary schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662971c
    [Tags]  erts  Tvh662971c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662817c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662817c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh662971c


    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  30  cur_time=${first_day_of_curr_month}
    EsaCliLibrary.Set Time  ${datetime_to_set}

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit
    Switch To ESA

    @{mbox_listener_list}=  Create List
    ...  ${CLEAN}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM_SUSPECT}
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${MARKETING}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${CLEAN}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM_SUSPECT}
    ...  ${ESA_PRIVATE_LISTENER_IP}  ${MARKETING}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PRIVATE_LISTENER_IP}

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
    Sync Appliances Datetime  ${SMA}  ${ESA}

    Set Test Variable  ${type}  Internal Users
    Set Test Variable  ${range}  30 days

    @{pattern}=  Create List
    ...  ${TEST_ID}_Summary_Information_for_Incoming
    ...  ${TEST_ID}_Summary_Information_for_Internal_Users_-_Incoming_Mail
    ...  ${TEST_ID}_Summary_Information_for_Outgoing
    ...  ${TEST_ID}_Summary_Information_for_Internal_Users_-_Outgoing_Mail
    ...  ${TEST_ID}_Top_Users_by_Clean_Messages_Received
    ...  ${TEST_ID}_Top_Users_by_Virus_Messages_Sent
    ...  ${TEST_ID}_Top_Users_by_Clean_Messages_Sent
    ...  ${TEST_ID}_Top_Users_by_Threat_Messages_Received

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Total Attempted Messages  6
    ...  Virus Detected  1
    ...  Spam Detected  2
    ...  Marketing Messages  0
    ...  Stopped by Content Filter  0
    ...  Clean Messages  3

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Virus Detected  1
    ...  Spam Detected  2
    ...  Marketing   0
    ...  Stopped by Content Filter  0
    ...  Clean   3

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Total Attempted Messages   6
    ...  Virus Detected   1
    ...  Spam Detected   2
    ...  Stopped by Content Filter  1
    ...  Clean Messages  2

    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Virus Detected   1
    ...  Spam Detected   2
    ...  Stopped by Content Filter  1
    ...  Clean  2

    Set Test Variable  @{expected_value3}

    @{expected_value4}=  Create List
    ...  Clean Messages   1
    ...  Clean Messages   1

    Set Test Variable  @{expected_value4}

    @{expected_value5}=  Create List
    ...  Virus   1
    Set Test Variable  @{expected_value5}

    @{expected_value6}=  Create List
    ...  Clean Messages  2
    Set Test Variable  @{expected_value6}

    @{expected_value7}=  Create List
    ...  Threat Messages   1
    ...  Threat Messages   1
    ...  Threat Messages   1

    Set Test Variable  @{expected_value7}

    @{expected_value8}=  Create List
    ...  Spam Detected   Virus Detected   Stopped by Content Filter
    ...  Marketing Messages  Clean Messages   Total Attempted Messages:
    ...  2   1   0   0   2   6
    Set Test Variable  @{expected_value8}

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  9  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    Set Test Variable  ${time_range}  last month
    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  30  cur_time=${first_day_of_curr_month}
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=30
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
        Email Scheduled Reports Add Report
        ...  ${sma_email_reports.INT_USERS}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=last month
        ...  schedule=daily:${hour_for_report}
        ...  email_to=user@${CLIENT}
       Commit Changes
       Set Time Set  ${time_to_set}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Verify Log Contains Records
       ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
       ...  timeout=180
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
       Email Scheduled Reports Delete Report  ${TEST_NAME}
       Commit Changes
    END

    FOR  ${index}  IN RANGE  0  8
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value8}
        Should Contain  ${out}  ${entry}
    END

Tvh663758c
    [Documentation]  Verify Outbreak Filters archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663758c
    [Tags]  erts  Tvh663758c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663499c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663499c
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh663758c

    @{mbox_listener_list}=  Create List
    ...  ${CLEAN}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM_SUSPECT}
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${MARKETING}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${VOFAUTO}  ${ESA_PUBLIC_LISTENER_IP}  ${VOFAUTO_MANUAL}
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${VOFMANUAL}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${CLEAN}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM_SUSPECT}
    ...  ${ESA_PRIVATE_LISTENER_IP}  ${MARKETING}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${VOFAUTO}  ${ESA_PRIVATE_LISTENER_IP}  ${VOFAUTO_MANUAL}
    ...  ${ESA_PRIVATE_LISTENER_IP}  ${VOFMANUAL}  ${ESA_PRIVATE_LISTENER_IP}

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

    Sync Appliances Datetime  ${SMA}  ${ESA}
    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${num_threats}  4
    Set Test Variable  ${non_threats}  4

    @{pattern}=  Create List
    ...  Type_custom_interval
    ...  ${TEST_ID}_Hit_Messages_from_Incoming
    ...  Threat_Summary_custom_interval
    ...  Details_custom_interval

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Threats Detected  ${num_threats}
    ...  Threat Type  Viral Attachment
    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Threats detected  ${non_threats}  Threats detected  0
    ...  Threats detected  ${num_threats}  Incoming messages
    ...  No Threat  Incoming messages  Other Threat
    ...  Incoming messages   Viral Attachment
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Total Messages  totals  Messages  4  Messages  4
    ...  Threat Category  Virus
    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Total Messages  ${num_threats}  Category  Virus
    ...  Threat Name  Viral Attachment
    Set Test Variable  @{expected_value3}

    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Threat Summary

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  9  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        Email Archived Reports Add Report
        ...  ${sma_email_reports.VOF}
        ...  title=${TEST_NAME}
        ...  report_format=${report}
        ...  email_to=testuser@${CLIENT_HOSTNAME}
        ${flag}=  Get From List  ${flg_list}  ${num}
        ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
        Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
        ${num}=  Evaluate  ${num} + 1
        Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
        Null Smtpd Stop
    END
    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    @{expected_value4}=  Create List
    ...  Threat Category   Virus  Messages  4   4
    ...  Threat Name  Viral Attachment
    Set Test Variable  @{expected_value4}

    FOR  ${entry}  IN  @{expected_value4}
        Should Contain  ${out}  ${entry}
    END

Tvh663233c
    [Documentation]  Verify Outbreak Filters schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663233c
    [Tags]  erts  Tvh663233c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663499c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663499c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh663233c

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Switch To ESA
    @{mbox_listener_list}=  Create List
    ...  ${CLEAN}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM_SUSPECT}
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${MARKETING}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${VOFAUTO}  ${ESA_PUBLIC_LISTENER_IP}  ${VOFAUTO_MANUAL}
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${VOFMANUAL}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${CLEAN}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM_SUSPECT}
    ...  ${ESA_PRIVATE_LISTENER_IP}  ${MARKETING}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${VOFAUTO}  ${ESA_PRIVATE_LISTENER_IP}  ${VOFAUTO_MANUAL}
    ...  ${ESA_PRIVATE_LISTENER_IP}  ${VOFMANUAL}  ${ESA_PRIVATE_LISTENER_IP}

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

    Sync Appliances Datetime  ${SMA}  ${ESA}

    Set Test Variable  ${num_threats}  4
    Set Test Variable  ${non_threats}  4

    @{pattern}=  Create List
    ...  Type_custom_interval
    ...  ${TEST_ID}_Hit_Messages_from_Incoming
    ...  Threat_Summary_custom_interval
    ...  Details_custom_interval


    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Threats Detected  ${num_threats}
    ...  Threat Type  Viral Attachment
    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Threats detected  ${non_threats}  Threats detected  0
    ...  Threats detected  ${num_threats}  Incoming messages
    ...  No Threat  Incoming messages  Other Threat
    ...  Incoming messages   Viral Attachment
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Total Messages  totals  Messages  4  Messages  4
    ...  Threat Category  Virus
    Set Test Variable  @{expected_value2}

    @{expected_value3}=  Create List
    ...  Total Messages  ${num_threats}  Category  Virus
    ...  Threat Name  Viral Attachment
    Set Test Variable  @{expected_value3}

    Set Appliance Under Test To SMA
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Threat Summary

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  9  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}


    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=1
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
        Email Scheduled Reports Add Report
        ...  ${sma_email_reports.VOF}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  schedule=daily:${hour_for_report}
        ...  email_to=user@${CLIENT}
        Commit Changes
        Set Time Set  ${time_to_set}
        ${flag}=  Get From List  ${flg_list}  ${num}
        ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
        Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
        ${num}=  Evaluate  ${num} + 1
        Verify Log Contains Records
        ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
        ...  timeout=180
        Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
        Null Smtpd Stop
        Email Scheduled Reports Delete Report  ${TEST_NAME}
        Commit Changes
    END
    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    @{expected_value4}=  Create List
    ...  Threat Category   Virus  Messages  4   4
    ...  Threat Name  Viral Attachment
    Set Test Variable  @{expected_value4}

    FOR  ${entry}  IN  @{expected_value4}
        Should Contain  ${out}  ${entry}
    END

Tvh664238c
    [Documentation]  Verify System Capacity archive report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664238c
    [Tags]  erts  Tvh664238c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    [Teardown]  Run Keywords
    ...  Common Cleanup For Archive Reports
    ...  General Test Case Teardown

    Switch To ESA
    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh664238c

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  365  cur_time=${first_day_of_curr_month}

    SmaCliLibrary.Set Time Set  ${datetime_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    @{listener_list}=  Create List
    ...  ${ESA_PUBLIC_LISTENER_IP}  ${ESA_PRIVATE_LISTENER_IP}

    FOR  ${listener}  IN  @{listener_list}
        Inject Messages
        ...  mail-from=${TEST_ID}@${CLIENT}
        ...  mbox-filename=${CLEAN}
        ...  num-msgs=${msg_count}
        ...  inject-host=${listener}
        ...  rcpt-host-list=${CLIENT}
        Deliver Now All
        Sleep  5s  Wait until messages will be delivered
    END

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  System Capacity
    Set Test Variable  ${range}  Year

    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    @{pattern}=  Create List
    ...  Average_Time_Spent
    ...  Average_Messages
    ...  Incoming_Connections
    ...  Incoming_Messages
    ...  Average_Incoming_Message_Size_(Bytes)
    ...  Total_Incoming_Message_Size_(Bytes)
    ...  Memory_Page

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Time  0.0
    Set Test Variable  @{expected_value0}
    @{expected_value1}=  Create List
    ...  Messages  0.0
    ...  Messages  0.0
    Set Test Variable  @{expected_value1}
    @{expected_value2}=  Create List
    ...  Connections  1
    Set Test Variable  @{expected_value2}
    @{expected_value3}=  Create List
    ...  Messages  1
    Set Test Variable  @{expected_value3}
    @{expected_value4}=  Create List
    ...  Message Size   134900.0
    Set Test Variable  @{expected_value4}
    @{expected_value5}=  Create List
    ...  Message Size   134900
    Set Test Variable  @{expected_value5}
    @{expected_value6}=  Create List
    ...  Pages Swapped   0.0
    ...  Pages Swapped   0.0
    Set Test Variable  @{expected_value6}

    Wait Until Keyword Succeeds  40m  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  14  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    FOR  ${report}  IN  @{report_type}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        Wait Until Keyword Succeeds  5m  20s
        ...  Email Archived Reports Add Report
        ...  ${sma_email_reports.SYSTEM_CAP}
        ...  title=${TEST_NAME}
        ...  report_format=${report}
        ...  time_range=last year
        ...  email_to=testuser@${CLIENT_HOSTNAME}
        ${flag}=  Get From List  ${flg_list}  ${num}
        ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
        Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
        ${num}=  Evaluate  ${num} + 1
        Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
        Null Smtpd Stop
    END

    FOR  ${index}  IN RANGE  0  7
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END

    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Replace String  ${out}  \\n  ${SPACE}
    Log  ${out}
    Remove File  ${path}

    @{expected_value7}=  Create List
    ...  Average Time Spent in Work Queue
    ...  Average Messages in Work Queue
    ...  Maximum Messages in Work Queue
    ...  Total Incoming Connections
    ...  Total Incoming Messages
    ...  Average Incoming Message Size
    ...  Total Incoming Message Size
    ...  Total Outgoing Connections
    ...  Total Outgoing Messages
    ...  Average Outgoing Message Size
    ...  Total Outgoing Message Size
    ...  Overall CPU Usage
    ...  CPU by Function
    ...  Memory Page Swapping
    Set Test Variable  @{expected_value7}

    FOR  ${entry}  IN  @{expected_value7}
        Should Contain  ${out}  ${entry}
    END

Tvh663827c
    [Documentation]  Verify Content Filters schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663827c
    [Tags]  erts  Tvh663827c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664000c
    [Teardown]  Run Keywords
    ...  Finalize Tvh664000c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh663827c
    Set Test Variable  ${msg_count}  1

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  150  cur_time=${first_day_of_curr_month}

    SmaCliLibrary.Set Time Set  ${datetime_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Inject Messages For Content Filters Report

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Content Filters
    Set Test Variable  ${range}  Year

    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    Sleep  40s  Wait till the message delivered
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    @{pattern}=  Create List
    ...  ${TEST_ID}_Top_Incoming
    ...  ${TEST_ID}_Top_Outgoing
    ...  ${TEST_ID}_Incoming
    ...  ${TEST_ID}_Outgoing

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Messages  3
    ...  Messages  1
    ...  Content Filter  myFilter1
    ...  Content Filter  myFilter2

    Set Test Variable  @{expected_value0}
    @{expected_value1}=  Copy List  ${expected_Value0}
    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Messages  3
    ...  Messages  1
    ...  Messages  4
    ...  Content Filter  myFilter1
    ...  Content Filter  myFilter2
    Set Test Variable  @{expected_value2}
    @{expected_value3}=  Copy List  ${expected_value2}
    Set Test Variable  @{expected_value3}

    @{expected_value4}=  Copy List  ${expected_value2}
    Set Test Variable  @{expected_value4}

    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  4  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    Set Test Variable  ${time_range}  num months:5
    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  150  cur_time=${first_day_of_curr_month}
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=150
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
        Email Scheduled Reports Add Report
        ...  ${sma_email_reports.FILTERS}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=num months:5
        ...  schedule=monthly:${hour_for_report}
        ...  email_to=user@${CLIENT}
       Commit Changes
       Set Time Set  ${time_to_set}
       ${flag}=  Get From List  ${flg_list}  ${num}
       ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
       Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
       ${num}=  Evaluate  ${num} + 1
       Verify Log Contains Records
       ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
       ...  timeout=180
       Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
       Null Smtpd Stop
       Email Scheduled Reports Delete Report  ${TEST_NAME}
       Commit Changes
    END
    FOR  ${index}  IN RANGE  0  4
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Split String  ${out}  \\n
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value4}
        Should Contain  ${out}  ${entry}
    END

Tvh664062c
    [Documentation]  Verify Sender Groups schedule report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664062c
    [Tags]  erts  Tvh664062c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664000c
    [Teardown]  Run Keywords
    ...  Finalize Tvh664000c
    ...  Common Cleanup For Schedule Reports
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh664062c
    Set Test Variable  ${msg_count}  1

    ${first_day_of_curr_month_to_set}=  Run On DUT  date +'%m/1/%Y %H:%M:%S'
    ${first_day_of_curr_month}=  Run On DUT  date +'%a %b 1 %H:%M:%S %Y %Z'
    EsaCliLibrary.Set Time  ${first_day_of_curr_month_to_set}
    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    ${datetime_to_set}=  Calculate Shifted Datetime
    ...  210  cur_time=${first_day_of_curr_month}

    SmaCliLibrary.Set Time Set  ${datetime_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Inject Messages For Content Filters Report

    Switch To SMA
    Smtp Routes New  .${NETWORK}  ${CLIENT_HOSTNAME}
    Commit

    Set Test Variable  ${type}  Sender Groups
    Set Test Variable  ${range}  Year

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    Sleep  40s  Wait till message delivered

    SmaCliLibrary.Set Time Set  ${first_day_of_curr_month_to_set}
    Sync Appliances Datetime  ${SMA}  ${ESA}

    @{pattern}=  Create List
    ...  Sender_Group
    ...  Mail_Flow

    Set Test Variable  @{pattern}

    @{expected_value0}=  Create List
    ...  Total Connections  7
    ...  Sender Group  UNKNOWNLIST
    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Create List
    ...  Relay  0
    ...  TCP Refuse  0
    ...  Accept  7
    ...  Reject  0

    Set Test Variable  @{expected_value1}

    @{expected_value2}=  Create List
    ...  Sender Group  UNKNOWNLIST
    ...  Accept (100.0%)   7
    ...  Total Incoming Connections:  7

    Set Test Variable  @{expected_value2}

    Switch To SMA
    Run Keyword And Ignore Error  Log Into DUT
    Navigate To  Email  Reporting  ${type}
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  SMA Should Contain ${type} Chart For ${range}

    @{report_type}=  Create List  csv  pdf
    @{flg_list}=  Create List  0  1
    @{count_list}=  Create List  2  1
    Set Test Variable  ${num}  0
    ${num}=  Convert To Integer  ${num}

    Set Test Variable  ${time_range}  num months:7
    FOR  ${report}  IN  @{report_type}
        Run Keyword And Ignore Error  Email Archived Reports Delete All Reports
        ${datetime_to_set}=  Calculate Shifted Datetime
        ...  210  cur_time=${first_day_of_curr_month}
        SmaCliLibrary.Set Time Set  ${datetime_to_set}
        Clean Up Delivery Queue
        Roll Over Now  mail_logs
        Null Smtpd Start  bind-ip=${CLIENT_IP}
        ${current_time}=  Set Time Get
        ${datetime_offset}=  Get Date Time Offset  ${current_time}  offset_days=210
        ${hour_for_report}=  Set Variable  ${datetime_offset[11:13]}:15
        ${time_to_set}=  Set Variable  ${datetime_offset[:14]}13:00
        Email Scheduled Reports Add Report
        ...  ${sma_email_reports.SENDER_GROUPS}
        ...  title=${TEST_ID}
        ...  report_format=${report}
        ...  time_range=num months:7
        ...  schedule=monthly:${hour_for_report}
        ...  email_to=user@${CLIENT}
        ...  num_of_rows=20
        Commit Changes
        Set Time Set  ${time_to_set}
        ${flag}=  Get From List  ${flg_list}  ${num}
        ${ARCHIVED_CSV_REPORT_MAILS_COUNT}=  Get From List  ${count_list}  ${num}
        Set suite variable  ${ARCHIVED_CSV_REPORT_MAILS_COUNT}
        ${num}=  Evaluate  ${num} + 1
        Verify Log Contains Records
        ...  MID .* From: .reporting@${SMA}. To: .user@${CLIENT}. >= 1
        ...  timeout=180
        Process Archived Mails And Extract CSV Reports Into ${SUITE_TMP_DIR}
        Null Smtpd Stop
        Email Scheduled Reports Delete Report  ${TEST_NAME}
        Commit Changes
    END
    FOR  ${index}  IN RANGE  0  2
        ${file_pattern}=  Get From List  ${pattern}  ${index}
        Log  ${file_pattern}
        Find And Verify CSV Report  ${SUITE_TMP_DIR}  *${file_pattern}*
        ...  @{expected_value${index}}
    END
    ${start_time}=  Get Time
    Navigate To  Email  Reporting  Archived Reports
    Click Element  xpath=//a[contains(text(),'${TEST_NAME}')]  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}

    ${out}=  Run  ${PDF2TXT_PATH} ${path}
    ${out}=  Split String  ${out}  \\n
    Log  ${out}
    Remove File  ${path}

    FOR  ${entry}  IN  @{expected_value2}
        Should Contain  ${out}  ${entry}
    END

Tvh663974c
    [Documentation]  Verify that the report contains the proper data
    ...  (and percentage) in case of several domains\n
    ...  http://tims.cisco.com/view-entity.cmd?tab=g_&ent=663974
    [Tags]  Tvh663974c  srts  wsrts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh663974c

    @{time_periods}=  Create List  Day  Week  30 days  Year
    ${msgs_count}=  Set Variable  10

    Switch To ESA
    ${fname}=  Prepare TXT File With Domain IP  ${CLIENT_IP}
    Smtp Session Spoof Enable  ${PUBLIC_LISTENER.name}  ${fname}
    Generate Email Reporting Data
    ...  rcpt-host-list=${CLIENT}
    ...  inject-host=${PUBLIC_LISTENER.ipv4}
    ...  ${CLEAN}=${msgs_count}

    Switch To SMA
    FOR  ${time_period}  IN  @{time_periods}
      ${table_params}=  Email Report Table Create Parameters
      ...  Incoming Mail Details
      ...  period=${time_period}
      ${reporting_data}=  Wait Until Keyword Succeeds
      ...  ${DATA_UPDATE_TIMEOUT}
      ...  10 sec
      ...  Email Report Table Get Data
          ...  Incoming Mail Details
          ...  ${table_params}
      Log  ${reporting_data}
      List Should Contain Value  ${reporting_data['Sender Domain']}  ${CLIENT}
      
      # To be checked if it is 'Total Attempted' or 'Connections Accepted'
      List Should Contain Value  ${reporting_data['Total Attempted']}  ${msgs_count}
    END
    Smtp Session Spoof Disable

Tvh662978c
    [Documentation]  When some e-mail groups are configured and
    ...  ungrouped appliances Verify Incoming
    ...  Mail: Domains page can be viewed for All Email Appliances\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662978c
    [Tags]  srts  Tvh662978c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662978c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662978c
    ...  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662978c
    Set Appliance Under Test To SMA
    Close All Browsers
    Selenium Close
    Selenium Login
    Navigate To  Email  Reporting  Incoming Mail
    Page Should Contain Element  //option[contains(text(),'All Email Appliances')]
