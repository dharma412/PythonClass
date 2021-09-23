
*** Settings ***
Resource     esa/global.txt
Resource     sma/global_sma.txt
Resource     sma/esasma.txt
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

*** Keywords ***
Initialize Suite
    Set Appliance Under Test To ESA
    global.DefaultTestSuiteSetup  should_revert_to_initial=${False}
    Smtp Routes New  domain=ALL  dest_hosts=/dev/null
    Commit
    Message Tracking Enable  tracking=centralized
    Commit Changes

    Set Appliance Under Test To SMA
    global_sma.DefaultTestSuiteSetup
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

General Test Case Setup
    FOR  ${dut_type}  IN  ESA  SMA
      Switch To ${dut_type}
      Diagnostic Tracking Delete Db  confirm=yes
      DefaultTestCaseSetup
    END

General Test Case Teardown
    Switch TO ESA
    FOR  ${dut_type}  IN  SMA  ESA
      Switch To ${dut_type}
      DefaultTestCaseTeardown
    END

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

Inject Custom Messages
    [Arguments]  ${mail_from}=sender@${CLIENT}  ${mail_to}=recipient@${CLIENT}
    ...  ${subject}=test_email  ${mail_body}=testmessage  ${msgs_count}=1
    ...  ${inject_host}=${PUBLIC_LISTENER_IP}
    ${mbox}=  injector.Create Custom Message
    ...  ${subject}
    ...  ${mail_from}
    ...  ${mail_to}
    ...  ${mail_body}
    Inject Messages
    ...  mbox-filename=${mbox}
    ...  num-msgs=${msgs_count}
    ...  inject-host=${inject_host}
    Remove File  ${mbox}

Inject ${msgs_count} Messages From ${mailbox}
    Inject Messages
    ...  mbox-filename=${mailbox}
    ...  num-msgs=${msgs_count}
    ...  inject-host=${PUBLIC_LISTENER_IP}

Wait Until SMA Gets Tracking Data
    Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  mesg_received=last week

Wait Until SMA Gets Tracking Data Count
     ${msgs_count}=  Email Tracking Search and Return  mesg_received=last week  sender_data=${MAIL_FROM_VAR}
     Should Be Equal As Integers  ${msgs_count}  2

Verify Tracking Count
    [Arguments]  ${period}  ${time}  ${emsg_count}
    ${messages}=  Email Message Tracking Search  mesg_received=custom range
    ...  start_date=${period}  start_time=${time}  sender_data=${MAIL_FROM_VAR}
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Integers  ${tracking_message_count}  ${emsg_count}

Do Search Tvh662451c
    [Arguments]  ${arg}
    ${res}=  Message Tracking Search
    ...  max_results=${arg}
    Log  ${res}
    ${page_count}=  Message Tracking Get Page Count  ${res}
    Log  ${page_count}
    ${count} =  Message Tracking Get Total Result Count  ${res}
    Log  ${count}
    Should Be True  ${count} == ${arg}

Do Search Tvh662478c

    ${mesges}=  Email Message Tracking Search  sender_ip=${d1_client_ip}
    ...  sender_ip_search_options=rejected_connections
    ${mesges1}=  Email Message Tracking Search  sender_ip=${d1_client_ip1}
    ...  sender_ip_search_options=rejected_connections
    ${tracking_message_count_mesges}=  Email Message Tracking Get Total Result Count  ${mesges}
    ${tracking_message_count_mesges1}=  Email Message Tracking Get Total Result Count  ${mesges1}
    ${tracking_message_count}=  Set Variable If  ${tracking_message_count_mesges} == 0
    ...  ${tracking_message_count_mesges1}  ${tracking_message_count_mesges}
    Should Be Equal As Strings  ${tracking_message_count}  ${msg_count}

Verify Tracking Data
    ${mesges1}=  Email Message Tracking Search  sender_ip=${d1_client_ip1}
    ...  sender_ip_search_options=rejected_connections
    ${tracking_message_count_mesges1}=  Email Message Tracking Get Total Result Count  ${mesges1}
    [Return]  ${tracking_message_count_mesges1}

Do Search Tvh662455c

    ${mesges}=  Email Message Tracking Search  sender_ip=${d1_client_ip}
    ...  sender_ip_search_options=rejected_connections
    ${tracking_message_count_mesges}=  Email Message Tracking Get Total Result Count  ${mesges}
    ${tracking_message_count_mesges1}=  Run Keyword If  ${tracking_message_count_mesges} == 0
    ...  Verify Tracking Data
    ${tracking_message_count}=  Set Variable If  ${tracking_message_count_mesges} == 0
    ...  ${tracking_message_count_mesges1}  ${tracking_message_count_mesges}
    Should Be Equal As Strings  ${tracking_message_count}  ${msg_count}

Verify ${msgs_count} Messages Filtered By Message Events ${checkboxes}
    [Documentation]  Wait until reporting data is generated and check if messages \n
    ...  count is shown as expected after setting of specified 'Message Event' checkboxes
    Wait Until SMA Gets Tracking Data
    ${messages}=  Email Message Tracking Search  message_event=${checkboxes}
    ${tracking_msgs_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Integers  ${tracking_msgs_count}  ${msgs_count}

Create DLP Filter For Word
    [Arguments]  ${matched_word}
    ...  ${policy_name}=${TEST_NAME}_policy  ${drop_message}={True}
    DLP Policy New  Custom Policy  Custom Policy
    ...  change_policy_name=${policy_name}  submit=${False}
    @{rules}=  Create List  rule_type:Words or Phrases,words_phrases:${matched_word}
    Dlp Policy Create Classifier  blade_name=blade_${TEST_NAME}
    ...  rules=${rules}  submit=${True}
    Run Keyword If  ${drop_message}
    ...  DLP Message Action Edit  Default Action  msg_action=Drop
    ${policy_settings}=  Create Dictionary
    ...  DLP Policies  Enable DLP (Customize settings)
    ...  ${policy_name}  ${True}
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}

Setup Tvh662497c
    General Test Case Setup
    Set Test Variable  ${MESSAGE_COUNT}  5
    Set Test Variable  ${MAIL_FROM_VAR}  ${TEST_NAME}@${CLIENT}
    Inject Messages
    ...  mail-from=${MAIL_FROM_VAR}
    ...  rcpt-host-list=${CLIENT_HOSTNAME}
    ...  num-msgs=${MESSAGE_COUNT}
    ...  mbox-filename=${CLEAN}
    ...  inject-host=${PUBLIC_LISTENER_IP}

Setup Tvh662506c
    General Test Case Setup
    Set Test Variable  ${MESSAGE_COUNT}  5
    Set Test Variable  ${MAIL_RCPT_TO}  ${TEST_NAME}@${CLIENT}
    ${address_file}=  Create Address List File  ${MAIL_RCPT_TO}
    Inject Messages
    ...  address-list=${address_file}
    ...  num-msgs=${MESSAGE_COUNT}
    ...  repeat-address-list=${MESSAGE_COUNT}
    ...  mbox-filename=${CLEAN}
    ...  inject-host=${PUBLIC_LISTENER_IP}

