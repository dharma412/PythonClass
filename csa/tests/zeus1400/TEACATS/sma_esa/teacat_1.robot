*** Settings ***
Library           Collections
Resource          sma/global_sma.txt
Resource          regression.txt
Resource          esa/global.txt

Suite Setup   Run Keywords
              ...  Set Aliases For Appliance Libraries
              ...  Set Appliance Under Test to SMA
              ...  DefaultRegressionSuiteSetup
Suite Teardown   DefaultRegressionSuiteTeardown

*** Variables ***
${CLOUD_USER}            cloud
${CLOUD_USER1}           cloud1
${CLOUD_USER_FULL_NAME}  CloudFullName
${CLOUD_PWD}             Cisco123$
${TIMEOUT}               1438
${PREVIEW}               //*[@id='form']//div/a[1]
${DELIVERY}              //*[@id='form']//td[2]/a
${firefox_prefs_browser.download.dir}  %{SARF_HOME}/tmp
${firefox_prefs_browser.download.folderList}  2
${firefox_prefs_browser.download.manager.showWhenStarting}  false
${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}  application/pdf,text/csv,application/csv

*** Keywords ***
Do CSCvm59381 Setup
    [Arguments]  ${user}=${CLOUD_USER}
    Set Appliance Under Test to SMA
    Set Suite Variable   ${FEATUREKEY}   cloud
    Feature Key Set Key  ${FEATUREKEY}
    Selenium Login
    Spam Quarantine Enable
    Spam Quarantine SlBl Enable
    Pvo Quarantines Enable
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Users Add User  ${user}  ${CLOUD_USER_FULL_NAME}  ${CLOUD_PWD}  user_role=Cloud Administrator
    Network Access Edit Settings  ${TIMEOUT}
    Commit Changes

Verify Pdf Report
    [Arguments]  ${msg}
    Sleep  10s
    ${start_time}=  Get Time
    Wait Until Keyword Succeeds  1m  10s
    ...  Click Element  xpath=${PREVIEW}  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .pdf  start_time=${start_time}  timeout=300
    ...  download_directory=%{SARF_HOME}/tmp
    Set Test Variable  ${path}
    Log  ${path}
    ${out}=  Run  /usr/local/bin/pdf2txt.py ${path}
    Log  ${out}
    Should Contain  ${out}  ${msg}
    Remove File  ${path}

Verify GUI Login OK
    [Arguments]  ${username}  ${password}
    Log Out Of DUT
    Log Into DUT  ${username}  ${password}
    ${title}=  Get Title
    Should Contain  ${title}  Cisco Content Security Management Virtual Appliance

Preview Pdf Report
      Click Element  ${DELIVERY}
      Sleep  5s

*** Test Cases ***
CSCvm59381
    [Documentation]  TEA CES: Unable to view SLBL Safe or Block List via gui using Cloud Admin credentials.
    ...  \n  Create a new user to use the 'Cloud Admin' user role.
    ...  \n  Login to the appliance with the new credentials recently created.
    ...  \n  Access the Spam quarantine via hyperlink
    ...  \n  Attempt to access the SL/BL list from the upper right hand corner.
    [Tags]  CSCvm59381  CSCve72840  invalid_not_applicable_for_smart_license  teacat

    Do CSCvm59381 Setup
    Spam Quarantine Search Page Open  user=${CLOUD_USER}  password=${CLOUD_PWD}
    @{safelist_entries}=   SAFELIST GET
    Page Should Contain  Safelist Management
    @{blocklist_entries}=   BLOCKLIST GET
    Page Should Contain  Blocklist Management
    Log Out of Dut
    Close Browser

CSCvm59892
    [Documentation]  TEA Evaluation of CVE-2016-0483 for SMA
    ...  \n  Patches submitted in OpenJdk version 1.7.0_65
    [Tags]  CSCvm59892  CSCuz74492  teacat
    ${SMA_IP}=  Get Host IP By Name  ${SMA}
    ${output}=  Execute Command And Get Output  ${SMA_IP}  /data/lib/java/jdk1.6.0/jre/bin/java -version
    Should Contain  ${output}  openjdk version "1.7.0_65"

CSCvm65318
    [Documentation]  TEA Evaluation of SMA for FreeBSD CVE-2018-6922
    ...  \n  Patches submitted in freebsd version >= 10.1
    ...  \n  maxqueuelen should be 100
    [Tags]  CSCvm65318  CSCvk74266  teacat

    ${command_output}=  Run On DUT  uname -a
    ${freebsd_version_text}  ${freebsd_version_name}=  Should Match Regexp  ${command_output}  (\\d+.\\d+)\\-RELEASE
    Should Be True  ${freebsd_version_name} >= 10.1
    ${sysctl_command_output}=  Run On DUT  sysctl net.inet.tcp.reass.maxqueuelen
    Should Contain  ${sysctl_command_output}  net.inet.tcp.reass.maxqueuelen: 100

CSCvq82017
    [Documentation]  TEA Cloud Admin cannot preview PDF Report for scheduled/archived reports
    ...  \n Steps to reproduce:
    ...  \n  1. Netinstall SMA 10.5.0-024
    ...  \n  2. Run SSW (System Setup Wizard)
    ...  \n  3. Enable Centralized services
    ...  \n  4. Add ESA (I used C000V build 10.0.0-125 ) , enable Centralized Reporting on ESA.
    ...  \n  5. On SMA generate Feature key for 'Cloud Administrator'
    ...         role using this link http://keys.sgg.cisco.com/key/fkey.cgi
    ...  \n  6. Go to System Administration -> Feature keys and apply key
    ...  \n  7. Go to System Administration -> Users and create user with 'Cloud Administrator' role.
    ...  \n  8. Log out and log back in as previously created user.
    ...  \n  9. Go to Email -> Reports -> Scheduled Reports -> Add ->
    ...         Choose a report type (I used 'Executive Summary' but any should do)
    ...  \n  10. Click on 'Preview PDF Report'
    ...  \n  11. Verify message in PDF file.
    [Tags]  CSCvq82017  teacat

    Library Order ESA
    Selenium Login
    Message Tracking Enable  tracking=centralized
    Centralized Email Reporting Enable
    Commit Changes
    Do CSCvm59381 Setup  ${CLOUD_USER1}
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  tracking=${True}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes
    Verify GUI Login OK  ${CLOUD_USER1}  ${CLOUD_PWD}
    Email Scheduled Reports Add Report  ${sma_email_reports.DELIVERY}  title=DeliveryStatus
    Preview Pdf Report
    Verify Pdf Report  DeliveryStatus
    Selenium Close

CSCvr36463
    [Documentation]  TEA Evaluation of sma for OpenSSL May 2016
    ...  \n  Netinstall  SMA and SSW
    ...  \n  Execute openssl version it should be>1.0.2k.6.1.188
    [Tags]  CSCvr36463  teacat

    ${output}=  Run On DUT  openssl version
    ${ssl_version_text}  ${ssl_version_name}=   Should Match Regexp  ${output}  CiscoSSL (.*)-fips
    Should Be True  '${ssl_version_name}' >= '1.0.2k.6.1.188'
