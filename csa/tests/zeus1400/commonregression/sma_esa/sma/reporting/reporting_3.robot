# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/reporting/reporting_3.txt#9 $
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
${firefox_prefs_browser.download.dir}=                          %{SARF_HOME}/tmp
${firefox_prefs_browser.download.folderList}=                   2
${firefox_prefs_browser.download.manager.showWhenStarting}=     false
${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=        application/pdf,text/csv
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
 	Select Window  MAIN
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
        Sleep  10s
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
    Run Keyword And Ignore Error  Start CLI Session If Not Open
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
    Run Keyword And Ignore Error  Start CLI Session If Not Open
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
    Switch To ESA
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

Tvh663254c
    [Documentation]  Verify export functionality for Virus Types Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663254c
    [Tags]  srts  Tvh663254c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663254c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663254c
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh663254c
    Set Test Variable  ${type}  Virus Types

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

    @{expected_value0}=  Create List
    ...  Messages   1
    ...  Virus Type    EICAR-AV-Test

    Set Test Variable  @{expected_value0}

    @{expected_value1}=  Copy List  ${expected_value0}
    Set Test Variable  @{expected_value1}

    @{expected_table_detail}=  Create List
    ...  Incoming Messages  1
    ...  Total Infected Messages  2
    ...  Outgoing Messages  1
    ...  Virus Type  EICAR-AV-Test

    Set Test Variable  @{expected_table_detail}

    Set Appliance Under Test To SMA
    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        ${table_params}=  Email Report Table Create Parameters
        ...  Virus Types Detail
        ...  period=${range}
        ${reporting_data}=  Wait Until Keyword Succeeds
        ...  ${DATA_UPDATE_TIMEOUT}
        ...  10 sec
        ...  Email Report Table Get Data
          ...  Virus Types Detail
          ...  ${table_params}
        Run Keyword And Ignore Error  Start CLI Session If Not Open
        Verify Export Data For Charts
        @{expected_value}=  Create List
        ...  @{expected_table_detail}
        Set Suite variable  @{expected_value}
        Set Test Variable  ${table_name}  Virus Types Detail
        Verify Export Data For Table ${table_name}
    END

Tvh662871c
    [Documentation]  Verify export functionality for Incoming Mail Summary Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662871c
    [Tags]  srts  Tvh662871c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662871c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662871c
    ...  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh662871c
    Set Test Variable  ${msg_count}  10

    Inject Messages For Incoming Mail Report

    @{range_list}=  Create List
    ...  Day
    ...  Week

    @{chart_ids}=  Create List
    ...  ss_0_0_0-links  ss_0_0_1-links

    Set Test Variable  @{chart_ids}

    @{pattern}=  Create List
    ...  Threat
    ...  Clean

    Set Test Variable  @{pattern}
    Set Test Variable  ${num_threats}  50
    Set Test Variable  ${num_clean}  31
    Set Test Variable  ${type}  Incoming Mail

    @{expected_table_detail}=  Create List
    ...  Clean            31
    ...  Spam Detected    20
    ...  Total Threat     50
    ...  Total Attempted   81
    ...  Connections Accepted  81
    ...  Stopped by Reputation Filtering  9
    ...  Stopped as Invalid Recipients  1
    ...  Stopped by Content Filter  10
    ...  Virus Detected  10
    ...  Marketing  0

    Set Test Variable  @{expected_table_detail}

    Set Appliance Under Test To SMA

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        ${table_params}=  Email Report Table Create Parameters
        ...  Incoming Mail Details
        ...  period=${range}
        ${reporting_data}=  Wait Until Keyword Succeeds
        ...  ${DATA_UPDATE_TIMEOUT}
        ...  10 sec
        ...  Email Report Table Get Data
          ...  Incoming Mail Details
          ...  ${table_params}
        @{expected_value0}=  Create List
        ...  Messages  ${num_threats}
        @{expected_value1}=  Create List
        ...  Messages  ${num_clean}
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
        Verify Export Data For Charts
        @{expected_value}=  Create List
        ...  @{expected_table_detail}
        Set Suite variable  @{expected_value}
        Set Test Variable  ${table_name}  Incoming Mail Details
        Verify Export Data For Table ${table_name}
    END

Tvh662817c
    [Documentation]  Verify export functionality for Outgoing Senders Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662817c
    [Tags]  srts  Tvh662817c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662817c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662817c
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh662817c

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
    @{range_list}=  Create List
    ...  Day
    ...  Week

    @{chart_ids}=  Create List
    ...  ss_0_0_0-links  ss_0_0_1-links

    Set Test Variable  @{chart_ids}

    @{pattern}=  Create List
    ...  Threat
    ...  Clean

    Set Test Variable  @{pattern}
    Set Test Variable  ${num_threats}  4
    Set Test Variable  ${num_clean}  2
    Set Test Variable  ${type}  Outgoing Senders

    @{expected_table_detail}=  Create List
    ...  Clean            2
    ...  Spam Detected    2
    ...  Total Threat     4
    ...  Total Messages  6
    ...  Stopped by Content Filter  1
    ...  Virus Detected  1

    Set Test Variable  @{expected_table_detail}

    Set Appliance Under Test To SMA

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        ${table_params}=  Email Report Table Create Parameters
        ...  Sender Details
        ...  period=${range}
        ${reporting_data}=  Wait Until Keyword Succeeds
        ...  ${DATA_UPDATE_TIMEOUT}
        ...  10 sec
        ...  Email Report Table Get Data
          ...  Sender Details
          ...  ${table_params}
        @{expected_value0}=  Create List
        ...  Threat Messages  ${num_threats}
        @{expected_value1}=  Create List
        ...  Clean Messages  ${num_clean}
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
        Run Keyword And Ignore Error  Start CLI Session If Not Open
        Verify Export Data For Charts
        @{expected_value}=  Create List
        ...  @{expected_table_detail}
        Set Suite variable  @{expected_value}
        Set Test Variable  ${table_name}  Sender Details
        Verify Export Data For Table ${table_name}
    END

Tvh663352c
    [Documentation]  Verify export functionality for Outgoing Destinations Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663352c
    [Tags]  srts  Tvh663352c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh662817c
    [Teardown]  Run Keywords
    ...  Finalize Tvh662817c
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh663352c

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

    @{range_list}=  Create List
    ...  Day
    ...  Week

    @{chart_ids}=  Create List
    ...  ss_0_0_0-links  ss_0_0_1-links

    Set Test Variable  @{chart_ids}

    @{pattern}=  Create List
    ...  Threat
    ...  Clean

    Set Test Variable  @{pattern}
    Set Test Variable  ${num_threats}  4
    Set Test Variable  ${num_clean}  2
    Set Test Variable  ${type}  Outgoing Destinations

    @{expected_table_detail}=  Create List
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

    Set Test Variable  @{expected_table_detail}

    Set Appliance Under Test To SMA

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
        ...  SMA Should Contain ${type} Chart For ${range}
        @{expected_value0}=  Create List
        ...  Threat Messages  ${num_threats}
        ...  Domain  ${CLIENT}
        @{expected_value1}=  Create List
        ...  Clean Messages  ${num_clean}
        ...  Domain  ${CLIENT}
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
        Verify Export Data For Charts
        @{expected_value}=  Create List
        ...  @{expected_table_detail}
        Set Suite variable  @{expected_value}
        Set Test Variable  ${table_name}  Outgoing Destinations Detail
        Verify Export Data For Table ${table_name}
    END

Tvh664000c
    [Documentation]  Verify export functionality for Content Filters Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664000c
    [Tags]  srts  Tvh664000c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664000c
    [Teardown]  Run Keywords
    ...  Finalize Tvh664000c
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh664000c

    Inject Messages For Content Filters Report

    @{range_list}=  Create List
    ...  Day
    ...  30 days

    @{chart_ids}=  Create List
    ...  ss_0_0_0-links  ss_0_0_1-links  ss_0_1_0-links  ss_0_1_1-links

    Set Test Variable  @{chart_ids}

    @{pattern}=  Create List
    ...  Filters_Top_Incoming
    ...  Filters_Top_Outgoing
    ...  Filters_Incoming
    ...  Filters_Outgoing

    Set Test Variable  @{pattern}

    Set Test Variable  ${type}  Content Filters

    Set Appliance Under Test To SMA

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
        ...  SMA Should Contain ${type} Chart For ${range}
        @{expected_value0}=  Create List
        ...  Messages  3
        ...  Messages  1
        ...  Content Filter  myFilter1
        ...  Content Filter  myFilter2
        @{expected_value1}=  Copy List  ${expected_value0}
        @{expected_value2}=  Copy List  ${expected_value0}
        @{expected_value3}=  Copy List  ${expected_value0}
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
        Set Test Variable  @{expected_value2}
        Set Test Variable  @{expected_value3}
        Verify Export Data For Charts
    END

Tvh663499c
    [Documentation]  Verify export functionality for Outbreak Filters Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663499c
    [Tags]  srts  Tvh663499c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663499c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663499c
    ...  General Test Case Teardown

    Set Test Variable  ${msg_count}  1
    Set Test Variable  ${TEST_ID}  Tvh663499c

    @{mbox_listener_list}=  Create List
    ...  ${CLEAN}  ${ESA_PUBLIC_LISTENER_IP}  ${SPAM}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${SPAM_SUSPECT}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MARKETING}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${VOFAUTO}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${VOFAUTO_MANUAL}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${VOFMANUAL}  ${ESA_PUBLIC_LISTENER_IP}
    ...  ${CLEAN}  ${ESA_PRIVATE_LISTENER_IP}  ${SPAM}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${FLASHPLA_EXE}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${SPAM_SUSPECT}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MARKETING}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${MSOFFICEDOCATTACH}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${VOFAUTO}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${VOFAUTO_MANUAL}  ${ESA_PRIVATE_LISTENER_IP}
    ...  ${VOFMANUAL}  ${ESA_PRIVATE_LISTENER_IP}

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
    @{chart_ids}=  Create List
    ...  ss_0_0_0-links  ss_0_4_0-links  ss_0_5_0-links

    Set Test Variable  @{chart_ids}

    @{pattern}=  Create List
    ...  Filters_Threats_by_Type
    ...  Hit_Messages_from_Incoming
    ...  Hit_Messages_by_Threat

    Set Test Variable  @{pattern}
    Set Test Variable  ${num_threats}  4
    Set Test Variable  ${non_threats}  4

    @{expected_table_detail1}=  Create List
    ...  Messages        ${num_threats}
    ...  Threat Category    Virus

    Set Test Variable  @{expected_table_detail1}

    @{expected_table_detail2}=  Create List
    ...  Total Messages        ${num_threats}
    ...  Category    Virus
    ...  Threat Name    Viral Attachment

    Set Test Variable  ${type}  Outbreak Filters

    Set Appliance Under Test To SMA

    Set Test Variable  ${num}  0
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Threat Summary
    @{expected_value0}=  Create List
    ...  Threats Detected  ${num_threats}
    ...  Threat Type  Viral Attachment
    @{expected_value1}=  Create List
    ...  Incoming messages  No Threat
    ...  Incoming messages  Viral Attachment
    ...  Threats detected  ${non_threats}
    ...  Threats detected  ${num_threats}
    @{expected_value2}=  Create List
    ...  Threat Level  ${num_threats}
    ...  Messages   ${num_threats}
    Set Test Variable  @{expected_value0}
    Set Test Variable  @{expected_value1}
    Set Test Variable  @{expected_value2}
    Verify Export Data For Charts
    @{expected_value}=  Create List
    ...  @{expected_table_detail1}
    Set Suite variable  @{expected_value}
    Set Test Variable  ${table_name}  Threat Summary
    Verify Export Data For Table ${table_name}
    @{expected_value}=  Create List
    ...  @{expected_table_detail2}
    Set Suite variable  @{expected_value}
    Set Test Variable  ${table_name}  Threat Details
    Verify Export Data For Table ${table_name}

