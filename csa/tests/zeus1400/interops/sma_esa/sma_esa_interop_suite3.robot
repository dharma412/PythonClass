
*** Settings ***
Resource     esa/injector.txt
Resource     regression.txt
Resource     sma/esasma.txt
Resource     sma/csdlresource.txt

Suite Setup  Run Keywords
...  Initialize Suite

Suite Teardown  Finalize Suite
Test Setup   General Test Case Setup


*** Variables ***
${CONFIG_PATH}     /data/pub/configuration
${DATA_UPDATE_TIMEOUT}=  30m
${RETRY_TIME}=  30s
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${Tvh1165328c_DLP_POLICY} =   PCI-DSS (Payment Card Industry Data Security Standard)
${PROFILE_NAME} =  smaesa_interop
${SPAM_NOTIF_SUBJ}=  Spam Quarantine Notification
${Outbreak_xpath}=  //*[@id='content']/form/dl/dd/table/tbody/tr[3]/td[3]/a
${Policy_xpath}=  //*[@id='content']/form/dl/dd/table/tbody/tr[4]/td[3]/a
${Virus_xpath}=   //*[@id='content']/form/dl/dd/table/tbody/tr[6]/td[3]/a
${Subject_xpath}=  //tbody[@class='yui-dt-data']/tr[1]/td[4]//div[@class='yui-dt-liner']//div[@class='trim-container']/span//a
${Tracking_xpath}=  //*[@id='form']/table/tbody/tr[2]/td[7]/a
${Spam_xpath}=  //tbody[@class='yui-dt-data']/tr[1]/td[5]//div[@class='yui-dt-liner']//div[@class='crop']//a
${expected_count}=  2

*** Keywords ***


Initialize Suite
    DefaultRegressionSuiteSetup
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Smtp Routes New  domain=ALL  dest_hosts=/dev/null
      Commit
      Selenium Login
      Message Tracking Enable  tracking=centralized
      Centralized Email Reporting Enable
      Commit Changes
      Admin Access Config Timeout   timeout_webui=1440  timeout_cli=1440
      Commit
    END
    @{ESA_NAMES}=    Create List
    Library Order SMA
    Selenium Login
    Network Access Edit Settings  1440
    Commit Changes
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    Spam Quarantine Enable
    Pvo Quarantines Enable
    FOR  ${esa}  IN  @{esa_appliances}
      Wait Until Keyword Succeeds  1m  10s
      ...  Security Appliances Add Email Appliance
      ...  ${esa}
      ...  ${${esa}_IP}
      ...  tracking=${True}
      ...  reporting=${True}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
      Commit Changes
      Append To List    ${ESA_NAMES}  ${esa}
    END
    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Wait Until Keyword Succeeds  5m  1m  Pvo Quarantines Enable
      Run Keyword And Ignore Error  Commit Changes
    END
    ${expected_count}=  Convert To Integer  ${expected_count}
    ${esa_cnt}=  Get Length  ${esa_appliances}
    ${expected_count}=  Evaluate    ${esa_cnt} * ${expected_count}
    Set Suite Variable  ${expected_count}
    Set Suite Variable  ${esa_cnt}
    Set Suite Variable  @{ESA_NAMES}

Finalize Suite
    FOR  ${appliance}  IN  @{esa_appliances}
      Clear Email Tracking Reporting Data
      Library Order ${appliance}
      Run Keyword And Ignore Error  Run On DUT  rm -rf ${CONFIG_PATH}/default_config.xml
      Selenium Close
    END
    DefaultRegressionSuiteTeardown

Clear Email Tracking Reporting Data
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Start Cli Session If Not Open
      Roll Over Now
      Commit
      Diagnostic Reporting Delete Db  confirm=yes
      Wait Until Ready
      Diagnostic Tracking Delete Db   confirm=yes
      Wait Until Ready
    END
    Library Order Sma
    Start Cli Session If Not Open
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready

General Test Case Setup
    FOR  ${dut_type}  IN  @{appliances}
      Run Keyword  Library Order ${dut_type}
      Set SSHLib Prompt  ${EMPTY}
      Restart CLI session
      DefaultTestCaseSetup
    END

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

PVO Search
    [Arguments]  ${name}=None  ${date_range}=today  ${exp_count}=0
    ${count}=  Pvo Search Policy Message  name=${name}  date_range=${date_range}
    Page Should Contain Element
    ...  //tbody[contains(@class,'yui-dt-data')]/tr['*']/td[1]  limit=${esa_cnt}
    #Run Keyword If  ${count} != ${exp_count}  Fail
    [Return]  ${count}

Spam Quarntine Search
    [Arguments]  ${date_range}=today  ${count}=${expected_count}
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  is_admin=${False}  date_range=${date_range}
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} != ${count}  Fail
    [Return]  ${actual_spam_count}

Get Expected Mail Count
    [Arguments]   ${table}=DLP Incident Details  ${column}=Messages  ${col_index}=0   ${count}=${expected_count}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  ${table}
    Log  ${reporting_data}
    @{col_values} =  Get From Dictionary  ${reporting_data}  ${column}
    ${mail_value} =  Get From List  ${col_values}  ${col_index}
    Run Keyword If  ${mail_value} != ${count}  Fail
    [Return]  ${mail_value}

Repeat Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=10
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}  repeat-address-list=1

Connect SSH
    Library Order SMA
    ${address} =  Get Host IP By Name  ${DUT}
    SSHLibrary.Open Connection    ${address}
    Set SSHLib Prompt  ]
    SSHLibrary.Login    ${RTESTUSER}    ${RTESTUSER_PASSWORD}
    Set SSHLib Prompt  >

