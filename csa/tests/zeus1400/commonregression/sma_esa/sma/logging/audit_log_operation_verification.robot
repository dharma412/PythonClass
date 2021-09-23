*** Settings ***
Resource     sma/global_sma.txt
Resource     esa/logs_parsing_snippets.txt
Resource     esa/injector.txt
Resource     regression.txt
Variables    sma/saml_constants.py

Suite Setup  Audit Log Suite Setup
Suite Teardown  Audit Log Suite Teardown

*** Variables ***
${CONFIG_DIR}          /data/pub/configuration
${DOWNLOAD_PATH}       %{HOME}/Downloads/
${LICENSE_FILE_PATH}   %{SARF_HOME}/tests/testdata/virtual
${LICENSE_FILE_NAME}   smalicense.xml
${LOG_PATH}            /data/pub
${SSH_TEXT_PATH}       xpath=//*[@id='action-results-message']

*** Keywords  ***
Audit Log Suite Setup
    Set Suite Variable  ${audit_log_name}  audit_logs 
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA

    global_sma.DefaultTestSuiteSetup
    Log Subscriptions Add Log
    ...  Audit Logs
    ...  ${audit_log_name}
    ...  filename=${audit_log_name}
    ...  log_size=5M
    Commit Changes

    SMANGGuiLibrary.Launch Dut Browser
    SMANGGuiLibrary.Login Into Dut

Audit Log Suite Teardown
    Log Subscriptions Delete  ${audit_log_name}
    Commit Changes
    SMANGGuiLibrary.Close Browser
    DefaultTestSuiteTeardown

Load License From File
   Copy File To DUT  ${LICENSE_FILE_PATH}/${LICENSE_FILE_NAME}  ${CONFIG_DIR}/

   #Checking CLI access to DUT. If cli session was closed, trying to reopen it
   ${ready}  ${out2}  Run Keyword And Ignore Error
   ...  Start CLI Session If Not Open

   Run Keyword If  '${ready}' == 'FAIL'
   ...  Fatal Error  Cli session is not available and can not be reopened!

   ${output}=  Load License  conf=file  conf_file=${LICENSE_FILE_NAME}

   Should Not Contain  ${output}  No License Installed
   Should Contain  ${output}  Feature keys added

Verify Rolled Over Log Using Time
    ${details}=  Run On Dut  cd ${LOG_PATH}/${audit_log_name};ls -lrt *.s
    Log Many  ${details}

    @{lines}=  Split String  ${details}  \n
    Log Many  ${lines}

    ${current_count}=  Get Length  ${lines}

    Should Be Equal As Numbers  ${current_count}  2

Copy Configuration File To Dut
    [Arguments]  ${config_file_path}  ${config_file_name}
    ${config_file}=  Join Path  ${config_file_path}  ${config_file_name}
    SCP
    ...  to_user=${RTESTUSER}
    ...  to_password=${RTESTUSER_PASSWORD}
    ...  from_location=${config_file}
    ...  to_location=${CONFIG_DIR}
    ...  to_host=${SMA}

Do Tvh1499731c Teardown
    Log Config Delete  ${log_name}
    commit
    Run On DUT  rm -rf ${LOG_PATH}/${log_name}
    DefaultTestCaseTeardown

Do Tvh1499733c Teardown
    Log Subscriptions Delete  ${log_name}
    Commit Changes
    Run On DUT  rm -rf ${LOG_PATH}/${log_name}
    DefaultTestCaseTeardown

Do Tvh1499734c Teardown
    Copy File  %{HOME}/.ssh/authorized_keys_dup  %{HOME}/.ssh/authorized_keys
    Remove File  %{HOME}/.ssh/authorized_keys_dup
    global_sma.Run Command On FTP Server  rm -rf ${ftp_log_folder}
    Log Subscriptions Set Retrieval Method to Manually Download
    ...  ${audit_log_name}
    ...  filename=${audit_log_name}
    Commit Changes
    OperatingSystem.Remove File  ${DOWNLOAD_PATH}/${audit_log_name}*
    DefaultTestCaseTeardown

Do Tvh1499736c Teardown
    DefaultTestCaseTeardown

Do Tvh1499737c Teardown
    SMANGGuiLibrary.Login Into Dut
    SMAGuiLibrary.Log Into Dut
    DefaultTestCaseTeardown

Do Tvh1499739c Teardown
    SMANGGuiLibrary.Login Into Dut
    Log Config Edit  ${audit_log_name}  log_level=3
    Commit

Do Tvh1499740c Teardown
    Log Subscriptions Edit Log  ${audit_log_name}  
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh1499742c Teardown
    Log Subscriptions Edit Log  ${audit_log_name}  log_size=10M  log_level=Info
    Commit Changes
    DefaultTestCaseTeardown

