*** Settings ***
Resource     sma/sar_sma.txt

Suite Setup  Sar Suite Setup
Suite Teardown  Sar Suite Teardown

*** Variables ***
${UNKNOWN_SOURCE_ATTACHMENT}  %{SARF_HOME}/tests/testdata/esa/advancedmalware/unscan.zip

*** Keywords ***
Verify Logs For Chained Profile Remediation Action For Delete OR Forward 
    [Arguments]  ${mid}
    ...  ${user_name}
    ...  ${batch_name}
    ...  ${action}
    ...  ${action_log_pattern}
    ...  ${remediation_status}
    ...  ${profile_name}
    ...  ${mail_addr1}
    ...  ${mail_addr}=${EMAIL_ADDRESS}

    Verify Log Contains Records
    ...  search_path=mail
    ...  timeout=90
    ...  Message ${mid} was initiated for '${action}' remedial action by '${user_name}' from source '${SMA}' in batch '${batch_name}' >= 1
    ...  Message ${mid} was processed with '${action}' remedial action for recipient '${mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}. >= 1

    Verify Log Contains Records
    ...  search_path=remediation
    ...  timeout=60
    ...  MID: ${mid} Unable to read message\\(s\\) from the recipient's \\(${mail_addr}\\) mailbox. Error: Please check credentials. Invalid username or password entered for exchange server.* >= 1
    ...  MID: ${mid} ${action_log_pattern} .* ${mail_addr1}.* >= 1
    ...  MID: ${mid} Remediation succeeded with \\`${profile_name}\\` profile for recipient .* Not trying further profiles. >= 1

Check Email Status
    [Arguments]  ${status}
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Page Should Contain  ${status} 

Delete Chained Profile
    [Arguments]  ${CHAINED_PROFILE_NAME}
    Account Settings Chained Profile Delete  ${CHAINED_PROFILE_NAME}
    Commit Changes

Check Email Remediation Failed Status
    [Arguments]  ${mid}  ${action}  ${user_name}  ${batch_name}  ${mail_addr}

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ...  more_details=${True}

    ${status}=  Set Variable  ${details['${mid}']['More Details']['summary']}
    ${result}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${result}  Delivered

    Should Match Regexp  ${status}  Message ${mid} was initiated for '${action}' remedial action by '${user_name}' from source '${SMA}' in batch '${batch_name}'
    Should Match Regexp  ${status}  Message ${mid} was processed with '${action}' remedial action for recipient '${mail_addr}' in batch '${batch_name}'. Remediation status: Failed. Reason: Message not found in user mailbox

Check Email Remediation Success Status
    [Arguments]  ${mid}  ${action}  ${user_name}  ${batch_name}  ${mail_addr}  ${remediation_status}

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ...  more_details=${True}

    ${status}=  Set Variable  ${details['${mid}']['More Details']['summary']}

    Should Match Regexp  ${status}  Message ${mid} was initiated for '${action}' remedial action by '${user_name}' from source '${SMA}' in batch '${batch_name}'
    Should Match Regexp  ${status}  Message ${mid} was processed with '${action}' remedial action for recipient '${mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}.

Do Tvh1414208c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 

    Quarantine Config Edit 
    ...  name=Policy
    ...  period=15m
    ...  action=release
    
    ${action}=  Create Dictionary
    ...  Send message to quarantine  Policy
    ${actions}=  Content Filter Create Actions
    ...  Quarantine  ${action}

    Add Content Filter  send_to_quaratine  ${actions}

Do Tvh1414208c Teardown

    Remove Content Filter  send_to_quaratine
    Do Common Testcase Teardown

Do Tvh1414246c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 

    ${settings}=  Mail Flow Policies Create Settings
    ...  Max. Messages Per Connection  100
    Mail Flow Policies Edit  ${ESA_PUB_LISTENER.name}  default  ${settings}
    commit Changes

Do Tvh1414246c Teardown
    ${settings}=  Mail Flow Policies Create Settings
    ...  Max. Messages Per Connection  10 
    Mail Flow Policies Edit  ${ESA_PUB_LISTENER.name}  default  ${settings}
    commit Changes

    Set Appliance Under Test to ESA
    Resumedel  ${SAR_DOMAIN}
    Do Common Testcase Teardown

Do Tvh1414234c Setup 
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 

    ${action}=  Create Dictionary
    ...  Header Name  SUBJECT 
    ...  Append to the Value of Existing Header  _modified 
    ${actions}=  Content Filter Create Actions
    ...  Add/Edit Header  ${action}

    Add Content Filter  subject_changed_cf  ${actions}