Enable Delivery logs and Verify Mail Queue
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Restart CLI Session
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    ${count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  PVO Search  name=Policy  date_range=today  exp_count=${esa_cnt}
    Restart CLI Session
    Log Config New
    ...  log_file=Delivery Logs
    ...  name=CSCvr25560
    Commit
    Wait Until Keyword Succeeds  5m  ${RETRY_TIME}  Pvo Release Policy Message  Policy  week
    Connect SSH
    Set SSHLib Prompt  ]
    FOR  ${path}  IN  /data/log/  /data/pub/
      Write  cd ${path}
      Read Until Prompt
      ${out}=  Execute Command   grep -Hrni "unexpected dealloc of delivery" ./*
      Should Be Empty  ${out}
    END
    SSHLibrary.Close Connection


Verify PVO quarantine Set Cookie contents in Response and Request Header

    FOR  ${quarantine}  IN  @{pvo_quarantines}
      Log  ${quarantine}
      Navigate To  Email  Message Quarantine  Policy, Virus and Outbreak Quarantines
      Click Element  ${pvo_${quarantine}_xpath}
      Run keyword unless  '${quarantine}'=='outbreak'  Click Element  ${mail_view_xpath}
      Click Element  ${mail_view_xpath}
      ${quarantine_url}=  Get Location
      Verify Set Cookie contents in Response and Request Header   ${quarantine_url}
    END

*** Test Cases ***


Tvh1231746c
    [Tags]  interop  Tvh1231746c
    [Documentation]  Add Domain-Based Executive Summary report in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1231746
    ...  1. In SMA ,navigate to Email->Reporting-> Scheduled Report
    ...  2. Add schedule report of the type "Domain Based Executive Summary"
    ...  3. Provide time range, schedule, and email id

    Email Scheduled Reports Add Domain Based Report  Domain-Based Executive Summary
    ...  report_generation=individual  domains=${CLIENT}  email_to=${ALERT_RCPT}
    ...  time_range=last year  schedule=monthly:03:30

    ${reports} =  Email Scheduled Reports Get Reports
    Length Should Be  ${reports}  1
    ${str_reports} =  Convert To String  ${reports}
    Log  ${str_reports}

    Should Contain  ${str_reports}  Report Type: Domain-Based Executive Summary;
    Should Contain  ${str_reports}  Report Title: Domain-Based Executive Summary;
    Should Contain  ${str_reports}  Format: PDF;
    Should Contain  ${str_reports}  Schedule: Monthly;


Tvh1231742c
    [Tags]  interop  Tvh1231742c
    [Documentation]  Configure Anti spam in ESA and verify presence of Spam mails in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165325
    ...  1. All the Centralised services for Email in SMA are enabled.
    ...  2. All the Centralised services in ESA are enabled.
    ...  3. ESA is attached to SMA.
    ...  4. Mails have been Quarantined in SMA under SPAM .
    ...  5. In SMA navigate to Email ->SPAM Quarantine and click on SPAM Q link.
    ...  6. Click on search and then click on subject of an email.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Sync Appliances Datetime  ${SMA}  @{ESA_NAMES}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Quarantines Spam Disable
      Commit Changes
      EUQ Enable  ${SMA}  ${SMA_IP}  enable_slbl=${False}
      AntiSpam Enable  IronPort
      ${settings}=  Create Dictionary  Positive Spam Apply Action  Spam Quarantine
      Mail Policies Edit Antispam  incoming  default  ${settings}
      Commit Changes
    END
    Library Order SMA
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To  https://${DUT}:83
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week
    Library Order SMA
    Selenium Login
    Spam Quarantine Edit
    ...  interface=Management
    ...  port=6025
    Commit Changes
    Clear Email Tracking Reporting Data
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Restart CLI Session
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Incoming Mail Summary  column=Messages  col_index=3  count=${expected_count}
    Library Order SMA
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Go To  https://${DUT}:83
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week
    Log  ${spam_count}
    Click Element  ${Spam_xpath}  don't wait
    Sleep  25s
    Page Should Contain  Message Details

Tvh1231738c
    [Tags]  interop  Tvh1231738c  teacat  CSCvn23986  Tvh1327172c  csdl
    [Documentation]  Check for Reporting to Tracking Drilldown from Virus & Outbreak Reports
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1231738
    ...  1. All the Centralised services for Email in SMA are enabled.
    ...  2. All the Centralised services in ESA are enabled.
    ...  3. ESA is attached to SMA.
    ...  4. Mails have been Quarantined in SMA under Virus and OutBreak .
    ...  5. In SMA navigate to Reporting -> Outbreak Filters-> Threat Summary
    ...  6. Click on the no. of messages for a particular Threat
    ...  7. Teacat CSCvn23986 steps:
    ...  7a)Configure SMA and ESA for CPQ.
    ...  7b)On SMA configure following via CLI -> telnet /tmp/smad.bd
    ...     >>> import smad
    ...     >>> smad.tasks.host_queues.max_concurrent_tasks = None
    ...  7c)Inject couple of Outbreak positive messages to ESA that will end up in SMA quarantine
    ...     Check messages are visible in message quarantine
    ...  7d)SMA -> CLI -> quarantineconfig -> outbreakmanage -> delete -> 1 (Check you are able get prompt back)
    ...  7e)As per teacat Defect, After trying to delete the outbreak messages from the CLI,
    ...     we do not get the prompt back and the CPQ goes down(The Centralized PVO Quarantine page do not open after this)
    ...  7f)Inject few more messages to ESA and Check the DB locks on SMA

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    ${exp_teacat_mail_cnt}=  Evaluate    ${esa_cnt} * 10
    Clear Email Tracking Reporting Data
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      ${settings}=  Create Dictionary
      ...  Outbreak Filters  Enable Outbreak Filtering (Customize settings)
      ...  Enable Message Modification  ${True}
      Mail Policies Edit Outbreak Filters  incoming  default  ${settings}
      Commit Changes
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  outbreak/vof-phishurl.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  outbreak/vof_multi_phishurl.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/testvirus.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Threat Details  column=Total Messages  col_index=0  count=${expected_count}
    Log  ${reporting_data}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Threat Details
    Log  ${reporting_data}
    @{col_values} =  Get From Dictionary  ${reporting_data}  Threat Name
    ${value} =  Get From List  ${col_values}  0
    Should Be Equal As Strings  ${value}  Phish
    ${table_data}=   Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Virus Types Detail  column=Total Infected Messages  col_index=0  count=${esa_cnt}
    Log  ${table_data}
    Reports Open Item  Email, Reporting, Outbreak Filters
    ...  Threat Summary
    ...  ${expected_count}
    Page Should Contain  Message Tracking
    ${res}=  Reports View Tracking Details
    ...  page=Email, Reporting, Outbreak Filters
    ...  name=Threat Summary
    ...  where=Threat Category, Total Messages:
    ...  what=Messages
    Log List  ${res}
    #Tvh1327172c
    ${outbreak_url}=  Get Location
    Verify Set Cookie contents in Response and Request Header   ${outbreak_url}
    ${value} =  Get From List  ${res}  0
    Should Be True  ${value} >= ${expected_count}
    ${value} =  Get From List  ${res}  1
    Should Be Equal As Strings  ${value}  True
    Clear Email Tracking Reporting Data
    Connect SSH
    Write  telnet /tmp/smad.bd
    Read Until Prompt
    Write  import smad\n
    Read Until Prompt
    write  smad.tasks.host_queues.max_concurrent_tasks = None
    Read Until Prompt
    Set SSHLib Prompt  ]
    Set SSHLib Timeout  60 seconds
    SSHLibrary.Close Connection
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Restart CLI Session
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Repeat Inject Custom Message  outbreak/vofmanual.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Threat Details  column=Total Messages  col_index=0  count=${exp_teacat_mail_cnt}
    Log  ${reporting_data}
    ${res}=  Quarantines Search Get All Messages  name=Outbreak
    Should Not Be Empty  ${res}
    Connect SSH
    Write  cli
    Read Until Prompt
    Write  quarantineconfig
    Read Until Prompt
    write  outbreakmanage
    Read Until Prompt
    write  delete
    Read Until Prompt
    write  1
    Read Until Prompt
    Set SSHLib Prompt  ]
    Set SSHLib Timeout  60 seconds
    SSHLibrary.Close Connection
    Navigate To  Email  Message Quarantine  Policy, Virus and Outbreak Quarantines
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Restart CLI Session
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Repeat Inject Custom Message  outbreak/vofmanual.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Threat Details  column=Total Messages  col_index=0  count=${exp_teacat_mail_cnt}
    Log  ${reporting_data}
    ${res}=  Quarantines Search Get All Messages  name=Outbreak
    Should Not Be Empty  ${res}
    Connect SSH
    Set SSHLib Prompt  \#
    write   /data/bin/runas pgsql psql -d system_quarantine
    ${out}=  Read Until Prompt
    Set SSHLib Timeout  60 seconds
    SSHLibrary.Close Connection
    Log  ${out}
    Should Not Contain  ${out}  Lock  msg=DB Lock issue exists
    Restart CLI Session

Tvh1231739c
    [Tags]  interop  Tvh1231739c  Tvh1231741c   Tvh1327174c  csdl
    [Documentation]  Check for PVO Quarantine to Tracking Drilldown for PVO messages
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1231739
    ...  1. All the Centralised services for Email in SMA are enabled.
    ...  2. All the Centralised services in ESA are enabled.
    ...  3. ESA is attached to SMA.
    ...  4. Mails have been Quarantined in SMA under PVO
    ...  5. In SMA navigate to Email ->PVO Quarantine and click on the no. of messages for Virus.
    ...  6. Click on "View" under "Tracking" column for an email.
    ...  7. Navigate to Email ->PVO Quarantine ,click on the no. of messages for Outbreak.
    ...  8. Click on "View" under "Tracking" column for an email.
    ...  9. navigate to Email ->PVO Quarantine and click on the no. of messages for Policy.
    ...  10. Click on "View" under "Tracking" column for an email.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Library Order ESA
    Restart CLI Session
    Policyconfig Edit Antispam Disable  Incoming  DEFAULT
    Commit
    Library Order SMA
    Selenium Login
    Run keyword and ignore error  Pvo Release Policy Message  Outbreak  week
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Restart CLI Session
      ${PUBLIC_LISTENER}=  Get ESA Listener
      ${text} =  Set Variable  ppt
      ${msg_body_or_attachment_cond}=  Create Dictionary
      ...  Contains text  ${text}
      ${conditions}=  Content Filter Create Conditions
      ...  Message Body or Attachment  ${msg_body_or_attachment_cond}
      ${quarantine_action}=  Create Dictionary
      ...  Send message to quarantine   Policy
      ...  Duplicate message   ${False}
      ${actions}=  Content Filter Create Actions
      ...  Quarantine  ${quarantine_action}
      Content Filter Add  Incoming  ${TEST_ID}  ${TEST_ID}
      ...  ${actions}  ${conditions}
      Commit Changes
      ${settings}=  Create Dictionary
      ...  Content Filters  Enable Content Filters (Customize settings)
      ...  ${TEST_ID}   ${True}
      Mail Policies Edit Content Filters  Incoming  default
      ...  ${settings}
      ${settings} =  Create Dictionary
      ...  Anti-Virus Scanning  Yes
      ...  Virus Infected Messages Apply Action  Quarantine
      Mail Policies Edit Antivirus
      ...  Incoming
      ...  default
      ...  ${settings}
      Commit Changes
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/testvirus.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  outbreak/vofmanual.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    FOR  ${type}  IN  Policy  Virus  Outbreak
      ${count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  ${type} Messages Count
      ${count}=  Convert To Integer  ${count}
      Should be Equal As Integers  ${count}  ${esa_cnt}
    END
    Library Order SMA
    #Tvh1327174c - Policy,Virus and Outbreak
    FOR  ${path}  IN  ${Policy_xpath}  ${Virus_xpath}  ${Outbreak_xpath}
      Navigate To  Email  Message Quarantine  Policy, Virus and Outbreak Quarantines
      Click Element  ${path}  don't wait
      Sleep  25s
      Click Element  ${Subject_xpath}  don't wait
      Sleep  25s
      Wait Until Page Contains  Message Details  60s
      Click Element  ${Tracking_xpath}  don't wait
      Sleep  25s
      Page Should Contain  Message Tracking
    END

Tvh1232385c
    [Tags]  interop  Tvh1232385c  Tvh1232354c  CSCvr25560  teacat
    [Documentation]  Verify functionality of Delay Scheduled Exit in PVO quarantine search result.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1232385
    ...  1. Centralised PVO is configured in both SMA and ESA.
    ...  2. SMA has received emails under Policy quarantine category.
    ...  3. Create quarantine for eg. "upq"
    ...  4. In the SMA , navigate to Email->Message Quarantine-> Policy, Virus and Outbreak.
    ...  5. Click on the no. of messages under Policy section
    ...  6. Select a mail and click on More Actions ->Delay Schedule Exit by 24 hrs and confirms the changes.
    ...  7. Verify that in the "Scheduled Exit" column delayed time should be shown.
    ...  8. Select a mail and click on More Actions -> Move .
    ...  9. Select the folder to which the mail will be moved (eg. "upq") and click on "Move.
    ...  10. Select another mail from the list and click on More Actions -> Send Copy
    ...  11. Enter the mail id (eg. test@cisco.com)to which the mail has to be sent and click on "Send".
    ...  \n Teacat CSCvr25560 Steps:
    ...  1.Install 13.5.0.012 build on SMA
    ...  2.Enable all centralized services for mail in SMA
    ...  3.Attach an ESA with SMA
    ...  4.Send mail through ESA to have them at SMA CPQ
    ...  5.Enable Delivery log at SMA
    ...  6.Select 1 mail and do release
    ...  7.Check mail logs
    ...   Expected Behavior: No app fault should occur in mail_logs

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Library Order Sma
    Selenium Login
    Add Policy Quarantine  name=upq  retention_period=20  retention_unit=Hours  default_action=delete
    Commit Changes
    Run keyword and ignore error  Pvo Delete Policy Message  Virus  week
    Run keyword and ignore error  Pvo Release Policy Message  Policy  week
    Run keyword and ignore error  Pvo Release Policy Message  Outbreak  week
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Restart CLI Session
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/testvirus.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  outbreak/vofauto.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order Sma
    Selenium Login
    FOR  ${type}  IN  Policy  Virus  Outbreak
      ${count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  ${type} Messages Count
      ${count}=  Convert To Integer  ${count}
      Should be Equal As Integers  ${count}  ${esa_cnt}
    END
    ${res}=  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value1}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value1}
    Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Schedule Exit By  -- by 24 Hours
    Log  ${res}
    Should Match Regexp  ${res}  .*1 Message delayed by 1 day.*
    ${res}=  Quarantines Search Get All Messages  name=Policy
    ${value}=  Get From List  ${res}  0
    ${value2}=  Get From Dictionary  ${value}  scheduled_exit
    Log  ${value2}
    Should Not Be Equal As Strings  ${value1}  ${value2}
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Send Copy To  testuser@${CLIENT}
    Log  ${res}
    Should Match Regexp  ${res}  .*Messages are successfully sent.*
    ${res}=  Quarantines Search View All Messages  name=Policy
    ${res}=  Quarantines Search Move To  upq
    Log  ${res}
    Should Match Regexp  ${res}  .*Message moved to upq quarantine.*
    Clear Email Tracking Reporting Data
    Enable Delivery logs and Verify Mail Queue

Tvh1231747c
    [Tags]  interop  Tvh1231747c  Tvh1231748c  CSCvq00125  teacat
    [Documentation]  Enable SLBL service
    ...  and Synchronize SLBL between SMA and ESA appliances
    ...  on Services -> Spam Quarantine page.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1231748
    ...  1. Navigate to Management Appliance ->Centralized Services
    ...  ->Spam Quarantine-> End-User Safelist/Blocklist.
    ...  2. Click on "Enable" and commit and submit the changes.
    ...  3. Navigate to Management Appliance -> Centralized Services -> Spam Quarantine.
    ...  4. Click on "Synchronise All Appliances.
    ...  Teacat CSCvq00125 steps
    ...  1)Configure SMA With Centralized message tracking
    ...    with the ESA it is fetching the data from.
    ...  2)Get the upload attachment tracking.20190319T044508Z_20190319T044508Z.s.gz.
    ...    and rename it to tracking.@20190319T044508Z_20190319T044508Z.s.gz.
    ...  3)Copy this file into your SMA to be imported into the database.
    ...  cp tracking.@20190319T044508Z_20190319T044508Z.s.gz /data/log/tracking/a.a.a.a/
    ...  The a.a.a.a stands for your ESA IP that is attached to your SMA.
    ...   4)Check /data/pub/trackerd_helper_logs/trackerd_helper.current logs and /var/log/messages


    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Library Order SMA
    Selenium Login
    Spam Quarantine SlBl Enable
    Commit Changes
    ${res}=  Spam Quarantine Sync Appliances
    Should Match Regexp  ${res}  .*Success.*
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Copy File To DUT
      ...  %{SARF_HOME}/tests/testdata/sma/tracking.@20190319T044508Z_20190319T044508Z.s.gz
      ...  /data/log/tracking/${${esa}_IP}/
      Sleep  3m
      ${output}=  Run on DUT  grep "splunkd" /var/log/messages
      Should Not Contain  ${output}  core dumped
      Sleep  2m
      ${output}=  Run on DUT  grep "TRACKERD_HELPER-0 : finished file" /data/pub/trackerd_helper_logs/trackerd_helper.current
      Should Contain  ${output}  TRACKERD_HELPER-0 : finished file
    END