Do Tvh1499745c Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut
    DefaultTestCaseSetup
    Interface Config Edit  Management  SSH=yes
    Commit
    ${config_filename}=  Configuration File Save Config   mask_passwd=${False}
    Set Test Variable  ${config_filename}
    Copy File From Dut To Remote Machine
    ...  from_loc=${CONFIG_DIR}/${config_filename}
    ...  remote_host=${CLIENT}
    ...  to_loc=%{HOME}/Downloads/
    ...  to_user=${TESTUSER}
    ...  to_password=${TESTUSER_PASSWORD}
    SMAGuiLibrary.Close Browser

Do Tvh1499745c Teardown
    Load License From File
    Copy Configuration File To Dut
    ...  %{HOME}/Downloads/
    ...  ${config_filename}

    Configure SSL For GUI
    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut
    Configuration File Load Config   ${config_filename}
    Commit Changes
    Remove File  %{HOME}/Downloads/${config_filename}
    Run On DUT  rm -rf ${CONFIG_DIR}/${config_filename}
    DefaultTestCaseTeardown

*** Test Cases ***

Tvh1499731c
    [Documentation]
    ...   Verify creating a log subscription Audit logs using CLI \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499731
    [Tags]  Tvh1499731c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1499731c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${log_name}  audit_log_new
    #### Log File Number (35 - Audit Logs) is used due to a bug in the clictorbase.py code####
    #### Update Log Number if Log Config Keyword Fails in Upcoming Releases####
    Log Config New  log_file=35  name=${log_name}
    Commit
    ${logs}=  Log Config Print
    Log Many  ${logs}
    Should Contain  ${logs}  ${log_name}

Tvh1499733c
    [Documentation]
    ...   Verify creating audit log subscription using GUI \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499733
    [Tags]  Tvh1499733c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1499733c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${log_name}  audit_log_gui

    Log Subscriptions Add Log  
    ...  Audit Logs
    ...  ${log_name}
    ...  filename=${log_name} 
    ...  log_size=5M
    Commit Changes
    ${logs}=  Log Subscriptions Get Logs
    Log Many  ${logs}
    Should Contain  ${logs}  ${log_name}

Tvh1499734c
    [Documentation]
    ...   Verify audit logs could be pushed via  SCP,  FTP and syslog and make
    ...   sure functionality is working fine \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1482020
    [Tags]  Tvh1499734c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1499734c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${ftp_log_folder}  ${FTP_SERVER_ROOT_DIR}/uploads/${TEST_ID}/ 
     
    Run Command On FTP Server  rm -rf ${ftp_log_folder}; mkdir -p ${ftp_log_folder}
    Log Subscriptions Set Retrieval Method to FTP Push
    ...  ${audit_log_name}
    ...  ${FTP_SERVER_IP}
    ...  /uploads/${Test_Id}
    ...  ${FTPUSER}
    ...  ${FTPUSER_PASSWORD}
    Commit Changes
    Roll Over Now  ${audit_log_name}
    ${out}=  global_sma.Run Command On FTP Server  ls ${ftp_log_folder}
    Should Contain  ${out}  ${audit_log_name}

    Log Subscriptions Set Retrieval Method to Syslog Push
    ...  ${audit_log_name}
    ...  ${CLIENT_IP}
    ...  protocol=udp
    ...  facility=user
    Commit Changes
    ${pattern}=  Grep File  /var/log/messages  *Log Subscription Settings.
    Should Contain  ${pattern}  Log Subscription Settings

    Log Subscriptions Set Retrieval Method to SCP Push
    ...  ${audit_log_name}
    ...  ${CLIENT_IP}
    ...  ${DOWNLOAD_PATH}
    ...  %{USER}
    ...  filename=${audit_log_name}

    ${ssh_text}=  SmaGuiLibrary.Get Text  ${SSH_TEXT_PATH}
    Log   ${ssh_text}

    ${rsa_key}=    Get Lines Containing String  ${ssh_text}  ssh-dss
    Log  ${rsa_key}
    Commit Changes

    Copy File  %{HOME}/.ssh/authorized_keys  %{HOME}/.ssh/authorized_keys_dup
    Append to File  %{HOME}/.ssh/authorized_keys  \n${rsa_key}

    Roll Over Now  ${audit_log_name}

    Wait Until Keyword Succeeds
    ...  3m  40s
    ...  OperatingSystem.File Should Exist  ${DOWNLOAD_PATH}/${audit_log_name}*

Tvh1499736c
    [Documentation]
    ...   Verify information printed in audit logs are appropriate and correct
    ...   for successful attempts (successful login via legacy and NGUI) \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499736
    [Tags]  Tvh1499736c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1499736c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    SmaGuiLibrary.Logout Of Dut
    SmaGuiLibrary.Log Into Dut
    SMANGGuiLibrary.Logout Of Dut
    SMANGGuiLibrary.Login Into Dut

    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Appliance: ${DUT}, Interaction Mode: GUI, User: admin.* Successful login >= 1
    ...  Appliance: ${DUT}, Interaction Mode: GUI, User: admin.* Session established successfully >= 1
    ...  Appliance: ${DUT}, Interaction Mode: API, User: admin.* Location: POST \\/sma\\/api\\/v2\\.0\\/login HTTP\\/1\\.0, Event: API Access Success. >= 1