Setup Tvh662498c
    General Test Case Setup
    ${from_user_name}=  Generate Random String
    ${to_rcpt_name}=  Generate Random String
    Set Test Variable  ${MESSAGE_COUNT}  5
    Set Test Variable  ${MAIL_RCPT_FROM}  ${from_user_name}@${CLIENT}
    Set Test Variable  ${MAIL_RCPT_TO}  ${to_rcpt_name}@${CLIENT}
    Set Test Variable  ${MESSAGE_SUBJECT}  Clean image
    ${address_file}=  Create Address List File  ${MAIL_RCPT_TO}
    Inject Messages
    ...  mail-from=${MAIL_RCPT_FROM}
    ...  address-list=${address_file}
    ...  num-msgs=${MESSAGE_COUNT}
    ...  repeat-address-list=${MESSAGE_COUNT}
    ...  mbox-filename=${CLEAN}
    ...  inject-host=${PUBLIC_LISTENER_IP}

Setup Tvh480881c
    General Test Case Setup
    Set Test Variable  ${MAIL_FROM_VAR}  ${TEST_NAME}@${CLIENT}
    Set Test Variable  ${MSG_COUNT}      1

Initialize Tvh662494c
    General Test Case Setup
    Switch To ESA
    Roll Over Now  mail_logs
    Smtp Routes Clear
    Smtp Routes New  domain=ALL  dest_hosts=${CLIENT_IP}
    Commit

Finalize Tvh662494c
    Switch To ESA
    Deleterecipients All
    Smtp Routes Clear
    Smtp Routes New  domain=ALL  dest_hosts=/dev/null
    Commit
    Run Keyword And Ignore Error  Null Smtpd Stop
    General Test Case Teardown

Initialize Tvh662472c
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

Finalize Tvh662472c
    Switch To ESA
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes
    General Test Case Teardown

Create MBOX Containing Message
    [Arguments]  ${mbox_path}  ${msg}
    Mailbox Load  ${mbox_path}
    Mailbox Lock
    Mailbox Add Message  ${msg}
    Mailbox Flush
    Mailbox Unlock
    Mailbox Unload

Create Plain Text MBOX
    [Arguments]  ${mbox_path}  ${subject}  ${body}  ${charset}=US-ASCII
    ${body}=  Evaluate  u"""${body}""".encode('${charset}')
    ${msg}=  Message Builder Create MIMEText  ${body}  charset=${charset}
    ${subject}=  Evaluate  u"""${subject}""".encode('${charset}')
    ${subj}=  Message Builder Create Mime Header  initial_value=${subject}
    ...  charset=${charset}  header_name=Subject
    ${subj}=  Message Builder Encode Mime Header  ${subj}
    Message Builder Add Headers  ${msg}
    ...  From=me@${CLIENT}
    ...  To=you@${CLIENT}
    ...  Subject=${subj}
    Create MBOX Containing Message  ${mbox_path}  ${msg}

Verify Messsage Tracking Data Not Empty
    ${results} =  Message Tracking Data Availability Get Tracking Data Range
    Log  ${results}
    Should Not Be Empty  ${results}
    Set Test Variable  ${results}

Initialize Tvh662495c
    General Test Case Setup
    Switch To ESA
    Roll Over Now

    Set Test Variable  ${MSG_COUNT}  1
    @{MSG_EVENT}=  Create List  dlp violations
    Set Test Variable  ${MSG_EVENT}
    Set Test Variable  ${DLP_POLICY_NAME}  ${TEST_NAME}
    Set Test Variable  ${MATCHED_WORD}  apple

    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable
    Create DLP Filter For Word  ${MATCHED_WORD}  policy_name=${DLP_POLICY_NAME}
    Commit Changes


Finalize Tvh662495c
    Select Window
    Switch To ESA
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes
    General Test Case Teardown

Initialize Tvh662507c
    General Test Case Setup
    Set Test Variable  ${MSG_COUNT}  5
    Set Test Variable  ${MAIL_FROM_VAR}  ${TEST_NAME}@${CLIENT}
    ${cur_time} =  Set Time
    ${half_day_var}=  Set Variable  12
    ${half_day_offset}=  Calculate Shifted Datetime  ${half_day_var}  cur_time=${cur_time}
    ...  offset_with=hours
    Set Time  ${half_day_offset}

    Inject Messages  num-msgs=${MSG_COUNT}  inject-host=${PUBLIC_LISTENER_IP}
    ...  mail-from=${MAIL_FROM_VAR}
    Sync Appliances Datetime  ${SMA}  ${ESA}

Do Tvh662499c Setup
    General Test Case Setup
    Set Test Variable  ${MESSAGE_COUNT}  5
    Set Test Variable  ${MAIL_FROM_VAR}  ${TEST_NAME}@${CLIENT}
    Inject Messages
    ...  mail-from=${MAIL_FROM_VAR}
    ...  rcpt-host-list=${CLIENT_HOSTNAME}
    ...  num-msgs=${MESSAGE_COUNT}
    ...  mbox-filename=${CLEAN}
    ...  inject-host=${PUBLIC_LISTENER_IP}

Initialize Tvh662478c
    Switch To ESA
    Diagnostic Tracking Delete Db  confirm=yes
    Selenium Login
    Message Tracking Disable
    Commit Changes
    Message Tracking Enable  tracking=centralized
    ...  track_info_for_rej_conn=${True}
    HAT Sender Group Edit Settings  InBoundMail  UNKNOWNLIST
    ...  sbrs_min=${EMPTY}  sbrs_max=${EMPTY}
    ...  policy=BLOCKED
    Commit Changes

Finalize Tvh662478c
    Switch To ESA
    Diagnostic Tracking Delete Db  confirm=yes
    HAT Sender Group Edit Settings  InBoundMail  UNKNOWNLIST
    ...  sbrs_min=-1.0  sbrs_max=10.0
    ...  policy=ACCEPTED
    Commit Changes
    Diagnostic Tracking Delete Db  confirm=yes
    Switch To SMA
    Diagnostic Tracking Delete Db  confirm=yes

Initialize Tvh662455c
    Switch To ESA
    Diagnostic Tracking Delete Db  confirm=yes
    Message Tracking Disable
    Commit Changes
    Message Tracking Enable  tracking=centralized
    ...  track_info_for_rej_conn=${True}
    HAT Sender Group Edit Settings  InBoundMail  UNKNOWNLIST
    ...  sbrs_min=${EMPTY}  sbrs_max=${EMPTY}
    ...  policy=BLOCKED
    Commit Changes

Finalize Tvh662455c
    Switch To ESA
    Diagnostic Tracking Delete Db  confirm=yes
    HAT Sender Group Edit Settings  InBoundMail  UNKNOWNLIST
    ...  sbrs_min=-1.0  sbrs_max=10.0
    ...  policy=ACCEPTED
    Commit Changes
    Diagnostic Tracking Delete Db  confirm=yes
    Switch To SMA
    Diagnostic Tracking Delete Db  confirm=yes

Initialize Tvh662451c
    Switch To ESA
    Message Tracking Edit Settings  tracking=local  track_info_for_rej_conn=${True}
    Commit Changes

Apply Single Content Filter
    [Arguments]  ${name}  ${conditions}  ${actions}  ${dest_policy}=Outgoing
    Content Filter Add  ${dest_policy}  ${name}  ${name}
    ...  ${actions}  ${conditions}
    @{filters_to_enable}=  Create List  ${name}
    Mailpolicy Edit Contentfilters  ${dest_policy}  Default Policy  custom
    ...  enable_filter_names=@{filters_to_enable}
    Commit Changes

