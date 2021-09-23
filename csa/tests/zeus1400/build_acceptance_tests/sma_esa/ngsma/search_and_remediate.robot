*** Settings ***
Resource     sma/sar_sma.txt

Suite Setup  Sar Suite Setup
Suite Teardown  Sar Suite Teardown


*** Keywords ***
Check Email Remediation Status
    [Arguments]  ${TEST_ID}  ${mid}
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  sender_envelope_option=Envelope Sender
    ...  sender_data=${TEST_ID}
    ...  sender_comparator=Begins with

    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details  mid=${mid}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Remediated

Do Tvh1434569c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Set Appliance Under Test to SMA
    Configure Time Zone

Do Tvh1434569c Teardown
    Set Appliance Under Test to SMA
    Unconfigure Time Zone
    Do Common Testcase Teardown

Do Tvh1414132c Teardown

    Delete Domain Mapping  ${domain}
    Delete Account Profile  ${profile_name}
    Do Common Testcase Teardown


*** Test Cases ***
Tvh1414077c
    [Documentation]  Check if you are able to apply delete and forward action for all the selected messages under SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414077
    [Tags]  Tvh1414077c  Tvh1414194c  Tvh1414174c  Tvh1414175c  autobat
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Forward and Delete

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=10
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body="test mail body"
    ...  subject='testmail'

    Verify And Wait For Log Records
    ...  wait_time=1 mins
    ...  MID .* queued for delivery.* >= 10
    ...  Message finished MID .* done >= 10

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search
    SMANGGuiLibrary.Message Tracking Remediate  mid=ALL
    ...  batch_name=${batch_name}
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=240

    Set Appliance Under Test to ESA
    Verify And Wait For Log Records
    ...  search_path=mail
    ...  wait_time=2 minutes
    ...  retry_time=1 minutes
    ...  Message .* was initiated for '${action}' remedial action by '${DUT_ADMIN}' from source '${SMA}' in batch '${batch_name}'. >= 10
    ...  Message .* was processed with '${action}' remedial action for recipient '${delete_mail_addr}' in batch '${batch_name}'. Remediation status: ${remediation_status}. >= 10

    Verify And Wait For Log Records
    ...  search_path=remediation
    ...  wait_time=2 minutes
    ...  retry_time=1 minutes
    ...  MID: .* ${forward_action_log} to ${forward_mail_addr}. >= 10
    ...  MID: .* ${delete_action_log} from ${delete_mail_addr} .* >= 10
    ...  MID: .* Remediation succeeded with \\`${ACCOUNT_PROFILE_NAME}\\` profile for recipient ${delete_mail_addr}. >= 10

Tvh1434569c
    [Documentation]  Verify the More Details of a message which is delivered
    ...  if the envelope header and summary has proper information of each category \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434569
    [Tags]  Tvh1434569c  Tvh1414189c  autobat
    [Setup]  Do Tvh1434569c Setup
    [Teardown]  Do Tvh1434569c Teardown

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
    ...  Message finished MID .* done == 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  confirm_remediation_action=cancel
    ...  wait_time=240

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ...  more_details=${True}

    ${status}=  Set Variable  ${details['${mid}']['status']}
    ${sender}=  Set Variable  ${details['${mid}']['More Details']['Sender']}
    ${recipient}=  Set Variable  ${details['${mid}']['More Details']['Recipient']}

    Should Contain  ${status}  Delivered
    Should Contain  ${sender}  ${TEST_ID}@${CLIENT}
    Should Contain  ${recipient}  ${EMAIL_ADDRESS}

Tvh1414247c
    [Documentation]  Verify the status of the messages on the tracking page if the status of the message has been changed to remediated \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414247
    [Tags]  Tvh1414247c  Tvh1414185c  autobat
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${action}=  Set Variable  Forward and Delete

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

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  cisco_mid=${mid}
    ...  wait_time=240 
    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ...  more_details=${True}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Delivered

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=test
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close

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
    Wait Until Keyword Succeeds
    ...  4m  30s
    ...  Check Email Remediation Status  ${TEST_ID}  ${mid}

Tvh1414132c
    [Documentation]
    ...  Verify if the status of a message gets changed to remediated once the remediation is successfull
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414132c
    [Tags]  Tvh1414132c  Tvh1414118c  Tvh1414133c  Tvh1414152c  autobat
    [Setup]   Do Common Testcase Setup
    [Teardown]  Do Tvh1414132c Teardown
    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${profile_name}  dummy_profile
    Set Test Variable  ${profile_description}  dummy_profile creation
    Set Test Variable  ${domain}  abc.com

    ${action}=  Set Variable  Delete

    Create OnPrem Account Profile
    ...  ${profile_name}
    ...  ${profile_description}
    ...  ${SAR_ONPREM_USER}
    ...  ${SAR_ONPREM_PASSWORD}
    ...  ${SAR_IP}

    Create Domain Mapping  ${profile_name}  ${domain}

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
    ...  confirm_remediation_action=Apply
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

    Wait Until Keyword Succeeds  4m  0s
    ...    Check Remediated Status  mid=${mid}
