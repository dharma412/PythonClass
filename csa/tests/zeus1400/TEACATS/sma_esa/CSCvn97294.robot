*** Settings ***
Suite Setup        DefaultRegressionSuiteSetup
Suite Teardown     DefaultRegressionSuiteTeardown
Test Setup         DefaultRegressionTestCaseSetup
Test Teardown      DefaultRegressionTestCaseTeardown
Resource           regression.txt


*** Keywords ***

Connect SSH
    Set SSHLib Timeout  300s
    Set SSHLib Prompt  ]
    Open Connection  ${DUT}
    Login  ${RTESTUSER}    ${RTESTUSER_PASSWORD}

Clear Email Tracking Reporting Data
    Library Order ESA
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready
    Library Order Sma
    Roll Over Now
    Commit
    Diagnostic Reporting Delete Db  confirm=yes
    Wait Until Ready
    Diagnostic Tracking Delete Db   confirm=yes
    Wait Until Ready


***Testcases***
CSCvn97294
    [Tags]  CSCvn97294  teacat
    [Documentation]  TEA Miscellaneous Files usage calculation includes tracking database size
    ...  1.verify the disk usage details before starting test.
    ...  2.Copy the stored Email tracking data to SMA and extract.
    ...  3.Verity like only Email tracking data only memroy size is increased.
    ...  4.steps to copy the email tracking data.
    ...      1.stop splunk on your SMA:  /data/bin/heimdall_svc down splunkd
    ...      2.remove existing db folder on that SMA: rm –rf /data/db/splunk
    ...      3.SCP DB from repo location to this SMA: “/data/db/splunk”
    ...      4.start splunk on your SMA:  /data/bin/heimdall_svc -u splunkd

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Clear Email Tracking Reporting Data
    Library Order ESA
    Selenium Login
    Message Tracking Enable  tracking=centralized
    Centralized Email Reporting Enable
    Commit Changes
    Library Order SMA
    Selenium Login
    Centralized Email Message Tracking Enable
    Centralized Email Reporting Enable
    Wait Until Keyword Succeeds  1m  10s
    ...  Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes
    ${email_tracking_usage} =  Disk Management Get Service Usage
    ...  Centralized Email Tracking
    Log  ${email_tracking_usage}
    ${mis_usage} =  Disk Management Get Service Usage
    ...  Miscellaneous Files
    Log  ${mis_usage}
    Connect SSH
    Write  /data/bin/heimdall_svc down splunkd
    Read Until Prompt
    Write  rm -rf /data/db/splunk
    Read Until Prompt
    Write  mkdir /data/db/splunk
    Read Until Prompt
    Copy File To DUT  %{SARF_HOME}/tests/testdata/sma/tracking.tgz  /data/db/splunk/
    Write  cd /data/db/splunk
    Read Until Prompt
    Write  tar -xzvf tracking.tgz
    Read Until Prompt
    Write  /data/bin/heimdall_svc -u splunkd
    Read Until Prompt
    ${email_tracking_usage1} =  Disk Management Get Service Usage
    ...  Centralized Email Tracking
    Log  ${email_tracking_usage1}
    ${mis_usage1} =  Disk Management Get Service Usage
    ...  Miscellaneous Files
    Log  ${mis_usage1}
    Should Be Equal As Strings  ${mis_usage}  ${mis_usage1}
    Should Not Be Equal As Strings  ${email_tracking_usage}  ${email_tracking_usage1}