Initialize Tvh663864c
    Set Test Variable  ${DLP_POLICY_NAME}  Dlp_Subject
    Set Test Variable  ${FILTER_NAME}  subject_drop

    General Test Case Setup
    Switch To ESA
    Roll Over Now  mail_logs
    Set Test Variable  ${TEST_ID}  Tvh663864c

    Antispam Disable  IronPort
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  not ${is_dlp_enabled}  DLP Enable

    ${header_contains_cond}=  Create Dictionary
    ...  Subject Header  Contains test
    ${conditions}=  Create Dictionary
    ...  Subject Header  ${header_contains_cond}
    ${add_tag_action}=  Create Dictionary
    ...  Enter a term  ${TEST_NAME}
    ${actions}=  Content Filter Create Actions
    ...  Add Message Tag  ${add_tag_action}
    Apply Single Content Filter  ${FILTER_NAME}  ${conditions}  ${actions}

    DLP Policy New  Custom Policy  Custom Policy
    ...  change_policy_name=${DLP_POLICY_NAME}  submit=${False}

    ${rule}=  Create Dictionary
    ...  rule_type       Words or Phrases
    ...  words_phrases   test
    ${rules}=  Evaluate  [','.join(map(lambda x: x[0] + ':' + x[1], ${rule}.iteritems()))]

    Dlp Policy Create Classifier  blade_name=blade
    ...  description=blade description
    ...  rules=${rules}
    ...  submit=${False}

    Dlp Policy Configure Filter Message Tags  msg_tags=${TEST_NAME}  submit=${True}
    Dlp Message Action Edit  Default Action  msg_action=Quarantine
    Mailpolicy Edit DLP  Outgoing  Default Policy  custom
    ...  enable_all_dlp_policies=${True}
    Commit Changes

Finalize Tvh663864c
    Switch To ESA
    @{filters_to_disable}=  Create List  ${FILTER_NAME}
    Mailpolicy Edit Contentfilters  outgoing  Default Policy  custom
    ...  disable_filter_names=@{filters_to_disable}
    Content Filter Delete  Outgoing  ${FILTER_NAME}
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    Antispam Enable  IronPort
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes
    General Test Case Teardown

Do Search Tvh662469c
    [Arguments]  ${arg}
    ${res}=  Message Tracking Search
    ...  max_results=${arg}
    Log  ${res}
    ${page_count}=  Message Tracking Get Page Count  ${res}
    Log  ${page_count}
    ${count} =  Message Tracking Get Total Result Count  ${res}
    Log  ${count}
    Should Be True  ${count} == ${arg}

Initialize Tvh662485c
    General Test Case Setup
    Set Test Variable  ${MESSAGE_COUNT}  4
    Set Test Variable  ${MAIL_FROM_VAR}  ${TEST_NAME}@${CLIENT}
    Inject Messages
    ...  mail-from=${MAIL_FROM_VAR}
    ...  rcpt-host-list=${CLIENT_HOSTNAME}
    ...  num-msgs=${MESSAGE_COUNT}
    ...  mbox-filename=${CLEAN}
    ...  inject-host=${PUBLIC_LISTENER_IP}

Initialize Tvh662504c
    General Test Case Setup
    Set Test Variable  ${MESSAGE_COUNT}  5
    Set Test Variable  ${MAIL_RCPT_TO}  ${TEST_NAME}@${CLIENT}
    ${address_file}=  Create Address List File  ${MAIL_RCPT_TO}
    Inject Messages
    ...  address-list=${address_file}
    ...  num-msgs=${MESSAGE_COUNT}
    ...  repeat-address-list=${MESSAGE_COUNT}
    ...  mbox-filename=${CLEAN}
    ...  inject-host=${PUBLIC_LISTENER_IP}

Initialize Tvh664098c
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

Finalize Tvh664098c
    Switch To ESA
    ${policy_settings}=  Create Dictionary  DLP Policies  Disable DLP
    Mail Policies Edit DLP  outgoing  Default  ${policy_settings}
    DLP Message Action Edit  Default Action  msg_action=Deliver
    DLP Policy Delete  ${DLP_POLICY_NAME}
    ${is_dlp_enabled}=  DLP Is Enabled
    Run Keyword If  ${is_dlp_enabled}  DLP Disable
    Commit Changes
    General Test Case Teardown

*** Test Cases ***

Tvh662497c
    [Documentation]  Verify Envelope Sender drilldown ("Begins with" criteria)\n
    ...  http://tims.cisco.com/warp.cmd?ent=480892
    [Tags]  Tvh662497c  erts
    [Setup]  Setup Tvh662497c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662497c

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  sender_data=${MAIL_FROM_VAR}
    ...  sender_comparator=Begins With
    Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}

Tvh480902c
    [Documentation]  Verify Envelope Sender drilldown ("Contains" criteria)\n
    ...  http://tims.cisco.com/warp.cmd?ent=480902
    [Tags]  Tvh480902c  erts
    [Setup]  Setup Tvh662497c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh480902c

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  sender_data=${MAIL_FROM_VAR}
    ...  sender_comparator=Contains
    Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}

Tvh662506c
    [Documentation]  Verify Envelope Recipient drilldown ("Begins with" criteria)\n
    ...  http://tims.cisco.com/warp.cmd?ent=480904
    [Tags]  Tvh662506c  erts
    [Setup]  Setup Tvh662506c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662506c

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  rcpt_data=${MAIL_RCPT_TO}
    ...  rcpt_comparator=Begins With
    Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}

Tvh662481c
    [Documentation]  Verify Envelope Recipient drilldown ("Is" criteria)\n
    ...  http://tims.cisco.com/warp.cmd?ent=480912
    [Tags]  Tvh662481c  erts
    [Setup]  Setup Tvh662506c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662481c

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  rcpt_data=${MAIL_RCPT_TO}
    ...  rcpt_comparator=Is
    Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}

Tvh662476c
    [Documentation]  Verify Subject drilldown (""Contains"" criteria)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480916
    [Tags]   Tvh662476c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}   Tvh662476c

    ${msgs_count}=  Set Variable  2
    ${search_value}=  Set Variable  spam
    ${spam_subject}=  Set Variable  ${TEST_ID}${search_value}${TEST_ID}
    ${ham_subject}=  Set Variable  ${TEST_ID}ham${TEST_ID}
    FOR  ${mail_subject}  IN  ${spam_subject}  ${ham_subject}
      Inject Custom Messages  subject=${mail_subject}  msgs_count=${msgs_count}
    END
    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return
    ...     subject_data=${search_value}
    ...     subject_comparator=Contains
    Should Be Equal As Integers  ${tracking_messages_count}  ${msgs_count}
    Page Should Contain  ${spam_subject}
    Page Should Not Contain  ${ham_subject}

Tvh662464c
    [Documentation]  Verify Subject drilldown ("Begins with" criteria)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480888
    [Tags]   Tvh662464c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}   Tvh662464c

    ${msgs_count}=  Set Variable  2
    ${search_value}=  Set Variable  spam
    ${spam_subject}=  Set Variable  ${search_value}${TEST_ID}
    ${ham_subject}=  Set Variable  ham${TEST_ID}
    FOR  ${mail_subject}  IN  ${spam_subject}  ${ham_subject}
      Inject Custom Messages  subject=${mail_subject}  msgs_count=${msgs_count}
    END
    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return
    ...     subject_data=${search_value}
    ...     subject_comparator=Begins With
    Should Be Equal As Integers  ${tracking_messages_count}  ${msgs_count}
    Page Should Contain  ${spam_subject}
    Page Should Not Contain  ${ham_subject}

