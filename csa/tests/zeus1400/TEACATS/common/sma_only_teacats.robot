license_smart.txt*** Settings ***
Resource           regression.txt
Resource           sma/saml.txt
Variables          sma/saml_constants.py
Suite Setup        CustomTestSuiteSetup
Suite Teardown     DefaultTestSuiteTeardown
Test Setup         DefaultRegressionTestCaseSetup
Test Teardown      DefaultRegressionTestCaseTeardown
Force Tags         teacat


*** Variables ***

${RANDOM_PASS}  randomstr
${IDP_file}    %{SARF_HOME}/tests/testdata/sma/saml/idp-metadata_unil.xml

*** Keywords ***
CustomTestSuiteSetup
    DefaultRegressionSuiteSetup
    Set Suite Variable  ${SSW}  ${False}

Enable FTP
    Run Keyword And Ignore Error  Log Out Of Dut
    Log Into Dut
    IP Interfaces Edit  Management   ftp_service=${True}
    Commit Changes

FTP Login
    [Arguments]  ${DUT_LOGIN_USER}=${DUT_ADMIN}  ${DUT_LOGIN_PASS}=${DUT_ADMIN_SSW_PASSWORD}
    Open Connection  ${CLIENT_HOSTNAME}
    Login   ${TESTUSER}    ${TESTUSER_PASSWORD}
    ${prompt}  Set SSHLib Prompt  $
    ${timeout}=  Set SSHLib Timeout  30 seconds
    Write  telnet ${DUT} 21
    ${out}=  Read Until  Escape character is '^]'
    Log  ${out}
    Write  USER ${DUT_LOGIN_USER}
    Read Until  331 Password required.
    Write  PASS ${DUT_LOGIN_PASS}
    Sleep  20s
    ${out}=  Read
    Log  ${out}
    Write  quit
    Close Connection
    Set SSHLib Prompt  ${EMPTY}
    [RETURN]  ${out}

Verify ktrace Status
    Connect SSH
    Write  ktrace
    ${out}=  Read Until Prompt
    Should Not Match Regexp  ${out}  .*Function not implemented.*
    Should Match Regexp  ${out}  .*ktrace.*
    Close Connection

Connect SSH
    Set SSHLib Timeout  300s
    Set SSHLib Prompt  ]
    Open Connection  ${DUT}
    Login  ${RTESTUSER}    ${RTESTUSER_PASSWORD}

Verify SSL Config Settings GUI
    [Arguments]  ${versions}=None
    ${ServicesList}  Get SSL Configuration Settings
    FOR  ${service}  IN   Appliance Management Web User Interface
    ...  Secure LDAP Services  Updater Service
      Page Should Contain  ${service}
      ${service_list}=  Get From Dictionary  ${ServicesList}  ${service}
      Lists Should Be Equal  ${versions}  ${service_list}
      ...  msg=${service} Enabled protocol details are mismatched
    END

***Test Cases***

CSCvp75623
    [Tags]  CSCvp75623  teacat
    [Documentation]  TEA Upgrade fails when doing 'Download'
    ...   and 'Install' separately from UI
    ...  1.Netinstall SMA with the build 12.0.0-229
    ...  2.Access SMA through GUI and navigate to Management Appliance \
    ...  -> System Administration -> System Upgrade
    ...  3.Under Upgrade Options, select the option "Download only" and
    ...  select the required build from the list of available upgrades,
    ...  then click on "Proceed"
    ...  4.Once download completes, Select the option
    ...  "Install" and click on "Proceed".
    ...  5.Once reboot is required, click on "Reboot Now".
    ...  6.Check Upgrade completes without any error.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Library Order SMA
    ${sma_version_old}=  Get Dut Build
    Log  ${sma_version_old}
    Update Config Validate Certificates  validate_certificates=NO
    Update Config Dynamichost  dynamic_host=${UPDATE_SERVER}
    Commit
    Selenium Login
    System Upgrade Download  ${SMA_UPGRADE_VERSION}
    System Upgrade Install  ${SMA_UPGRADE_VERSION}
    Sleep  30  Compensate default reboot delay
    Wait until DUT Reboots    wait_for_ports=443
    ${sma_version_new}=  Get Dut Build
    Log  ${sma_version_new}
    Selenium Login
    Selenium Close

CSCvr92163
    [Tags]  CSCvr92163  teacat
    [Documentation]  TEA Application fault seen for SAML when SMA
    ...  is using Import IDP Metadata
    ...  1) Net-install 13.0.0-187 and complete SSW
    ...  2) Browser to GUI > System Administration > SAML and
    ...  add IDP under Identity Provider --> Add Identity Provider
    ...  3) Configure a 'Profile name' and choose 'Import IDP Metadata'
    ...  4) Upload the attached IDP metadata file
    ...  5) You will see an application fault upon Submit.
    ...  6) You can commit the upload after going to "default screen"
    ...  in application window. However, after commit, every time you
    ...  browse to GUI > System Administration > SAML, you will see an "Application Fault"

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Library Order SMA
    Selenium Login
    ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  Assertion Consumer URL             ${ASSERTION_CONSUMER_URL}
    ...  SP Certificate                     ${CERT_FILE}
    ...  Private Key                        ${CERT_KEY}
    ...  Certificate Passphrase             ${CERTIFICATE_PASSPHRASE}
    ...  Sign Requests                      ${SIGN_REQUEST}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_file}
    SAML Add SP And IDP  ${TEST_NAME}  ${TEST_IDP_PROFILE}  ${settings}
    Commit Changes
    Navigate to   Management  System Administration  SAML
    Page Should Not Contain  Application Error



