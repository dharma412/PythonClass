*** Settings ***
Resource     sma/sar_sma.txt

Suite Setup  Sar Suite Setup
Suite Teardown  Sar Suite Teardown

*** Variables ***
${filter_name} =   Tvh1414124c_filter
${toast_widget_content}=  Remediation Report Status
${view_details}=  View Details
${remediation_report_ready}=  Remediation Report is Ready

*** Keywords ***
Disable URL Filtering
    ${URL_status}=  Url Filtering Is Enabled
    Run Keyword If  ${URL_status}
    ...  Url Filtering Disable
    Commit Changes

Do Tvh1414156c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Url Filtering Enable

    ${urls_filter}  Create List  Search Engines and Portals  Web-based Email  Shopping  Social Networking  News  Health and Nutrition
    ${action_value}  Create Dictionary  Add Categories  ${urls_filter}
    ...   Defang URL  None
    ...   Perform Action for All Messages  None

    ${condition_value}  Create Dictionary  Add Categories  ${urls_filter}
    ${conditions}  Content Filter Create Conditions
    ...  URL Category Condition  ${condition_value}
    ${actions}  Content Filter Create Actions
    ...  URL Category Action  ${action_value}
    Content Filter Add  Incoming  ${filter_name}
    ...   ${filter_name}  ${actions}  ${conditions}
    ${settings}=        Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  Enable All  ${True}
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

Do Tvh1414156c Teardown
    Content Filter Delete  Incoming  ${filter_name}
    ${settings}=        Create Dictionary
    ...  Content Filters  Disable Content Filters
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

    Do Common Testcase Teardown

Check Toast Widget location
    [Arguments]  ${items}
    ${y}=  Get From List  ${items}  0
    ${x}=  Get From List  ${items}  1
    Should Be True  ${y} > 1000
    Should Be True  ${x} > 800

Verify Toast Widget Visible
    ${status}=   SMANGGuiLibrary.Toast Widget Visible
    Should be True   ${status}

Verify Latest Remediated Batch Details
    [Arguments]  ${batch_name_latest}  ${view_details_availability}
    ${fetch_toast_widget_content}=  SMANGGuiLibrary.Toast Widget Content
    Log Many  ${fetch_toast_widget_content}
    Should Contain    ${fetch_toast_widget_content}     ${remediation_report_ready}
    Should Contain    ${fetch_toast_widget_content}     ${batch_name_latest}
    Run Keyword If  '${view_details_availability}'=='False'
    ...  Should Not Contain    ${fetch_toast_widget_content}     ${view_details}

Do Tvh1469432c Setup
    Do Common Testcase Setup
    SMAGuiLibrary.Centralized Email Reporting Disable
    SMAGuiLibrary.Commit Changes

Do Tvh1469432c Teardown
    SMAGuiLibrary.Centralized Email Reporting Enable
    SMAGuiLibrary.Commit Changes
    Do Common Testcase Teardown

*** Test Cases ***
Tvh1414103c
    [Documentation]
    ...  Documentation - Verify if Remediation action is available in Tracking for Admin User
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414103c
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469347
    [Tags]       Tvh1414103c  Tvh1403415c  Tvh1469347c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=user@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  confirm_remediation_action=Apply
    ...  retry_time=240

    ${loc_tracking}=  SMANGGuiLibrary.Toast Widget Location
    Log Many  ${loc_tracking}
    ${items}=  Get Dictionary Values  ${loc_tracking}
    Check Toast Widget location  ${items}

    SMANGGuiLibrary.Go To Monitoring Page Nowait
    Wait Until Keyword Succeeds  30 sec  1 sec   Verify Toast Widget Visible
    ${loc_monitoring}=  SMANGGuiLibrary.Toast Widget Location
    Log Many  ${loc_monitoring}
    ${items}=  Get Dictionary Values  ${loc_monitoring}
    Check Toast Widget location  ${items}
    SMANGGuiLibrary.Wait For Angular

    SMANGGuiLibrary.Go To Quarantine Nowait
    Wait Until Keyword Succeeds  30 sec  1 sec   Verify Toast Widget Visible
    ${loc_quarantine}=  SMANGGuiLibrary.Toast Widget Location
    Log Many  ${loc_quarantine}
    ${items}=  Get Dictionary Values  ${loc_quarantine}
    Check Toast Widget location  ${items}
    SMANGGuiLibrary.Wait For Angular