Tvh662496c
    [Documentation]  Verify Subject drilldown ("Is" criteria)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480917
    [Tags]   Tvh662496c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}   Tvh662496c

    ${msgs_count}=  Set Variable  2
    ${spam_subject}=  Set Variable  spam
    ${ham_subject}=  Set Variable  ham
    FOR  ${mail_subject}  IN  ${spam_subject}  ${ham_subject}
      Inject Custom Messages  subject=${mail_subject}  msgs_count=${msgs_count}
    END
    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return
    ...     subject_data=${spam_subject}
    ...     subject_comparator=Is
    Should Be Equal As Integers  ${tracking_messages_count}  ${msgs_count}
    Page Should Contain  ${spam_subject}
    Page Should Not Contain  ${ham_subject}

Tvh662486c
    [Documentation]  Verify Subject drilldown ("Is Empty" criteria)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480894
    [Tags]   Tvh662486c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}   Tvh662486c

    ${msgs_count}=  Set Variable  2
    Inject Custom Messages  subject=  msgs_count=${msgs_count}

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return
    ...     subject_comparator=Is Empty
    Should Be Equal As Integers  ${tracking_messages_count}  ${msgs_count}

Tvh662498c
    [Documentation]  Verify that all searches above are case insensitive\n
    ...  http://tims.cisco.com/warp.cmd?ent=480913
    [Tags]  Tvh662498c  erts
    [Setup]  Setup Tvh662498c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662498c

    Wait Until SMA Gets Tracking Data

    FOR  ${mail_sender_in_case}  IN  ${MAIL_RCPT_FROM.lower()}  ${MAIL_RCPT_FROM.upper()}
      ${tracking_messages_count}=  Email Tracking Search and Return  sender_data=${mail_sender_in_case}
      Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}
    END
    FOR  ${mail_sender_in_case}  IN  ${MAIL_RCPT_TO.lower()}  ${MAIL_RCPT_TO.upper()}
      ${tracking_messages_count}=  Email Tracking Search and Return  rcpt_data=${mail_sender_in_case}
      Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}
    END
    FOR  ${message_in_case}  IN  ${MESSAGE_SUBJECT.lower()}  ${MESSAGE_SUBJECT.upper()}
      ${tracking_messages_count}=  Email Tracking Search and Return  subject_data=${message_in_case}
      Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}
    END

Tvh480881c
    [Documentation]  Verify MID drilldown\n
    ...  http://tims.cisco.com/warp.cmd?ent=480881
    [Tags]  Tvh480881c  erts
    [Setup]  Setup Tvh480881c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh480881c

    Switch to ESA
    Roll Over Now
    Inject Messages  num-msgs=${MSG_COUNT}  inject-host=${PUBLIC_LISTENER_IP}
    ...  mail-from=${MAIL_FROM_VAR}
    ${mid_value}=  Get Mid Value  MID .* ICID .* From: <${TEST_NAME}@${CLIENT}>

    Switch to SMA
    Wait Until SMA Gets Tracking Data
    ${messages}=  Email Message Tracking Search  ironport_mid=${mid_value}
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Integers  ${tracking_message_count}  ${MSG_COUNT}

Tvh662489c
    [Documentation]  Verify Message Events drilldown (Spam Positive checkbox)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480908
    [Tags]  Tvh662489c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662489c

    ${msgs_count}=  Set Variable  5
    @{checkboxes}=  Create List  spam positive
    Inject ${msgs_count} Messages From ${SPAM}
    Inject ${msgs_count} Messages From ${CLEAN}
    Verify ${msgs_count} Messages Filtered By Message Events ${checkboxes}

Tvh662471c
    [Documentation]  Verify Message Events drilldown (Suspect Spam checkbox)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480898
    [Tags]  Tvh662471c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662471c

    ${msgs_count}=  Set Variable  5
    @{checkboxes}=  Create List  suspect spam
    Inject ${msgs_count} Messages From ${SPAM_SUSPECT}
    Inject ${msgs_count} Messages From ${CLEAN}
    Verify ${msgs_count} Messages Filtered By Message Events ${checkboxes}

Tvh662487c
    [Documentation]  Verify Message Events drilldown (Virus Positive checkbox)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480901
    [Tags]  Tvh662487c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662487c

    ${msgs_count}=  Set Variable  5
    @{checkboxes}=  Create List  virus positive
    Inject ${msgs_count} Messages From ${TESTVIRUS}
    Inject ${msgs_count} Messages From ${CLEAN}
    Verify ${msgs_count} Messages Filtered By Message Events ${checkboxes}

Tvh662494c
    [Documentation]  Verify Message Events drilldown (Delivered checkbox)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480890
    [Tags]  Tvh662494c  erts
    [Setup]  Initialize Tvh662494c
    [Teardown]  Finalize Tvh662494c
    Set Test Variable  ${TEST_ID}  Tvh662494c

    ${msgs_count}=  Set Variable  5
    ${log_pattern}=  Set Variable  Info: Message done DCID
    @{checkboxes}=  Create List  delivered

    FOR  ${arg}  IN  ${None}  hard_bounce=100
      Null Smtpd Start  ${arg}
      Inject Messages
      ...  num-msgs=${msgs_count}
      ...  inject-host=${PRIVATE_LISTENER_IP}
      Run Keyword If  '${arg}' == '${None}'  Deliver Now All
      Run Keyword If  '${arg}' == '${None}'  Sleep  5
      Null Smtpd Stop
    END
    Verify And Wait For Log Records  ${log_pattern} >= ${msgs_count}
    Switch TO SMA
    Verify ${msgs_count} Messages Filtered By Message Events ${checkboxes}

Tvh662509c
    [Documentation]  Verify Message Events drilldown (Hard bounced checkbox)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480914
    [Tags]  Tvh662509c  erts
    [Setup]  Initialize Tvh662494c
    [Teardown]  Finalize Tvh662494c
    Set Test Variable  ${TEST_ID}  Tvh662509c

    ${msgs_count}=  Set Variable  5
    ${log_pattern}=  Set Variable  Info: Bounced: DCID
    @{checkboxes}=  Create List  hard bounced

    FOR  ${arg}  IN  ${None}  hard_bounce=100
      Null Smtpd Start  ${arg}
      Inject Messages
      ...  num-msgs=${msgs_count}
      ...  inject-host=${PRIVATE_LISTENER_IP}
      Run Keyword If  '${arg}' == '${None}'  Deliver Now All
      Run Keyword If  '${arg}' == '${None}'  Sleep  5
      Null Smtpd Stop
    END
    Verify And Wait For Log Records  ${log_pattern} >= ${msgs_count}
    Switch TO SMA
    Verify ${msgs_count} Messages Filtered By Message Events ${checkboxes}

Tvh662479c
    [Documentation]  Verify Message Events drilldown (Soft bounced checkbox)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=480885
    [Tags]  Tvh662479c  erts
    [Setup]  Initialize Tvh662494c
    [Teardown]  Finalize Tvh662494c
    Set Test Variable  ${TEST_ID}  Tvh662479c

    ${msgs_count}=  Set Variable  5
    ${log_pattern}=  Set Variable  Info: Delayed: DCID
    @{checkboxes}=  Create List  soft bounced

    FOR  ${arg}  IN  ${None}  soft_bounce=100
      Null Smtpd Start  ${arg}
      Inject Messages
      ...  num-msgs=${msgs_count}
      ...  inject-host=${PRIVATE_LISTENER_IP}
      Run Keyword If  '${arg}' == '${None}'  Deliver Now All
      Run Keyword If  '${arg}' == '${None}'  Sleep  5
      Null Smtpd Stop
    END
    Verify And Wait For Log Records  ${log_pattern} >= ${msgs_count}
    Switch TO SMA
    Verify ${msgs_count} Messages Filtered By Message Events ${checkboxes}