Do Tvh1414234c Teardown
 
    Remove Content Filter  subject_changed_cf 
    Do Common Testcase Teardown

Do Tvh1414119c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 
    Set Test Variable  ${ACCOUNT_PROFILE_NAME_1}  testing_onprem_1
    Set Test Variable  ${ACCOUNT_PROFILE_DESCRIPTION}  ${account_profile_name1}_description

    Diagnostic Tracking Delete DB  confirm=Yes
    Commit Changes

    ${settings}=  Create Dictionary
    ...  Profile Name                ${ACCOUNT_PROFILE_NAME_1}
    ...  Description                 ${ACCOUNT_PROFILE_DESCRIPTION}
    ...  Profile Type                ${PROFILE_TYPE_ONPREM}
    ...  Username                    ${SAR_ONPREM_USER}
    ...  Password                    Cisco12
    ...  Host                        ${SAR_IP}
    Account Settings Account Profile Create  ${settings}
    Commit Changes

    ${ACCOUNT_PROFILE_LIST}  Create List
    ...  ${ACCOUNT_PROFILE_NAME_1}
    ...  ${ACCOUNT_PROFILE_NAME}
 
    Set Suite Variable  ${CHAINED_PROFILE_NAME}  chained
    Set Suite Variable  ${CHAINED_PROFILE_DESCRIPTION}  ${CHAINED_PROFILE_NAME}_description
    ${settings}=  Create Dictionary
    ...  Profile Name   ${CHAINED_PROFILE_NAME}
    ...  Description    ${CHAINED_PROFILE_DESCRIPTION}
    ...  Mar Profiles   ${ACCOUNT_PROFILE_LIST}
    Account Settings Chained Profile Create  ${settings}
    Commit Changes

    Delete Domain Mapping  ${SAR_DOMAIN}
  
    ${settings}=  Create Dictionary
    ...  Domain Name        ${SAR_DOMAIN}
    ...  Mapped Profile     ${CHAINED_PROFILE_NAME}
    Account Settings Domain Mapping Create  ${settings}
    Commit Changes
  
    Set Appliance Under Test to SMA 
    Restart CLI Session
    Configure Time Zone

Do Tvh1414119c Teardown
    Set Appliance Under Test to ESA
    EsaCliLibrary.Smtp Routes Delete
    ...  domain=${SAR_DOMAIN}
    Commit
    Delete Domain Mapping  ${SAR_DOMAIN}
    Delete Chained Profile  ${CHAINED_PROFILE_NAME}
    Delete Account Profile  ${ACCOUNT_PROFILE_NAME_1} 
    Create Domain Mapping  ${ACCOUNT_PROFILE_NAME}  ${SAR_DOMAIN} 
    Commit Changes

    EsaCliLibrary.Smtp Routes New
    ...  domain=${SAR_DOMAIN}
    ...  dest_hosts=${SAR_IP}
    Commit
  
    Set Appliance Under Test to SMA
    Start CLI Session
    Unconfigure Time Zone
    Do Common Testcase Teardown 

Do Tvh1434571c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 

    ${action}=  Create Dictionary
    ...  Filename  Contains unscan 
    ${actions}=  Content Filter Create Actions
    ...  Strip Attachment by File Info  ${action}

    Add Content Filter  test_attachment  ${actions}

Do Tvh1434571c Teardown

    Remove Content Filter  test_attachment
    Do Common Testcase Teardown

Do Tvh1414244c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Set Appliance Under Test to SMA
    Restart CLI Session
    Configure Time Zone

Do Tvh1414244c Teardown
    Set Appliance Under Test to SMA
    Unconfigure Time Zone
    Do Common Testcase Teardown

*** Test Cases ***
Tvh1414208c
    [Documentation]  Verify remediation for messages released by Quarantine manually \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414208
    [Tags]  Tvh1414208c  Tvh1414224c  srts
    [Setup]   Do Tvh1414208c Setup 
    [Teardown]  Do Tvh1414208c Teardown

    ${action}=  Set Variable  Forward and Delete 

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Set Appliance Under Test to ESA
    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* quarantined to \\"Policy\\" \\(content filter:send_to_quaratine\\) == 1

    Quarantines Search View All Messages  name=Policy
    Quarantines Search Release  action_on=Action on All 1 items

    ${mid}=  Get Mid Value  MID .* released from quarantine \\"Policy\\" \\(manual\\)

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* released from quarantine \\"Policy\\" \\(manual\\) == 1
    ...  MID .* released from all quarantines == 1
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=test
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Forward And Delete
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${forward_action_log}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  ${delete_mail_addr}

