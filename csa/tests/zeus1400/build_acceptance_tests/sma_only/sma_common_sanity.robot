** Settings ***
Suite Setup        CustomTestSuiteSetup
Suite Teardown     DefaultTestSuiteTeardown
Test Setup         DefaultRegressionTestCaseSetup
Test Teardown      DefaultRegressionTestCaseTeardown
Resource           regression.txt

*** Variables ***
${default_cert}     default-cert.txt
${EDIT_SETTINGS_BUTTON}   //input[@value='Edit Settings']
${CANCEL_BUTTON}   //input[@value='Cancel']

*** Keywords ***

CustomTestSuiteSetup
    DefaultRegressionSuiteSetup
    Set Suite Variable  ${SSW}  ${False}
    Library Order SMA
    ${sma_base_version} =  Get SMA version
    Log  Base SMA version ${sma_base_version}
    Set Suite Variable  ${sma_base_version}
    Start Cli Session If Not Open
    Set Manifest Server

Verify Default Certificate Availabilty
    Library Order SMA
    ${out}=  Run On DUT  ls /data/share
    Log  ${out}
    Should Contain  ${out}  ${default_cert}

Set Manifest Server
    Update Config Validate Certificates  validate_certificates=NO
    Update Config Dynamichost  dynamic_host=${UPDATE_SERVER}:443
    Commit

Get SMA version
    Start Cli Session If Not Open
    ${version_output}=  Version
    ${version_val} =  Get Lines Matching Pattern  ${version_output}  Version:*
    ${sma_version} =  Fetch From Right  ${version_val}  :
    [Return]  ${sma_version.strip()}

Check Image version
    [Arguments]  ${verify_image}=${sma_base_version}  ${operation}=Before upgrade
    ${sma_build} =  Get SMA version
    Log  SMA version ${operation} ${sma_build}
    Should Be Equal  ${sma_build}  ${verify_image}
    ...  msg=image verification failed ${operation}

Config File Save Load CLI
    Library Order SMA
    ${cli_config_file}=  Save Config
    Log  ${cli_config_file}
    ${cli_result}=  Load Config From File   ${cli_config_file}
    Log  ${cli_result}
    Commit
    Should Be Equal As Strings  ${cli_result}  True

Config File Save Load GUI
    Library Order SMA
    Selenium Login
    ${gui_config_file}=  Configuration File Save Config
    Log  ${gui_config_file}
    Configuration File Load Config   ${gui_config_file}
    Commit Changes
    Selenium Close

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

Verify SSL Config Settings CLI
    [Arguments]  ${versions}=TLSv1.1,TLSv1.2
    ${CLI_ServicesList}  Ssl Config Get Settings
    FOR  ${service}  IN  WebUI  Updater  LDAPS
      ${service_list}=  Get From Dictionary  ${CLI_ServicesList}  ${service}
      Should Be Equal As Strings  ${versions}  ${service_list}
      ...  msg=${service} Enabled protocol details are mismatched
    END

Verify Checkbox Status
    [Arguments]  ${service}  @{items}
    FOR  ${item}  IN  @{items}
      ${locator}  Set Variable  //input[@id='${service}_${item}']
      Log  ${locator}
      Run Keyword If  '${item}' != 'SSLv3.0'
      ...  Checkbox Should Be Selected  ${locator}
    END

***Test Cases***

Tvh1159789c

    [Tags]  Tvh1159789c  Tvh1224704c  Tvh1161605c  Tvh1307354c  bat  cli_upq
    [Documentation]
    ...  TIMS LINK:http://tims.cisco.com/view-entity.cmd?ent=1159789
    ...  Precondition:
    ...  SMA appliance is up and running with a existing build
    ...  Steps:
    ...  1. ssh to SMA appliance with admin credential.
    ...  2. enter the below commands in cli
    ...  -> updateconfig
    ...  - VALIDATE_CERTIFICATES -> enter 'No'
    ...  -> dynamichost
    ...  enter dynamic host as 'update-manifests.ironport.com'
    ...  ->then Commit the changes
    ...  3. then enter 'upgrade' command
    ...  4a. either select 'DOWNLOADINSTAL'
    ...  4b. then choose the desired build , Choose 'yes' for save config ,
    ...   and enter the email ID to send the config file in mail.
    ...  5a. or first enter 'DOWNLOAD' and then install.
    ...  6. Once upgrade completed successfully, launch the SMA UI
    ...  and log in with admin credential.
    ...  7. Go to Options -> Log out.
    ...  8. Log In again
    ...  9. Login to the SMA through SSH
    ...  10. Give the command 'cli'
    ...  11. Once in CLI mode, give the command 'version'
    ...  12.Check current version of the appliance displayed.


    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Library Order SMA
    Check Image version  verify_image=${sma_base_version}
    Upgrade Downloadinstall
    ...  ${SMA_UPGRADE_VERSION}
    ...  seconds=10
    ...  save_cfg=yes
    ...  email=yes
    ...  email_addr=${ALERT_RCPT}
    Sleep  1m  Compensate default reboot delay
    Wait until DUT Reboots    wait_for_ports=443
    Check Image version  verify_image=${SMA_UPGRADE_VERSION}
    ...  operation=After Upgrade
    Verify Default Certificate Availabilty
    Start Cli Session If Not Open
    ${out}=  Version
    ${CURRENT_DUT_VERSION}=  Evaluate
    ...  re.search(r'Version: (\\d+\.\\d+\.\\d+-\\d+)', '''${out}''').groups()[0]  re
    Log  ${CURRENT_DUT_VERSION}
    Should Be Equal  ${CURRENT_DUT_VERSION}  ${SMA_UPGRADE_VERSION}
    ...  msg=image verification failed via cli
    Selenium Login
    Log Out Of Dut
    Log Into Dut
    Selenium Close

