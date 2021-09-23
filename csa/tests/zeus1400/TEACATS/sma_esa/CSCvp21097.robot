# This teacat works only on SMA M190 model

*** Settings ***
Suite Setup        DefaultRegressionSuiteSetup
Suite Teardown     DefaultRegressionSuiteTeardown
Test Setup         DefaultRegressionTestCaseSetup
Test Teardown      DefaultRegressionTestCaseTeardown
Resource     esa/injector.txt
Resource     regression.txt
Resource     sma/esasma.txt



*** Variables ***
${DATA_UPDATE_TIMEOUT}=  20m
${RETRY_TIME}=  15s
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/


*** Keywords ***
Clear Email Tracking Reporting Data
    Library Order ESA
    Start CLI Session If Not Open
    Roll Over Now
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready
    Library Order Sma
    Start CLI Session If Not Open
    Roll Over Now
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready

Spam Quarntine Search
    [Arguments]  ${date_range}=today
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  is_admin=${False}  date_range=${date_range}
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} == '0'  Fail
    [Return]  ${actual_spam_count}


***Testcases***
CSCvp21097
    [Tags]  CSCvp21097  teacat
    [Documentation]  TEA M190 jack names discrepancy causes etherconfig & euq issues
    ...  1.Obtain an M190 SMA.
    ...  2.Enable message tracking and EUQ on the SMA.
    ...  3.Attach a compatible ESA.
    ...  4.Send at least one email into the EUQ
    ...  5.Using service access, observe the jack_names variable in
    ...   /data/db/config/system.network/data.cfg.gz.
    ...  6.In the CLI, run etherconfig -> media and observe the interfaces displayed.
    ...  7.While logged into the GUI as admin, open the EUQ GUI and search for messages

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Clear Email Tracking Reporting Data
    Library Order ESA
    Selenium Login
    Message Tracking Enable  tracking=centralized
    Centralized Email Reporting Enable
    Quarantines Spam Disable
    Commit Changes
    EUQ Enable  ${SMA}  ${SMA_IP}  enable_slbl=${False}
    AntiSpam Enable  IronPort
    ${settings}=  Create Dictionary  Positive Spam Apply Action  Spam Quarantine
    Mail Policies Edit Antispam  incoming  default  ${settings}
    Commit Changes
    Library Order SMA
    Selenium Login
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    Spam Quarantine Enable
    Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To  https://${DUT}:83
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week
    Library Order SMA
    Selenium Login
    Spam Quarantine Edit
    ...  interface=Management
    ...  port=6025
    Commit Changes
    Library Order ESA
    Start CLI Session If Not Open
    ${PUBLIC_LISTENER}=  Get ESA Listener
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  antispam/spam_suspect.mbox
    Inject Messages  inject-host=${PUBLIC_LISTENER.ipv4}  num-msgs=2
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}
    Library Order SMA
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Go To  https://${DUT}:83
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week
    Log  ${spam_count}
    ${output}=  Run on DUT  cat /data/pub/euqgui_logs/euqgui.current
    Should Not Contain  ${output}  An application fault occurred
    ${output}=  Run on DUT  cat /data/db/config/system.network/data.cfg | grep 'jack_names'
    Log  ${output}
    Should Contain  ${output}  {"Data 2":"igb1","Data 1":"igb0"}
    ${address}=  Get Host IP By Name  ${DUT}
    SSHLibrary.Open Connection  ${address}
    Set SSHLib Prompt  >
    SSHLibrary.Login   ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Write  cli
    Read Until Prompt
    Write  etherconfig
    Read Until Prompt
    Write  media
    Sleep  20s
    ${out}=  Read
    Log  ${out}
    Should Contain  ${out}  Data 1
    Should Contain  ${out}  Data 2
