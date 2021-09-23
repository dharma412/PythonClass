*** Settings ***

Resource     esa/injector.txt
Resource     regression.txt
Resource     sma/esasma.txt
Resource     sma/global_sma.txt

*** Variables ***
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/

*** Keywords ***

Inject Custom Message
    [Arguments]  ${mails}  ${inject-host}
    ${MAIL_MBOX}=  Join Path  ${MAIL_PATH}  ${mails}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_ID}@${CLIENT}
    ...  mbox-filename=${MAIL_MBOX}

*** Test Cases ***

Quarantine
    [Documentation]  Verify spam quarantine functionality
    [Tags]  Quarantine

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    DefaultRegressionSuiteSetup
    ${ESA_PUBLIC_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUBLIC_LISTENER_IP}
    Admin Access Config Timeout   timeout_webui=1440  timeout_cli=1440
    Commit
    Smtp Routes New  domain=ALL  dest_hosts=/dev/null
    Message Tracking Enable  tracking=centralized
    Centralized Email Reporting Enable
    ${local_spam_quarantine_enabled}=  Quarantines Spam Is Enabled
    Run Keyword If  ${local_spam_quarantine_enabled}  Quarantines Spam Disable
    Antispam Enable  IronPort
    EUQ Enable  ${SMA}  ${SMA_IP}  enable_slbl=${True}
    ${settings}=  Create Dictionary  Positive Spam Apply Action  Spam Quarantine
    Mail Policies Edit Antispam  incoming  default  ${settings}
    Commit Changes
    Selenium Close
    Library Order SMA
    Clean System Quarantines
    Roll Over Now  mail_logs
    Spam Quarantine Enable
    Spam Quarantine Edit
    ...  interface=Management
    ...  port=6025
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes
    Selenium Close
    FOR  ${esa}  IN  @{esa_appliances}
         Library Order ${esa}
         Restart CLI session
         ${PUBLIC_LISTENER}=  Get ESA Listener
         Inject Custom Message  antispam/spam_suspect.mbox  ${PUBLIC_LISTENER.ipv4}
         Inject Custom Message  antispam/spam_url.mbox  ${PUBLIC_LISTENER.ipv4}
    END
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    SMANGGuiLibrary.Launch Dut Browser
    SMANGGuiLibrary.Login Into Dut  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ${spam_msgs}=  SMANGGuiLibrary.Spam Quarantine Search
    Log  ${spam_msgs}
    Spam Quarantine Delete  wheretype=From  subject=Contains   type_name=danel
    Spam Quarantine Release
    ...  mesg_received=Last 7 days  wheretype=To
    ...  subject=Contains   type_name=suspectspam@suspectspam.com
    SMANGGuiLibrary.Close Browser