Tvh1174834c

    [Tags]  Tvh1174834c  bat  cli_upq
    [Documentation]
    ...  TIMS LINK:http://tims.cisco.com/view-entity.cmd?ent=1174834
    ...  Steps:
    ...  1. Login to SMA cli using admin credential.
    ...  2. Enter command "saveconfig " .
    ...  3. Enter "No" for masked password option.
    ...  4. Enter command "loadconfig " .
    ...  5. Enter "No" for "Do you want to load network settings"
    ...  and "Do you want to load disk quota settings?".
    ...  6. Select option "Paste via CLI" and paste the config file.
    ...  7. Commit the changes and check it is succeeds

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Config File Save Load CLI

Tvh1174837c

    [Tags]  Tvh1174837c  bat  cli_upq
    [Documentation]
    ...  TIMS LINK:http://tims.cisco.com/view-entity.cmd?ent=1174837
    ...  Steps:
    ...  1. In SMA GUI ,Navigate to Management Appliance ->
    ...  System Administration->Configuration File.
    ...  2. Select Current Configuration-> Configuration File :
    ...  Download file to local computer to view or save
    ...  3. Do not select "Mask passwords in the Configuration Files ".
    ...   Submit the changes.
    ...  4. In SMA GUI ,Navigate to Management Appliance
    ...  ->System Administration->Configuration File.
    ...  5. Select "Load Configuration-> Load Configuration->
    ...  "Load a configuration file from local computer"
    ...  6. Browse and select the config file to be loaded and click "Load".
    ...  7. Commit the changes and check it is succeeds

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Config File Save Load GUI

Tvh1174881c

    [Tags]  Tvh1174881c  bat  cli_upq
    [Documentation]
    ...  Verify that  Disk Quotas allocations for PVO can be modified
    ...  http://tims.cisco.com/view-entity.cmd?ent=1174881
    ...  Precondition:
    ...  SMA is netinstalled and load license has been done .
    ...  Steps:
    ...  1. Navigate to Management Appliance-> System Administration-> Disk Management.
    ...  2. Click on "Edit Disk Quotas".
    ...  3. Change the value for PVO( for eg change 200G to 100G). Submit the changes
    ...  4. Disk Quota for PVO should get changed successfully.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${user_pvo_quota}  50
    Selenium Login
    Disk Management Edit Quotas
    ...  pvo_quarantine=${user_pvo_quota}
    Commit Changes
    ${pvo_quota} =  Disk Management Get Service Quota
    ...  Policy, Virus & Outbreak Quarantines
    Should Be Equal As Numbers  ${pvo_quota}  ${user_pvo_quota}
    Selenium Close

