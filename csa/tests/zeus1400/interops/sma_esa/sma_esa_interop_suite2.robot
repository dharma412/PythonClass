# $Id: //prod/main/sarf_centos/tests/zeus1350/build_acceptance_tests/sma_esa_interop/sma_esa_interop_suite2.txt#2 $ $DateTime: 2020/03/24 02:19:21 $ $Author: vsugumar $

*** Settings ***
Resource     esa/injector.txt
Resource     regression.txt
Resource     sma/esasma.txt
Resource     sma/csdlresource.txt
Resource     email_interop_resource.txt

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
${expected_count}=  2
${ldap_user}=   ldapinterop2
${PASSWORD}    Ironport@123

*** Keywords ***


Initialize Suite
    DefaultRegressionSuiteSetup
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      Smtp Routes New  domain=ALL  dest_hosts=/dev/null
      Commit
      Admin Access Config Timeout   timeout_webui=1440  timeout_cli=1440
      Commit
      Selenium Login
      Message Tracking Enable  tracking=centralized
      Centralized Email Reporting Enable
      Commit Changes
    END
    @{ESA_NAMES}=    Create List
    Library Order SMA
    Selenium Login
    Network Access Edit Settings  1440
    Commit Changes
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    FOR  ${appliance}  IN  @{esa_appliances}
      Wait Until Keyword Succeeds  1m  10s
      ...  Security Appliances Add Email Appliance
      ...  ${appliance}
      ...  ${${appliance}_IP}
      ...  tracking=${True}
      ...  reporting=${True}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
      Commit Changes
      Append To List    ${ESA_NAMES}  ${appliance}
    END
    ${expected_count}=  Convert To Integer  ${expected_count}
    ${esa_cnt}=  Get Length  ${esa_appliances}
    ${expected_count}=  Evaluate    ${esa_cnt} * ${expected_count}
    Set Suite Variable  ${expected_count}
    Set Suite Variable  ${esa_cnt}
    Set Suite Variable  @{ESA_NAMES}
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp(dir="%{SARF_HOME}/tmp")  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}
    Set Suite Variable  ${MAIL}  ${ldap_user}@${CLIENT}
    Set Suite Variable  ${MAIL_LOCAL_ADDRESS}  ldapinterop2@${CLIENT}
    LDAP Client Connect  ${LDAP_AUTH_SERVER}
    ...  ldap_server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  basedn=${LDAP_BASEDN}
    ...  binddn=${LDAP_BINDDN}
    ...  password=${LDAP_PASSWORD}
    LDAP Client Create User  uid=${ldap_user}  password=${PASSWORD}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}  mail=${MAIL}
    ...  mail_local_address=${MAIL_LOCAL_ADDRESS}

Finalize Suite
    Ldap Client Delete User  ${ldap_user}
    Ldap Client Disconnect
    Run Keyword And Ignore Error  Remove Directory  ${SUITE_TMP_DIR}  recursive=${True}
    FOR  ${appliance}  IN  @{esa_appliances}
      Clear Email Tracking Reporting Data
      Library Order ${appliance}
      Run Keyword And Ignore Error  Run On DUT  rm -rf ${CONFIG_PATH}/default_config.xml
      Selenium Close
    END
    DefaultRegressionSuiteTeardown

Clear Email Tracking Reporting Data
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ESA
      Roll Over Now
      Commit
      Diagnostic Reporting Delete Db  confirm=yes
      Wait Until Ready
      Diagnostic Tracking Delete Db   confirm=yes
      Wait Until Ready
    END
    Library Order Sma
    Restart CLI Session
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready

General Test Case Setup
    FOR  ${dut_type}  IN  @{appliances}
      Run Keyword  Library Order ${dut_type}
      Restart CLI Session
      DefaultTestCaseSetup
    END

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

Inject Custom Spam Message
     [Arguments]  ${mails}  ${inject-host}
     ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
     Inject Messages  inject-host=${inject-host}  num-msgs=1
     ...  address-list=${rcpt_file}  mail-from=${TEST_ID}@${CLIENT}
     ...  mbox-filename=${MAIL_MBOX}

