*** Settings ***
Resource     sma/sar_sma.txt

Suite Setup  Sar Suite Setup
Suite Teardown  Sar Suite Teardown

*** Keywords ***
Check Email Remediation Failed Status
    [Arguments]  ${mid}  ${action}  ${user_name}  ${batch_name}  ${mail_addr}

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ...  more_details=${True}

    ${status}=  Set Variable  ${details['${mid}']['More Details']['summary']}

    Should Match Regexp  ${status}  Message ${mid} was initiated for '${action}' remedial action by '${user_name}' from source '${SMA}' in batch '${batch_name}'
    Should Match Regexp  ${status}  Message ${mid} was processed with '${action}' remedial action for recipient '${mail_addr}' in batch '${batch_name}'. Remediation status: Failed. Reason: Authentication error

Edit Mailbox Remediation in Account Settings With Custom Value
    [Arguments]  ${number_of_attempts}

    ${settings}=  Create Dictionary
    ...  Maximum number of attempts  ${number_of_attempts}
    Account Settings Mailbox Remediation Edit Settings  ${settings}
    Commit Changes

Check Email Remediation Status
    [Arguments]  ${TEST_ID}  ${mid}
    SMANGGuiLibrary.Message Tracking Search  sender_envelope_option=Envelope Sender
    ...  sender_data=${TEST_ID}
    ...  sender_comparator=Begins with

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details  mid=${mid}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Remediated

Do Tvh1414181c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 

    Set Appliance Under Test to SMA    
    Restart CLI Session
    Configure Time Zone 

    Set Appliance Under Test to ESA

Do Tvh1414181c Teardown

    Set Appliance Under Test to SMA
    Start CLI Session
    Unconfigure Time Zone
    SMANGGuiLibrary.Clear Tracking Search

    Set Appliance Under Test to ESA
    Delete Domain Mapping  ${SAR_DOMAIN}
    Delete Account Profile  ${ACCOUNT_PROFILE_NAME_1}
    Create Domain Mapping  ${ACCOUNT_PROFILE_NAME}  ${SAR_DOMAIN}
    Commit Changes

    Do Common Testcase Teardown

Do Tvh1414172c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 

    Set Appliance Under Test to ESA
    ${settings}=  Mail Flow Policies Create Settings
    ...  Max. Messages Per Connection  1100
    Mail Flow Policies Edit  ${ESA_PUB_LISTENER.name}  default  ${settings}
    commit Changes

Do Tvh1414172c Teardown
    Set Appliance Under Test to ESA
    ${settings}=  Mail Flow Policies Create Settings
    ...  Max. Messages Per Connection  10
    Mail Flow Policies Edit  ${ESA_PUB_LISTENER.name}  default  ${settings}
    commit Changes

    Do Common Testcase Teardown

*** Test Cases ***
Tvh1414076c
    [Documentation]  Check if you are able to apply delete action for all the selected messages under SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414076
    [Tags]  Tvh1414076c  Tvh1414167c  Tvh1434532c  srts
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Delete

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=10
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID .* queued for delivery.* >= 10
    ...  Message finished MID .* done >= 10

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name}
    ...  delete_email=${True}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=300

    Set Appliance Under Test to ESA
    Wait Until Keyword Succeeds  10m  1m  Verify And Wait For Log Records
    ...  search_path=mail
    ...  wait_time=5 minutes
    ...  retry_time=1 minutes
    ...  Message .* was initiated for '${action}' remedial action by '${DUT_ADMIN}' from source '${SMA}' in batch '${batch_name}'. >= 10
    ...  Message .* was processed with '${action}' remedial action for recipient '${delete_mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}. >= 10

    Wait Until Keyword Succeeds  10m  1m  Verify And Wait For Log Records
    ...  search_path=remediation
    ...  wait_time=5 minutes
    ...  retry_time=1 minutes
    ...  MID: .* ${delete_action_log} from ${delete_mail_addr}. >= 10
    ...  MID: .* Remediation succeeded with \\`${ACCOUNT_PROFILE_NAME}\\` profile for recipient .* >= 10

Tvh1414078c
    [Documentation]  Check if you are able to apply forward action for all the selected messages under SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414078
    [Tags]  Tvh1414078c  Tvh1414168c  Tvh1414193c  Tvh1414190c  Tvh1434533c  srts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${action}=  Set Variable  Forward

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=10
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID .* queued for delivery.* >= 10
    ...  Message finished MID .* done >= 10

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name}
    ...  forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=300

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  search_path=mail
    ...  wait_time=2 minutes
    ...  retry_time=1 minutes
    ...  Message .* was initiated for '${action}' remedial action by '${DUT_ADMIN}' from source '${SMA}' in batch '${batch_name}'. >= 10
    ...  Message .* was processed with '${action}' remedial action for recipient '${delete_mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}. >= 10

    Verify Log Contains Records
    ...  search_path=remediation
    ...  timeout=120
    ...  MID: .* ${forward_action_log} to ${forward_mail_addr}. >= 10
    ...  MID: .* Remediation succeeded with \\`${ACCOUNT_PROFILE_NAME}\\` profile for recipient .* >= 10

Tvh1414180c
    [Documentation]  Verify if you are able to give the mail address in the forward action box \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414180
    [Tags]  Tvh1414180c  Tvh1414186c  srts
    [Setup]  Do Common Testcase Setup
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

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  forward_email_address=${forward_mail_addr1}
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
    ...  ${forward_mail_addr1}