Tvh1224705c

    [Tags]  Tvh1224705c  bat  cli_upq
    [Documentation]
    ...  TIMS LINK:http://tims.cisco.com/view-entity.cmd?ent=1224705
    ...  Precondition:
    ...  1. SMA appliance has a build which has
    ...  default certificate under /data/share.
    ...  Steps:
    ...  1. SSH to SMA appliance with admin credential.
    ...  2 Enter 'revert' command.
    ...  3. Select the desired build which is not supposed
    ...  to have default certificate.
    ...  4. After revert, login to SMA as rtestuser .
    ...  5. Navigate to /data/share.
    ...  6. Attempt to access SMA SSH and GUI as admin.
    ...  Expected Behavior :
    ...  1. SMA should get reverted successfully and
    ...  new version should be displayed.
    ...  2. default certificate should be present at /data/share.
    ...  3. Both SSH and GUI should be accessible.
    ...  4.Config file should get uploaded to and downloaded
    ...  from the SMA successfully.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Check Image version  verify_image=${SMA_UPGRADE_VERSION}
    ...  operation=Before Revert
    Verify Default Certificate Availabilty
    Revert
    ...  version=${sma_base_version}
    ...  continue_revert=yes
    ...  confirm_revert=yes
    Wait Until DUT Reboots  wait_for_ports=22,443,80
    Check Image version  verify_image=${sma_base_version}
    ...  operation=After Revert
    Verify Default Certificate Availabilty
    SSL Config Gui  versions=All Services  ssl_method=TLSv1.0
    ...  confirm=Enable for all services
    Commit
    Config File Save Load GUI
    Start Cli Session If Not Open
    Config File Save Load CLI

Tvh1307352c

    [Tags]  Tvh1307352c  Tvh1224703c  bat  cli_upq
    [Documentation]
    ...  TIMS LINK:http://tims.cisco.com/view-entity.cmd?ent=1307352
    ...  Precondition:
    ...  The SMA should be pointed to the correct
    ...  Upgrade Server (update-manifests.ironport.com)
    ...  Steps:
    ...  1. Login to the SMA through CLI
    ...  2. Give the command 'upgrade'
    ...  3. Give the command 'DOWNLOAD'
    ...  4. Select the required image from 'upgrades avaliable' list
    ...  5. Once Download starts, keep monitoring the status by
    ...  giving the command 'DOWNLOADSTATUS'
    ...  6. Once Download completes, give the command 'INSTALL'
    ...  7. For the question 'Do you want to install it?', give 'YES'
    ...  8. Choose either 'Encrypt passwords' or 'Plain passwords'
    ...  9. For the question 'Do you wish to proceed with the upgrade?' give 'YES'
    ...  10. Once installation completes, reboot the appliance

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Check Image version  verify_image=${sma_base_version}
    ...  operation=Before Download install
    Set Manifest Server
    Verify Default Certificate Availabilty
    Upgrade Download
    ...  ${SMA_UPGRADE_VERSION}
    FOR   ${index}   IN RANGE  10
      ${status}=  Upgrade Downloadstatus
      Run Keyword If  ${status} == 100   Exit For Loop
      Sleep  1m
    END
    Run Keyword Unless  ${status} == 100
    ...  Fail  msg=Upgrade image was not downloaded
    Upgrade Install
    ...  ${SMA_UPGRADE_VERSION}
    ...  seconds=10
    ...  save_cfg=yes
    ...  include_pw=no
    ...  email=yes
    ...  email_addr=${ALERT_RCPT}
    Sleep  1m  Compensate default reboot delay
    Wait until DUT Reboots    wait_for_ports=443
    Check Image version  verify_image=${SMA_UPGRADE_VERSION}
    ...  operation=After Download install
    Verify Default Certificate Availabilty

Tvh1307353c
    [Tags]  Tvh1307353c  bat  gui_upq
    [Documentation]
    ...  TIMS LINK:http://tims.cisco.com/view-entity.cmd?ent=1307353
    ...  Precondition:
    ...  The SMA should be pointed to the correct
    ...  Upgrade Server (update-manifests.ironport.com)
    ...  Steps:
    ...  1. Login to the SMA
    ...  2. Navigate to System Administration -> System Upgrade
    ...  3. Click on 'Upgrade Options'
    ...  4. Select 'Download'
    ...  5. Select the required image from the List of available
    ...  upgrade images at upgrade server.
    ...  6. Make sure 'Mask Passwords' is not selected, either
    ...  'Plain Passwords' or 'Encrypt Passwords' should be selected.
    ...  7. Click on 'Proceed'.
    ...  8. Once download completes, select 'Install' and click proceed.
    ...  9. Once installation completes, reboot the appliance.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Library Order SMA
    Check Image version  verify_image=${sma_base_version}
    Selenium Login
    System Upgrade Download  ${SMA_UPGRADE_VERSION}
    System Upgrade Install  ${SMA_UPGRADE_VERSION}
    Sleep  30  Compensate default reboot delay
    Wait until DUT Reboots    wait_for_ports=443
    Check Image version  verify_image=${SMA_UPGRADE_VERSION}
    ...  operation=after upgrade
    Selenium Close
    Selenium Login
    Selenium Close

