*** Settings ***
Resource     sma/sar_sma.txt

Suite Setup  Sar Suite Setup
Suite Teardown  Sar Suite Teardown

*** Variables ***
${ATTACHMENT_CONTAINS_URL}=  %{SARF_HOME}/tests/testdata/esa/sar/sar_url.txt
${ATTACHMENT_CONTAINS_MANY_URL}=  %{SARF_HOME}/tests/testdata/esa/sar/sar_multiple_url.txt
${URL}=  https://www.google.com

*** Keywords ***
Check Url Email Status
    [Arguments]  ${mid}
    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details  mid=${mid}
    ${status}=  Set Variable  ${details['${mid}']['status']}
    Should Contain  ${status}  Delivered

Do Tvh1414216c Setup
    Do Common Testcase Setup

    Set Test Variable  ${TEST_ID}  ${TEST NAME} 
    Add Url Content Filter  ${TEST_ID}_url

Do Tvh1414216c Teardown
    Set Appliance Under Test to ESA
    Remove Url Content Filter  ${TEST_ID}_url

    Do Common Testcase Teardown

Do Tvh1414250c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  ${TEST NAME} 

    Add Url Content Filter  Defang_URL
    Set Appliance Under Test to SMA
    Restart CLI Session
    Configure Time Zone

Do Tvh1414250c Teardown
    Set Appliance Under Test to ESA
    Remove Url Content Filter  Defang_URL

    Set Appliance Under Test to SMA
    Start CLI Session
    Unconfigure Time Zone
    Do Common Testcase Teardown

*** Test Cases ***
Tvh1414216c
    [Documentation]  Verify remediation of message without message-id while sending \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414208
    [Tags]  Tvh1414216c  srts
    [Setup]   Do Tvh1414216c Setup 
    [Teardown]  Do Tvh1414216c Teardown

    ${action}=  Set Variable  Forward and Delete 
    ${Content_filter_name}=  Set Variable  ${TEST_ID}_url

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=user5@${SAR_DOMAIN}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${SAR_MESSAGE_ID_URL}

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* URL ${URL} has reputation .* matched Action: URL defanged
    ${mid1}=  Evaluate  ${mid} + 1

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  Subject .*testmail.* >= 1
    ...  MID .* URL ${URL} has reputation .* matched Action: URL defanged >= 1
    ...  MID .* rewritten to MID .* by url-reputation-defang-strip-action filter.*${Content_filter_name}.* >=1
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
    ...  ${mid1}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${forward_action_log}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  ${delete_mail_addr}

Tvh1414250c
    [Documentation]  Verify Tracking results are returned based on the URL Search selecting both In Mail Body and In Attachment \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414250
    [Tags]  Tvh1414250c  Tvh1414141c  Tvh1434548c  Tvh1414248c  erts 
    [Setup]  Do Tvh1414250c Setup
    [Teardown]  Do Tvh1414250c Teardown

    ${action}=  Set Variable  Forward and Delete
    ${Content_filter_name}=  Set Variable  Defang_URL

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${delete_mail_addr}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body=${URL}
    ...  subject='testing defang URL action'
    ...  attach-filename=${ATTACHMENT_CONTAINS_URL}

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* URL ${URL} has reputation .* matched Action: URL defanged 
    ${mid1}=  Evaluate  ${mid} + 1

    Wait Until Keyword Succeeds  10m  1m  Verify Log Contains Records  search_path=mail  timeout=60
    ...  Subject .*testing defang URL action.* >= 1
    ...  MID .* attachment.*sar_url.txt.* >= 1
    ...  MID .* URL ${URL} has reputation .* matched Action: URL defanged >= 1
    ...  MID .* Attachment sar_url.txt URL .* has reputation .* matched Action: Attachment stripped >= 1
    ...  MID .* rewritten to MID .* by url-reputation-defang-strip-action filter.*${Content_filter_name}.* >=1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  url=${URL}
    ...  url_in_mail_body=${True}
    ...  wait_time=240

    Check Url Email Status  ${mid}
    SMANGGuiLibrary.Clear Tracking Search

    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  url=https://www.facebook.com
    ...  url_in_attachment=${True}

    Check Url Email Status  ${mid}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close
    ...  wait_time=60

    Set Appliance Under Test to ESA
    Wait Until Keyword Succeeds  10m  1m  Verify Logs For Remediation Action For Forward And Delete
    ...  ${mid1}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action}
    ...  ${forward_action_log}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  ${delete_mail_addr}

Tvh1414249c
    [Documentation]  Verify Tracking results are returned based on the URL Search selecting "In Attachment"
    ...  when URL action is Strip with multiple URLs in attachment \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1414249
    [Tags]  Tvh1414249c  Tvh1414200c  erts 
    [Setup]  Do Tvh1414250c Setup
    [Teardown]  Do Tvh1414250c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${Content_filter_name}=  Set Variable  Defang_URL

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${EMAIL_ADDRESS}
    ...  mail-from=${TEST_ID}@${CLIENT}
    ...  msg-body=${URL}
    ...  subject='testing Strip URL action'
    ...  attach-filename=${ATTACHMENT_CONTAINS_MANY_URL}

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* URL ${URL} has reputation .* matched Action: URL defanged

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  Subject .*testing Strip URL action.* >= 1
    ...  MID .* attachment.*sar_multiple_url.txt.* >= 1
    ...  MID .* URL ${URL} has reputation .* matched Action: URL defanged >= 1
    ...  MID .* Attachment sar_multiple_url.txt URL .* has reputation .* matched Action: Attachment stripped >= 1
    ...  MID .* rewritten to MID .* by url-reputation-defang-strip-action filter.*${Content_filter_name}.* >=1
    ...  Message finished MID .* done >= 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    ...  url=${URL}
    ...  url_in_mail_body=${True}
    ...  wait_time=240

    Check Url Email Status  ${mid}
    SMANGGuiLibrary.Clear Tracking Search

    @{many_url_list}=  Create List  https://docs.python.org  https://www.javatpoint.com  *learnpython*
    :FOR  ${url}  IN  @{many_url_list}
    \    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    \    ...  url=${url}
    \    ...  url_in_attachment=${True}
    \    Check Url Email Status  ${mid}
    \    SMANGGuiLibrary.Clear Tracking Search

Tvh1434516c
    [Documentation]  Verify if Client ID and secret are reused for ESA which is removed and added to SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1434516
    [Tags]  Tvh1434516c  srts
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${action}=  Set Variable  Forward
    ${action1}=  Set Variable  Forward and Delete

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
    Selenium Close
    Selenium Login
    Security Appliances Delete Email Appliance  ${ESA}
    Commit Changes

    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Message Tracking Search  cisco_hosts=${ESA}
    SMANGGuiLibrary.Message Tracking Remediate  mid=${mid}
    ...  batch_name=${batch_name}
    ...  delete_and_forward_email_address=${forward_mail_addr}
    ...  confirm_remediation_action=Apply
    ...  remediation_status_action=Close

    Set Appliance Under Test to ESA
    Verify Logs For Remediation Action For Forward And Delete
    ...  ${mid}
    ...  ${DUT_ADMIN}
    ...  ${batch_name}
    ...  ${action1}
    ...  ${forward_action_log}
    ...  ${delete_action_log}
    ...  ${remediation_status}
    ...  ${ACCOUNT_PROFILE_NAME}
    ...  ${forward_mail_addr}
    ...  ${delete_mail_addr}