Tvh662453c
    [Documentation]  Verify Message Events drilldown
    ...  (Currently in Outbreak Quarantine checkbox)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=662453
    [Tags]  Tvh662453c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662453c

    ${msgs_count}=  Set Variable  5
    ${log_pattern}=  Set Variable  Outbreak Filters: verdict positive
    @{checkboxes}=  Create List  currently in outbreak quarantine

    Inject ${msgs_count} Messages From ${VOF_ALL}
    Inject ${msgs_count} Messages From ${CLEAN}

    Switch To ESA
    Verify And Wait For Log Records  ${log_pattern} >= ${msgs_count}
    Switch TO SMA
    Verify ${msgs_count} Messages Filtered By Message Events ${checkboxes}

Tvh662501c
    [Documentation]  Verify that search result is narrowed if multiple
    ...  checkboxes are selected for Message Event field\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=662501
    [Tags]  Tvh662501c  erts
    [Setup]  Initialize Tvh662494c
    [Teardown]  Finalize Tvh662494c
    Set Test Variable  ${TEST_ID}  Tvh662501c
    ${spam_count}=  Set Variable  1
    ${suspect_spam_count}=  Set Variable  2
    ${virus_count}=  Set Variable  3
    ${vof_count}=  Set Variable  4
    ${deliverd_count}=  Set Variable  5
    ${soft_bounced_count}=  Set Variable  6
    @{checkboxes_set1}=  Create List  delivered  soft bounced  spam positive
    @{checkboxes_set2}=  Create List  soft bounced  virus positive  suspect spam
    @{checkboxes_set3}=  Create List  delivered  virus positive  currently in outbreak quarantine

    FOR  ${mbox}  ${msgs_count}  IN
    ...  ${SPAM}          ${spam_count}
    ...  ${SPAM_SUSPECT}  ${suspect_spam_count}
    ...  ${TESTVIRUS}     ${virus_count}
    ...  ${VOF_ALL}       ${vof_count}
      Inject ${msgs_count} Messages From ${mbox}
    END
    FOR  ${arg}  ${msgs_count}  IN
    ...  ${None}            ${deliverd_count}
    ...  soft_bounce=100    ${soft_bounced_count}
      Null Smtpd Start  ${arg}
      Inject Messages
      ...  num-msgs=${msgs_count}
      ...  inject-host=${PRIVATE_LISTENER_IP}
      Run Keyword If  '${arg}' == '${None}'  Deliver Now All
      Run Keyword If  '${arg}' == '${None}'  Sleep  5
      Null Smtpd Stop
    END
    Switch To ESA
    FOR  ${log_pattern}  ${msgs_count}  IN
    ...  interim verdict using engine: CASE spam positive  ${spam_count}
    ...  interim verdict using engine: CASE spam suspect  ${suspect_spam_count}
    ...  antivirus positive  ${virus_count}
    ...  Outbreak Filters: verdict positive  ${vof_count}
    ...  Info: Message done DCID  ${deliverd_count}
    ...  Info: Delayed: DCID  ${soft_bounced_count}
      Verify And Wait For Log Records  ${log_pattern} >= ${msgs_count}
    END
    Switch TO SMA
    Wait Until SMA Gets Tracking Data
    FOR  ${checkboxes}  ${msgs_count}  IN
    ...  ${checkboxes_set1}  ${${deliverd_count}+${soft_bounced_count}+${spam_count}}
    ...  ${checkboxes_set2}  ${${soft_bounced_count}+${virus_count}+${suspect_spam_count}}
    ...  ${checkboxes_set3}  ${${deliverd_count}+${virus_count}+${vof_count}}
      ${messages}=  Email Message Tracking Search  message_event=${checkboxes}
      ${tracking_msgs_count}=  Email Message Tracking Get Total Result Count  ${messages}
      Should Be Equal As Integers  ${tracking_msgs_count}  ${msgs_count}
    END

Tvh662475c
    [Documentation]  Verify Message ID header drilldown\n
    ...  http://tims.cisco.com/warp.cmd?ent=662475
    [Tags]  Tvh662475c  erts
    [Setup]  Setup Tvh480881c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662475c

    Switch to ESA
    Roll Over Now
    Inject Messages  num-msgs=${MSG_COUNT}  inject-host=${PUBLIC_LISTENER_IP}
    ...  mail-from=${MAIL_FROM_VAR}

    ${mid_value}=  Get Mid Value  MID .* ICID .* From: <${TEST_NAME}@${CLIENT}>
    ${mid_header}=  Get Message ID Header Value  MID ${mid_value} Message-ID .*

    Switch to SMA
    Wait Until SMA Gets Tracking Data
    FOR  ${mid_header_value}  IN  ${mid_header}  <${mid_header}>
      ${messages}=  Email Message Tracking Search  mesg_id_header=${mid_header_value}
      ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
      Should Be Equal As Integers  ${tracking_message_count}  ${MSG_COUNT}
    END

Tvh662503c
    [Documentation]  Verify Date and Time range drilldown\n
    ...  (search for last days)
    ...  http://tims.cisco.com/warp.cmd?ent=662503
    [Tags]  Tvh662503c  erts
    [Setup]  Setup Tvh480881c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662503c

    ${cur_time} =  Set Time
    ${six_days_var}=  Set Variable  6
    ${twelve_days_var}=  Set Variable  12
    ${week_ago_var}=  Calculate Shifted Datetime  ${six_days_var}  cur_time=${cur_time}
    ${weeks_ago_var}=  Calculate Shifted Datetime  ${twelve_days_var}  cur_time=${cur_time}

    FOR  ${period}  IN  ${${six_days_var}-1}  ${${twelve_days_var}-1}
      ${date_offset}=  Calculate Shifted Datetime  ${period}  cur_time=${cur_time}
      Set Time  ${date_offset}
      Inject Messages  num-msgs=${MSG_COUNT}  inject-host=${PUBLIC_LISTENER_IP}
      ...  mail-from=${MAIL_FROM_VAR}
    END
    Sync Appliances Datetime  ${SMA}  ${ESA}
    Wait Until SMA Gets Tracking Data

    FOR  ${period}  ${emsg_count}  IN
    ...  ${week_ago_var[:-9]}  1
    ...  ${weeks_ago_var[:-9]}  2
      ${messages}=  Email Message Tracking Search  mesg_received=custom range
      ...  start_date=${period}
      ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
      Should Be Equal As Integers  ${tracking_message_count}  ${emsg_count}
    END