Tvh1174882c

    [Tags]  Tvh1174882c  bat  gui_upq
    [Documentation]
    ...  http://tims.cisco.com/view-entity.cmd?ent=1174882
    ...  Steps:
    ...  1. Navigate to "System Status " page.
    ...  2. Hover on "My Favorites" and click on "Add This
    ...  Page to My Favorites".
    ...  3. Add the page .
    ...  4. Hover on "My Favorites"
    ...  5. Due to defect CSCvq57673 system page
    ...  not deleted from My favorites page
    ...  Expected Result:
    ...  1. System Status should be visible in list of pages
    ...  under My Favorites.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${page_name}  System Status
    Selenium Login
    My Favorites Add  Management Appliance -> Centralized Services -> System Status
    ...  name=${page_name}
    ...  add_via_menu=True
    Commit Changes
    ${pages}  My Favorites Get List
    Log  ${pages}
    List Should Contain Value  ${pages}  ${page_name}
    My Favorites Go To  ${page_name}
    ${title}=  Get Title
    Should Match Regexp  ${title}  ${page_name}
    My Favorites Delete  ${page_name}
    Commit Changes
    ${pages}  My Favorites Get List
    Log  ${pages}
    List Should Not Contain Value  ${pages}  ${page_name}
    Selenium Close

Tvh1174883c

    [Tags]  Tvh1174883c  bat  gui_upq
    [Documentation]
    ...  http://tims.cisco.com/view-entity.cmd?ent=1174883
    ...  Steps:
    ...  1. Navigate to Email-> Message Quarantine->PVO
    ...  2. Hover on "My Favorites" and click on "Add This
    ...  Page to My Favorites".
    ...  3. Add the page .
    ...  4. Hover on "My Favorites"
    ...  5. Click on "View All My Favorites" and assign PVO as landing page .
    ...  6. Log out and log into SMA.
    ...  7. PVO should be visible in list of pages under My Favorites.
    ...  8. PVO page should open.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${page_name}  Policy, Virus and Outbreak Quarantines
    Selenium Login
    My Favorites Add  Email -> Message Quarantine -> Policy, Virus and Outbreak Quarantines
    ...  name=${page_name}
    ...  add_via_menu=True
    Commit Changes
    ${pages}  My Favorites Get List
    Log  ${pages}
    List Should Contain Value  ${pages}   ${page_name}
    Navigate To  My Favorites  ${page_name}
    My Favorites Set Landing Page  ${page_name}
    Log Out Of Dut
    Log Into Dut
    ${title}=  Get Title
    Should Match Regexp  ${title}  ${page_name}
    Selenium Close

Tvh1175022c

    [Tags]  Tvh1175022c  bat  gui_upq
    [Documentation]
    ...  Add various pages in 'My Reports' for the Reporting Dashboard
    ...  http://tims.cisco.com/view-entity.cmd?ent=1175022
    ...  Steps:
    ...  1.Navigate to Email->Reporting -> My Reports and click on
    ...  Add Module icon on the right.
    ...  2. Select the report (for eg. Sender Details) to be shown and click OK.
    ...  3. Navigate to Web->Reporting -> My Web Reports and click on Add Module icon on the right.
    ...  4. Select the report to be shown(eg . Top Users: Bandwidth Used) and click OK.
    ...  5. Sender Details page should be added to Email->Reporting -> My Reports page.
    ...  6. Top Users: Bandwidth Used page should be added to Web->Reporting -> My Web Reports

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Selenium Login
    My Dashboard Reports Add  Time Range   Sender Details
    ${is_exist}=  My Dashboard Report Exists  Time Range   Sender Details
    Should Be True  ${is_exist}
    My Dashboard Delete  Time Range   Sender Details
    My Reports Add Module  Time Range  Users  Top Users: Bandwidth Used
    ${names}=  My Reports Get Modules List
    List Should Contain Value  ${names}  Top Users: Bandwidth Used
    My Reports Delete Module  Top Users: Bandwidth Used
    Selenium Close

Tvh1186998c

    [Tags]  Tvh1186998c  Tvh1186999c  Tvh1187024c  gui_upq
    [Documentation]
    ...  http://tims.cisco.com/view-entity.cmd?ent=1186999
    ...  Steps:
    ...  1. Login to SMA.
    ...  2. Go to Management Appliance -> System Administration
    ...  -> SSL Configuration
    ...  3. Check presence of all four existing services:
    ...  -Application Management Web User Interface
    ...  -Secure LDAP Services
    ...  -EUQ
    ...  -Update Service
    ...  Expected Result:
    ...  All the four services & their respective protocol
    ...  details should be displayed.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${proto_list}  Create List  TLS v1.2 TLS v1.1
    Library Order SMA
    Selenium Login
    Verify SSL Config Settings GUI  versions=${proto_list}
    Verify SSL Config Settings CLI
    Selenium Close