CSCvm89757
    [Tags]  CSCvm89757  authentication  teacat  ftp  standard
    [Documentation]   CSCvm89757 :  TEA SMA - Unable to access FTP after incorrect password
    ...  Install the SMA version 11.5.0-056 and run SSW.
    ...  Login with appliances credentials.
    ...  In SMA, navigate to Management appliances >> Network >> IP Interface and enable FTP on port 21.
    ...  Login to client with credentials rtestuser/ironport.
    ...  Run the command “ftp <SMA IP>” e.g. I used ftp 10.76.68.41.
    ...  Type user name and password of that SMA.
    ...  Firstly type incorrect password and then try to login again using FTP .
    ...  Use URL “ftp://10.76.68.41/” and do the same.
    ...  Check wether you are able to login FTP again or not.
    Enable FTP
    ${out}  FTP Login  DUT_LOGIN_PASS=${RANDOM_PASS}
    Should Contain  ${out}  530 Password invalid.
    ${out}  FTP Login
    Should Not Contain  ${out}  451 Server Error
    Should Contain  ${out}  230 Login successful.
    Open Browser  ftp://${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}@${DUT_IP}/
    Page Should Contain  ftp://${DUT_ADMIN}@${DUT_IP}/

CSCvo25716
    [Tags]  CSCvo25716  teacat
    [Documentation]  CSCvo25716: TEA SMAs need ktrace
    ...  Netinstall the SMA and execute loadlicense.
    ...  Login to SMA as rtestuser and execute the command “ktrace”.
    ...  “ktrace “ command should be supported by SMA.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Verify ktrace Status

CSCvo71423
    [Tags]  CSCvo71423  teacat
    [Documentation]  TEA SMA: SSL Server allows anonymous Authentication \n
    ...  Should not connect from Client using Null Cipher

    Set Aliases For Appliance Libraries
    Set Appliance Under Test To SMA
    Set SSHLib Prompt  $
    Open Connection  ${CLIENT}
    Login  ${RTESTUSER}  ${RTESTUSER_PASSWORD}
    Write  openssl s_client -connect ${SMA}:443 -cipher aNULL
    ${out}  Read Until Prompt
    Log  ${out}
    Should Contain  ${out}  SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure
    Close Connection
    Set SSHLib Prompt  ${EMPTY}