Tvh662474c
    [Documentation]  Verify Date and Time range drilldown\n
    ...  (search for current day)
    ...  http://tims.cisco.com/warp.cmd?ent=662474
    [Tags]  Tvh662474c  erts
    [Setup]  Setup Tvh480881c
    [Teardown]  General Test Case Teardown

    Set Test Variable  ${TEST_ID}  Tvh662474c

    Sync Appliances Datetime  ${SMA}  ${ESA}
    ${six_hours_var}=  Set Variable  6
    ${thirty_hours_var}=  Set Variable  30
    ${cur_time} =  Set Time
    ${hours_ago_var}=  Calculate Shifted Datetime  ${six_hours_var}  cur_time=${cur_time}
    ...  offset_with=hours
    ${day_ago_var}=  Calculate Shifted Datetime  ${thirty_hours_var}  cur_time=${cur_time}
    ...  offset_with=hours

    FOR  ${period}  IN  ${${six_hours_var}-1}  ${${thirty_hours_var}-1}
      ${date_offset}=  Calculate Shifted Datetime  ${period}  cur_time=${cur_time}
      ...  offset_with=hours
      Set Time  ${date_offset}
      Inject Messages  num-msgs=${MSG_COUNT}  inject-host=${PUBLIC_LISTENER_IP}
      ...  mail-from=${MAIL_FROM_VAR}
      Wait Until SMA Gets Tracking Data
    END
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Wait Until SMA Gets Tracking Data Count
    Sync Appliances Datetime  ${SMA}  ${ESA}

    FOR  ${period}  ${time}  ${emsg_count}  IN
    ...  ${hours_ago_var[:-9]}  ${hours_ago_var[-8:-3]}  1
    ...  ${day_ago_var[:-9]}  ${day_ago_var[-8:-3]}  2
      Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
      ...  Verify Tracking Count  ${period}  ${time}  ${emsg_count}
    END

