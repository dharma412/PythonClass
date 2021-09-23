*** Settings ***
Resource     sma/sar_sma.txt

Suite Setup  Sar Suite Setup
Suite Teardown  Sar Suite Teardown

*** Variables ***
${cloud_username}  cloud
${toast_widget_content}=  Remediation Report Status
${view_details}=  View Details
${remediation_report_ready}=  Remediation Report is Ready

*** Keywords ***
Inject And Verify Mail Logs
    [Arguments]  ${num_msgs}
    Set Appliance Under Test to ESA    
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=${num_msgs}
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=abc@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= ${num_msgs}
    ...  Message finished MID .* done == ${num_msgs} 

Edit Mailbox Remediation in Account Settings With Custom Value
    [Arguments]  ${number_of_attempts}

    ${settings}=  Create Dictionary
    ...  Maximum number of attempts  ${number_of_attempts}
    Account Settings Mailbox Remediation Edit Settings  ${settings}
    Commit Changes

Verify MOR Reporting Count 
    [Arguments]  ${num_msgs}  ${total_message_count}

    SMANGGuiLibrary.Remediation Report Summary
    ${summary}=  SMANGGuiLibrary.Mailbox Search And Remediate Summary

    Should Contain  ${summary['Messages Deleted']}  ${num_msgs} 
    Should Contain  ${summary['Messages Forwarded']}  ${num_msgs} 
    Should Contain  ${summary['Messages Forwarded and Deleted']}  ${num_msgs} 
    Should Contain  ${summary['total']}  ${total_message_count} 
    Should Contain  ${summary['Messages Failed']}  0

    ${count}=  SMANGGuiLibrary.Remediation Report Summary
    LogMany  ${count}
    Should Contain  ${count['Messages Remediated']['total']}  ${total_message_count}
   
Verify MOR Batch Id Details
    [Arguments]  ${batch_id}  ${batch_name}  ${batch_description}

    SMANGGuiLibrary.Remediation Report Summary
    ${result}=  SMANGGuiLibrary.Remediation Batch Report Details  ${batch_id}
    Should Contain  ${result['Batch Name']}  ${batch_name}
    Should Contain  ${result['Batch Description']}  ${batch_description}

Verify MOR Batch Details
    [Arguments]  ${batch_status}  ${batch_id}

    SMANGGuiLibrary.Remediation Report Summary
    ${detail}=  SMANGGuiLibrary.Remediation Batches Detail
    ${Status}=  Set Variable  ${detail['${batch_id}']['Status']}
    Should Contain  ${Status}  ${batch_status}

Do Tvh1434685c Teardown
    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Select Reports  Mail Flow Summary
 
    Set Appliance Under Test to ESA
    Do Common Testcase Teardown

Do Tvh1434723c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 

    Set Appliance Under Test to ESA
    ${settings}=  Mail Flow Policies Create Settings
    ...  Max. Messages Per Connection  350
    Mail Flow Policies Edit  ${ESA_PUB_LISTENER.name}  default  ${settings}
    commit Changes

Do Tvh1434723c Teardown
    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Select Reports  Mail Flow Summary

    Set Appliance Under Test to ESA
    ${settings}=  Mail Flow Policies Create Settings
    ...  Max. Messages Per Connection  10
    Mail Flow Policies Edit  ${ESA_PUB_LISTENER.name}  default  ${settings}
    commit Changes

    Create Domain Mapping  ${ACCOUNT_PROFILE_NAME}  ${SAR_DOMAIN}
    Commit Changes
 
    Do Common Testcase Teardown

Do Tvh1414105c Teardown
    Do Common Testcase Teardown

    Set Appliance Under Test to SMA
    User Config Delete  ${cloud_username}  confirm=YES
    Feature Key Delete Key  ${cloud_username}     
    Commit

Verify Toast Widget Data
    [Arguments]  ${batch_name}  ${view_details_availability}
    ${fetch_toast_widget_data}=  SMANGGuiLibrary.Toast Widget Content
    Log Many  ${fetch_toast_widget_data}
    Run Keyword If  '${view_details_availability}'=='False'
    ...  Should Contain    ${fetch_toast_widget_data}     ${toast_widget_content}
    ...  Should Contain    ${fetch_toast_widget_data}     ${batch_name}
    ...  ELSE
    ...  Should Contain    ${fetch_toast_widget_data}     ${remediation_report_ready}
    ...  Should Contain    ${fetch_toast_widget_data}     ${view_details}


*** Test Cases ***
Tvh1434685c
    [Documentation]  MOR Summary/ Batch Summary Page - Verify Reporting data, counters , table on Summary Page 
    ...  of Remediation Reports for Hosts \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434685
    [Tags]  Tvh1434685c  Tvh1434681c  Tvh1434719c  erts 
    [Setup]  Do Common Testcase Setup 
    [Teardown]  Do Tvh1434685c Teardown

    ${action}=  Set Variable  Delete
    ${action1}=  Set Variable  Forward
    ${action2}=  Set Variable  Forward and Delete 

    Inject And Verify Mail Logs  3

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=test
    ...  delete_email=${True}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Wait Until Keyword Succeeds  5m  5s  Verify Logs For Messages Remediation Action For Delete OR Forward
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${delete_mail_addr}
    ...  3

    Set Appliance Under Test to ESA
    Roll Over Now  mail_logs
    Roll Over Now  logname=remediation

    Inject And Verify Mail Logs  3 
    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name}
    ...  forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240
 
    Set Appliance Under Test to ESA 
    Wait Until Keyword Succeeds  5m  5s  Verify Logs For Messages Remediation Action For Delete OR Forward
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action1}
    ...  ${forward_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  3

    Roll Over Now  mail_logs
    Roll Over Now  logname=remediation

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name}
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Wait Until Keyword Succeeds  5m  5s  Verify Logs For Messages Remediation Action For Forward And Delete
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action2}
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
    ...  Verify MOR Reporting Count  3  9

