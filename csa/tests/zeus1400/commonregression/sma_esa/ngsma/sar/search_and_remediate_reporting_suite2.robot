*** Settings ***
Resource     sma/sar_sma.txt

Suite Setup  Sar Suite Setup
Suite Teardown  Sar Suite Teardown
*** Variables ***
${action_delete}=  Delete
${action_forward}=  Forward
${action_forward_delete}=  Forward and Delete

*** Keywords ***
Verify Logs For Remediation No Message Mailbox Fail
    [Arguments]  ${mid}
    ...  ${user_name}
    ...  ${batch_name}
    ...  ${action}
    ...  ${remediation_status}
    ...  ${profile_name}
    ...  ${mail_addr}

    Verify Log Contains Records
    ...  search_path=mail
    ...  timeout=90
    ...  Message ${mid} was initiated for '${action}' remedial action by '${user_name}' from source '${SMA}' in batch '${batch_name}'. >= 1
    ...  Message ${mid} was processed with '${action}' remedial action for recipient '${mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}. Reason: Message not found in user mailbox >=1

    Verify Log Contains Records
    ...  search_path=remediation
    ...  timeout=90
    ...  MID: ${mid} Remediation was skipped after attempting with \\`${profile_name}\\` profile for recipient ${mail_addr}. >= 1 

Verify Logs For Remediation No Domain Map Fail
    [Arguments]  ${mid}
    ...  ${user_name}
    ...  ${batch_name}
    ...  ${action}
    ...  ${remediation_status}
    ...  ${profile_name}
    ...  ${mail_addr1}
    ...  ${mail_addr}=${EMAIL_ADDRESS}

    Verify Log Contains Records
    ...  search_path=mail
    ...  timeout=90
    ...  Message ${mid} was initiated for '${action}' remedial action by '${user_name}' from source '${SMA}' in batch '${batch_name}'. >= 1
    ...  Message ${mid} was processed with '${action}' remedial action for recipient '${mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}. Reason: No profiles mapped for domain >=1

    Verify Log Contains Records
    ...  search_path=remediation
    ...  timeout=90
    ...  MID: ${mid} Skipping mailbox remedial action since domain map is not configured for recipient's .*domain. >= 1

Verify Logs For Messages Remediation No Domain Map Fail
    [Arguments] 
    ...  ${user_name}
    ...  ${batch_name}
    ...  ${action}
    ...  ${remediation_status}
    ...  ${profile_name}
    ...  ${mail_addr1}
    ...  ${num_msgs}
    ...  ${mail_addr}=${EMAIL_ADDRESS}

    Verify Log Contains Records
    ...  search_path=mail
    ...  timeout=90
    ...  Message .* was initiated for '${action}' remedial action by '${user_name}' from source '${SMA}' in batch '${batch_name}'. >= ${num_msgs}
    ...  Message .* was processed with '${action}' remedial action for recipient '${mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}. Reason: No profiles mapped for domain >= ${num_msgs}

    Verify Log Contains Records
    ...  search_path=remediation
    ...  timeout=90
    ...  MID: .* Skipping mailbox remedial action since domain map is not configured for recipient's .*domain. >= ${num_msgs}