Tvh1414181c
    [Documentation]  Verify if you are able to remediate a remediated message when the action was forward in the previous case \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414181
    [Tags]  Tvh1414181c  Tvh1434559c  Tvh1414170c  srts
    [Setup]  Do Tvh1414181c Setup
    [Teardown]  Do Tvh1414181c Teardown

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
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
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

    #Remediatng a remediated message
    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  forward_email_address=user7@scale.com
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Delete OR Forward
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${forward_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  user7@scale.com

    Set Test Variable  ${ACCOUNT_PROFILE_NAME_1}  testing_onprem_1
    Set Test Variable  ${ACCOUNT_PROFILE_DESCRIPTION}  ${account_profile_name1}_description

    ${settings}=  Create Dictionary
    ...  Profile Name                ${ACCOUNT_PROFILE_NAME_1}
    ...  Description                 ${ACCOUNT_PROFILE_DESCRIPTION}
    ...  Profile Type                ${PROFILE_TYPE_ONPREM}
    ...  Username                    ${SAR_ONPREM_USER}
    ...  Password                    Cisco12
    ...  Host                        ${SAR_IP}
    Account Settings Account Profile Create  ${settings}
    Commit Changes

    Edit Mailbox Remediation in Account Settings With Custom Value  1
    Delete Domain Mapping  ${SAR_DOMAIN}

    ${settings}=  Create Dictionary
    ...  Domain Name        ${SAR_DOMAIN}
    ...  Mapped Profile     ${ACCOUNT_PROFILE_NAME_1}
    Account Settings Domain Mapping Create  ${settings}
    Commit Changes

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  forward_email_address=user6@scale.com
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close

    Set Appliance Under Test to ESA
    Verify Log Contains Records
    ...  search_path=mail
    ...  timeout=90
    ...  Message ${mid} was initiated for '${action}' remedial action by '${DUT_ADMIN}' from source '${SMA}' in batch '${batch_name}'. >= 1
    ...  Message ${mid} was processed with '${action}' remedial action for recipient '${EMAIL_ADDRESS}' in batch '${batch_name}'. Remediation status: Failed. Reason: Authentication error >= 1

    Set Appliance Under Test to SMA
    @{remediation_action}=  Create List  Failed
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=All Hosts
    ...  remediation_result=${remediation_action}
    ...  wait_time=180

    Check Email Remediation Failed Status  ${mid}
    ...  ${action}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${EMAIL_ADDRESS}

Tvh1414191c
   [Documentation]  Verify if you are able to see the status changed to "remediated" in the tracking page when
   ...  forward action is applied already \n
   ...  http://tims.cisco.com/view-entity.cmd?ent=1414191
    [Tags]  Tvh1414191c  srts
    [Setup]  Do Common Testcase Setup
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
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=test
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

    Set Appliance Under Test to SMA
    Wait Until Keyword Succeeds
    ...  4m  30s
    ...  Check Email Remediation Status  ${TEST_ID}  ${mid}

Tvh1414192c
   [Documentation]  Verify If you are able to select the individual messages and click on remediate \n
   ...  http://tims.cisco.com/view-entity.cmd?ent=1414192
    [Tags]  Tvh1414192c  srts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=2
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${SAR_MESSAGE_ID}

    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID .* queued for delivery >= 2
    ...  Message finished MID .* done >= 2

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  cisco_mid=${mid}
    ...  wait_time=240
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  confirm_remediation_action=Cancel

    SMANGGuiLibrary.Clear Tracking Search

    ${mid1}=  Evaluate  ${mid} - 1
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}  cisco_mid=${mid1}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid1}
    ...  confirm_remediation_action=Cancel

Tvh1414172c
    [Documentation]  Verify if you are able to apply the delete and forward action on more than 1000 messages \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414172
    [Tags]  Tvh1414172c  Tvh1414142c  Tvh1414182c  erts
    [Setup]  Do Tvh1414172c Setup
    [Teardown]  Do Tvh1414172c Teardown

    ${action}=  Set Variable  Forward and Delete

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1000
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${SAR_MESSAGE_ID}

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify And Wait For Log Records
    ...  wait_time=6 mins
    ...  MID .* queued for delivery.* >= 1000
    ...  Message finished MID .* done >= 1000

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name}
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_msg_count=1000
    ...  remediation_status_action=Close
    ...  wait_time=900

    Set Appliance Under Test to ESA
    Wait Until Keyword Succeeds  20m  5m  Verify and Wait For Log Records
    ...  search_path=mail
    ...  wait_time=5 minutes
    ...  retry_time=2 minutes
    ...  Message .* was initiated for '${action}' remedial action by '${DUT_ADMIN}' from source '${SMA}' in batch '${batch_name}'. >= 1000

    Wait Until Keyword Succeeds  20m  5m  Verify And Wait For Log Records
    ...  search_path=remediation
    ...  wait_time=5 minutes
    ...  retry_time=2 minutes
    ...  MID: .* ${forward_action_log} to ${forward_mail_addr}. >= 1000
    ...  MID: .* ${delete_action_log} from ${delete_mail_addr} .* >= 1000
    ...  MID: .* Remediation succeeded with \\`${ACCOUNT_PROFILE_NAME}\\` profile for recipient ${delete_mail_addr}. >= 1000

    Wait Until Keyword Succeeds  20m  5m  Verify And Wait For Log Records
    ...  search_path=mail
    ...  wait_time=2 minutes
    ...  retry_time=2 minutes
    ...  Message .* was processed with '${action}' remedial action for recipient '${delete_mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}. >= 1000