Tvh662472c
    [Documentation]  Verify Message Events drilldown
    ...  (DLP Violations checkbox + specified DLP policy name)\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=662472
    [Tags]  Tvh662472c  erts
    [Setup]  Initialize Tvh662472c
    [Teardown]  Finalize Tvh662472c
    Set Test Variable  ${TEST_ID}  Tvh662472c

    ${msgs_count}=  Set Variable  5
    ${log_pattern}=  Set Variable  Dropped by DLP
    @{checkboxes}=  Create List  dlp violations

    FOR  ${mbox}  IN  ${CLEAN}  ${ZIP_ATTACHMENT_WITH_EXCELFILE}
      Inject Messages
      ...  mbox-filename=${mbox}
      ...  num-msgs=${msgs_count}
      ...  inject-host=${PRIVATE_LISTENER_IP}
    END
    Verify And Wait For Log Records  ${log_pattern} >= ${msgs_count}
    Switch TO SMA
    Wait Until SMA Gets Tracking Data
    ${messages}=  Email Message Tracking Search
    ...  message_event=${checkboxes}  dlp_policy=${DLP_POLICY_NAME}
    ${tracking_msgs_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Integers  ${tracking_msgs_count}  ${msgs_count}

Tvh663540c
    [Documentation]  Verify the option of Message Tracking search UI
    ...   which allows you to search DLP messages\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=663540
    [Tags]  Tvh663540c  erts
    [Setup]  Initialize Tvh662472c
    [Teardown]  Finalize Tvh662472c
    Set Test Variable  ${TEST_ID}  Tvh663540c

    ${msgs_count}=  Set Variable  5
    ${log_pattern}=  Set Variable  Dropped by DLP
    @{checkboxes}=  Create List  dlp violations
    @{low_severity}=  Create List  low
    @{medium_severity}=  Create List  medium
    @{high_severity}=  Create List  high
    @{critical_severity}=  Create List  critical

    Inject Messages
    ...  mbox-filename=${ZIP_ATTACHMENT_WITH_EXCELFILE}
    ...  num-msgs=${msgs_count}
    ...  inject-host=${PRIVATE_LISTENER_IP}

    Verify And Wait For Log Records  ${log_pattern} >= ${msgs_count}
    Switch TO SMA
    Wait Until SMA Gets Tracking Data
    FOR  ${severity}  IN  ${low_severity}  ${medium_severity}
    ...  ${high_severity}  ${critical_severity}
      ${messages}=  Email Message Tracking Search
      ...  message_event=${checkboxes}
      ...  dlp_policy=${DLP_POLICY_NAME}
      ...  dlp_violation_severities=${severity}
      ${tracking_msgs_count}=  Email Message Tracking Get Total Result Count  ${messages}
      Run Keyword If  ${severity} == ${high_severity}
      ...  Should Be Equal As Integers  ${tracking_msgs_count}  ${msgs_count}
      Run Keyword If  ${severity} != ${high_severity}
      ...  Should Be Equal As Integers  ${tracking_msgs_count}  0
    END

Tvh662482c
    [Documentation]  Verify HOST drilldown
    ...  http://tims.cisco.com/warp.cmd?ent=480887
    [Tags]  Tvh662482c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662482c

    ${msg_count}  Set Variable  2
    Inject Messages  num-msgs=${msg_count}  inject-host=${PUBLIC_LISTENER_IP}
    Wait Until SMA Gets Tracking Data

    ${messages}=  Email Message Tracking Search  cisco_ironport_host=${ESA}
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Strings  ${tracking_message_count}  ${msg_count}

Tvh662452c
    [Documentation]  Verify Sender IP drilldown
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662452c
    [Tags]  Tvh662452c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662452c

    ${d1_client_ip}=  Get Host IP By Name  ${CLIENT}
    ${msg_count}  Set Variable  10
    Inject Messages  num-msgs=${msg_count}  inject-host=${PUBLIC_LISTENER_IP}
    Wait Until SMA Gets Tracking Data

    ${messages}=  Email Message Tracking Search  sender_ip=${d1_client_ip}
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Strings  ${tracking_message_count}  ${msg_count}

Tvh662462c
    [Documentation]  Verify Subject drilldown (for non-ASCII subjects)
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662462c
    [Tags]  Tvh662462c  erts
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662462c

    ${msg_count}  Set Variable  10
    ${non_ascii_subject}=  Evaluate  u'\\u0421\\u0430\\u0431\\u0434\\u0436\\u0435\\u043a\\u0442'
    ${unicode_subject_mbox}=  Join Path  ${SUITE_TMP_DIR}  unicode_subject.mbox
    Create Plain Text MBOX  ${unicode_subject_mbox}
    ...  ${non_ascii_subject}  ${TEST_NAME}  UTF-8

    Inject Messages  num-msgs=${msg_count}  inject-host=${PUBLIC_LISTENER_IP}
    ...  mbox-filename=${unicode_subject_mbox}
    Wait Until SMA Gets Tracking Data

    ${messages}=  Email Message Tracking Search  subject_data=${non_ascii_subject}
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Strings  ${tracking_message_count}  ${msg_count}

Tvh662507c
    [Documentation]  SETUP
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662507c
    [Tags]  Tvh662507c  erts
    [Setup]  Initialize Tvh662507c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662507c

    Wait Until SMA Gets Tracking Data
    ${messages}=  Email Message Tracking Search  mesg_received=last day
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Integers  ${tracking_message_count}  ${MSG_COUNT}

Tvh662495c
    [Documentation]  Verify Message Events drilldown (DLP Violations checkbox)
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662495c
    [Tags]  Tvh662495c  erts
    [Setup]  Initialize Tvh662495c
    [Teardown]  Finalize Tvh662495c
    Set Test Variable  ${TEST_ID}  Tvh662495c

    Switch To ESA
    Inject Custom Messages  mail_body=Hi, ${CLIENT}, ${MATCHED_WORD}
    ...  inject_host=${PRIVATE_LISTENER_IP}
    ${mid}=  Get Mid Value  MID .* DLP violation

    Switch To SMA
    Wait Until SMA Gets Tracking Data
    Verify ${MSG_COUNT} Messages Filtered By Message Events ${MSG_EVENT}
    Click Link  Show Details  don't wait
    Select Window  Message Details
    Page Should Contain  Message ${mid} aborted: Dropped by DLP

Tvh662465c
    [Documentation]  Verify drilldown using multiple criterias
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662465c
    [Tags]  Tvh662465c  erts
    [Setup]  Initialize Tvh662495c
    [Teardown]  Finalize Tvh662495c
    Set Test Variable  ${TEST_ID}  Tvh662465c

    Switch To ESA
    Inject Custom Messages  mail_body=Hi, ${CLIENT}, ${MATCHED_WORD}
    ...  subject=${TEST_NAME}  inject_host=${PRIVATE_LISTENER_IP}
    ${mid_value}=  Get Mid Value  MID .* DLP violation
    ${mid_header}=  Get Message ID Header Value  MID ${mid_value} Message-ID .*

    Switch To SMA
    Wait Until SMA Gets Tracking Data

    ${messages}=  Email Message Tracking Search  sender_data=${CLIENT}  sender_comparator=Contains
    ...  subject_data=${TEST_NAME}  message_event=${MSG_EVENT}
    ...  mesg_id_header=${mid_header}  ironport_mid=${mid_value}
    ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Integers  ${tracking_message_count}  ${MSG_COUNT}

Tvh662468c
    [Documentation]  Verify that Sender IP drilldown works\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662468c
    [Tags]  Tvh662468c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh664098c
    [Teardown]  Finalize Tvh664098c
    Set Test Variable  ${TEST_ID}  Tvh662468c

    ${d1_client_ip}=  global_sma.Get Host IP By Name  ${CLIENT}
    ${d1_ip}=  Catenate  SEPARATOR=.  d1  ${CLIENT}
    ${status}  ${d1_client_ip1}=  Run Keyword And Ignore Error  global_sma.Get Host IP By Name  ${d1_ip}
    ${msg_count}  Set Variable  10
    Switch To ESA
    Inject Messages  rcpt-host-list=${CLIENT}  num-msgs=${msg_count}  inject-host=${PUBLIC_LISTENER_IP}
    Switch To SMA
    Wait Until SMA Gets Tracking Data
    ${mesges}=  Email Message Tracking Search  sender_ip=${d1_client_ip}
    Log  ${mesges}
    ${mesges1}=  Email Message Tracking Search  sender_ip=${d1_client_ip1}
    ${tracking_message_count_mesges}=  Email Message Tracking Get Total Result Count  ${mesges}
    ${tracking_message_count_mesges1}=  Email Message Tracking Get Total Result Count  ${mesges1}
    ${tracking_message_count}=  Set Variable If  ${tracking_message_count_mesges} == 0
    ...  ${tracking_message_count_mesges1}  ${tracking_message_count_mesges}
    Should Be Equal As Strings  ${tracking_message_count}  ${msg_count}

Tvh664098c
    [Documentation]  Verify the admin can search attachment names in message tracking\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh664098c
    [Tags]  Tvh664098c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh664098c
    [Teardown]  Finalize Tvh664098c
    Set Test Variable  ${TEST_ID}  Tvh664098c

    ${msgs_count}=  Set Variable  5
    ${log_pattern}=  Set Variable  Dropped by DLP
    @{checkboxes}=  Create List  dlp violations
    Inject Messages
    ...  rcpt-host-list=${CLIENT}
    ...  mbox-filename=${ZIP_ATTACHMENT_WITH_EXCELFILE}
    ...  num-msgs=${msgs_count}
    ...  inject-host=${PRIVATE_LISTENER_IP}

    Switch TO SMA
    Wait Until SMA Gets Tracking Data
    ${messages}=  Email Message Tracking Search
    ...  attachment_name=dict_excel.zip
    ${tracking_msgs_count}=  Email Message Tracking Get Total Result Count  ${messages}
    Should Be Equal As Integers  ${tracking_msgs_count}  ${msgs_count}

Tvh663795c
    [Documentation]  Verify the option of Message Tracking search UI
    ...   which allows you to search DLP messages\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=663795
    [Tags]  Tvh663795c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh662472c
    [Teardown]  Finalize Tvh662472c
    Set Test Variable  ${TEST_ID}  Tvh663795c

    ${msgs_count}=  Set Variable  5
    ${log_pattern}=  Set Variable  Dropped by DLP
    @{checkboxes}=  Create List  dlp violations
    @{low_severity}=  Create List  low
    @{medium_severity}=  Create List  medium
    @{high_severity}=  Create List  high
    @{critical_severity}=  Create List  critical

    Inject Messages
    ...  rcpt-host-list=${CLIENT}
    ...  mbox-filename=${ZIP_ATTACHMENT_WITH_EXCELFILE}
    ...  num-msgs=${msgs_count}
    ...  inject-host=${PRIVATE_LISTENER_IP}

    Switch TO SMA
    Wait Until SMA Gets Tracking Data
    FOR  ${severity}  IN  ${low_severity}  ${medium_severity}
    ...  ${high_severity}  ${critical_severity}
      ${messages}=  Email Message Tracking Search
      ...  message_event=${checkboxes}
      ...  dlp_policy=${DLP_POLICY_NAME}
      ...  dlp_violation_severities=${severity}
      ${tracking_msgs_count}=  Email Message Tracking Get Total Result Count  ${messages}
      Run Keyword If  ${severity} != ${high_severity}
      ...  Should Be Equal As Integers  ${tracking_msgs_count}  0
      Run Keyword If  ${severity} == ${high_severity}
      ...  Should Be Equal As Integers  ${tracking_msgs_count}  ${msgs_count}
    END

Tvh662477c
    [Documentation]  Verify Date and Time range drilldown\n
    ...  (search for a month)
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662477c
    [Tags]  Tvh662477c  srts  wsrts  1ESA1SMA
    [Setup]  General Test Case Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662477c
	
    Inject Messages
    ...  mail-from=${TEST_NAME}@${CLIENT}
    ...  rcpt-host-list=${CLIENT_HOSTNAME}
    ...  num-msgs=1
    ...  mbox-filename=${CLEAN}
    ...  inject-host=${PUBLIC_LISTENER_IP}
    
    ${output} =  Wait Until Keyword Succeeds  5 min  10 sec
    ...  Verify Messsage Tracking Data Not Empty
    Log  ${output}

    ${result_str}=  Convert To String  ${results}
    Should Contain  ${result_str}  Ip: ${ESA_IP}
    Should Contain  ${result_str}  Description: ${ESA}

Tvh662510c
    [Documentation]  Verify that each search result contains "Show Details" link
    ...  during upgrade\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662510c
    [Tags]  srts  Tvh662510c  wsrts  1ESA1SMA
    [Setup]  Do Tvh662499c Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662510c

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  sender_data=${MAIL_FROM_VAR}
    ...  sender_comparator=Begins With
    Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}
    ${show_details_count}=  Get Matching Xpath Count  //a[contains(text(),'Show Details')]
    Should Be Equal  ${show_details_count}  ${MESSAGE_COUNT}

Tvh662499c
    [Documentation]  verify that query for messages is really canceled and no results appear\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662499c
    [Tags]  srts  wsrts  Tvh662499c  1ESA1SMA
    [Setup]  Do Tvh662499c Setup
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662499c

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  sender_data=${MAIL_FROM_VAR}
    ...  sender_comparator=Begins With
    Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}
    Navigate To  Message Tracking  Message Tracking
    Click Element  //input[@id='clearButton']
    Page Should Not Contain Element  //span[contains(text(),'Generated')]

