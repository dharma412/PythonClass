*** Settings ***
Resource     esa/injector.txt
Resource     regression.txt
Resource     esa/logs_parsing_snippets.txt

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Initialize Suite
Suite Teardown  Finalize Suite

*** Variables ***
${DATA_UPDATE_TIMEOUT}=  20m
${RETRY_TIME}=  15s
${firefox_prefs_browser.download.dir}=                          %{SARF_HOME}/tmp
${firefox_prefs_browser.download.folderList}=                   2
${firefox_prefs_browser.download.manager.showWhenStarting}=     false
${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=        application/pdf,text/csv,application/csv

*** Keywords ***
Initialize Suite
    Set Appliance Under Test To ESA
    global.DefaultTestSuiteSetup  should_revert_to_initial=${False}
    Smtp Routes New  domain=ALL  dest_hosts=/dev/null
    Commit
    Diagnostic Tracking Delete Db  confirm=yes
    Message Tracking Enable  tracking=centralized
    Commit Changes

    Set Appliance Under Test To SMA
    global_sma.DefaultTestSuiteSetup
    Diagnostic Tracking Delete Db  confirm=yes
    Centralized Email Message Tracking Enable
    Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes

    ${PUBLIC_LISTENER_IP}=  Get ESA Public IP
    ${PRIVATE_LISTENER_IP} =  Get ESA Private IP
    Set Suite Variable  ${PUBLIC_LISTENER_IP}
    Set Suite Variable  ${PRIVATE_LISTENER_IP}
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${PUBLIC_LISTENER}
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp(dir="%{SARF_HOME}/tmp")  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}

Finalize Suite
    Switch To ESA
    Log Out Of Dut
    Close Browser
    Launch Dut Browser
    Log Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Smtp Routes Clear All  confirm=True
    Message Tracking Disable
    Commit Changes
    global.DefaultTestSuiteTeardown

    Switch To SMA
    Log Out Of Dut
    Close Browser
    Launch Dut Browser
    Log Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Security Appliances Delete Email Appliance  ${ESA}
    Centralized Email Message Tracking Disable
    Commit Changes
    global_sma.DefaultTestSuiteTeardown
    Run Keyword And Ignore Error  Remove Directory  ${SUITE_TMP_DIR}  recursive=${True}

Switch To ${dut}
    Set Appliance Under Test To ${dut}
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Execute JavaScript  window.focus()
    Run Keyword And Ignore Error  Log Out Of DUT
    Run Keyword And Ignore Error  Log Into DUT

Email Tracking Search and Return
    [Arguments]  ${sender_data}=  ${sender_comparator}=
    ...  ${rcpt_data}=  ${rcpt_comparator}=
    ...  ${subject_data}=  ${subject_comparator}=  ${mesg_received}=
    ${messages}=  Email Message Tracking Search
    ...  sender_data=${sender_data}    sender_comparator=${sender_comparator}
    ...  rcpt_data=${rcpt_data}        rcpt_comparator=${rcpt_comparator}
    ...  subject_data=${subject_data}  subject_comparator=${subject_comparator}
    ...  mesg_received=${mesg_received}

    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Run Keyword If  '${tracking_message_count}' == '0'  Fail
    [Return]  ${tracking_message_count}

Create Address List File
    [Documentation]  Creates file with ip(s) (precise recipient) for \n
    ...  smtp_spam tool. That file is being created within ${SUITE_TMP_DIR}-dir.
    [Arguments]  ${data_string}=$test_user@${CLIENT}

    ${frandom_string}=  Generate Random String
    ${file_path}=  Join Path  ${SUITE_TMP_DIR}  ${frandom_string}.txt
    OperatingSystem.Create File  ${file_path}
    Append To File  ${file_path}  ${data_string}
    [Return]  ${file_path}

Wait Until SMA Gets Tracking Data
    Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return

*** Test Cases ***

CSCvo69559
    [Documentation]
    ...  1. Setup centralized message tracking on ESA & SMA
    ...  2. Create a private listener that will accept emails from your smtp_spam
    ...  3. Smtp route all to /dev/null
    ...  4. Inject emails into your private listener with this smtp_spam command
    ...  5. Wait for you emails to make it over to message tracking, and run a query on these emails we just injected via SMA GUI.
    ...  6. Choose one of the complicated messages and click on message details.
    ...  7. Click "Printable PDF".
    ...  8. Print is working as expected and no app fault is witnessed.
    ...  9. Box UI is working fine (no unresponsiveness being witnessed here).
    ...  10. Specific searching of message by MID or by applying a filter in message tracking is working as expected.

    [Tags]  CSCvo69559  srts  teacat

    Set Test Variable  ${TEST_NAME}  CSCvo69559
    Set Test Variable  ${MAIL_FROM_VAR}  ${TEST_NAME}@${CLIENT}
    Set Test Variable  ${MAIL_RCPT_TO}  ${TEST_NAME}@${CLIENT}
    ${address_file}=  Create Address List File  ${MAIL_RCPT_TO}
    Switch to ESA
    Roll Over Now
    Generate Email Reporting Data
    ...  address-list=${address_file}
    ...  mail-from=${MAIL_FROM_VAR}
    ...  rcpt-host-list=${CLIENT}
    ...  addr-per-msg=500
    ...  inject-host=${PRIVATE_LISTENER_IP}
    ...  ${SPAM}=250

    ${mid_value}=  Get Mid Value  MID .* ICID .* From: <${TEST_NAME}@${CLIENT}>

    Switch to SMA
    Wait Until SMA Gets Tracking Data
    Click Link  Show Details  don't wait
    Select Window  Message Details
    Maximize Browser Window
    Execute JavaScript  window.focus()
    Click Link  Printable (PDF)  don't wait
    ${start_time}=  Get Time
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=180  download_directory=%{SARF_HOME}/tmp
    Log  ${path}
    Sleep  5s
    Close Window
    Remove File  ${path}
    Selenium Close
    Selenium Login
    Sleep  5s
    ${messages}=  Email Message Tracking Search  ironport_mid=${mid_value}
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Run Keyword If  '${tracking_message_count}' == '0'  Fail