PVO Search
    [Arguments]  ${name}=None  ${date_range}=today  ${exp_count}=0
    ${count}=  Pvo Search Policy Message  name=${name}  date_range=${date_range}
    Page Should Contain Element  //tbody[contains(@class,'yui-dt-data')]/tr['*']/td[1]
    ...  limit=${esa_cnt}
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

Do Tvh1165329c Setup
    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    General Test Case Setup
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Run Keyword And Ignore Error  Null Smtpd Stop
      Null Smtpd Start
      Clean System Quarantines
      Roll Over Now  mail_logs
    END
    Library Order SMA
    Selenium Login
    Clean System Quarantines
    Roll Over Now  mail_logs
    Spam Quarantine Edit
    ...  interface=Management
    ...  port=6025
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_fname=${TEST_ID}@${CLIENT}
    ...  spam_notif_freq=daily
    ...  spam_notif_week_day=${None}
    ...  spam_notif_days=Mon, Tue, Wed, Thu, Fri, Sat, Sun
    ...  spam_notif_hours=03,15,21
    ...  spam_notif_baddr=test@${CLIENT}
    ...  spam_notif_enable_login=${True}
    Spam Quarantine SlBl Enable
    Commit Changes
    IP Interfaces Edit  Management  isq_https_service=83  isq_default=https://${DUT}:83/  hostname=${DUT}
    Commit Changes
    Ldap Add Server Profile
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}
    ...  base_dn=${LDAP_BASEDN}
    ...  auth_method=anonymous
    ...  server_type=OpenLDAP
    ...  port=${LDAP_AUTH_PORT}
    Ldap Edit Isq End User Authentication Query
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}.isq_auth
    ...  (uid={u})
    ...  mail
    ...  ${True}
    Ldap Edit Isq Alias Consolidation Query
    ...  ${PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}.isq_consolidate
    ...  (mailLocalAddress={a})
    ...  mail
    ...  ${True}
    Commit Changes
    Spam Quarantine Edit EndUser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=LDAP
    Commit Changes
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To  https://${DUT}:83
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=week

*** Test Cases ***
Tvh1165326c
    [Tags]  interop  Tvh1165326c
    [Documentation]  Enable all the Centralized  services for Email in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165326
    ...  1. Login to SMA GUI, navigate to management>centralized services>Email>message tracking.
    ...  2. Enable Message Tracking.
    ...  3. Management Appliances>Centralized Services>Email>Spam Quarantine,enable Spam Quarantine.
    ...  4. Management Appliances>Centralized Services>Email>PVO Quarantine,enable PVO.
    ...  5. Commit Changes.

    Spam Quarantine Enable
    PVO Quarantines Enable
    Commit Changes

Tvh1165327c
    [Tags]  interop  Tvh1165327c
    [Documentation]  To verify the settings for configuring PVO in SMA and ESA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165327
    ...  1. LOgin to SMA gui.
    ...  2. Navigate to Management Appliances>Centralized Services>Email>Policy,Virus and Outbreak Quarantines
    ...  3. Launch Migration Wizard for the required ESA. Submit and Commit the changes.
    ...  4. Login to ESA . Go to Security Services ->Centralized Services-> PVO Quarantines . Enable and commit changes.
    FOR  ${esa_name}  IN  @{ESA_NAMES}
      Wait Until Keyword Succeeds  5m  1m  Security Appliances Edit Email Appliance
      ...  ${esa_name}
      ...  pvo=${true}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
      Commit Changes
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