Verify MOR Reporting Summary Count
    [Arguments]  ${num_msgs}  
    ...  ${num_batches}
    ...  ${batch_delete}=None
    ...  ${batch_forward}=None  
    ...  ${batch_forward_delete}=None
    ...  ${batch_fail}=None

    ${rem_rep_summary}=  SMANGGuiLibrary.Remediation Report Summary
    ${batch_count}=    SMANGGuiLibrary.Remediation Batch Count
    ${batches_details}=  SMANGGuiLibrary.Remediation Batches Detail
    ${num_batch} =  Convert To Integer  ${num_batches}
    LogMany  ${batches_details}

    ${forward_count}=  Set Variable  0
    ${delete_count}=   Set Variable  0
    ${forward_delete_count}=  Set Variable  0
    ${failed_count}=  Set Variable  0

    FOR    ${key}    IN    @{batches_details.keys()}
       ${forward_count}=  Run Keyword If    '${batches_details['${key}']['Batch Name']}'== '${batch_forward}'  Set Variable  '${batches_details['${key}']['Message Status']['Messages Forwarded']}'
    ...   ELSE  Set Variable  ${forward_count}
       ${delete_count}=  Run Keyword If    '${batches_details['${key}']['Batch Name']}'== '${batch_delete}'  Set Variable  '${batches_details['${key}']['Message Status']['Messages Deleted']}'
    ...  ELSE  Set Variable  ${delete_count}
       ${forward_delete_count}=  Run Keyword If    '${batches_details['${key}']['Batch Name']}'== '${batch_forward_delete}'  Set Variable  '${batches_details['${key}']['Message Status']['Messages Forwarded and Deleted']}'
    ...  ELSE  Set Variable  ${forward_delete_count}
       ${failed_count}=  Run Keyword If    '${batches_details['${key}']['Batch Name']}'== '${batch_fail}'  Set Variable  '${batches_details['${key}']['Message Status']['Messages Failed']}'
    ...  ELSE  Set Variable  ${failed_count}
    END
    Should Be Equal  ${batch_count}  ${num_batch}
    Run Keyword If    '${batch_forward}'!='None'  Should Be Equal  ${forward_count}  ${num_msgs}
    Run Keyword If    '${batch_delete}'!='None'  Should Be Equal  ${delete_count}  ${num_msgs}
    Run Keyword If    '${batch_forward_delete}'!='None'  Should Be Equal  ${forward_delete_count}  ${num_msgs}
    Run Keyword If    '${batch_fail}'!='None'  Should Be Equal  ${failed_count}  ${num_msgs}    

    ${sar_summary}=  SMANGGuiLibrary.Mailbox Search And Remediate Summary
    ${sar_total_count}=  Set Variable  ${sar_summary['total']}
    ${rem_rep_total_count}=  Set Variable  ${rem_rep_summary['Messages Remediated']['total']}
    Should Be Equal As Numbers  ${sar_total_count}  ${rem_rep_total_count}

Verify Chinese Batch Name In Batches Detail
    [Arguments]
    ...  ${chinese_batch_name}
    ...  ${chinese_batch_description}
 
    SMANGGuiLibrary.Remediation Report Summary
    ${batch_detail}=  SMANGGuiLibrary.Remediation Batches Detail
    LogMany  ${batch_detail}
    FOR    ${key}    IN    @{batch_detail.keys()}
      Should Be Equal  ${batch_detail['${key}']['Batch Name']}  ${chinese_batch_name}
      Should Be Equal  ${batch_detail['${key}']['Batch Description']}  ${chinese_batch_description}
    END

Verify Chinese Batch Name Desc
    [Arguments]
    ...  ${batch_id}
    ...  ${chinese_batch_name}
    ...  ${chinese_batch_description}

    SMANGGuiLibrary.Remediation Report Summary
    SMANGGuiLibrary.Remediation Batch Report Details  ${batch_id}
    ${Batch_Summary}=  SMANGGuiLibrary.Remediation Batch Report Details  ${batch_id}
    LogMany  ${Batch_Summary}
    
    Should Be Equal  ${Batch_Summary['Batch Name']}  ${chinese_batch_name}
    Should Be Equal  ${Batch_Summary['Batch Description']}  ${chinese_batch_description}

Verify MOR Batch Id Details
    [Arguments]  ${batch_id}
    ...  ${batch_name}
    ...  ${mid}
    ...  ${Status}
    ...  ${From}
    ...  ${Action}
    ...  ${Initiated_By}
    ...  ${Initiated_Source}
    ...  ${To}=${EMAIL_ADDRESS}
  
    SMANGGuiLibrary.Remediation Report Summary
    SMANGGuiLibrary.Remediation Batch Report Details  ${batch_id}
    ${Batch_Summary}=  SMANGGuiLibrary.Remediation Batch Report Details  ${batch_id}

    Should Be Equal  ${Status}  '${Batch_Summary['${mid}']['Status']}'
    Should Be Equal  ${From}  '${Batch_Summary['${mid}']['From']}'
    Should Be Equal  '${To}'  '${Batch_Summary['${mid}']['To']}'
    Should Be Equal  ${Action}  '${Batch_Summary['Action Taken']}'
    Should Be Equal  ${Initiated_By}  '${Batch_Summary['Initiated By']}'
    Should Be Equal  ${Initiated_Source}  '${Batch_Summary['Initiated Source']}'