Tvh1187050c

    [Tags]  Tvh1187050c  bat  gui_upq
    [Documentation]
    ...  http://tims.cisco.com/view-entity.cmd?ent=1187050
    ...  Steps:
    ...  1. Login to SMA.
    ...  2. Go to Management Appliance -> System Administration
    ...  -> SSL Configuration
    ...  3. Click on 'Edit Settings'
    ...  4. Edit the SSl services by enabling/disabling
    ...  Application Management Web User Interface/Secure
    ...  LDAP Services/EUQ/Update Service
    ...  5. Click 'Submit'
    ...  6. Commit the changes.
    ...  Expected Results:
    ...  before commit "Attention" After you commit your changes,
    ...  the settings of the SSL Configuration can cause all related
    ...  services to restart. This leads to interruption in the services."
    ...  Success message 'Success Your changes have been committed.'
    ...  is displayed at the top of the page and the changes are saved.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Selenium Login
    ${proto_list}  Create List  TLS v1.2 TLS v1.1 TLS v1.0
    FOR  ${service}  IN   Appliance Management Web User Interface
    ...  Secure LDAP Services  Updater Service
      Edit SSL Configuration Settings
      ...  ${service}
      ...  TLS v1.0
      ...  enable=True
    END
    Run Keyword And Ignore Error  Commit Changes
    Selenium Close
    Wait Until Keyword Succeeds  60s  10s  Selenium Login
    Verify SSL Config Settings GUI  versions=${proto_list}
    ${proto_list}  Create List  TLS v1.2 TLS v1.1
    FOR  ${service}  IN   Appliance Management Web User Interface
    ...  Secure LDAP Services  Updater Service
      Edit SSL Configuration Settings
      ...  ${service}
      ...  TLS v1.0
    END
    Run Keyword And Ignore Error  Commit Changes
    Selenium Close
    Wait Until Keyword Succeeds  60s  10s  Selenium Login
    Verify SSL Config Settings GUI  versions=${proto_list}
    Selenium Close

Tvh1187025c
    [Tags]  Tvh1187025c  Tvh1187052c  bat  cli_upq
    [Documentation]
    ...  http://tims.cisco.com/view-entity.cmd?ent=1187025
    ...  1. Login to SMA.
    ...  2. Go to Management Appliance -> System Administration
    ...  -> SSL Configuration
    ...  3. Click on 'Edit Settings'
    ...  Expected Result:
    ...  1.A page is displayed with checkbox across each protocol.
    ...  The already enabled protocol is checked and the disabled ones
    ...  are unchecked.
    ...  2.Only SSLv3.0 protocol should be displayed under EUQ

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{proto_xpath_list}  Create List  TLSv1.1  TLSv1.2
    @{service_list}  Create List   WebUI  LDAPS  Updater
    Selenium Login
    Navigate To  Management Appliance  System Administration  SSL Configuration
    Click Button  ${EDIT_SETTINGS_BUTTON}
    FOR  ${service}  IN  @{service_list}
      Verify Checkbox Status  ${service}  @{proto_xpath_list}
    END
    Click Button  ${CANCEL_BUTTON}
    Selenium Close

Tvh1187051c

    [Tags]  Tvh1187051c  bat  gui_upq
    [Documentation]
    ...  http://tims.cisco.com/view-entity.cmd?ent=1187051
    ...  Precondition :
    ...  User has already made the changes from GUI.
    ...  Steps:
    ...  1. Go to CLI mode.
    ...  2. Type 'sslconfig'
    ...  3. Type 'VERSIONS'
    ...  Expected Result:
    ...  Both the data in CLI should be in sync
    ...  with the data displayed in GUI.

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Set Test Variable  ${cli_proto_list}   TLSv1.1,TLSv1.0,TLSv1.2
    ${gui_proto_list}  Create List  TLS v1.2 TLS v1.1 TLS v1.0
    Selenium Login
    FOR  ${service}  IN   Appliance Management Web User Interface
    ...  Secure LDAP Services  Updater Service
      Edit SSL Configuration Settings
      ...  ${service}
      ...  TLS v1.0
      ...  enable=True
    END
    Run Keyword And Ignore Error  Commit Changes
    Selenium Close
    Wait Until Keyword Succeeds  60s  10s  Selenium Login
    Verify SSL Config Settings GUI  versions=${gui_proto_list}
    Verify SSL Config Settings CLI  versions=${cli_proto_list}