Tvh664017c
    [Documentation]  Verify export functionality for System Capacity Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664017c
    [Tags]  srts  Tvh664017c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh664017c
    [Teardown]  Run Keywords
    ...  General Test Case Teardown

    @{range_list}=  Create List
    ...  Day
    ...  90 days

    Set Test Variable  @{range_list}

    @{chart_ids_common}=  Create List
    ...  ss_0_0_0-links  ss_0_1_0-links  ss_0_2_0-links

    @{chart_ids_inout}=   Create List
    ...  ss_0_0_0-links  ss_0_1_0-links  ss_0_2_0-links  ss_0_3_0-links

    Set Test Variable  @{chart_ids_common}
    Set Test Variable  @{chart_ids_inout}

    @{pattern}=  Create List
    ...  Average_Time_Spent
    ...  Average_Messages
    ...  Maximum_Messages
    ...  Incoming_Connections
    ...  Incoming_Messages
    ...  Incoming_Message_Size
    ...  Incoming_Message_Size_Bytes
    ...  Outgoing_Connections
    ...  Outgoing_Messages
    ...  Outgoing_Message_Size
    ...  Outgoing_Message_Size_Bytes
    ...  Overall_CPU_Usage
    ...  CPU_by_Function
    ...  Memory_Page

    Set Test Variable  @{pattern}

    Set Test Variable  ${type}  System Capacity
    @{expected_value0}=  Create List
    ...  Time  0.0
    Set Test Variable  @{expected_value0}
    @{expected_value1}=  Create List
    ...  Messages  0.0
    ...  Messages  0.0
    Set Test Variable  @{expected_value1}
    @{expected_value3}=  Create List
    ...  Connections  1
    Set Test Variable  @{expected_value3}
    @{expected_value4}=  Create List
    ...  Messages  1
    Set Test Variable  @{expected_value4}
    @{expected_value5}=  Create List
    ...  Message Size   134900.0
    Set Test Variable  @{expected_value5}
    @{expected_value6}=  Create List
    ...  Message Size   134900
    Set Test Variable  @{expected_value6}
    @{expected_value13}=  Create List
    ...  Pages Swapped   0.0
    ...  Pages Swapped   0.0
    Set Test Variable  @{expected_value13}

    Set Appliance Under Test To SMA

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        Wait Until Keyword Succeeds  40m  ${RETRY_TIME}
        ...  SMA Should Contain ${type} Chart For ${range}
        Navigate To  Email  Reporting  ${type}
        Select From List  xpath=//select[@id='date_range']  ${range}
        @{chart_ids}=  Copy List  ${chart_ids_common}
        Set Test Variable  @{chart_ids}
        Verify Export Data For Charts
        Click Link  xpath=//div/a[text() = 'Incoming Mail']
        Wait Until Page Loaded  timeout=180
        @{chart_ids}=  Copy List  ${chart_ids_inout}
        Set Test Variable  ${num}  3
        Verify Export Data For Charts
        Click Link  xpath=//div/a[text() = 'Outgoing Mail']
        Wait Until Page Loaded  timeout=180
        Set Test Variable  ${num}  7
        Verify Export Data For Charts
        Click Link  xpath=//div/a[text() = 'System Load']
        Wait Until Page Loaded  timeout=180
        @{chart_ids}=  Copy List  ${chart_ids_common}
        Set Test Variable  ${num}  11
        Verify Export Data For Charts
    END

