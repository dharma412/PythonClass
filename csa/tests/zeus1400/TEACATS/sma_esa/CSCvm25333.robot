# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/TEACATS/sma_esa/CSCvm25333.txt#3 $ $DateTime: 2020/03/31 03:20:25 $ $Author: sarukakk $

*** Settings ***
Library           SmaGuiLibrary
Library           Collections
Resource          sma/global_sma.txt
Resource          regression.txt
Resource          esa/injector.txt
Resource          esa/global.txt
Resource          esa/logs_parsing_snippets.txt
Resource          esa/backdoor_snippets.txt
Resource          sma/esasma.txt

Suite Setup   Do Suite Setup
Suite Teardown   Do Suite Teardown

*** Variables ***

*** Keywords ***
Do Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup
    ...  should_revert_to_initial=${False}
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup

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
    ${res}=  Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  isq=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Log  ${res}
    Run Keyword If  ${commit}  Commit Changes

Inject High Volume Mails
    FOR  ${index}  IN RANGE  10
        Generate Email Reporting Data
        ...  rcpt-host-list=${CLIENT}
        ...  inject-host=${ESA_PUB_LISTENER_IP}
        ...  ${SPAM}=250
        ...  ${SPAM_SUSPECT}=250
    END

Close SSH connection
   Set SSHLib Prompt  ${Empty}
   SSHLibrary.Close Connection

*** Test Cases ***

Tvh1231019c
    [Documentation]  EUQ storage system start times over 5 minutes break EUQ
    ...  1. Attach ESA to SMA
    ...  2. Send 100000 mails to ESA
    ...  3. Restart EUQ server after 5 minutes
    ...  4. Check in EUQ logs EUQ storage initialization not failed
    ...  http://tims/view-entity.cmd?ent=1231019
    [Tags]  srts  teacat  CSCvm25333  Tvh1231019c  CSCvn31781

    Set Test Variable  ${TEST_ID}  Tvh1231019c
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    Set Appliance Under Test to ESA
    Prepare Spam Quarantine On ESA
    Login To WebUI  SMA
    Enable Spam Quarantine On SMA  commit=${False}
    Add ESA to SMA
    Roll Over Now  euq_logs
    FOR  ${index}  IN RANGE  20
        Inject High Volume Mails
        Sleep  10s
    END
    Sleep  5m
    Run On DUT  /data/bin/heimdall_svc recycle euq_server
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Sleep  60s
    ${matches}  ${found}=  Log Search  .*EUQ Server Storage Initialization failed.*  search_path=euq  timeout=15
    Should Be Equal As Numbers  ${matches}  0