Verify MOR Inprogress With SAR Summary
    [Arguments]  ${num_success_msgs}
    ...  ${num_inprogress_msgs}

    SMANGGuiLibrary.Remediation Report Summary    
    ${summary}=  SMANGGuiLibrary.Mailbox Search And Remediate Summary
    ${total_count}=  Set Variable  ${summary['total']}
    ${tc}=  Evaluate  str(${total_count}) 
    ${count}=  Convert To Integer  ${tc}
    ${forward_count}=  Set Variable  ${summary['Messages Forwarded']}
    ${in_progress_count}=  Set Variable  ${summary['Messages Remediated In-Progress']}
    
    Should Be Equal As Numbers  ${forward_count}  ${num_success_msgs}
    Should Be Equal As Numbers  ${in_progress_count}  ${num_inprogress_msgs}

    ${sar_summary}=  SMANGGuiLibrary.Remediation Report Summary
    ${messages_remediated}=  Set Variable  ${sar_summary['Messages Remediated']['Messages Searched and Remediated']}
    
    Should Be Equal As Numbers  ${messages_remediated}  ${count-1}   

Tracking Reporting Delete DB
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes
    Commit

Reporting Common TestCase Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Set Appliance Under Test to SMA
    Restart CLI Session
    Configure Time Zone

Reporting Common Testcase Teardown
    Set Appliance Under Test to SMA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Tracking Reporting Delete DB
    Unconfigure Time Zone
    SMANGGuiLibrary.Select Reports  Mail Flow Summary

    Do Common Testcase Teardown


Do Tvh1434717c Teardown

    Set Appliance Under Test to ESA
    EsaCliLibrary.Smtp Routes Delete
    ...  domain=${SAR_DOMAIN}
    Commit
    Sleep  10s
    EsaCliLibrary.Smtp Routes New
    ...  domain=${SAR_DOMAIN}
    ...  dest_hosts=${SAR_IP}
    Commit

    Reporting Common Testcase Teardown

Do Tvh1414100c Setup

    Set Test Variable  ${policy_name_drop}  policy_drop
    Set Test Variable  ${filter_name_drop}  filter_drop
    Set Test Variable  ${policy_name_quarantine}  policy_quarantine
    Set Test Variable  ${filter_name_quarantine}  filter_quarantine
    Set Test Variable  ${drop_mail_addr}  user5@${SAR_DOMAIN}
    Set Test Variable  ${quarantine_mail_addr}  user6@${SAR_DOMAIN} 
    Set Suite Variable  ${ESA_LOG_ERRORS}  ${Empty}
    Reporting Common Testcase Setup

    Set Appliance Under Test to ESA
    ${drop_action}=  Create Dictionary
    ...  Drop (Final Action)  drop it
    ${actions}=  Content Filter Create Actions
    ...  Drop (Final Action)  ${drop_action}
    Content Filter Add  Incoming  ${filter_name_drop}
    ...  ${filter_name_drop}  ${actions}
    ${settings}=    Create Dictionary
    ...  Insert Before       Default Policy
    ...  Sender Option       Any Sender
    ...  Recipient Option    Following Recipient
    ...  Recipients to Add   ${drop_mail_addr}
    Mail Policies Add  incoming  policy_drop  ${settings}
    Commit Changes

    ${filter_settings}=    Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${filter_name_drop}  ${True}
    
    Mail Policies Edit Content Filters
    ...  incoming  policy_drop  ${filter_settings}
    Commit Changes

    ${quarantine_action}=  Create Dictionary
    ...  Send message to quarantine  Policy
    ${actions}=  Content Filter Create Actions
    ...  Quarantine  ${quarantine_action}
    Content Filter Add  Incoming  ${filter_name_quarantine}
    ...  ${filter_name_quarantine}  ${actions}
    ${qr_settings}=    Create Dictionary
    ...  Insert Before       Default Policy
    ...  Sender Option       Any Sender
    ...  Recipient Option    Following Recipient
    ...  Recipients to Add   ${quarantine_mail_addr}
    Mail Policies Add  incoming  policy_quarantine  ${qr_settings}
    Commit Changes

    ${quarantine_settings}=    Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${filter_name_quarantine}  ${True}

    Mail Policies Edit Content Filters
    ...  incoming  policy_quarantine  ${quarantine_settings}
    Commit Changes