Tvh1165325c
    [Tags]  interop  Tvh1165325c
    [Documentation]  Configure Anti spam in ESA and verify presence of Spam mails in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165325
    ...  1. In ESA, navigate to security services>centralized services>spam quarantine, and edit the details.
    ...  2. Navigate to Monitor-> Spam quarantine . Disable Spam Quarantine locally.
    ...  3. Go to Security Services -> Enable Ironport Anti Spam.
    ...  4. Navigate to Mail Policies-> Incoming mail Policies.
    ...  5. Go to Anti Spam option and enable it by selecting the radio button "Use IronPort Anti-Spam service".
    ...  6. Send Spam positive mail to ESA.
    ...  7. Check the Email Reporting in SMA-> Email.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Set Test Variable  ${spam_messages_count}  2
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
    Selenium Login
    Spam Quarantine Edit
    ...  interface=Management
    ...  port=6025
    Commit Changes
    FOR  ${esa_name}  IN  @{ESA_NAMES}
      Wait Until Keyword Succeeds  5m  1m  Security Appliances Edit Email Appliance
      ...  ${esa_name}
      ...  isq=${true}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    END
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Incoming Mail Summary  column=Messages  col_index=3  count=${expected_count}

Tvh1165330c
    [Tags]  interop  Tvh1165330c
    [Documentation]  Configure  Antivirus quarantine  in ESA and verify presence of Virus quarantined mails in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165330
    ...  1. Navigate to Incoming mail policy-> enable Enable Anti-Virus Scanning.
    ...  2. Set action as Quarantine for "Virus Infected Message". Submit the changes.
    ...  3. Send Virus infected mail to ESA .

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
      ${settings} =  Create Dictionary
      ...  Anti-Virus Scanning  Yes
      ...  Virus Infected Messages Apply Action  Quarantine
      Mail Policies Edit Antivirus
      ...  Incoming
      ...  default
      ...  ${settings}
      Commit Changes
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antivirus/FlashPla_exe.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/virus_encrypted.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Selenium Login
    ${table_data}=   Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=Virus Types Detail  column=Total Infected Messages  col_index=0  count=${esa_cnt}
    Log  ${table_data}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  Virus Types Detail
    Log  ${reporting_data}
    @{col_values} =  Get From Dictionary  ${reporting_data}  Virus Type
    ${value} =  Get From List  ${col_values}  0
    Should Be Equal As Strings  ${value}  EICAR-AV-Test
    ${value} =  Get From List  ${col_values}  1
    Should Be Equal As Strings  ${value}  W32/Redart-A

Tvh1174799c
    [Tags]  interop  Tvh1174799c
    [Documentation]  Configure OutBreakFilter quarantine in ESA and verify presence of OF quarantined mails in SMA
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1174799
    ...  1. Navigate to Incoming mail policy-> Outbreak Filters.
    ...  2. Enable Outbreak Filtering.
    ...  3. Enable message modification and submit the changes.
    ...  4. Send mails (for eg. containing phising url ) to ESA.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${settings}=  Create Dictionary
      ...  Outbreak Filters  Enable Outbreak Filtering (Customize settings)
      ...  Enable Message Modification  ${True}
      Mail Policies Edit Outbreak Filters  incoming  default  ${settings}
      Commit Changes
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  outbreak/vof-phishurl.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  outbreak/vof_multi_phishurl.mbox  ${PUBLIC_LISTENER.ipv4}
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