Tvh663925c
    [Documentation]  Verify export functionality for DLP Incidents Report\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh663925c
    [Tags]  srts  Tvh663925c  wsrts
    [Setup]  Run Keywords
    ...  General Test Case Setup
    ...  Initialize Tvh663925c
    [Teardown]  Run Keywords
    ...  Finalize Tvh663925c
    ...  General Test Case Teardown

    @{range_list}=  Create List
    ...  Day
    ...  Year

    @{chart_ids}=  Create List
    ...  ss_0_0_0-links  ss_0_0_1-links

    Set Test Variable  @{chart_ids}

    @{pattern}=  Create List
    ...  Top_Incidents_by_Severity
    ...  DLP_Incident_Summary

    Set Test Variable  @{pattern}
    Set Test Variable  ${type}  DLP Incidents

    @{expected_table_detail}=  Create List
    ...  DLP Policy         DLP_POLICY_0
    ...  Dropped    0
    ...  High     0
  ...  Medium   20
    ...  Low   0
    ...  Critical  0
    ...  Total  20
    ...  Delivered (encrypted)   0
    ...  Delivered (clear)   20

    Set Test Variable  @{expected_table_detail}

    Set Appliance Under Test To SMA

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        ${table_params}=  Email Report Table Create Parameters
        ...  DLP Incident Details
        ...  period=${range}
        ${reporting_data}=  Wait Until Keyword Succeeds
        ...  ${DATA_UPDATE_TIMEOUT}
        ...  10 sec
        ...  Email Report Table Get Data
          ...  DLP Incident Details
          ...  ${table_params}
        @{expected_value0}=  Create List
        ...  High   0
        ...  Critical   0
        ...  Medium   20
        ...  Low    0
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
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
        Verify Export Data For Charts
        @{expected_value}=  Create List
        ...  @{expected_table_detail}
        Set Suite variable  @{expected_value}
        Set Test Variable  ${table_name}  DLP Incident Details
        Verify Export Data For Table ${table_name}
    END