Do Tvh1414100c Teardown

    Set Appliance Under Test to ESA
    Content Filter Delete  Incoming  ${filter_name_drop}
    Content Filter Delete  Incoming  ${filter_name_quarantine}
    Commit Changes
    Mail Policies Delete  incoming  ${policy_name_drop}
    Mail Policies Delete  incoming  ${policy_name_quarantine} 
    Commit Changes 
	
    Set Appliance Under Test to SMA
    Run Keyword And Ignore Error  Start CLI Session If Not Open
    Tracking Reporting Delete DB
    Unconfigure Time Zone

    Do Common Testcase Teardown

Do Tvh1434705c Setup

    Reporting Common Testcase Setup

    Set Appliance Under Test to ESA
    Edit Mailbox Remediation in Account Settings With Custom Values  1

Do Tvh1434705c Teardown

    Set Appliance Under Test to ESA
    Create Domain Mapping  ${ACCOUNT_PROFILE_NAME}  ${SAR_DOMAIN}
    Commit Changes
    Edit Mailbox Remediation in Account Settings With Custom Values  2

    Reporting Common Testcase Teardown

Do Tvh1434732c Teardown

    Set Appliance Under Test to ESA
    Create Domain Mapping  ${ACCOUNT_PROFILE_NAME}  ${SAR_DOMAIN}
    Commit Changes

    Reporting Common Testcase Teardown

*** Test Cases ***

Tvh1434725c
    [Documentation]
    ...   Verify Batch Detail Report and status of all messages
    ...   triggered for remediation in detail
    ...   http://tims.cisco.com/view-entity.cmd?ent=1434725
    [Tags]      Tvh1434725c  erts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Reporting Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Set Appliance Under Test to SMA
    ${date}  ${from_time}  ${to_time} =  Get Search Date And Time
 
    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1
    
    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search
    ...  mesg_received=Custom Range
    ...  from_date=${date}
    ...  from_time=${from_time}
    ...  to_date=${date}
    ...  to_time=${to_time}
    ...  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  forward_email_address=${forward_mail_addr}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Delete OR Forward
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action_forward}
    ...  ${forward_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}

    ${batch_id}=  Get Batch Id
    
    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page 
    SMANGGuiLibrary.Select Reports    Remediation Report
    Wait Until Keyword Succeeds
    ...  20m  30s
    ...  Verify MOR Batch Id Details  ${batch_id}  ${batch_name}  ${mid}  'Success'  '${TEST_ID}@${CLIENT}'  '${action_forward}'  '${DUT_ADMIN}'  '${SMA}'

Tvh1434715c
    [Documentation]  
    ...  Verify Batch Summary page with Batch ID, Batch name and
    ...  total number of messages remediate against a batch
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434715
    [Tags]    Tvh1434715c  Tvh1434707c  erts
    [Setup]  Reporting Common Testcase Setup
    [Teardown]  Reporting Common Testcase Teardown

    ${batch_name_delete}=  Set Variable  test_delete
    ${batch_name_forward}=  Set Variable  test_forward
    ${batch_name_forward_delete}=  Set Variable  test_forward_delete 
    ${num_msgs}=  Set Variable  '3'
    ${num_batches}=  Set Variable  3

    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=3
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID .* queued for delivery.* >= 3
    ...  Message finished MID .* done >= 3 


    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name_delete}
    ...  delete_email=${True}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Wait Until Keyword Succeeds  5m  5s  Verify Logs For Messages Remediation Action For Delete OR Forward
    ...  ${DUT_ADMIN}
    ...  ${batch_name_delete}
    ...  ${action_delete}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${delete_mail_addr}
    ...  3

    Roll Over Now  mail_logs
    Roll Over Now  logname=remediation
    
    Set Appliance Under Test to SMA
    Diagnostic Tracking Delete DB  confirm=yes
    Commit

    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=3
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Wait Until Keyword Succeeds  5m  5s  Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID .* queued for delivery.* >= 3
    ...  Message finished MID .* done >= 3


    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name_forward}
    ...  forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA

    Wait Until Keyword Succeeds  5m  5s  Verify Logs For Messages Remediation Action For Delete OR Forward
    ...  ${DUT_ADMIN}
    ...  ${batch_name_forward}
    ...  ${action_forward}
    ...  ${forward_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  3

    Roll Over Now  mail_logs
    Roll Over Now  logname=remediation
    Set Appliance Under Test to SMA
    Diagnostic Tracking Delete DB  confirm=yes
    Commit

    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=3
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Wait Until Keyword Succeeds  5m  5s  Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID .* queued for delivery.* >= 3
    ...  Message finished MID .* done >= 3


    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name_forward_delete}
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Wait Until Keyword Succeeds  5m  5s  Verify Logs For Messages Remediation Action For Forward And Delete
    ...  ${DUT_ADMIN}
    ...  ${batch_name_forward_delete}
    ...  ${action_forward_delete}
    ...  ${forward_action_log}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  ${delete_mail_addr}
    ...  3

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    SMANGGuiLibrary.Select Reports    Remediation Report
    Wait Until Keyword Succeeds
    ...  20m  30s
    ...  Verify MOR Reporting Summary Count  ${num_msgs}  ${num_batches}  batch_delete=${batch_name_delete}  batch_forward=${batch_name_forward}  batch_forward_delete=${batch_name_forward_delete}
    