Tvh1414246c
    [Documentation]  Verify the search of messages using delivered as status filter when 
    ...  processing status messages are also there in the tracking page \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414246
    [Tags]  Tvh1414246c  srts
    [Setup]  Do Tvh1414246c Setup
    [Teardown]  Do Tvh1414246c Teardown

    Suspend Del  10  ${SAR_DOMAIN}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=50
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Wait Until Keyword Succeeds
    ...  3m  10s
    ...  Check Email Status  Processing

    Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID .* queued for delivery.* >= 50

    Resumedel  ${SAR_DOMAIN} 
    Set Appliance Under Test to SMA
    Wait Until Keyword Succeeds 
    ...  3m  30s
    ...  Check Email Status  Delivered 
  
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA} 
    ...  delivered=${True}
    SMANGGuiLibrary.Page Should Contain  Delivered 

Tvh1414234c
    [Documentation]  Verify the case when the subject is being changed by the content filter then the
    ...  ESA is able to able to remediate the message with the new subject or not \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414234
    [Tags]  Tvh1414234c  srts
    [Setup]  Do Tvh1414234c Setup
    [Teardown]  Do Tvh1414234c Teardown

    ${action}=  Set Variable  Forward

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='Original'

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  mesg_received=Last 7 days  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
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

Tvh1414119c
    [Documentation]  Verify if the on demand remediation happens according to the 
    ...  Chained profiles configured under account settings \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414119
    [Tags]  Tvh1414119c  Tvh1427517c  Tvh1434287c  Tvh1414243c  Tvh1434567c  Tvh1434576c  erts 
    [Setup]  Do Tvh1414119c Setup
    [Teardown]  Do Tvh1414119c Teardown

    ${action}=  Set Variable  Delete

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='Testmail'

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
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Chained Profile Remediation Action For Delete OR Forward
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${delete_mail_addr}

    EsaCliLibrary.Smtp Routes Delete
    ...  domain=${SAR_DOMAIN}
    Commit

    EsaCliLibrary.Smtp Routes New
    ...  domain=${SAR_DOMAIN}
    ...  dest_hosts=/dev/null
    commit
    Roll Over Now  mail_logs

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='Testmail_fail'

    ${mid1}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done == 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid1}
    ...  batch_name=${batch_name}
    ...  delete_email=${True}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240
 
    Set Appliance Under Test to ESA 
    Verify Log Contains Records
    ...  search_path=mail
    ...  timeout=90
    ...  Message ${mid1} was initiated for '${action}' remedial action by '${DUT_ADMIN}' from source '${SMA}' in batch '${batch_name}' >= 1
    ...  Message ${mid1} was processed with '${action}' remedial action for recipient '${delete_mail_addr}' in batch '${batch_name}'. Remediation status: Failed. Reason: Message not found in user mailbox >= 1 

    Set Appliance Under Test to SMA
    @{remediation_action}=  Create List  Failed
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=All Hosts
    ...  remediation_result=${remediation_action}
    ...  wait_time=240

    Check Email Remediation Failed Status  ${mid1}
    ...  ${action}
    ...  ${DUT_ADMIN}  
    ...  ${batch_name}
    ...  ${delete_mail_addr}

Tvh1434571c
    [Documentation]  Verify the search of messages in the tracking page using attachment filter \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434571
    [Tags]  Tvh1434571c  srts
    [Setup]  Do Tvh1434571c Setup
    [Teardown]  Do Tvh1434571c Teardown

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'
    ...  attach-filename=${UNKNOWN_SOURCE_ATTACHMENT}

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  attachment_name=unscan
    ...  attachment_comparator=Begins with
    ...  wait_time=240

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details  mid=${mid}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Delivered

Tvh1414244c
    [Documentation]  Verify the search and remediate logs if the message is
    ...  been remediated with specific action selected \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414244
    [Tags]  Tvh1414244c  Tvh1434568c  Tvh1434541c  Tvh1434565c  Tvh1434574c  srts
    [Setup]  Do Tvh1414244c Setup
    [Teardown]  Do Tvh1414244c Teardown

    ${action}=  Set Variable  Forward and Delete

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
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
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Forward And Delete
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${forward_action_log}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  ${delete_mail_addr}

    Set Appliance Under Test to SMA
    @{remediation_action}=  Create List  Success
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=All Hosts
    ...  subject_data=testmail
    ...  subject_comparator=Begins with
    ...  remediation_result=${remediation_action}
    ...  wait_time=240

    Check Email Remediation Success Status  ${mid}
    ...  ${action}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${delete_mail_addr}
    ...  ${remediation_status}
