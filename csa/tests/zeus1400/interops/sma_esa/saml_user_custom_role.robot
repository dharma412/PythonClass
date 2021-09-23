# $ Id: $
# $ DateTime:  $
# $ Author: $

*** Settings ***
Resource     sma/global_sma.txt
Resource     esa/global.txt
Resource     regression.txt
Resource     sma/esasma.txt
Resource     sma/saml.txt
Library      SeleniumLibrary
Library      OperatingSystem

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Set Appliance Under Test to SMA
...  Initialize Suite

Suite Teardown  Finalize Suite

*** Variables ***
${DATA_UPDATE_TIMEOUT}=  30m
${RETRY_TIME}=  30s
${expected_count}=  2
${Full_Name}  test_user
${user_password}  Aa#124578
${CONFIG_PATH}     /data/pub/configuration
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${Report_Link}  //a[contains (text(),'All Reports')]
${Quarantine_Link}  //a[contains (text(),'Policy')]
${spam_qxpath}=  //a[@title='Spam Quarantine (open in new window)']
${MAIL_ADDR}   testuser@cisco.com
${MAIL_BADDR}  test@cisco.com
${TEST_EUQ_SP_PROFILE}=  euq_sp_profile
${TEST_EUQ_IDP_PROFILE}=   euq_idp_profile

*** Keywords ***
Initialize Suite
    global_sma.DefaultTestSuiteSetup
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    PVO Quarantines Enable
    Commit Changes

    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=SAML 2.0

    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_fname=${MAIL_ADDR}
    ...  spam_notif_username=testuser
    ...  spam_notif_domain=cisco.com
    ...  spam_notif_enable_login=${True}
    ...  spam_notif_consolidate=${True}
    ...  spam_notif_baddr=${MAIL_BADDR}

    Spam Quarantine SlBl Enable
    Commit Changes
    IP Interfaces Edit  Management  isq_https_service=83  isq_default=https://${DUT}:83/  hostname=${DUT}
    Commit Changes
    Selenium Close

    ${esa_duts}=  Set Variable  ${ESA_IDS}
    @{esa_appliances}=  Split String  ${esa_duts}  ,
    Set Suite Variable  @{esa_appliances}
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup
    ...  should_revert_to_initial=${False}
    ${ESA_ORIG_CONF}=  Save Config
    Set Suite Variable  ${ESA_ORIG_CONF}
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    ${ESA_PUB_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${ESA_PUB_LISTENER}
    Message Tracking Enable  tracking=centralized
    Centralized Email Reporting Enable
    Clean System Quarantines
    Quarantines Spam Disable
    Euq Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    Commit Changes
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp(dir="%{SARF_HOME}/tmp")  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}
    @{ESA_NAMES}=    Create List

    Library Order SMA
    Selenium Login
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    FOR  ${appliance}  IN  @{esa_appliances}
      Wait Until Keyword Succeeds  1m  10s
      ...  Security Appliances Add Email Appliance
      ...  ${${appliance}}
      ...  ${${appliance}_IP}
      ...  tracking=${True}
      ...  reporting=${True}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
      Commit Changes
      Append To List    ${ESA_NAMES}  ${${appliance}}
    END
    ${expected_count}=  Convert To Integer  ${expected_count}
    ${esa_cnt}=  Get Length  ${esa_appliances}
    ${expected_count}=  Evaluate    ${esa_cnt} * ${expected_count}
    Set Suite Variable  ${expected_count}
    Set Suite Variable  ${esa_cnt}

    Library Order Sma
    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Wait Until Keyword Succeeds  5m  1m  Pvo Quarantines Enable
      Run Keyword And Ignore Error  Commit Changes
    END
    Library Order Sma
    Clean System Quarantines
    Start Cli Session If Not Open
    Roll Over Now  mail_logs
    Add Users With All Possible Roles
    Add Customer/Devops SAML Config Azure  ${USER_ROLE}
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID_Azure}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP FOR EUQ  ${TEST_EUQ_SP_PROFILE}  ${TEST_EUQ_IDP_PROFILE}  ${settings}
    Commit Changes

Finalize Suite
    Clear Email Tracking Reporting Data
    Set Appliance Under Test To ESA
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ${appliance}
      PVO Quarantines Disable
      Commit Changes
      Selenium Close
    END
    DefaultTestSuiteTeardown

    Set Appliance Under Test To SMA
    DefaultTestSuiteTeardown

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

Do Tvh1437041c Setup
    Set Appliance Under Test to SMA
    DefaultTestCaseSetup
    Selenium Login

Go To Spam Quarantine
    Navigate To  Email  Message Quarantine  Spam Quarantine
    Click Element  ${spam_qxpath}  don't wait
    Run Keyword And Ignore Error  Capture Page Screenshot
    ${title_var}        Get Window Titles
    Select Window       title=@{title_var}[1]