Tvh1434717c
    [Documentation]
    ...   Verify Batch Summary with Remediation Passed and Failed Combination
    ...   http://tims.cisco.com/view-entity.cmd?ent=1434717
    [Tags]      Tvh1434717c  Tvh1434708c  erts
    [Setup]  Reporting Common Testcase Setup
    [Teardown]  Do Tvh1434717c Teardown

    ${batch_name_delete_success}=  Set Variable  test_success
    ${batch_name_delete_fail}=  Set Variable  test_fail
    ${remediation_status_fail}=  Set Variable  Failed
    ${num_msgs}=  Set Variable  '1'
    ${num_batches}=  Set Variable  2

    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=abc@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name_delete_success}
    ...  delete_email=${True}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Delete OR Forward
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name_delete_success}
    ...  ${action_delete}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${delete_mail_addr}


    EsaCliLibrary.Smtp Routes Delete
    ...  domain=${SAR_DOMAIN}
    Commit
    
    Sleep  10s
    EsaCliLibrary.Smtp Routes New
    ...  domain=${SAR_DOMAIN}
    ...  dest_hosts=/dev/null
    Commit

    Roll Over Now  mail_logs
    Roll Over Now  logname=remediation

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=abc@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name_delete_fail}
    ...  delete_email=${True}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Remediation No Message Mailbox Fail
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name_delete_fail}
    ...  ${action_delete}
    ...  ${remediation_status_fail}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${delete_mail_addr}

    Set Appliance Under Test to SMA

    SMANGGuiLibrary.Go To Monitoring Page
    SMANGGuiLibrary.Select Reports    Remediation Report
    Wait Until Keyword Succeeds
    ...  20m  30s
    ...  Verify MOR Reporting Summary Count  ${num_msgs}  ${num_batches}  batch_delete=${batch_name_delete_success}  batch_fail=${batch_name_delete_fail}

