*** Settings ***
Library           SmaGuiLibrary
Resource          regression.txt
Resource          esa/global.txt
Resource          esa/injector.txt
Resource          sma/csdlresource.txt

Suite Setup  Do CSCvq85670 Setup
Suite Teardown  Do CSCvq85670 Teardown

*** Variables ***
${Spam_xpath}=  //tbody[@class='yui-dt-data']/tr[1]/td[5]//div[@class='yui-dt-liner']//div[@class='crop']//a
${mbox.SPAM}  /home/testuser/work/sarf_centos/tests/testdata/esa/antispam/spam_suspect.mbox
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/
${TEST_ID}  CSCvq85670
${DATA_UPDATE_TIMEOUT}=  20m
${RETRY_TIME}=  15s
${UID}=  CSCvq856701
${UID2}=  CSCvq856702
${PASSWORD}=  ironport
${PASSWORD2}=  ironport2

*** Keywords ***

Do CSCvq85670 Setup
    DefaultRegressionSuiteSetup
    Set Suite Variable  ${MAIL1}  ${UID}@${CLIENT}
    Set Suite Variable  ${MAIL_ROUTING_ADDRESS1}  ${UID}_routing@${CLIENT}
    Set Suite Variable  ${MAIL_LOCAL_ADDRESS1}  ${UID}_local@${CLIENT}
    Set Suite Variable  ${MAIL2}  ${UID2}@${CLIENT}
    Set Suite Variable  ${MAIL_ROUTING_ADDRESS2}  ${UID2}_routing@${CLIENT}
    Set Suite Variable  ${MAIL_LOCAL_ADDRESS2}  ${UID2}_local@${CLIENT}
    :FOR  ${appliance}  IN  @{esa_appliances}
    \  Library Order ${appliance}
    \  Smtp Routes New  domain=ALL  dest_hosts=/dev/null
    \  Commit
    \  Selenium Login
    \  Quarantines Spam Disable
    \  Message Tracking Enable  tracking=centralized
    \  Centralized Email Reporting Enable
    \  EUQ Enable  ${SMA}  ${SMA_IP}  enable_slbl=${False}
    \  AntiSpam Enable  IronPort
    \  ${settings}=  Create Dictionary  Positive Spam Apply Action  Spam Quarantine
    \  Mail Policies Edit Antispam  incoming  default  ${settings}
    \  Commit Changes
    Library Order SMA
    Selenium Login
    Spam Quarantine Enable
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    Commit Changes
    LDAP Client Connect  ${LDAP_AUTH_SERVER}
    ...  ldap_server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  basedn=${LDAP_BASEDN}
    ...  binddn=${LDAP_BINDDN}
    ...  password=${LDAP_PASSWORD}
    Run Keyword And Ignore Error  Ldap Client Delete User  ${UID}
    Run Keyword And Ignore Error  Ldap Client Delete User  ${UID2}
    LDAP Client Create User  uid=${UID}  password=${PASSWORD}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}  mail=${MAIL1}
    ...  mail_local_address=${MAIL_LOCAL_ADDRESS1}
    ...  mail_routing_address=${MAIL_ROUTING_ADDRESS1}
    Commit Changes
    LDAP Client Create User  uid=${UID2}  password=${PASSWORD2}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}  mail=${MAIL2}
    ...  mail_local_address=${MAIL_LOCAL_ADDRESS2}
    ...  mail_routing_address=${MAIL_ROUTING_ADDRESS2}
    Commit Changes
    Set Suite Variable  ${PROFILE_NAME}  mainldapprofile
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
    Commit Changes
    Spam Quarantine Edit EndUser Access
    ...  end_user_access_enable=${True}
    ...  end_user_hide_body=${True}=${True}
    ...  end_user_auth=LDAP
    Commit Changes
    Wait Until Keyword Succeeds  5m  1m  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes

Do CSCvq85670 Teardown
    Clear Email Tracking Reporting Data
    Run Keyword And Ignore Error  Ldap Client Delete User  ${UID}
    Run Keyword And Ignore Error  Ldap Client Delete User  ${UID1}
    LDAP Client Disconnect
    DefaultRegressionSuiteTeardown

Spam Quarantine Search
    [Arguments]  ${date_range}=today
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  date_range=${date_range}
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    [Return]  ${actual_spam_count}

Clear Email Tracking Reporting Data
    :FOR  ${appliance}  IN  @{esa_appliances}
      Library Order ESA
      Roll Over Now
      Commit
      Diagnostic Reporting Delete Db  confirm=yes
      Wait Until Ready
      Diagnostic Tracking Delete Db   confirm=yes
      Wait Until Ready
    END
    Library Order Sma
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready

*** Test Cases ***

CSCvq85670
    [Documentation]  Unauthorized Access to users mail
    ...  1. Enable Centralized message tracking and reporting.
    ...  2. Create two LDAP Users and enable Spam Quarantine End User Access.
    ...  3. Clear the reporting Data and send Spam messages to LDAP users.
    ...  4. Check Spam Quarantine messages recieved.
    Clear Email Tracking Reporting Data
    Library Order SMA
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run Keyword And Ignore Error  Turn SLBL Entries  Delete
    Go To  https://${DUT}:83
    Run Keyword And Ignore Error  Spam Quarantine Delete Messages  date_range=today
    Commit Changes
    Library Order SMA
    Selenium Login
    Spam Quarantine Edit
    ...  interface=Management
    ...  port=6025
    Commit Changes
    Library Order ESA
    Start CLI Session If Not Open
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${PUBLIC_LISTENER}
    ${recipient}=  Set Variable  ${MAIL1}
    ${SUITE_TMP_DIR}=  Evaluate  tempfile.mkdtemp()  tempfile
    Set Suite Variable  ${SUITE_TMP_DIR}
    ${rcpt_file}=  Join Path  ${SUITE_TMP_DIR}  ${TEST_ID}_rcpts.txt
    OperatingSystem.Create File  ${rcpt_file}
    OperatingSystem.Append To File  ${rcpt_file}  ${recipient}
    Inject Messages  inject-host=${PUBLIC_LISTENER.ipv4}  num-msgs=1
    ...  address-list=${rcpt_file}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${mbox.SPAM}
    Library Order SMA
    Go To Euq Gui  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Go To  https://${DUT}:83
    ${spam_count}=  Wait Until Keyword Succeeds  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
    ...  Spam Quarantine Search  date_range=today
    Log  ${spam_count}
    Click Element  ${Spam_xpath}
    Page Should Contain  Message Details
    Sleep  25s
    ${url}=  Get Location
    Log Out Of DUT
    Go To  ${url}
    Log Into DUT  ${MAIL1}  ${PASSWORD}
    Page Should Contain  Message Details
    Log Out Of DUT
    Go To  ${url}
    Log Into DUT  ${MAIL2}  ${PASSWORD2}
    @{spam_quarantines_messages}=  Spam Quarantine Advanced Search
    ...  date_range=today
    ${actual_spam_count}=  Get Length  ${spam_quarantines_messages}
    Should Be Equal As Integers  ${actual_spam_count}  0
    Remove File  ${rcpt_file}