Tvh1414141c
    [Documentation]
    ...   Verify if URL Search option is available in Advanced Search of Message Tracking page
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414141c
    [Tags]      Tvh1414141c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  url=${True}
    
Tvh1414098c
    [Documentation]      
    ...  Verify if in the More details of a message we have
    ...  Delivered as a last state for a delivered message in tracking
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414098c
    [Tags]     Tvh1414098c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  cisco_mid=${mid}
    ...  wait_time=240

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Delivered

Tvh1414123c
    [Documentation]
    ...  Verify if the remediation happend even if there are special characters in teh subject
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414123c
    [Tags]      Tvh1414123c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Delete

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='#@!testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1
 
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_email=${True}
    ...  wait_time=240

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

Tvh1414146c
    [Documentation]
    ...  Tvh1414146c - Verify tracking page is getting when cancel the
    ...  remediate option on message details
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414146c
    [Tags]    Tvh1414146c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  confirm_remediation_action=Cancel
    ...  wait_time=240

Tvh1414113c
    [Documentation]
    ...  Verify if the "YES" option gets highlighted once you select any of the action
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414113c
    [Tags]      Tvh1414113c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  confirm_remediation_action=Apply
    ...  wait_time=240

Tvh1414148c
    [Documentation]
    ...  Verify if we get a confirm remediation POP-UP box when we click on
    ...  remediate button after selecting the individual messages
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414148c
    [Tags]    Tvh1414148c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  wait_time=240

Tvh1414153c
    [Documentation]
    ...  Verify if we get a remediation status pop up box as soon as
    ...  we click on the APPLY button on the remediation pop up box
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414153c
    [Tags]    Tvh1414153c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  confirm_remediation_action=Apply
    ...  wait_time=240

Tvh1414134c
    [Documentation]  
    ...  Verify if the status of a message in a tracking page gets changed to delivered
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414134c
    [Tags]  Tvh1414134c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  cisco_mid=${mid}
    ...  wait_time=240

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Delivered

Tvh1414097c
    [Documentation]
    ...   Verify if get a remediation status pop up saying that "Remediation of all "x" no. of messages got initiated
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414097c
    ...   http://tims.cisco.com/view-entity.cmd?ent=1469346
    ...   http://tims.cisco.com/view-entity.cmd?ent=1469348
    ...   http://tims.cisco.com/view-entity.cmd?ent=1469351
    ...   http://tims.cisco.com/view-entity.cmd?ent=1469431
    [Tags]      Tvh1414097c  Tvh1414127c  Tvh1469346c  Tvh1469348c  Tvh1469351c  Tvh1469431c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=3
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=user@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid_list}=  Get All Mids  MID .* queued for delivery
    FOR  ${mid}  IN  @{mid_list}
      Run Keyword  Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID ${mid} queued for delivery.* >= 1
    ...  Message finished MID ${mid} done >= 1
    END

    ${midstring}=  Evaluate  ",".join(${mid_list})

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${midstring}
    ...  batch_name=${batch_name}
    ...  delete_email=${True}
    ...  confirm_remediation_action=Apply
    ...  remediation_status=Message(s) Initiated
    ...  remediation_msg_count=3
    ...  remediation_status=Remediation of ${batch_name}
    ...  wait_time=240

    ${batch_name_latest}=  Set Variable  second_remediate_Tvh1414097c
    Roll Over Now  mail_logs

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=user@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail2'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID ${mid} queued for delivery >= 1
    ...  Message finished MID ${mid} done >= 1

    SMANGGuiLibrary.Message Tracking Search
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name_latest}
    ...  description=${batch_name_latest}
    ...  forward_email_address=${forward_mail_addr}
    ...  retry_time=180

    Wait Until Keyword Succeeds
    ...  500sec  2sec
    ...  Verify Latest Remediated Batch Details  ${batch_name_latest}  True
    SMANGGuiLibrary.Toast Widget View Details
    SMANGGuiLibrary.Page Should Contain  Remediation Report Batch Detail
    SMANGGuiLibrary.Page Should Contain  Batch Messages