Enable Externalauth Customer
    [Arguments]  ${user_role}
    Users Edit External Authentication  SAML
    ...  extauth_attribute_name_map=
    ...  group_mapping=${SAML_GROUP_Azure}:${user_role}
    Commit Changes

Add Customer/Devops SAML Config Azure
    [Arguments]  ${user_role}
    ${settings}=  Create Dictionary
    ...  User Role                          ${user_role}
    ...  SP Entity ID                       ${SP_ENTITY_ID_Azure}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP  ${TEST_SP_PROFILE}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes

Clear Email Tracking Reporting Data
    FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ESA
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

Check Spam Count
    [Arguments]  ${expected}=${expected_count}
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  date_range=week
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Run Keyword If  ${actual_spam_count} != ${expected}  Fail
    [Return]  ${actual_spam_count}

Get Expected Mail Count
    [Arguments]   ${table}=DLP Incident Details  ${column}=Messages  ${col_index}=0   ${count}=0
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Email Report Table Get Data  ${table}
    Log  ${reporting_data}
    @{col_values} =  Get From Dictionary  ${reporting_data}  ${column}
    ${mail_value} =  Get From List  ${col_values}  ${col_index}
    Run Keyword If  ${mail_value} != ${count}  Fail
    [Return]  ${mail_value}

Add User With Specified Role
   [Arguments]  ${User}  ${Role}
   Users Add User  ${User}  ${Full_Name}  ${user_password}  ${Role}

Add Users With All Possible Roles
   Run Keyword If  ${USE_SMART_LICENSE} == 0
   ...  Feature Key Set Key  cloud
   User Roles Email Role Add  EmailRole01  reporting_access=Appliances
   ...  report_type=All Reports  tracking_access=${True}
   ...  quarantine_access=${True}  quarantine_type=spam
   Add User With Specified Role  customuser  EmailRole01
   User Roles Email Role Add  EmailRole02
   ...  quarantine_access=${True}  quarantine_type=outbreak
   User Roles Email Role Edit  EmailRole02
   ...  quarantine_access=${True}  quarantine_type=virus
   User Roles Email Role Edit  EmailRole02
   ...  quarantine_access=${True}  quarantine_type=policy
   Add User With Specified Role  customuser1  EmailRole02
   Commit Changes

Check Message Tracking
   ${messages}=  Email Message Tracking Search
   ${tracking_message_count}=  Email Message Tracking Get Total Result Count  ${messages}
   Should Be Equal As Strings  ${tracking_message_count}  5

*** Test Cases ***

Tvh1437041c
    [Tags]  interop  Tvh1437041c
    [Documentation]  To verify the access of saml custom user
    ...  TIMS Link:https://tims.cisco.com/view-entity.cmd?ent=1437041
    ...  1. Login as admin and create SAML profile with SP and IDP.
    ...  2. create custom roles ( like pvo access, spam access, "only reporing" etc"
    ...  3. Enable external authenticateion under "users" -> system administrator page.
    ...  4. Provide SAML group name and User Role as "custom role". (save the changes)
    ...  5. Send Live traffic into reporting, tracking, spam and PVO from ESA to SMA.
    ...  6. Now logout.
    ...  7. Login again as saml "custom user" by clicking on SSO button.
    ...  8. Validate the behaviour according to custom roles.

    [Setup]  Do Tvh1437041c Setup

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    FOR  ${esa}  IN  @{esa_appliances}
      Library Order ${esa}
      Start CLI Session If Not Open
      ${PUBLIC_LISTENER}=  Get ESA Listener
      Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
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
      ${settings}=  Create Dictionary
      ...  Outbreak Filters  Enable Outbreak Filtering (Customize settings)
      ...  Enable Message Modification  ${True}
      Mail Policies Edit Outbreak Filters  incoming  default  ${settings}
      Commit Changes
      Inject Custom Message  contentscanning/MSOfficePptAttach.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  antivirus/testvirus.mbox  ${PUBLIC_LISTENER.ipv4}
      Inject Custom Message  outbreak/vofmanual.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Library Order SMA
    Enable Externalauth Customer  EmailRole01
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Click Link  ${Report_Link}
    Go To Spam Quarantine
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Check Spam Count
    Close Window
    ${title_var}        Get Window Titles
    Select Window       title=@{title_var}[0]
    Go To  https://${DUT}
    Click Link  ${Report_Link}
    Get Expected Mail Count  table=Incoming Mail Details
    ...  column=Stopped by Content Filter  col_index=0  count=1
    Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Check Message Tracking
    Log Out of DUT
    Log Into Dut
    Enable Externalauth Customer  EmailRole02
    Log Out of DUT
    SSO Log Into Dut  ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure
    Click Link  ${Quarantine_Link}
    FOR  ${type}  IN  Policy  Virus  Outbreak
       ${count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}  ${type} Messages Count
       ${count}=  Convert To Integer  ${count}
       Should be Equal As Integers  ${count}  1
    END
    Selenium Close