Tvh1165322c
    [Tags]  interop  Tvh1165322c
    [Documentation]  Verify the functionality of PVO search result in SMA.
    ...  link:Verify the functionality of PVO search result in SMA
    ...  1. Go to ESA, NAvigate to Mail Policies> Incoming Content Filter and Add Incoming Content Filter
    ...  2. Enable Content filters in Incoming Mail Policy
    ...  3. Enable Antivirus and set action as quarantine in Incoming Mail Policy
    ...  4. Send mails with content filter and virus
    ...  5. In SMA, navigate to Email->Message Quarantine ->Policy , Virus and Outbreak Quarantines.
    ...  6. Click on the no. of mail under policy section.
    ...  7. Click on the no. of mail under Virus section.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Library Order SMA
    Selenium Login
    Run Keyword And Ignore Error  Pvo Delete Policy Message  Virus  week
    Run Keyword And Ignore Error  Pvo Release Policy Message  Policy  week
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Selenium Login
      Start CLI Session If Not Open
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
    END
    FOR  ${type}  IN  Policy  Virus
      ${count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  ${type} Messages Count
      ${count}=  Convert To Integer  ${count}
      Should be Equal As Integers  ${count}  ${esa_cnt}
    END

Tvh1174601c
    [Tags]  interop  Tvh1174601c
    [Documentation]  Verify functionality of release and delete actions in PVO quarantine search result.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1174601
    ...  1. In the SMA , navigate to Email->Message Quarantine-> Policy, Virus and Outbreak.
    ...  2. Click on the no. of messages under Policy section.
    ...  3. Select a mail and click on release.
    ...  4. Select another mail from the list and click on delete.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Pvo Delete Policy Message  Virus  today
    Pvo Release Policy Message  Policy  today

Tvh1174878c
    [Tags]  interop  Tvh1174878c
    [Documentation]  Verify that a custom centralized quarantine can be added
    ...  and assigned to DLP default message action in ESA
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1174878
    ...  1. In SMA, navigate to Email->Message Quarantine->PVO Quarantine.
    ...  2. Click on "Add Policy Quarantine".
    ...  3. Add Quarantine name for eg. "upq". Submit the changes.
    ...  4. In ESA, navigate to Mail Policies-> DLP Policy Customization.
    ...  5. Click on "Default Action" . Select "upq" in "Policy Quarantine" section.
    ...  6. Send DLP mails to ESA.
    ...  7. In SMA, navigate to Email->Message Quarantine->PVO Quarantine.

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Clear Email Tracking Reporting Data
    Sync Appliances Datetime  ${SMA}  @{ESA_NAMES}
    Library Order SMA
    Selenium Login
    Add Policy Quarantine  name=upq  retention_period=20  retention_unit=Hours  default_action=delete
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      #Start CLI Session If Not Open
      Restart CLI Session
      Selenium Login
      Dlp Enable
      Commit Changes
      Dlp Edit Settings  enable_matched_content_logging=${True}
      Dlp Message Action Edit  Default Action
      ...  msg_action=quarantine
      ...  quarantine_policy=upq (centralized)
      Dlp Policy New
      ...  Regulatory Compliance
      ...  ${Tvh1165328c_DLP_POLICY}
      ...  submit=${True}
      ${settings}=  Create Dictionary
      ...  DLP Policies  Enable DLP (Customize settings)
      ...  ${Tvh1165328c_DLP_POLICY}  ${True}
      ...  Enable All  ${True}
      Mail Policies Edit DLP  outgoing  default  ${settings}
      Commit Changes
      Sleep  1m
      ${PRIVATE_LISTENER_IP} =  Get ESA Private IP
      Inject Custom Message  dlp/credit_card.mbox  ${PRIVATE_LISTENER_IP}
      Inject Custom Message  dlp/credit_card.mbox  ${PRIVATE_LISTENER_IP}
    END
    Library Order SMA
    Selenium Login
    ${table_data}=   Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  ${RETRY_TIME}
    ...  Get Expected Mail Count  table=DLP Incident Details  column=Total  col_index=0  count=${expected_count}
    Log  ${table_data}
    ${table_data}=   Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}
    ...  ${RETRY_TIME}
    ...  Email Report Table Get Data  DLP Incident Details
    Log  ${table_data}
    Sleep  1m
    ${policy}=  Pvo Policy Get List
    Log  ${policy}
    ${policy_values} =  Get From Dictionary  ${policy}  upq
    ${mail_value}=  Get From Dictionary  ${policy_values}  messages
    Should Be Equal As Integers  ${mail_value}  ${expected_count}

