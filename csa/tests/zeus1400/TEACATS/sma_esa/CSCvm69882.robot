*** Settings ***
Library           Collections
Resource          sma/global_sma.txt
Resource          regression.txt
Resource          esa/global.txt
Resource          esa/injector.txt
Resource          esa/logs_parsing_snippets.txt
Resource          esa/backdoor_snippets.txt

Suite Setup   Run Keywords
              ...  Set Aliases For Appliance Libraries
              ...  Set Appliance Under Test to SMA
              ...  DefaultRegressionSuiteSetup
Suite Teardown   DefaultRegressionSuiteTeardown

*** Variables ***
${TIMEOUT}               1438
${DATA_UPDATE_TIMEOUT}=  20m
${RETRY_TIME}=  15s
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/

*** Keywords ***
Do CSCvm69882 Setup
    Set Appliance Under Test to SMA
    Selenium Login
    Spam Quarantine Enable
    Spam Quarantine SlBl Enable
    Pvo Quarantines Enable
    Run Keyword And Ignore Error  Pvo Delete Policy Message  Virus  week
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  ${TIMEOUT}
    Commit Changes
    Library Order ESA
    Start Cli Session If Not Open
    Policyconfig Edit Antispam Disable  Incoming  DEFAULT
    Commit
    Library Order SMA
    Selenium Login
    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}=${PUBLIC_LISTENER_IP4}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

PVO Search
    [Arguments]  ${name}=None  ${date_range}=today
    ${count}=  Pvo Search Policy Message  name=${name}  date_range=${date_range}
    Run Keyword If  ${count}==0  Fail
    [Return]  ${count}

Close SSH connection
   Set SSHLib Prompt  ${Empty}
   SSHLibrary.Close Connection

*** Test Cases ***
CSCvm69882
    [Documentation]  TEA SMA doesn't show headers, message or message parts in PVO quarantine
    ...  \n  make incoming virus mail as quarantine in mail policiy and send virus mail box
    ...  \n  Verify message,headers are present in  PVO quarantine Virus Category mails.
    [Tags]  CSCvh82678  CSCvm69882  teacat  invalid_not_applicable_for_smart_license

    Do CSCvm69882 Setup
    Set Appliance Under Test to ESA
    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    ${PUBLIC_LISTENER_IP}=  Get ESA Public IP
    ${PRIVATE_LISTENER_IP} =  Get ESA Private IP
    Set Suite Variable  ${PUBLIC_LISTENER_IP}
    Set Suite Variable  ${PRIVATE_LISTENER_IP}
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${PUBLIC_LISTENER_IP4}  ${PUBLIC_LISTENER.ipv4}
    ${text} =  Set Variable  ppt
    ${msg_body_or_attachment_cond}=  Create Dictionary
    ...  Contains text  ${text}
    ${conditions}=  Content Filter Create Conditions
    ...  Message Body or Attachment  ${msg_body_or_attachment_cond}
    ${quarantine_action}=  Create Dictionary
    ...  Send message to quarantine   Policy
    ...  Duplicate message   ${False}
    ${actions}=  Content Filter Create Actions
    ...  Quarantine  ${quarantine_action}
    Content Filter Add  Incoming  ${TEST_ID}  ${TEST_ID}
    ...  ${actions}  ${conditions}
    ${settings}=  Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${TEST_ID}   ${True}
    Mail Policies Edit Content Filters  Incoming  default
    ...  ${settings}
    ${settings} =  Create Dictionary
    ...  Anti-Virus Scanning  Yes
    ...  Virus Infected Messages Apply Action  Quarantine
    Mail Policies Edit Antivirus
    ...  Incoming
    ...  default
    ...  ${settings}
    Commit Changes
    Pvo Quarantines Enable
    Run Keyword and Ignore Error  Commit Changes
    Inject Custom Message  antivirus/testvirus.mbox
    Set Appliance Under Test to SMA
    ${count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  PVO Search  name=Virus  date_range=today
    Run Keyword and Ignore Error  Should Be Equal As Integers  ${count}  1
    Click link  [WARNING: VIRUS DETECTED]real virus in rar file in attachment
    Page Should Contain  Headers
    Page Should Contain  Message
    Page Should Contain  Message Parts
    Set Appliance Under Test to ESA
    Pvo Quarantines Disable
    Commit Changes