Tvh1499737c
    [Documentation]
    ...   Verify information printed in audit logs are appropriate and correct for unsuccessful
    ...   attempts (unsuccessful login via legacy and NGUI) \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499737
    [Tags]  Tvh1499737c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1499737c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    SmaGuiLibrary.Logout Of Dut
    Run Keyword And Ignore Error  SmaGuiLibrary.Log Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_TMP_PASSWORD}
    SMANGGuiLibrary.Logout Of Dut
    Run Keyword And Ignore Error  SMANGGuiLibrary.Login Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_TMP_PASSWORD}

    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=90
    ...  Appliance: ${DUT}, Interaction Mode: GUI, User: admin.* Permission denied reason - Invalid username or passphrase >= 1
    ...  Appliance: ${DUT}, Interaction Mode: API, User: admin, Role: Administrator, .* Invalid username or passphrase >= 1

Tvh1499739c
    [Documentation]
    ...   Verify audit logs in different levels Info, Debug. \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499739
    [Tags]  Tvh1499739c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1499739c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}
    SMANGGuiLibrary.Logout Of Dut
    SMANGGuiLibrary.Login Into Dut

    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=60
    ...  Info: Appliance: ${DUT}, Interaction Mode: API, User: admin.* Location: POST \\/sma\\/api\\/v2\\.0\\/login HTTP\\/1\\.0, Event: API Access Success. >= 1

    Log Config Edit  ${audit_log_name}  log_level=4
    Commit
    Roll Over Now  ${audit_log_name}

    SMANGGuiLibrary.Logout Of Dut 
    Run Keyword And Ignore Error  SMANGGuiLibrary.Login Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_TMP_PASSWORD}

    Verify Log Contains Records
    ...  search_path=${audit_log_name}
    ...  timeout=60
    ...  Debug: .*Error - Code: 401, Details: Invalid username or passphrase.* >= 1

Tvh1499740c
    [Documentation]
    ...   Verify audit logs could be rolled over using time \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499740 \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499743
    [Tags]  Tvh1499740c  Tvh1499743c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1499740c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Run On DUT  rm -rf ${LOG_PATH}/${audit_log_name}/*.s

    Log Subscriptions Edit Log  ${audit_log_name}  rollover_interval=60s
    Commit Changes

    Wait Until Keyword Succeeds
    ...  1m  30s
    ...  Verify Rolled Over Log Using Time

Tvh1499742c
    [Documentation]
    ...   Verify audit logs could be rolled over using File size \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499742
    [Tags]  Tvh1499742c  srts
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Do Tvh1499742c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Roll Over Now  ${audit_log_name}

    Log Subscriptions Edit Log  ${audit_log_name}  log_size=100K  log_level=Trace
    Commit Changes

    Run On DUT  rm -rf ${LOG_PATH}/${audit_log_name}/*.s

    FOR  ${val}   IN RANGE    1  15
       SMANGGuiLibrary.Logout Of Dut
       SMANGGuiLibrary.Login Into Dut
    END

    ${files_details}=  Run On Dut  cd ${LOG_PATH}/${audit_log_name};ls -lrt *.s
    Log Many  ${files_details}

    @{file}=  Split String  ${files_details}
    Log Many  ${file}
    Set Test Variable  ${byte}  1000.0
    ${size}=  Evaluate  ${file[4]} / ${byte}
    Log Many  ${size}
    ${file_size_int}=  Convert To Integer  ${size}
    Log Many  ${file_size_int}
    ${file_size}=  Convert To String  ${file_size_int}
    Log Many  ${file_size}

    Should Contain Any  ${file_size}  9  8  10

Tvh1499745c
    [Documentation]
    ...   Verify after executing diagnostic >> reload , audit log is present as
    ...   default log subscription \n
    ...   http://tims.cisco.com/view-entity.cmd?ent=1499745
    [Tags]  Tvh1499745c  srts
    [Setup]  Do Tvh1499745c Setup
    [Teardown]  Do Tvh1499745c Teardown

    Diagnostic Reload  confirm=yes   wipedata=no
    Wait Until DUT Is Accessible

    Wait Until Keyword Succeeds  10 minutes  15 seconds
    ...  Start CLI Session if Not Open

    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}

    Start CLI Session If Not Open

    ${logs}=  Log Config Print
    Log Many  ${logs}

    Should Not Contain  ${logs}  ${audit_log_name}

    SMAGuiLibrary.Launch Dut Browser
    SMAGuiLibrary.Log Into Dut

    ${all_logs}=  Log Subscriptions Get Logs
    Log Many  ${all_logs}  
    Should Not Contain  ${all_logs}  ${audit_log_name}
    SMAGuiLibrary.Close Browser