Tvh1414100c
    [Documentation]
    ...   Verify if messages with status Aborted, Quarantined etc can be remediated from tracking
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414100
    [Tags]      Tvh1414100c  srts
    [Setup]  Do Tvh1414100c Setup
    [Teardown]   Do Tvh1414100c Teardown

    Set Appliance Under Test to ESA

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${drop_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* ready .* bytes from <${TEST_ID}@${CLIENT}>

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID ${mid} matched all recipients for per-recipient policy ${policy_name_drop} in the inbound table >= 1
    ...  Message aborted MID ${mid} Dropped by content filter '${filter_name_drop}' in the inbound table >= 1
    ...  Message finished MID ${mid} done >= 1

    
    Roll Over Now  mail_logs
    Roll Over Now  logname=remediation

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${quarantine_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* ready .* bytes from <${TEST_ID}@${CLIENT}>

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID ${mid} matched all recipients for per-recipient policy ${policy_name_quarantine} in the inbound table >= 1
    ...  Message finished MID ${mid} done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ${error}=  Run Keyword And Expect Error   *  SMANGGuiLibrary.Message Tracking Remediate  mid=ALL  wait_time=240
    LogMany  ${error}
    Should Contain  ${error}  ValueError

Tvh1434720c
    [Documentation]
    ...   verify if the batch name is given in Chinese language
    ...   it comes in proper format in MOR reports
    ...   http://tims.cisco.com/view-entity.cmd?ent=1434720
    ...   Chinese Character - U+3732 U+3733 U+3735 U+3739

    [Tags]      Tvh1434720c  erts
    [Setup]  Do Common Testcase Setup 
    [Teardown]  Reporting Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${chinese_unicode_batchname}=  Set Variable  \u3732\u3733\u3735\u3739
    ${chinese_batch_description}=  Set Variable  \u3731\u3737\u3734\u3738

    Set Appliance Under Test to SMA
    ${date}  ${from_time}  ${to_time} =  Get Search Date And Time

    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search
    ...  mesg_received=Custom Range
    ...  from_date=${date}
    ...  from_time=${from_time}
    ...  to_date=${date}
    ...  to_time=${to_time}
    ...  cisco_hosts=${ESA}

    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${chinese_unicode_batchname}
    ...  description=${chinese_batch_description}
    ...  forward_email_address=${forward_mail_addr}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    ${batch_id}=  Wait Until Keyword Succeeds  2m  5s  Get Batch Id

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    SMANGGuiLibrary.Select Reports    Remediation Report
    Wait Until Keyword Succeeds
    ...  20m  30s
    ...  Verify Chinese Batch Name Desc  ${batch_id}  ${chinese_unicode_batchname}  ${chinese_batch_description}

Tvh1434705c
    [Documentation]
    ...  Verify if the count gets updated according to the last state of remediation
    ...  when there is a double remediation i.e first forward as succ and second Delete as Fail for same message
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434732
    [Tags]  Tvh1434705c  erts
    [Setup]  Do Tvh1434705c Setup
    [Teardown]  Do Tvh1434705c Teardown

    ${batch_name_forward}=  Set Variable  test_forward
    ${batch_name_delete}=  Set Variable  test_delete
    ${num_msgs}=  Set Variable  '3'
    ${num_batches}=  Set Variable  2


    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=3
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID .* queued for delivery.* >= 3
    ...  Message finished MID .* done >= 3

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name_forward}
    ...  forward_email_address=${forward_mail_addr}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Messages Remediation Action For Delete OR Forward
    ...  ${DUT_ADMIN}
    ...  ${batch_name_forward}
    ...  ${action_forward}
    ...  ${forward_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  3


    Delete Domain Mapping  ${SAR_DOMAIN}
    Commit

    Sleep  10s
    Roll Over Now  mail_logs
    Roll Over Now  logname=remediation

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name_delete}
    ...  delete_email=${True}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Messages Remediation No Domain Map Fail
    ...  ${DUT_ADMIN}
    ...  ${batch_name_delete}
    ...  ${action_delete}
    ...  ${remediation_status_fail}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  3

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    SMANGGuiLibrary.Select Reports    Remediation Report
    Wait Until Keyword Succeeds
    ...  20m  30s
    ...  Verify MOR Reporting Summary Count  ${num_msgs}  ${num_batches}  batch_forward=${batch_name_forward}  batch_fail=${batch_name_delete}

Tvh1434732c
    [Documentation]
    ...  Verify if the SAR count includes the actual remediation count and not the in progress count
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434732
    [Tags]  Tvh1434732c  erts
    [Setup]  Reporting Common Testcase Setup
    [Teardown]  Do Tvh1434732c Teardown

    ${batch_name_forward}=  Set Variable  test
    ${batch_name_progress}=  Set Variable  test_in_progress

    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name_forward}
    ...  forward_email_address=${forward_mail_addr}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Delete OR Forward
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name_forward}
    ...  ${action_forward}
    ...  ${forward_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}

	
    Delete Domain Mapping  ${SAR_DOMAIN}
    Commit

    Sleep  10s
    Roll Over Now  mail_logs
    Roll Over Now  logname=remediation
	
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name_progress}
    ...  forward_email_address=${forward_mail_addr}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Remediation No Domain Map Fail
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name_progress}
    ...  ${action_forward}
    ...  ${remediation_status_fail}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    SMANGGuiLibrary.Select Reports    Remediation Report
    Wait Until Keyword Succeeds
    ...  20m  10s
    ...  Verify MOR Inprogress With SAR Summary  1  1