Tvh1165329c
    [Tags]  interop  Tvh1165329c
    [Documentation]  To verify the functionality of  End User Spam Quarantine in SMA.
    ...  link:http://tims.cisco.com/view-entity.cmd?ent=1165329
    ...  1. Navigate to Management Appliance ->Centralised Services -> Spam Quarantine.
    ...  2. Click on "Edit Settings".
    ...  3. In Edit Spam Quarantine page
    ...  a. Enable End-User Quarantine Access (eg . using LDAP/ SAML)
    ...  b. Enable Spam Notification
    ...  4. In Spam Notification Section -> enter the below settings
    ...  a. enter the from address
    ...  b. Enter email address in 'Deliver Bounce Message To' section.
    ...  c. select the Notification schedule
    ...  5. Click on submit, and Enable End user safe list / block list,Commit changes
    ...  6. Go to Network tab -> IP interfaces -> click on management interface
    ...  7. Enter the spam quarantine port for 'HTTPS'.
    ...  8. Enter the end user spam quarantine URL
    ...  9. Click on submit and commit changes
    [Setup]  Do Tvh1165329c Setup

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    ${recipient}=  Set Variable  ${MAIL_LOCAL_ADDRESS}
    ${rcpt_file}=  Join Path  ${SUITE_TMP_DIR}  ${TEST_ID}_rcpts.txt
    OperatingSystem.Create File  ${rcpt_file}
    OperatingSystem.Append To File  ${rcpt_file}  ${recipient}\n
    Set Test Variable  ${rcpt_file}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Spam Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Spam Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order Sma
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarntine Search  date_range=week
    Log Out of DUT
    Log Into DUT  ${ldap_user}  ${PASSWORD}
    Library Order SMA
    Force ISQ Notifications
    Verify Log Contains Records
    ...  ISQ: Quarantined MID >= ${esa_cnt}

    ${mid}=  Get Mid Value  MID .* Subject .*${SPAM_NOTIF_SUBJ}.*
    Verify Log Contains Records
    ...  MID ${mid} .* .*test@${CLIENT}.* >= ${esa_cnt}

    ${ENCOED_MAIL_CONTENT}=  Fetch Mail Content Using Drain
    Message Load  ${ENCOED_MAIL_CONTENT}
    ${subj}=  Message Get  Subject
    Should Contain  ${subj}  ${SPAM_NOTIF_SUBJ}
    ${COMMAND}=  Catenate  python -c "import re, base64; data = '''${ENCOED_MAIL_CONTENT}'''.split('Notification')[1]; decoded_data = base64.b64decode(data);
    ...  urls = re.findall('''<a href=.(.*?).>''', decoded_data) ; print str(list(set(urls)))[1:-2]"
    ${RETURN_CODE}  ${URLS_LIST}=  OperatingSystem.Run And Return Rc And Output   ${COMMAND}
    Log  ${URLS_LIST}
    @{email_urls}=  Split String  ${URLS_LIST}  ,
    Log  ${RETURN_CODE}
    ${email_urls_count}=  Get Length  ${email_urls}
    Log  ${email_urls_count}
    Should Be Equal As Numbers  ${email_urls_count}  5
    FOR  ${url}  IN  @{email_urls}
         Run Keyword If  'Detail' in "${url}"
         ...  Check Detail Message Through Email Links  ${url}
    END
    Message Unload
    Run Keyword And Ignore Error  Null Smtpd Stop

Tvh1327180c
    [Documentation]  Tvh1327180c- Check the behaviour Http Response of Spam Quarantine portal with and without samesite attribute.
    [Tags]  Tvh1327180c  interop
    [Setup]  Run keywords  Close All Browsers
     ...  AND  Set Suite variable  ${SQ_USER}  ${DUT_ADMIN}
     ...  AND  Set Suite variable  ${SQ_USER_PASSWORD}  ${DUT_ADMIN_SSW_PASSWORD}

    # Step 1. Log into DUT and navigate to Email -> Message Quarantine -> Spam Quarantine.
     Selenium Login
     Reload Page
     Navigate To  Email  Message Quarantine  Spam Quarantine

    # Step 2. Click on Spam-Q link and search messages. Open and view  message
     Click Element  ${spam_quarantine_link}
     Sleep  5
     Select Window  NEW
     Spam Quarantine Advanced Search  is_admin=${False}  date_range=week
     Click Element  ${spam_quarantine_message_xpath}

    # Step 3. Open the Spam Q notification link in a different browser for externaly authenticated user .
     Selenium Login
     Log Out of DUT
     Go To  https://${DUT}:83
     Login To Spam Quarantine

    # Step 4. Check user is not logged out from main SMA-GUI portal on main browser.
     Switch Browser  1
     Select Window  MAIN
     Reload Page
     Page Should not contain  //input[@name='username']
     Click Element  ${spam_quarantine_link}
