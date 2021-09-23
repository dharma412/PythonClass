*** Settings ***
Resource     esa/injector.txt
Resource     regression.txt
Resource     sma/esasma.txt

Suite Setup  Do Suite Setup
Suite Teardown  Finalize Suite
Force Tags  backup.general

*** Variables ***

${SESSION_TIMEOUT}         1440
${DATA_UPDATE_TIMEOUT}=  20m
${RETRY_TIME}=  15s
${SENDER}=  def@ironport.com
${expected_count}  0
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${SLBL spam positive}=  SLBL spam positive
${CONFIG_PATH}     /data/pub/configuration

*** Keywords ***

Do Suite Setup
    Library Order ESA
    DefaultRegressionSuiteSetup
    ${ESA_PUBLIC_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUBLIC_LISTENER_IP}
    Smtp Routes New  domain=ALL  dest_hosts=/dev/null
    Message Tracking Enable  tracking=centralized
    Centralized Email Reporting Enable
    ${local_spam_quarantine_enabled}=  Quarantines Spam Is Enabled
    Run Keyword If  ${local_spam_quarantine_enabled}  Quarantines Spam Disable
    EUQ Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    Antispam Enable  IronPort
    ${settings}=  Create Dictionary  Positive Spam Apply Action  Spam Quarantine
    Mail Policies Edit Antispam  incoming  default  ${settings}
    Commit Changes
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes
    ${dut_hostname}  ${domain}=  Split String  ${DUT}  .
    Set Suite Variable  ${RECIPIENT_ADDRESS}  xyz@ironport.${domain}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Run Keyword And Ignore Error  Null Smtpd Stop
      Null Smtpd Start
      Roll Over Now  mail_logs
    END
    Library Order SMA
    Selenium Login
    Network Access Edit Settings  ${SESSION_TIMEOUT}
    Clean System Quarantines
    Spam Quarantine Enable
    Pvo Quarantines Enable
    Spam Quarantine Edit
    ...  interface=Management
    ...  port=6025
    Spam Quarantine SlBl Enable
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    ${ISQ_URL}=  Catenate  SEPARATOR=  https://  ${DUT}  :83
    Set Suite Variable  ${ISQ_URL}
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp()  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}
    IP Interfaces Edit  Management  isq_https_service=83  isq_default=https://${DUT}:83/  hostname=${DUT}
    Commit Changes
    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes
    Spam Quarantine Delete Message
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Wait Until Keyword Succeeds  5m  1m  Pvo Quarantines Enable
      Run Keyword And Ignore Error  Commit Changes
    END
    ${esa_cnt}=  Get Length  ${esa_appliances}
    Set Suite Variable  ${esa_cnt}

Spam Quarntine Search
    [Arguments]  ${date_range}=today  ${count}=${expected_count}
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  is_admin=${False}  date_range=${date_range}
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} == ${count}  Fail
    [Return]  ${actual_spam_count}

Add SLBL admin and Verify
    [Arguments]  ${listtype}  ${address}  ${senders}
    ${slbl_admin_added}=   SLBL Admin Is Recipient Exist
    ...  ${listtype}  ${address}
    Run Keyword If  ${slbl_admin_added}
    ...  SLBL Admin Delete Recipient  ${listtype}  ${address}

    SLBL Admin Add Recipient
    ...  ${listtype}
    ...  ${address}
    ...  ${senders}
    ${slbl_admin_added}=   SLBL Admin Is Recipient Exist
    ...  ${listtype}  ${address}
    Should Be True  ${slbl_admin_added}

Login To ISQ
    [Arguments]  ${user}
    ...  ${password}
    Selenium Close
    Set Appliance Under Test to SMA
    Set Up Selenium Environment
    Launch DUT Browser  url=${ISQ_URL}
    Log Into DUT  ${user}  ${password}

Database Sync for Safelist Or Blocklist
    [Arguments]  ${listtype}  ${address}  ${senders}
    Login To ISQ
    ...  ${DUT_ADMIN}
    ...  ${DUT_ADMIN_SSW_PASSWORD}

    Add SLBL admin and Verify
    ...  ${listtype}
    ...  ${address}
    ...  ${senders}

    Set Appliance Under Test to ESA
    Roll Over Now  mail_logs
    Sleep  5s  msg=Wait for logs roll over

    Set Appliance Under Test to SMA
    Selenium Login
    ${synced}=  Spam Quarantine Sync Appliances
    Log  "Database Synchronisation is ${synced}"

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  wait_time=3 minutes
    ...  retry_time=1 minute
    ...  SLBL: Database watcher updated from snapshot >= 1