Tvh662451c
    [Documentation]  Verify that messages search works with
    ...  "Max. results returned" specifier
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662451c
    [Tags]  Tvh662451c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh662451c
    [Teardown]  Run Keywords
    ...  Smtp Session Spoof Disable
    Set Test Variable  ${TEST_ID}  Tvh662451c
    ${fname}=  Smtp Session Spoof Prepare Ips File  netmask=19  strict=${False}
    Smtp Session Spoof Enable  ${PUBLIC_LISTENER.name}  ${fname}

    Generate Email Reporting Data
    ...  rcpt-host-list=${CLIENT}
    ...  inject-host=${PUBLIC_LISTENER_IP}
    ...  max-msgs-per-conn=1
    ...  ${CLEAN}=100
    ...  ${SPAM}=100
    ...  ${TESTVIRUS}=100
    ...  ${SPAM_SUSPECT}=100
    ...  ${MARKETING}=100
    ...  ${VOFAUTO_MANUAL}=100
    ...  ${VOF_ALL}=100

    # for max_results=1000 - looping over ~50 pages will take a lot of time
    # maybe 500 would be enough???
    FOR  ${value}  IN  250  500
      Wait Until Keyword Succeeds
      ...  15 min
      ...  0 sec
      ...  Do Search Tvh662451c  ${value}
    END

Tvh662478c
    [Documentation]  verify that search results contain only rejected connections
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662478c
    [Tags]  Tvh662478c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh662478c
    [Teardown]  Finalize Tvh662478c
    Set Test Variable  ${TEST_ID}  Tvh662478c

    ${d1_client_ip}=  Get Host IP By Name  ${CLIENT}
    ${d1_ip}=  Catenate  SEPARATOR=.  d1  ${CLIENT}
    ${status}  ${d1_client_ip1}=  Run Keyword And Ignore Error  Get Host IP By Name  ${d1_ip}
    Set Suite Variable  ${d1_client_ip}
    Set Suite Variable  ${d1_client_ip1}
    Set Test Variable  ${msg_count}  2
    Inject Messages  num-msgs=${msg_count}  max-msgs-per-conn=1  inject-host=${PUBLIC_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}

    Switch To SMA
    Log Out Of Dut
    Close Browser
    Launch Dut Browser
    Log Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    Wait Until Keyword Succeeds
    ...  20 min
    ...  10 sec
    ...  Do Search Tvh662478c

Tvh662455c
    [Documentation]  verify that Show Details link is displayed for every ICID
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662455c
    [Tags]  Tvh662455c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh662455c
    [Teardown]  Finalize Tvh662455c
    Set Test Variable  ${TEST_ID}  Tvh662455c

    ${d1_client_ip}=  Get Host IP By Name  ${CLIENT}
    ${d1_ip}=  Catenate  SEPARATOR=.  d1  ${CLIENT}
    ${status}  ${d1_client_ip1}=  Run Keyword And Ignore Error  Get Host IP By Name  ${d1_ip}
    Set Suite Variable  ${d1_client_ip}
    Set Suite Variable  ${d1_client_ip1}
    Set Test Variable  ${msg_count}  2
    Switch To ESA
    Roll Over Now  mail_logs
    Null Smtpd Start
    Inject Messages  num-msgs=${msg_count}  max-msgs-per-conn=1  inject-host=${PUBLIC_LISTENER_IP}
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    Null Smtpd Stop
    Switch To SMA
    Wait Until Keyword Succeeds
    ...  15 min
    ...  10 sec
    ...  Do Search Tvh662455c
    ${show_details_count} =  Get Matching Xpath Count  //a[contains(text(),'Show Details')]
    Should Be Equal  ${show_details_count}  ${msg_count}

Tvh663864c
    [Documentation]  Verify that all violations due to content in
     ...  the headers will be attributed in Message Details on Message
     ...  Tracking page and shown in processing details\n
     ...  http://tims.cisco.com/view-entity.cmd?ent=Tvh663864c
    [Tags]  Tvh663864c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh663864c
    [Teardown]  Finalize Tvh663864c
    Set Test Variable  ${TEST_ID}  Tvh663864c

    ${msgs_count}=  Set Variable  1
    @{checkboxes}=  Create List  dlp violations
    @{low_severity}=  Create List  low

    ${MBOX_MATCH}=  Join Path  ${SUITE_TMP_DIR}  dlp_subject_match.mbox
    Create Plain Text MBOX  ${MBOX_MATCH}
    ...  test DLP ${TEST_NAME}  This is a test message to check DLP
    Set Test Variable  ${MBOX_MATCH}

    Inject Messages  inject-host=${PRIVATE_LISTENER_IP}  num-msgs=${msgs_count}
    ...  rcpt-host-list=${CLIENT}  mail-from=test@${CLIENT}
    ...  mbox-filename=${MBOX_MATCH}

    Verify And Wait For Log Records
    ...  MID .* Subject 'test DLP ${TEST_NAME}' >= ${msgs_count}
    ...  MID .* DLP violation >= ${msgs_count}
    ...  MID .* quarantined to \\"Policy\\" \\(DLP violation\\) >= ${msgs_count}

    Switch TO SMA
    Wait Until SMA Gets Tracking Data
    ${messages}=  Email Message Tracking Search
    ...  message_event=${checkboxes}
    ...  dlp_policy=${DLP_POLICY_NAME}
    ...  dlp_violation_severities=${low_severity}
    Log  ${messages}

    ${tracking_msgs_count}=  Email Message Tracking Get Total Result Count
    ...  ${messages}
    Should Be Equal As Integers  ${tracking_msgs_count}  ${msgs_count}

Tvh662485c
    [Documentation]  Verify Envelope Sender drilldown ("Is" criteria)\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662485c
    [Tags]  Tvh662485c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh662485c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662485c

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  sender_data=${MAIL_FROM_VAR}
    ...  sender_comparator=Is
    Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}

Tvh662504c
    [Documentation]  Verify Envelope Recipient drilldown ("Contains" criteria)\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662504c
    [Tags]  Tvh662504c  srts  wsrts  1ESA1SMA
    [Setup]  Initialize Tvh662504c
    [Teardown]  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662504c

    ${tracking_messages_count}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Tracking Search and Return  rcpt_data=${MAIL_RCPT_TO}
    ...  rcpt_comparator=Contains
    Should Be Equal As Integers  ${tracking_messages_count}  ${MESSAGE_COUNT}

Tvh662469c
    [Documentation]  Verify that connections search works with
    ...  "Max. results returned" specifier\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh662469c
    [Tags]  Tvh662469c  srts  wsrts  1ESA1SMA
    [Setup]  General Test Case Setup
    [Teardown]  Run Keywords
    ...  Smtp Session Spoof Disable
    ...  General Test Case Teardown
    Set Test Variable  ${TEST_ID}  Tvh662469c

    Switch To ESA
    Message Tracking Edit Settings  tracking=local  track_info_for_rej_conn=${True}
    Commit Changes

    ${fname}=  Smtp Session Spoof Prepare Ips File  netmask=19  strict=${False}
    Smtp Session Spoof Enable  ${PUBLIC_LISTENER.name}  ${fname}

    Generate Email Reporting Data
    ...  rcpt-host-list=${CLIENT}
    ...  inject-host=${PUBLIC_LISTENER_IP}
    ...  max-msgs-per-conn=1
    ...  ${CLEAN}=100
    ...  ${SPAM}=100
    ...  ${TESTVIRUS}=100
    ...  ${SPAM_SUSPECT}=100
    ...  ${MARKETING}=100
    ...  ${VOFAUTO_MANUAL}=100
    ...  ${VOF_ALL}=100

    FOR  ${value}  IN  250  500
      Wait Until Keyword Succeeds
      ...  15 min
      ...  0 sec
      ...  Do Search Tvh662469c  ${value}
    END
