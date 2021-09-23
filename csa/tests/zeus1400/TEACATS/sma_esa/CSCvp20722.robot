*** Settings ***
Resource          sma/global_sma.txt
Resource          regression.txt
Resource          esa/global.txt
Resource          esa/logs_parsing_snippets.txt
Resource          esa/backdoor_snippets.txt
Resource          sma/esasma.txt

Suite Setup   Do Suite Setup
Suite Teardown   Do Suite Teardown

*** Variables ***
${firefox_prefs_browser.download.dir}=                          %{SARF_HOME}/tmp
${firefox_prefs_browser.download.folderList}=                   2
${firefox_prefs_browser.download.manager.showWhenStarting}=     false
${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=        application/pdf,text/csv,application/csv

*** Keywords ***
Do Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup
    ...  should_revert_to_initial=${False}
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup
    ${fpath}=  Catenate  SEPARATOR=/  %{SARF_HOME}  tmp
    Set Suite Variable  ${fpath}

Do Suite Teardown
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteTeardown
    Set Appliance Under Test to SMA
    Selenium Login
    Execute JavaScript  window.focus()
    Security Appliances Delete Email Appliance  ${ESA}
    Commit Changes
    global_sma.DefaultTestSuiteTeardown

Prepare Spam Quarantine On ESA
    Login To WebUI  ESA
    Clean System Quarantines
    Quarantines Spam Disable
    Enable EUQ On ESA

Login To WebUI
    [Arguments]  ${dut}
    Set Appliance Under Test to ${dut}
    Selenium Close
    Selenium Login

Enable EUQ On ESA
    [Arguments]  ${commit}=${True}
    Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    Run Keyword If  ${commit}  Commit Changes

Enable Spam Quarantine On SMA
    [Arguments]  ${commit}=${True}
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    Run Keyword If  ${commit}  Commit Changes

Add ESA to SMA
    [Arguments]  ${commit}=${True}
    Centralized Email Reporting Enable
    ${res}=  Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  reporting=${True}
    ...  isq=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Log  ${res}
    Run Keyword If  ${commit}  Commit Changes

Inject High Volume Mails
    FOR  ${index}  IN RANGE  2
        Generate Email Reporting Data
        ...  rcpt-host-list=${CLIENT}
        ...  inject-host=${ESA_PUB_LISTENER_IP}
        ...  ${SPAM}=10
        ...  ${CLEAN}=10
        ...  ${TESTVIRUS}=10
        ...  ${MARKETING}=10
        ...  ${SPAM_SUSPECT}=10
    END

General Test Case Teardown
    @{files}=  OperatingSystem.List Files In Directory  ${fpath}  *.csv  absolute
    Log  ${files}

    ${len_files}=  Get Length  ${files}
    Run Keyword If  '${len_files}' != '0'
    ...  Cleanup Files  @{files}

Cleanup Files
   [Arguments]  @{files}
   FOR  ${file}  IN  @{files}
      Remove File  ${file}
   END

Add IMS And GrayMail Feature Key
    ${gm_unsubscription_fkey}=  Generate DUT Feature Key  gm_unsubscription
    Start Cli Session If Not Open
    Feature Key Activate  ${gm_unsubscription_fkey}
    Restart CLI Session
    Feature Key Set Key  ims

Find And Verify CSV Report
    [Arguments]  ${dir}  ${file_pattern}  @{key_value_pairs}
    ${file_names}=  OperatingSystem.List Files In Directory
    ...  ${dir}  ${file_pattern}
    Log  ${file_names}
    ${csv_report_file_path}=  OperatingSystem.Join Path
    ...  ${dir}  ${file_names[0]}
    ${csv_data}=  Csv Parser Get Data  ${csv_report_file_path}
    Log  ${csv_data}
    ${key}=  Get From List  ${key_value_pairs}  0
    ${value}=  Get Slice From List  ${key_value_pairs}  1
    Lists Should Be Equal  ${csv_data['${key}']}  ${value}

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
             ...  download_directory=${fpath}
        Set Test Variable  ${path}
        Log  ${path}
        ${file_pattern}=  Get From List  ${pattern}  ${num}
        Log  ${file_pattern}
        ${index}=  Get Index From List  ${files_skipped}  ${file_pattern}
        Log  ${index}
        Run Keyword If  '${index}'=='-1'
        ...  Find And Verify CSV Report  ${fpath}  *${file_pattern}*
             ...  @{expected_value${num}}
        Remove File  ${path}
        ${num}=  Evaluate  ${num} + 1
    END

*** Test Cases ***

CSCvp20722
    [Documentation]
    ...  1. Attach ESA to SMA
    ...  2. Send High Volume Mails
    ...  3. Verify mail count is properly displayed in csv reports
    [Tags]  srts  teacat  CSCvp20722
    [Teardown]  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh1231019c
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    Set Appliance Under Test to ESA
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Add IMS And GrayMail Feature Key
    Login To WebUI  ESA
    Centralized Email Reporting Enable
    Commit Changes
    Diagnostic Reporting Delete DB  confirm=yes
    Diagnostic Tracking Delete DB  confirm=yes
    Prepare Spam Quarantine On ESA
    Login To WebUI  SMA
    Enable Spam Quarantine On SMA  commit=${False}
    Diagnostic Reporting Delete DB  confirm=yes
    Diagnostic Tracking Delete DB  confirm=yes
    Add ESA to SMA
    Roll Over Now  euq_logs
    Run Keyword if   '${ESA_LIB_VERSION}' >= 'phoebe1210'
    ...  IMS and Graymail Graymail Enable
    ...  enable_unsubscription=${False}
    Run Keyword if   '${ESA_LIB_VERSION}' < 'phoebe1210'
    ...  Graymail Enable  enable_unsubscription=${True}
    ${gm_settings}=  Create Dictionary
    ...  Graymail Detection                     Use Graymail Detection
    ...  Enable Marketing Email Scanning        ${True}
    ...  Marketing Email Apply Action           Deliver
    ...  Marketing Email Alternate Host         ${CLIENT_IP}
    ...  Marketing Email Subject Text Action    Prepend
    ...  Marketing Email Add Subject Text       [MARKETING]
    Mail Policies Edit Graymail
    ...  incoming  default  ${gm_settings}
    EsaGuiLibrary.Commit Changes
    Inject High Volume Mails
    Sleep  10s

    @{range_list}=  Create List
    ...  Day
    ...  Week

    @{chart_ids}=  Create List
    ...  ss_0_0_0-links  ss_0_0_1-links  ss_0_1_0-links

    Set Test Variable  @{chart_ids}

    @{pattern}=  Create List
    ...  Threat
    ...  Clean
    ...  Graymail

    Set Test Variable  @{pattern}
    Set Test Variable  ${num_threats}  60
    Set Test Variable  ${num_clean}    20
    Set Test Variable  ${num_market}   20
    Set Test Variable  ${type}  Incoming Mail

    Set Appliance Under Test To SMA

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        ${table_params}=  Email Report Table Create Parameters
        ...  Incoming Mail Details
        ...  period=${range}
        ${reporting_data}=  Wait Until Keyword Succeeds
        ...  30 min
        ...  10 sec
        ...  Email Report Table Get Data
          ...  Incoming Mail Details
          ...  ${table_params}
        @{expected_value0}=  Create List
        ...  Messages  ${num_threats}
        @{expected_value1}=  Create List
        ...  Messages  ${num_clean}
        @{expected_value2}=  Create List
        ...  Messages  ${num_market}
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
        Set Test Variable  @{expected_value2}
        Verify Export Data For Charts
    END
    Navigate To  Email  Reporting  High Volume Mail
    @{chart_ids}=  Create List
    ...  ss_0_0_0-links

    @{pattern}=  Create List
    ...  Top_Subjects_RawData

    @{mail_count}=  Create List
    ...   20  20  20  20  20
    Set Test Variable  @{mail_count}

    @{top_subjects}=  Create List
    ...  clean image  marketing email  real virus in rar file in attachment  spam  suspectspam
    Set Test Variable  @{top_subjects}

    FOR  ${range}  IN  @{range_list}
        Set Test Variable  ${num}  0
        Set Test Variable  ${range}
        @{expected_value0}=  Create List
        ...  Messages  @{mail_count}
        @{expected_value1}=  Create List
        ...  Top Subjects  @{top_subjects}
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
        Verify Export Data For Charts
    END
    @{chart_ids}=  Create List
    ...  ss_0_1_0-links

    @{pattern}=  Create List
    ...  Top_Envelope_Senders

    FOR  ${range}  IN  @{range_list}
        @{expected_value0}=  Create List
        ...  Messages  100
        @{expected_value1}=  Create List
        ...  Sender  user123@${Client}
        Set Test Variable  @{expected_value0}
        Set Test Variable  @{expected_value1}
        Verify Export Data For Charts
    END