Create Recipients List File
    [Arguments]  ${recepients}
    ${rcpts}=  Join Path  ${SUITE_TMP_DIR}  ${TEST_ID}_rcpts.txt
    OperatingSystem.Create File  ${rcpts}
    OperatingSystem.Append To File  ${rcpts}  ${recepients}
    [Return]  ${rcpts}

Database Slbl Sync
    [Arguments]  ${LIST_TYPE}  ${LIST_TYPE_SENDER}
    Set Appliance Under Test to SMA
    Selenium Login
    Database Sync for Safelist Or Blocklist
    ...  ${LIST_TYPE}
    ...  ${RECIPIENT_ADDRESS}
    ...  ${LIST_TYPE_SENDER}
    ${rcpts}=  Create Recipients List File   ${RECIPIENT_ADDRESS}
    [Return]  ${rcpts}

Inject Message And Verify Log
    [Arguments]  ${mbox-filename}  ${mail-from}  ${spam_negative}
    Inject Messages
    ...  mbox-filename=${mbox-filename}
    ...  mail-from=${mail-from}
    ...  address-list=${rcpts}
    ...  num-msgs=1000
    ...  inject-host=${ESA_PUBLIC_LISTENER_IP}
    Verify And Wait For Log Records
    ...  MID .* ICID .* From: .*${mail-from}.* >= 1
    ...  MID .* using engine.* ${spam_negative} >= 1

Euq Spam Quarantine Search
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Go To  https://${DUT}:83
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week
    Log  ${spam_count}
    [Return]  ${spam_count}

Spam Quarantine Delete Message
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To  https://${DUT}:83
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week
    Commit Changes

Check If Backup Is Completed
    ${out} =  Backup Config Status
    Should Contain  ${out}  No backup in progress

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1000
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

Finalize Suite
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Run Keyword And Ignore Error  Run On DUT  rm -rf ${CONFIG_PATH}/default_config.xml
      Selenium Close
    END
    DefaultRegressionSuiteTeardown

*** Testcases ***

CSCvt34780
    [Tags]  Teacat  CSCvt34780
    [Documentation]  Netinstall SMA do loadlicense and SSW
    ...  Enable all the centralized services for Email
    ...  Enable SLBL in Spam quarantine
    ...  Attach ESA and inject mail to ESA
    ...  Run the backup job from source SMA , backup all the data for SLBL as well
    ...  Keep checking the euq count during backup and after cpq phase 2 verify the count is decrease
    [Teardown]  Spam Quarantine Delete Message

    Set Test Variable   ${TEST_ID}  ${TEST_NAME}
    Sync Appliances Datetime  ${SMA}  ${SMA2}  ${ESA}
    Set Test Variable   ${LIST_TYPE}  Blocklist
    ${rcpts}=  Database Slbl Sync  ${LIST_TYPE}  ${LIST_TYPE}_1_${SENDER}
    Set Suite Variable  ${rcpts}

    FOR  ${index}  IN RANGE  10
      Inject Message And Verify Log
      ...  ${SPAM}
      ...  ${LIST_TYPE}_1_${SENDER}
      ...  ${SLBL spam positive}
    END

    Library Order SMA2
    Centralized Email Reporting Enable
    Commit Changes

    Library Order SMA
    Selenium Login
    ${spam_count}=  Euq Spam Quarantine Search
    Should Be Equal As Strings  ${spam_count}  100
    Selenium Close

    ${ip}=  Get Host IP By Name  ${SMA2}
    Set Suite Variable  ${SMA2_IP}  ${ip}

    Library Order ESA
    Start Cli Session If Not Open
    Policyconfig Edit Antispam Disable  Incoming  DEFAULT
    Commit
    Library Order SMA
    Selenium Login
    Run Keyword and ignore Error
    ...  Wait Until Keyword Succeeds  5m  30s  Pvo Release Policy Message  Policy  week
    Library Order ESA
    Selenium Login
    Start CLI Session If Not Open
    ${PUBLIC_LISTENER}=  Get ESA Listener
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
    Commit Changes
    ${settings}=  Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${TEST_ID}   ${True}
    Mail Policies Edit Content Filters  Incoming  default
    ...  ${settings}
    Commit Changes
    FOR  ${index}  IN RANGE  10
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${PUBLIC_LISTENER.ipv4}
    END

    Library Order Sma
    Restart Cli Session
    ${euq_count_befor_bkp}=  Run on DUT  lsof | grep euq | wc -l
    Log  ${euq_count_befor_bkp}

    Roll Over Now
    Set Test Variable  ${Backup_Name}  single_backup
    Backup Config Schedule
    ...  job_name=${Backup_Name}
    ...  backup_type=now
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=Yes

    ${euq_count_aftr_bkp}=  Run on DUT  lsof | grep euq | wc -l
    Log  ${euq_count_aftr_bkp}
    Should Be True  ${euq_count_aftr_bkp} <= ${euq_count_befor_bkp}