Tvh1414149c
    [Documentation]
    ...   Verify if we get a correct count of a indiviidual
    ...   messages selected below the search criteria box.
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414149c
    [Tags]      Tvh1414149c  Tvh1414150c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${attempts_count}=  Set Variable  5 
    ${attempts_count}=  Convert To Integer  ${attempts_count}
    ${i}=  Set Variable  1

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=6
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 6

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  delivered=True
    ...  wait_time=240
    FOR  ${i}  IN RANGE  1   ${attempts_count}
         ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
         ...  mid=${mid}
         ${status}=  Set Variable  ${details['${mid}']['status']}
         Should Contain  ${status}   Delivered
         ${mid1}=  Evaluate  int('''${mid}''')+1
         ${mid}=  Evaluate  str('''${mid1}''')
    END

Tvh1414137c
    [Documentation]      
    ...  Verify if the we get a successfull remediation and
    ...  initiation logs in mail logs when remediation is done
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414137c
    [Tags]      Tvh1414137c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Forward

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  forward_email_address=${forward_mail_addr}
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Delete OR Forward
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${forward_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}

Tvh1414155c
    [Documentation]
    ...   Verify if we get the message details according to our requirement
    ...   in the tracking page when we click on Modify button on the search criteria box
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414155c
    [Tags]      Tvh1414155c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Delete

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_email=${True}
    ...  remediation_status_action=Close
    ...  wait_time=240

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

Tvh1414090c
    [Documentation]
    ...  Verify if after clicking on check box of Message Details,
    ...  we get a string saying all "x" no of messages got slected
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414090c
    [Tags]  Tvh1414090c  Tvh1414093c  Tvh1414092c  Tvh1385353c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${num_msgs}=  Set Variable  5
    
    Set Appliance Under Test to SMA
    Restart CLI Session
    Diagnostic Tracking Delete DB  confirm=yes
    Commit
    
    Set Appliance Under Test to ESA
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=5
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 5

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  confirm_remediation_action=Cancel
    ...  wait_time=240
    
    SMANGGuiLibrary.Page Should Contain  ${num_msgs}
    SMANGGuiLibrary.Page Should Contain  Messages Selected  

Tvh1414156c
    [Documentation]
    ...   Verify if we get the tracking results when the URL action is Defang URL with Search in Message body
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414156c
    [Tags]      Tvh1414156c  Tvh1413608c  srts
    [Setup]  Do Tvh1414156c Setup
    [Teardown]  Do Tvh1414156c Teardown
    ${URL_name}=  Set Variable  https://www.google.com 

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  subject='URL Test With Mail Body'
    ...  msg-body=${URL_name}

    ${mid}=  Get Mid Value  MID .* queued for delivery
    ${mid1}=  Evaluate  ${mid} + 1

    Verify And Wait For Log Records
    ...  search_path= mail
    ...  timeout=120
    ...  MID .* rewritten to MID .* by url-category-defang-action filter.*${filter_name} >=1
    ...  Message finished MID .* done >= 1
    ...  MID .* queued for delivery >= 1

    SMANGGuiLibrary.Message Tracking Search
    ...  url=${URL_name}
    ...  url_in_mail_body=${True}
    ...  wait_time=240

Tvh1469432c
    [Documentation]
    ...   Verify Toast Widget Notification for SMA with Centralized Reporting Disabled
    ...  http://tims.cisco.com/view-entity.cmd?ent=1469432
    [Tags]  Tvh1469432c  erts
    [Setup]  Do Tvh1469432c Setup
    [Teardown]  Do Tvh1469432c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${batch_name_latest}=  Set Variable  test_Tvh1469432c
    Roll Over Now  mail_logs

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=user@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID ${mid} queued for delivery >= 1
    ...  Message finished MID ${mid} done >= 1

    SMANGGuiLibrary.Message Tracking Search
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name_latest}
    ...  description=${batch_name_latest}
    ...  forward_email_address=${forward_mail_addr}
    ...  retry_time=240

     Wait Until Keyword Succeeds
     ...  500sec  2sec
     ...  Verify Latest Remediated Batch Details  ${batch_name_latest}  False

