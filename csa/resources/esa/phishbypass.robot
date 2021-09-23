*** Settings ***
Resource     esa/global.txt
Resource     esa/logs_parsing_snippets.txt
Resource     esa/injector.txt
Resource     regression.txt

*** Variables ***
${SENDER_GROUP_NAME}  PHISHBYPASSLIST 


*** Keywords  ***
Phishbypass Suite Setup
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

    Add Sendegroup Via GUI 

Phishbypass Suite Teardown
    Remove Sendegroup Via GUI 

    DefaultTestSuiteTeardown

Add Sendegroup Via GUI
    HAT Sender Group Add
    ...  ${PUBLIC_LISTENER_NAME} 
    ...  name=${SENDER_GROUP_NAME}
    ...  order=1
    ...  policy=CYBERSEC_AWARENESS_ALLOWED
    ...  sender_host=${CLIENT_IP}, Phishing Bypass 
    commit changes

Remove Sendegroup Via GUI
    HAT Sender Group Delete
    ...  ${PUBLIC_LISTENER_NAME}
    ...  ${SENDER_GROUP_NAME}
    commit changes

Do Common Testcase Setup
    DefaultTestCaseSetup

    EsaCliLibrary.Smtp Routes New
    ...  domain=ALL
    ...  dest_hosts=/dev/null
    commit

    Roll Over Now  mail_logs

Do Common Testcase Teardown
    EsaCliLibrary.Smtp Routes Delete
    ...  domain=ALL
    Commit

    DefaultTestCaseTeardown
