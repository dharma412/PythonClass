*** Settings ***
Library      Telnet  30
Resource     esa/backdoor_snippets.txt
Resource     esa/global.txt
Resource     esa/injector.txt
Resource     regression.txt
Resource     esa/logs_parsing_snippets.txt

Variables    esa/mbox.py

*** Variables ***
${MAILBOX_O365}=  office365
${MAILBOX_GSUITE}=  gsuite
${ROUTING_MODE_JOURNAL}=  journaling
${ROUTING_MODE_BCC}=  bcc
${NON_JOURNAL_ACTION_DROP}=  drop
${NON_JOURNAL_ACTION_DELIVER}=  deliver
${ALLOW_TRAFFIC}=  external-inbound

${JOURNAL_RECIPIENT_EMAIL}=  journal_recipient@journal.cisco.com
${HEIMDALL_JOURNAL_LOG}=  journal_transformer
${EXPECTED_LOG_JOURNAL}=  SENDER: original_sender@cisco.com
${HERMES_SERVICE}=  hermes
${JOURNAL_PUB_LOG_FILE}=  /data/pub/easy_pov/easy_pov.current

*** Keywords ***
Do Easypov Suite Setup
    [Arguments]  ${enable_easypov}=1

    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA
    DefaultTestSuiteSetup

    ${ESA_PUB_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${ESA_PUB_LISTENER}
    ${ESA_PUBLIC_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUBLIC_LISTENER_IP}
    ${CLIENT_D1_IP}=  Get Host IP By Name  d1.${CLIENT}
    Set Suite Variable  ${CLIENT_D1_IP}
    Set Suite Variable  ${PUBLIC_LISTENER_NAME}  ${ESA_PUB_LISTENER.name}

    ${ESA_PRIVATE_LISTENER}=  Get ESA Listener  Private
    Set Suite Variable  ${ESA_PRIVATE_LISTENER}
    ${ESA_PRIVATE_LISTENER_IP}=  Get ESA Private IP
    Set Suite Variable  ${ESA_PRIVATE_LISTENER_IP}    

    Listenerconfig Edit Rcptaccess Edit  ${ESA_PUB_LISTENER.name}
    ...  ALL
    ...  access=1

    EsaCliLibrary.Smtp Routes New
    ...  domain=ALL
    ...  dest_hosts=/dev/null

    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Set Key  cloud
    Commit

    Run Keyword If  ${enable_easypov} == 1
    ...  Enable EasyPoV

Do Easypov Suite Teardown
    Listenerconfig Edit Rcptaccess Edit  ${ESA_PUB_LISTENER.name}
    ...  ALL
    ...  access=2

    EsaCliLibrary.Smtp Routes Clear
    Commit
    Disable EasyPoV

    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Feature Key Delete Key  cloud
    Commit

    DefaultTestSuiteTeardown

Enable EasyPoV
    [Arguments]   ${mailbox}=${MAILBOX_O365}  ${routing_mode}=${ROUTING_MODE_JOURNAL}
    ...  ${journal_mail_to}=${JOURNAL_RECIPIENT_EMAIL}
    ...  ${non_journal_action}=${NON_JOURNAL_ACTION_DROP}
    ...  ${allow-traffic}=${ALLOW_TRAFFIC}

    ${output}=  Journal Config Enable  mailbox=${mailbox}
    ...  routing-mode=${routing_mode}
    ...  journal-mail-to=${journal_mail_to}
    ...  non-journal-action=${non_journal_action}
    ...  allow-traffic=${allow-traffic}
    Commit

    ${status}=  Journal Config Is Enabled
    Should Be True  ${status}

    Wait Until Keyword Succeeds  30 sec  5 sec
    ...  Is EasyPoV Enabled

    [return]  ${output}

Disable EasyPoV
    Journal Config Disable
    Commit

Is EasyPoV Enabled
    ${status}=  Dut File Exists  ${JOURNAL_PUB_LOG_FILE}
    Should Be True  ${status}

Inject Message And Check Log
    [Arguments]   ${msg_box}  ${search_str}  ${recipient_email}=${JOURNAL_RECIPIENT_EMAIL}
    ...  ${inject_iface}=${ESA_PUBLIC_LISTENER_IP}
    ...  ${is_search_str_re}=${FALSE}  ${does_log_contain_str}=${TRUE}  ${str_count}=1
    ...  ${log_timeout}=60  ${log_type}=mail

    Rollover Now
    Inject Messages  mbox-filename=${msg_box}  inject-host=${inject_iface}  num-msgs=1
    ...  rcpt-host-list=${recipient_email}

    Verify And Wait For Log Records
    ...  search_path=${log_type}
    ...  ${search_str} ==${str_count}
