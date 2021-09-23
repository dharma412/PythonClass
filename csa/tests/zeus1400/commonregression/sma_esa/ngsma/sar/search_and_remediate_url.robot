*** Settings ***
Resource     sma/sar_sma.txt

Suite Setup  Sar Suite Setup
Suite Teardown  Sar Suite Teardown

*** Variables ***
${filter_name} =   Tvh1414124c_filter
${disclaimer_name}=  test_disclaimer
${url_name}=   https://www.google.com

*** Keywords  ***
Disable URL Filtering
    ${URL_status}=  Url Filtering Is Enabled
    Run Keyword If  ${URL_status}
    ...  Url Filtering Disable
    Commit Changes

Do Tvh1414124c Setup
    Do Common Testcase Setup
    ${disclaimer_text}=  Set Variable  This is a Test Disclaimer

    Textconfig New
    ...  resource_type=Message Disclaimer
    ...  resource_name=${disclaimer_name}
    ...  encoding_type=US-ASCII
    ...  notification_template=${disclaimer_text}
    Commit

    ${msg_body_cond}=  Create Dictionary
    ...  Contains text  google
    ${conditions}=  Content Filter Create Conditions
    ...  Message Body                        ${msg_body_cond}
    ${add_action} =  Create Dictionary
    ...  Disclaimer Text  ${disclaimer_name}
    ${actions}=  Content Filter Create Actions
    ...  Add Disclaimer Text  ${add_action}
    Content Filter Add  Incoming  ${filter_name}
    ...  ${filter_name}  ${actions}  ${conditions}
    ${settings}=    Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${filter_name}  ${True}
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

    Set Test Variable  ${TEST_ID}  Tvh1414124c

Do Tvh1414124c Teardown
    Content Filter Delete  Incoming  ${filter_name}
    ${settings}=    Create Dictionary
    ...  Content Filters  Disable Content Filters
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

    Do Common Testcase Teardown

Do Tvh1414157c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${Content_filter_name}  Defang_URL 

    Url Filtering Enable  url_click_tracking=${True}
    Outbreak Filters Enable
    Commit Changes
   
    ${result}  ${msg}  Run Keyword And Ignore Error  Verify URL Filtering Status As Connected
    Run Keyword If   '${result}' == 'FAIL'
    ...  Verify Engine Is Updated  enrollment_client
    Verify URL Filtering Status As Connected

    ${action_value}=  Create Dictionary
    ...  CustomRange Reputation URL Min value  -10.00
    ...  CustomRange Reputation URL Max value  +10.00
    ...  Scan Type  All
    ...  Defang Reputation URL  None

    ${actions}=  Content Filter Create Actions 
    ...  URL Reputation Action  ${action_value}
    
    Content Filter Add  Incoming  ${Content_filter_name}
    ...  ${Content_filter_name}  ${actions} 
    Commit Changes

    ${settings}=  Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${Content_filter_name}  ${True}
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

Do Tvh1414157c Teardown
    Disable URL Filtering
    Outbreak Filters Disable

    Content Filter Delete  Incoming  ${Content_filter_name}
    ${settings}=        Create Dictionary
    ...  Content Filters  Disable Content Filters
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

    Do Common Testcase Teardown

Do Tvh1414158c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${Content_filter_name}  Defang_URL

    Url Filtering Enable  url_click_tracking=${True}
    Outbreak Filters Enable
    Commit Changes

    ${result}  ${msg}  Run Keyword And Ignore Error  Verify URL Filtering Status As Connected
    Run Keyword If   '${result}' == 'FAIL'
    ...  Verify Engine Is Updated  enrollment_client
    Verify URL Filtering Status As Connected

    ${action_value}=  Create Dictionary
    ...  CustomRange Reputation URL Min value  -10.00
    ...  CustomRange Reputation URL Max value  +10.00
    ...  Scan Type  All
    ...  Defang Reputation URL  None

    ${actions}=  Content Filter Create Actions
    ...  URL Reputation Action  ${action_value}

    Content Filter Add  Incoming  ${Content_filter_name}
    ...  ${Content_filter_name}  ${actions}
    Commit Changes

    ${settings}=  Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${Content_filter_name}  ${True}
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

Do Tvh1414158c Teardown

    Disable URL Filtering
    Outbreak Filters Disable

    Content Filter Delete  Incoming  ${Content_filter_name}
    ${settings}=        Create Dictionary
    ...  Content Filters  Disable Content Filters
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

    Set Time Zone Setup  continent=America
    ...  country=United States
    ...  zone=Los_Angeles
    commit

    Do Common Testcase Teardown