CSCvo35447
    [Tags]  CSCvo35447  teacat
    [Documentation]  TEA SMA may corrupt Splunk database on bootup
    ...  1. Reboot the SMA
    ...  2.  Login to the SMA through SSH
    ...  3.  Run this grep –
    ...       grep -iE "version|splunk" /data/log/heimdall/heimdall/*ent
    ...  4.   The splunk process starts and continues without stopping.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Library Order SMA
    Selenium Login
    Reboot
    Sleep  30  Compensate default reboot delay
    Wait until DUT Reboots    wait_for_ports=443
    ${sma_version}=  Get Dut Build
    Connect SSH
    FOR  ${index}  IN RANGE  20
        Write  grep -iE "version|splunk" /data/log/heimdall/heimdall/*ent
        ${output}=  Read Until Prompt
        Should Not Contain  ${output}  DOWN
        Should Not Contain  ${output}  failed
        Should Contain  ${output}  splunkd: starting
        Should Contain  ${output}  splunkd: started PID
        Should Contain  ${output}  ${sma_version}
        Sleep  10s
    END

CSCvo75955
    [Tags]  CSCvo75955  teacat
    [Documentation]  TEA Traceback Received When Trying To Enable TLSv1.1 or TLSv1.2 For EUQ Service
    ...  1.  Upgrade SMA to 11.0.0-112
    ...  2.  To Enable TLSv1.1 or TLSv1.2 For EUQ Service
    ...  3.  Check there is no traceback

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    FOR  ${ssl_method}  IN  TLSv1.0  TLSv1.1  TLSv1.2  SSLv3.0
      ${status}  ${msg}  Run Keyword And Ignore Error  SSL Config Gui  versions=All Services  ssl_method=${ssl_method}  confirm=Enable for all services
      Run Keyword if  '${status}' != 'PASS' and '${msg}' != 'None'  Log  SSL Config failed in SSL version:${ssl_method} and Traceback:${msg}
      ...  ELSE  Log  SSL config succeeds without any traceback.
    END

CSCvo89547
    [Tags]  CSCvo89547  teacat
    [Documentation]
    ...  Verify connectivity issues with remote access

    Library Order SMA
    Selenium Login
    Remote Access Enable  password=${DUT_ADMIN_SSW_PASSWORD}  secure_tunnel=${True}
    ...  port=45
    ${output}=  Log Search  sshtunnel search_path=  heimdall
    ${len}=  Get Length  ${output}
    Should Be True  ${len}  >= 1
    ${SMA_IP}=  Get Host IP By Name  ${SMA}
    ${out}=  Run  ping -c 1 ${SMA_IP}
    Should Contain  ${out}  64 bytes
    Remote Access Disable
    Selenium Close

CSCvq33138
    [Tags]  CSCvq33138  teacat
    [Documentation]  CSCvo25716:  This is an enhancement
        ...  to make google analytics on NG-sma
        ...  to be user-defined, that is, Enabled or Disabled
        ...  login to sma
        ...  go to management
        ...  go to system administration
        ...  go to General settings
        ...  navigate to edit settings
        ...  check the checkbox according to the user input (enable or disable)
        ...  commit changes
        ...  get the changed information and confirm.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Selenium Login
    ${analytics_status}=  Get General Analytics Setting Status
    Should Be True  ${analytics_status}
    Edit General Settings
    Commit Changes
    ${analytics_status}=  Get General Analytics Setting Status
    Should Not Be True  ${analytics_status}
    Edit General Settings  edit_analytics=True
    Commit Changes
    ${analytics_status}=  Get General Analytics Setting Status
    Should Be True  ${analytics_status}
    Selenium Close

CSCvr01351
    [Tags]  CSCvr01351  teacat
    [Documentation]  CSCvr01351:TEA Virtual SMA is missing
        ...  files necessary for backup processes
        ...  Download the 10.0.0-088 or 10.1.0-037 virtual SMA.
        ...  Standard deployment procedure.
        ...  Log into the command line of the appliance.
        ...  Enable service access to the appliance.
        ...  List the contents of the /data/home/ directory.
        ...  check for smaduser directory and subordinate files and folders (.ssh)

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Connect SSH
    Write  ls -l /data/home
    ${out}=  Read Until Prompt
    Should Match Regexp  ${out}  .*smaduser.*
    Write  ls -l /data/home/smaduser/
    ${out}=  Read Until Prompt
    Should Match Regexp  ${out}  .*ssh.*
    Close Connection

CSCvs87067
    [Tags]  CSCvs87067  teacat
    [Documentation]  TEA SMA 'sslconfig' does not disable SSLv3
    ...  when configured to do so
    ...  Steps: 1.Netinstall and do SSW.
    ...  2.Check SMA rejects the connection using SSLv3 when it was disabled
    ...  3.SMA allows connection to TLS port 443 when SSLv3 is disabled
    ...  4.SMA negotiates TLSv1 protocol on demand when SSLv3 disabled
    ...  5.SMA allows connection to port 443 using SSLv3 after it
    ...  is being re-enabled
    ...  6.SMA negotiates the highest TLSv1.2 protocol for port 443,
    ...  on demand, even when SSLv3 is enabled
    ...  7.SMA ssl settings remain the same after reboot

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${gui_proto_list}  Create List  TLS v1.2 TLS v1.1 TLS v1.0 SSL v3.0
    Library Order SMA
    SSL Config Gui  versions=All Services  ssl_method=SSLv3.0  confirm=Disable for all services
    SSL Config Gui  versions=All Services  ssl_method=TLSv1.0  confirm=Enable for all services
    Commit

    ${CLI_ServicesList}  Ssl Config Get Settings
    List Should Not Contain Value  ${CLI_ServicesList}  SSLv3.0
    ${out}  Run  openssl s_client -connect ${SMA}:443 -ssl3
    Log  ${out}
    Should Contain  ${out}  ssl handshake failure

    FOR  ${ssl_mode}  IN  no_ssl3  tls1
      ${out}  Run   openssl s_client -connect ${SMA}:443 -${ssl_mode}
      Log  ${out}
      Should Not Contain  ${out}  ssl handshake failure
    END
    Library Order SMA
    Selenium Login
    FOR  ${service}  IN   Appliance Management Web User Interface
    ...  Secure LDAP Services  Updater Service
      Edit SSL Configuration Settings
      ...  ${service}
      ...  SSL v3
      ...  enable=True
    END
    Run Keyword And Ignore Error  Commit Changes
    Selenium Close

    Wait Until Keyword Succeeds  60s  10s  Selenium Login
    Verify SSL Config Settings GUI  versions=${gui_proto_list}

    @{verify_list}  Create List  ssl3  SSLv3
    ...  no_ssl3  TLSv1.2
    FOR  ${ssl_mode}  ${proto}  IN  @{verify_list}
      ${out}  Run   openssl s_client -connect ${SMA}:443 -${ssl_mode}
      Log  ${out}
      Should Contain  ${out}  Protocol${SPACE}${SPACE}:${SPACE}${proto}
      Should Not Contain  ${out}  ssl handshake failure
    END
    Reboot
    Sleep  30  Compensate default reboot delay
    Wait until DUT Reboots    wait_for_ports=443
    Selenium Login
    Verify SSL Config Settings GUI  versions=${gui_proto_list}
