*** Settings ***
Resource     esa/global.txt
Resource     esa/logs_parsing_snippets.txt
Resource     esa/injector.txt
Resource     regression.txt

*** Variables ***
${CSA_HAPPY_CLICKERS_LIST_PATH}  %{SARF_HOME}/tests/testdata/esa/csa/${CSA_HAPPY_CLICKERS_LIST}

*** Keywords  ***
Csa Suite Setup

    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA

    DefaultTestSuiteSetup

    ${ESA_PUB_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${ESA_PUB_LISTENER}
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    ${ESA_PR_LISTENER_IP}=  Get ESA Private IP
    Set Suite Variable  ${ESA_PR_LISTENER_IP}

    RAT Recipient Edit  InBoundMail   All  action=Accept
    Commit Changes

    Admin Access Config Timeout
    ...  timeout_webui=1440
    ...  timeout_cli=1440
    Commit

    Enable CSA Via CLI 
    Replace Happy Clickers List 

    ${status_msgs}=  Csa Show List
    Log  ${status_msgs}
    ${report_list}=  Get From List  ${status_msgs}  0
    ${status}=  Get From List  ${status_msgs}  2
    ${report_list}=  Convert To Integer  ${report_list}
    ${csa_list}=  Convert To Integer  2020
    Should Be Equal  ${report_list}  ${csa_list} 
    Should Contain  ${status}  Active

Csa Suite Teardown
    Disable CSA Via CLI 

    DefaultTestSuiteTeardown

Enable CSA Via CLI 
    Csa Config Enable
    ...  csa_region=AMERICA
    ...  csa_token=${CSA_TOKEN}
    ...  csa_polling_interval=7d
    commit

    Verify Log Contains Records  search_path=csa_logs  timeout=60
    ...  CSA: The update of the Repeat Clickers list was completed at \\[.*\\]. Version: 1 >= 1
    ...  An application fault occurred.* == 0

Enable CSA Via GUI
    Csa Enable  csa_server=AMERICAS
    ...  csa_token=${CSA_TOKEN}
    ...  csa_polling_interval=1d
    commit changes

Disable CSA Via CLI
    Csa Config Disable
    ...  csa_disable=Y
    commit

Disable CSA Via GUI
    Csa Disable
    Commit Changes

Check Happy Clickers List
    [Arguments]  ${csa_happy_clickers_list}
    ${output} =  Run On Dut  ls /data/csa/reports
    Should Contain  ${output}  ${csa_happy_clickers_list}
 
Replace Happy Clickers List
    Wait Until Keyword Succeeds  30 sec  5 sec
    ...  Check Happy Clickers List  ${CSA_HAPPY_CLICKERS_LIST}

    SCP
    ...  from_location=${CSA_HAPPY_CLICKERS_LIST_PATH}
    ...  to_location=/data/csa/reports/
    ...  to_host=${ESA}

    Restart Service And Check Status  hermes

Clear Heimdall Csa Logs
     Heimdall Rollover Log  csa_logs 
     Restart Service And Check Status  csa 
     Restart Service And Check Status  hermes

Do Common Testcase Setup
    DefaultTestCaseSetup

    EsaCliLibrary.Smtp Routes New
    ...  domain=ALL
    ...  dest_hosts=/dev/null
    commit

    Roll Over Now  mail_logs
    Roll Over Now  csa
    Clear Heimdall Csa Logs

Do Common Testcase Teardown
    EsaCliLibrary.Smtp Routes Delete
    ...  domain=ALL
    Commit

    DefaultTestCaseTeardown