*** Test Cases ***
Tvh1434562c
    [Documentation]   
    ...   verify if the tracking search results shows only the no.of messages
    ...   which are delivered and not the duplicate entries
    ...   http://tims.cisco.com/view-entity.cmd?ent=1434562c
    [Tags]      Tvh1434562c  erts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Delete
    ${attempts_count}=  Set Variable  9 
    ${attempts_count}=  Convert To Integer  ${attempts_count}
    ${i}=  Set Variable  1

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=11
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 10

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  delivered=True
    ...  wait_time=340
    :FOR  ${i}  IN RANGE  1   ${attempts_count}
         ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
         ...  mid=${mid}       
         ${status}=  Set Variable  ${details['${mid}']['status']}
         Should Contain  ${status}   Delivered
         ${mid1}=  Evaluate  int('''${mid}''')+1
         ${mid}=  Evaluate  str('''${mid1}''')  
    END

Tvh1414114c
    [Documentation]     
    ...   Verify if the check box is still enable even if the status
    ...   got changed to REMEDIATED due to the forward action
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414114c
    [Tags]      Tvh1414114c  Tvh1414165c  erts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Forward
    ${forward_mail_addr}=  Set Variable  user5@${SAR_DOMAIN} 

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

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  confirm_remediation_action=Cancel
    ...  wait_time=240

Tvh1414117c
    [Documentation]  
    ...  Verify if the more details of a remediated message shows the last state as remediated
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414117c
    [Tags]  Tvh1414117c  Tvh1385377c  erts
    [Setup]  Do Common Testcase Setup
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
    ...  cisco_mid=${mid}
    ...  wait_time=240

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Delivered

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_email=${True}

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

     Wait Until Keyword Succeeds  4m  0s 
     ...    Check Remediated Status  mid=${mid} 

Tvh1414075c
    [Documentation]
    ...   Verify if we have Delete Emails/Forward Email/Delete
    ...   and Forward  in user Mailbox  remediation actions available
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414075c
    [Tags]       Tvh1414075c  erts
    [Setup]  Do Common Testcase Setup
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
    ...  confirm_remediation_action=Cancel
    ...  wait_time=240

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Cancel
    ...  wait_time=240

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Cancel
    ...  wait_time=240

Tvh1414158c
    [Documentation]
    ...   verify if we get the tracking search results when we enter the partial URL in the text box to search with the Message Body
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414158c
    [Tags]      Tvh1414158c  erts
    [Setup]  Do Tvh1414158c Setup
    [Teardown]  Do Tvh1414158c Teardown

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body=${url_name}
    ...  subject='testing defang URL action'

    ${mid}=  Get Mid Value  MID .* URL ${url_name} has reputation .* matched Action: URL defanged

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* URL ${url_name} has reputation .* matched Action: URL defanged >= 1
    ...  MID .* rewritten to MID .* by url-reputation-defang-strip-action filter.*${Content_filter_name}.* >=1
    ...  Message finished MID .* done >= 1

    SMANGGuiLibrary.Message Tracking Search
    ...  url=https://www.goog*
    ...  url_in_mail_body=${True}
    ...  wait_time=240
	
    SMANGGuiLibrary.Page Should Contain  ${mid}   

Tvh1414157c
    [Documentation]
    ...   Verify if we get the tracking results when the URL action is remove URL with search in message body
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414157c
    [Tags]      Tvh1414157c  erts
    [Setup]  Do Tvh1414157c Setup
    [Teardown]  Do Tvh1414157c Teardown 
	
    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body=${url_name}
    ...  subject='testing defang URL action'

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* rewritten to MID .* by url-reputation-defang-strip-action filter.*${Content_filter_name}.* >=1
    ...  Message finished MID .* done >= 1

    SMANGGuiLibrary.Message Tracking Search
    ...  url=${url_name}
    ...  url_in_mail_body=${True}
    ...  wait_time=240
	
    SMANGGuiLibrary.Page Should Contain  ${mid}

Tvh1414124c

    [Documentation]
    ...   Verify if the remediation happens even  when the message gets changed due to the content filter configured as Add Disclaimer text
    ...   http://tims.cisco.com/view-entity.cmd?ent=1414124c
    [Tags]      Tvh1414124c  erts
    [Setup]  Do Tvh1414124c Setup
    [Teardown]  Do Tvh1414124c Teardown

    ${action}=  Set Variable  Delete

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  rcpt-host-list=${delete_mail_addr}
    ...  subject='URL Test With Mail Body'
    ...  msg-body=${url_name}

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1


    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  cisco_mid=${mid}
    ...  wait_time=240

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Delivered

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_email=${True}
    ...  wait_time=240

    Verify Logs For Remediation Action For Delete OR Forward
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${delete_mail_addr}

    Wait Until Keyword Succeeds  4m  0s
    ...   Check Remediated Status  mid=${mid}