Tvh1434528c
    [Documentation]  verify if the rejected connection doesnot show any remediated or delivered message in SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434528
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469344
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469350
    [Tags]  Tvh1434528c  Tvh1469344c  Tvh1469350c  erts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Delete
    ${msg_recv}=  Set Variable  Today

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=user@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_email=${True}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=go back
    ...  retry_time=300
    ...  toast_widget_action=cancel
    SMANGGuiLibrary.Page Should Contain  Message Tracking

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Delete OR Forward
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${delete_mail_addr}

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search Rejected Connections
    ...  mesg_received=${msg_recv}

    SMANGGuiLibrary.Page Should Not Contain  Remediated
    SMANGGuiLibrary.Page Should Not Contain  Delivered

Tvh1434721c
    [Documentation]  verify if we give long batch description it comes in a proper allignment in batch 
    ...  description under MOR reports --->batch summary \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434685
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469343
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469342
    [Tags]  Tvh1434721c  Tvh1434512c  Tvh1434534c  Tvh1469343c  Tvh1469342c  erts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Tvh1434685c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME} 
    ${action}=  Set Variable  Forward and Delete
    ${batch_name}=  Set Variable  test_search_and_remediate_ngui_sma_delete_and_forward_
    ${batch_description}=  Set Variable  test_search_and_remediate_ngui_sma_delete_and_forward_remediate_action_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
  
    Set Appliance Under Test to SMA 
    Restart CLI Session
    ${date}  ${from_time}  ${to_time}=  Get Search Date And Time  

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=user@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

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
    ...  description=${batch_description}
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=go to status report
    ...  retry_time=240
    ...  toast_widget_action=verify
    SMANGGuiLibrary.Page Should Contain  Messages Searched and Remediated

    Set Appliance Under Test to ESA
    Verify Logs For Messages Remediation Action For Forward And Delete
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${forward_action_log}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  ${delete_mail_addr}
    ...  1
 
    ${batch_id}=  Get Batch Id 
    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    SMANGGuiLibrary.Select Reports    Remediation Report
    Wait Until Keyword Succeeds
    ...  20m  30s
    ...  Verify MOR Batch Id Details  ${batch_id}  ${batch_name}  ${batch_description} 

Tvh1434723c
    [Documentation]  Verify if you are able to see the in  progress state in batch summary when more than 
    ...  100 messages are remediated at once \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434723
    [Tags]  Tvh1434723c  erts 
    [Setup]  Do Tvh1434723c Setup 
    [Teardown]  Do Tvh1434723c Teardown 

    ${action}=  Set Variable  Forward

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=100
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  wait_time=4 mins
    ...  MID .* queued for delivery.* >= 100
    ...  Message finished MID .* done >= 100 

    Delete Domain Mapping  ${SAR_DOMAIN} 
    Edit Mailbox Remediation in Account Settings With Custom Value  3

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name}
    ...  forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=420

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  search_path=mail
    ...  wait_time=2 minutes
    ...  retry_time=2 minutes
    ...  Message .* was initiated for '${action}' remedial action by '${DUT_ADMIN}' from source '${SMA}' in batch '${batch_name}'. >= 100 
    ...  Message .* was processed with '${action}' remedial action for recipient '${delete_mail_addr}' in batch '${batch_name}'. Remediation status: Failed. Reason: No profiles mapped for domain >= 100 

    ${batch_id}=  Get Batch Id

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    SMANGGuiLibrary.Select Reports    Remediation Report
    Wait Until Keyword Succeeds
    ...  20m  30s
    ...  Verify MOR Batch Details  In Progress  ${batch_id}

Tvh1414105c
    [Documentation]  Verify if Remediation action is available in Tracking for Cloud Admin User \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414105
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469341
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469353
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469354
    [Tags]  Tvh1414105c  skip_in_sl_mode  Tvh1469341c  Tvh1469353c  Tvh1469354c  srts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Tvh1414105c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${action}=  Set Variable  Delete
    ${user_name}=  Set Variable  cloud

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=user@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    Feature Key Set Key  ${cloud_username}  duration=2592000
    User Config New  ${cloud_username}  Cloud  ${DUT_ADMIN_SSW_PASSWORD}  Cloud Administrators
    Commit

    SMANGGuiLibrary.Close Browser
    SMANGGuiLibrary.Launch Dut Browser
    SMANGGuiLibrary.Login Into Dut  ${cloud_username}  ${DUT_ADMIN_SSW_PASSWORD}
    SMANGGuiLibrary.View Data For Appliance  ${ESA}

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_email=${True}
    ...  confirm_remediation_action=Apply
    ...  retry_time=180
    ...  toast_widget_action=verify

    Wait Until Keyword Succeeds
    ...  200sec  2sec
    ...  Verify Toast Widget Data  ${batch_name}  False

    Set Appliance Under Test to ESA
    Verify Logs For Messages Remediation Action For Delete OR Forward
    ...  ${user_name}
    ...  ${batch_name}
    ...  ${action}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${delete_mail_addr}
    ...  1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    SMANGGuiLibrary.Toast Widget Visible Time

    Wait Until Keyword Succeeds
    ...  300sec  2sec
    ...  Verify Toast Widget Data  ${batch_name}  True


