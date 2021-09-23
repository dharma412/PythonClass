*** Settings ***
Resource     sma/eaas_sma.txt

Suite Setup
...  Eaas Suite Setup
Suite Teardown
...  Eaas Suite Teardown


*** Keywords ***
Do Tvh1451903c Setup
    Do Common Testcase Setup
    Set Test Variable  ${TEST_ID}  Tvh1451903c

Do Tvh1451903c Teardown
    Restart CLI Session
    Diagnostic Tracking Delete DB  confirm=Yes
    Diagnostic Reporting Delete DB  confirm=yes
    Commit
    Do Common Testcase Teardown


Do Tvh1451904c Setup
    Do Tvh1451903c Setup
    Set Test Variable  ${TEST_ID}  Tvh1451904c
    Run On DUT  route add ${KINESIS_APP_SERVER}/24 127.0.0.1 -blackhole
    Run On DUT  route add ${KINESIS_APP_SERVER_OPTIONAL} 127.0.0.1 -blackhole
    Roll Over Now  mail_logs
    Roll Over Now  eaas

Do Tvh1451904c Teardown
    Set Appliance Under Test to ESA
    Run On DUT  route delete ${KINESIS_APP_SERVER}/24 127.0.0.1 -blackhole
    Run On DUT  route delete ${KINESIS_APP_SERVER_OPTIONAL} 127.0.0.1 -blackhole
    Do Tvh1451903c Teardown

Verify Phishing Details
    [Arguments]  ${total_message_count}  ${success_message_count}  ${failed_message_count}
    SMANGGuiLibrary.Select Reports   Mail Flow Summary
    SMANGGuiLibrary.Select Reports   Advanced Phishing Protection
    ${phising_forward_details}=   SMANGGuiLibrary.Advanced Phishing Protection Forward Details
    LogMany      ${phising_forward_details}
    Should Contain  ${phising_forward_details['Total Messages']}  ${total_message_count}
    Should Contain  ${phising_forward_details['Messages Accepted']}  ${success_message_count}
    Should Contain  ${phising_forward_details['Messages Failed when Forwarding to Cisco Advanced Phishing Protection Cloud Service']}  ${failed_message_count}

Verify APP Success Tracking
    [Arguments]  ${mid}
    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ...  more_details=${True}
    ...  retry_time=120
    LogMany   ${details}
    ${app_log}=  Set Variable  ${details['${mid}']['More Details']['summary']}
    Should Match Regexp  ${app_log}  Message ${mid} succesfully forwarded to Cisco Advanced Phishing Protection Cloud Service

Verify APP Failed Tracking
    [Arguments]  ${mid}
    ${details}=  SMANGGuiLibrary.Message Tracking Get Message Details
    ...  mid=${mid}
    ...  more_details=${True}
    ...  retry_time=120
    LogMany   ${details}
    ${app_log}=  Set Variable  ${details['${mid}']['More Details']['summary']}
    Should Match Regexp  ${app_log}  Message ${mid} was not forwarded to Cisco Advanced Phishing Protection Cloud Service

*** Test Cases ***
Tvh1451903c
    [Documentation]  NGUI SMA - Verify reporting and tracking for successful
    ...  forwarding in SMA
    ...  http://tims.cisco.com/view-entity.cmd?ent=1451903
    [Tags]  Tvh1451903c  Tvh1451905c  autobat 
    [Setup]  Do Tvh1451903c Setup
    [Teardown]  Do Tvh1451903c Teardown

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${CLIENT}
    ...  mail-from=${TEST_ID}@apptest.com
    ...  mbox-filename=${EAAS_APP}

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID ${mid} mail headers enqueued for forwarding to Cisco Advanced Phishing Protection Cloud Service == 1

    Verify Log Contains Records  search_path=eaas  timeout=60
    ...  eaas : MID.*Message Headers are in queue for forwarding to Cisco Advanced Phishing Protection Cloud Service == 1
    ...  eaas : MID.*Message Headers are successfully forwarded to Cisco Advanced Phishing Protection Cloud Service == 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    Wait Until Keyword Succeeds
    ...  21m  30s
    ...  Verify Phishing Details  1  1  0

    @{msg_action}=  Create List  Successful
    SMANGGuiLibrary.Message Tracking Search
    ...  advance_phising_protection_forwarding=${msg_action}
    ...  wait_time=180

    Verify APP Success Tracking  ${mid}

Tvh1451904c
    [Documentation]  NGUI SMA - Verify reporting and tracking for failed to
    ...  forward metadata in SMA
    ...  http://tims.cisco.com/view-entity.cmd?ent=1451904
    [Tags]  Tvh1451904c  Tvh1451906c  autobat 
    [Setup]  Do Tvh1451904c Setup
    [Teardown]  Do Tvh1451904c Teardown

    Inject Messages
    ...  inject-host=${ESA_PUB_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${CLIENT}
    ...  mail-from=${TEST_ID}@apptest.com
    ...  mbox-filename=${EAAS_APP}

    Set Appliance Under Test to ESA
    ${mid}=  Get Mid Value  MID .* queued for delivery

    Verify Log Contains Records  search_path=mail  timeout=60
    ...  MID ${mid} mail headers enqueued for forwarding to Cisco Advanced Phishing Protection Cloud Service == 1

    Verify Log Contains Records  search_path=eaas  timeout=60
    ...  eaas : MID.*Message Headers are in queue for forwarding to Cisco Advanced Phishing Protection Cloud Service == 1
    ...  eaas : MID.*Message Headers forwarding to Cisco Advanced Phishing Protection Cloud Service Failed. Unable to establish connection with the cloud service == 1

    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Go To Monitoring Page
    Wait Until Keyword Succeeds
    ...  21m  30s
    ...  Verify Phishing Details  1  0  1

    @{msg_action}=  Create List  Failed
    SMANGGuiLibrary.Message Tracking Search
    ...   advance_phising_protection_forwarding=${msg_action}
    ...  wait_time=180

    Verify APP Failed Tracking  ${mid}