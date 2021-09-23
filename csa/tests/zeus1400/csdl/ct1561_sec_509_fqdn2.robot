*** Settings ***
Resource     sma/csdlresource.txt
Resource     esa/logs_parsing_snippets.txt

Force Tags         csdl  SEC-509-FQDN-2
Suite Setup        Initialize Suite Setup
Suite Teardown     CSDL Suite Teardown


*** Variables ***
${CERT_FILES_DIR}=           %{SARF_HOME}/tests/testdata/sma/csdl/fqdn
${CLI_LOGS_PATH}=            /data/pub/cli_logs/cli.current
${ERR_MSG}=                  A valid domain name is a string that must match the following rules
${CONFIG_DIR}=               /data/pub/configuration/
${ERROR_MSG_XPATH}=          //span[contains(text(),'more')]
${FQDN_CHECKBOX}=            //input[@id='fqdn_validation' and @disabled]
${EDIT_SETTINGS}=            //input[@value='Edit Settings...']
${GUI_LOGS_PATH}=            /data/pub/gui_logs/gui.current


*** Keywords ***
Initialize Suite Setup
    CSDL Suite Setup
    Login To Dut
    ${SMA_BASE_BUILD}=  Get Current Dut Version
    Set Suite Variable  ${SMA_BASE_BUILD}

Setup DUT after Reboot
    Start CLI Session If Not Open
    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_TMP_PASSWORD}
    Load License From File
    Selenium Login

Check Peer Cert FQDN Validation From GUI
    [Arguments]  ${status}
    ${settings}=  Get SSL Configuration Settings
    Log Dictionary  ${settings}
    ${output}=  Get From Dictionary
    ...  ${settings}  Peer Certificate FQDN Validation
    Should Contain  ${output}  ${status}

Get Current Dut Version
    Start Cli Session If Not Open
    ${out}=  Version
    ${CURRENT_DUT_VERSION}=  Evaluate
    ...  re.search(r'Version: (\\d+\.\\d+\.\\d+-\\d+)', '''${out}''').groups()[0]  re
    Log  ${CURRENT_DUT_VERSION}
    [Return]  ${CURRENT_DUT_VERSION}

Delete CertAuthority Certs
    [Arguments]  ${no_of_certs}
    FOR  ${index}  IN RANGE  1  ${no_of_certs} + 1
        Cert Authority Delete  1  y
        Commit
    END

Verify FQDN For Valid Certificates
    [Arguments]  ${cert_and_key}
    FOR  ${cert}  ${key}  IN  @{cert_and_key}
        Restart CLI Session
        Roll Over Now  logname=cli_logs
        Sleep  5s  msg=Wait for logs roll over
        ${cert_text}=  OperatingSystem.Get File  ${CERT_FILES_DIR}/${cert}
        ${cert_key_text}=  OperatingSystem.Get File  ${CERT_FILES_DIR}/${key}
        Cert Config Setup  ${cert_text}  ${cert_key_text}
        ...  one_cert=yes
        ...  intermediate=no
        ...  fqdn=yes
        Verify And Wait For Log Records
        ...  search_path=${CLI_LOGS_PATH}
        ...  wait_time=2 mins
        ...  Certificate is FQDN compliant >= 1
    END

Verify FQDN For Invalid Certificates
    [Arguments]  ${cert_and_key}
    FOR  ${cert}  ${key}  IN  @{cert_and_key}
        ${cert_text}=  OperatingSystem.Get File  ${CERT_FILES_DIR}/${cert}
        ${cert_key_text}=  OperatingSystem.Get File  ${CERT_FILES_DIR}/${key}
        Run Keyword And Expect Error
        ...  ConfigError: failed due to certificate pair with invalid FQDN*
        ...  Cert Config Setup  ${cert_text}  ${cert_key_text}
        ...  one_cert=yes
        ...  intermediate=no
        ...  fqdn=yes
    END

Tvh1562986c Teardown
    Wait until DUT Is Accessible    wait_for_ports=${DUT_PORT}    timeout=360
    Setup DUT after Reboot
    ${result}=  Load Config Via Cli  ${config_text}
    Commit
    DefaultTestCaseTeardown


*** Test Cases ***
Tvh1562972c
    [Documentation]  Verify GUI certificate authorities custom CA has FQDN check box \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562972c \n
    [Tags]  Tvh1562972c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Navigate To  Network  Certificates
    Click Element  ${EDIT_SETTINGS}
    Page Should Contain Checkbox  ${FQDN_CHECKBOX}

Tvh1562975c
    [Documentation]  Verify custom CA with proper FQDN/DNS names can only be imported through GUI \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562975c \n
    [Tags]  Tvh1562975c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Run Keywords  Delete CertAuthority Certs  3
    ...  AND  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{cert_files_non_fqdn}=  Create List  _.com.pem  _isco.com.pem  10.10.9.12.pem  123ab.536212.pem
    ...  asjndkasjfd.pem  www.cisco._om.pem  ww_.cisco.com.pem  www._.com.pem  www.cisco._.pem
    @{cert_files_fqdn}=  Create List  cisco.com.pem  www.cisco.com.pem  _.cisco.com.pem

    FOR  ${cert}  IN  @{cert_files_non_fqdn}
        Run Keyword And Expect Error  *
        ...  Edit Certificate Authorities  custom_list_enable=${True}
        ...  custom_list_cert_path=${CERT_FILES_DIR}/${cert}  fqdn_validation=${True}
        Click Element  ${ERROR_MSG_XPATH}
        Page Should Contain    ${ERR_MSG}
    END

    FOR  ${cert}  IN  @{cert_files_fqdn}
        Roll Over Now  logname=gui_logs
        Sleep  5s  msg=Wait for logs roll over
        Edit Certificate Authorities  custom_list_enable=${True}
        ...  custom_list_cert_path=${CERT_FILES_DIR}/${cert}  fqdn_validation=${True}
        Commit Changes
        Verify And Wait For Log Records
        ...  search_path=${GUI_LOGS_PATH}
        ...  wait_time=2 mins
        ...  Certificate successfully uploaded >= 1
		...  Custom CA Certificate is FQDN compliant >= 1
    END

Tvh1562981c
    [Documentation]  Paste certificate with proper FQDN/DNS name in CN & No SAN field from CLI,  \n
    ...  Verify certificate can be added successfully\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562981c \n
    ...  Paste certificate with proper FQDN/DNS name in SAN/CN from CLI, Verify \n
    ...  certificate is accepted \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562979c \n
    [Tags]   Tvh1562981c  Tvh1562979c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{cert_and_key}=  Create List  _.com.pem  _.com_key.pem  _isco.com.pem  _isco.com_key.pem
    ...  10.10.9.12.pem  10.10.9.12_key.pem  123ab.536212.pem  123ab.536212_key.pem  abc.def.ghi.pem
    ...  abc.def.ghi_key.pem  ad_^^,com.pem  ad_^^,com_key.pem  ahduhd.dhfouda.pem  ahduhd.dhfouda_key.pem
    ...  asjndkasjfd.pem  asjndkasjfd_key.pem  mailer_1.mail_client.com,ca.com.pem
    ...  mailer_1.mail_client.com,ca.com_key.pem  ww_.cisco.com.pem  ww_.cisco.com_key.pem
    ...  www._.com.pem  www._.com_key.pem  www.cisco._.pem  www.cisco._key.pem  www.cisco._om.pem
    ...  www.cisco._om_key.pem
    Verify FQDN For Invalid Certificates  ${cert_and_key}
    @{cert_and_key}=  Create List  www.cisco.com.pem  www.cisco.com_key.pem  cisco.com.pem  cisco.com_key.pem
    Verify FQDN For Valid Certificates  ${cert_and_key}

Tvh1562980c
    [Documentation]  Create certificates with below common names and SAN through XCA/LCA tools \n
    ...  and sign it with CA if required, export those in .pem (Certificate and private key) format.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562980c \n
    [Tags]   Tvh1562980c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{nocn_cert_and_key}=  Create List  nocn_cisco.com.pem  nocn_cisco.com_key.pem
    ...  nocn_www.cisco.com.pem  nocn_www.cisco.com_key.pem
    Verify FQDN For Valid Certificates  ${nocn_cert_and_key}

    @{nocn_cert_and_key}=  Create List  nocn_.com.pem  nocn_.com_key.pem  nocn_10.10.9.12.pem
    ...  nocn_10.10.9.12_key.pem  nocn_123ab.536212.pem     nocn_123ab.536212_key.pem
    ...  nocn_abc.def.ghi.pem  nocn_abc.def.ghi_key.pem  nocn_ad_^^,com.pem  nocn_ad_^^,com_key.pem
    ...  nocn_ahduhd.dhfouda.pem  nocn_ahduhd.dhfouda_key.pem  nocn_asjndkasjfd.pem  nocn_asjndkasjfd_key.pem
    ...  nocn_isco.com.pem  nocn_isco.com_key.pem  nocn_mailer_1.mail_client.com,ca.com.pem
    ...  nocn_mailer_1.mail_client.com,ca.com_key.pem  nocn_ww_.cisco.com.pem  nocn_ww_.cisco.com_key.pem
    ...  nocn_www._.com.pem  nocn_www._.com_key.pem  nocn_www.cisco._.pem  nocn_www.cisco._key.pem
    ...  nocn_www.cisco._om.pem  nocn_www.cisco._om_key.pem
    Verify FQDN For Invalid Certificates  ${nocn_cert_and_key}

Tvh1562978c
    [Documentation]  Paste certificate with Non-FQDN name in SAN/CN/Both from CLI, Verify \n
    ...  certificate not accepted with proper error message \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562978c \n
    [Tags]   Tvh1562978c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{comb_cert_and_key}=  Create List  comb_www._._.pem  comb_www._._key.pem  comb_www.cisco.com.pem
    ...  comb_www.cisco.com_key.pem
    Verify FQDN For Invalid Certificates  ${comb_cert_and_key}

Tvh1562977c
    [Documentation]  Verify custom CA with Non-FQDN/DNS names can be imported through GUI when \n
    ...  FQDN validation is disabled \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562977c \n
    [Tags]  Tvh1562977c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Run Keywords  Delete CertAuthority Certs  2
    ...  AND  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{cert_files_non_fqdn}=  Create List  Root_CA.pem  test-root.net.pem
    FOR  ${cert}  IN  @{cert_files_non_fqdn}
        Roll Over Now  logname=gui_logs
        Sleep  5s  msg=Wait for logs roll over
        Edit Certificate Authorities  custom_list_enable=${True}
        ...  custom_list_cert_path=${CERT_FILES_DIR}/${cert}  fqdn_validation=${False}
        Commit Changes
        Verify And Wait For Log Records
        ...  search_path=${GUI_LOGS_PATH}
        ...  wait_time=2 mins
        ...  Certificate successfully uploaded >= 1
		...  Custom CA Certificate is not FQDN compliant >= 1
    END
    ${custom_list}=  Get All Custom Trusted Root Cert
    should contain  ${custom_list}  Root CA
    should contain  ${custom_list}  test-root.net

Tvh1562974c
    [Documentation]  Verify custom CA with proper FQDN/DNS names can only be imported through CLI \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562974c \n
    ...  verify CLI certauthority cusom CA has FQDN option \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562971c \n
    [Tags]  Tvh1562974c  Tvh1562971c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Run Keywords  Delete CertAuthority Certs  3
    ...  AND  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{cert_files_non_fqdn}=  Create List  _.com.pem  _isco.com.pem  10.10.9.12.pem  123ab.536212.pem
    ...  asjndkasjfd.pem  www.cisco._om.pem  ww_.cisco.com.pem  www._.com.pem  www.cisco._.pem
    @{cert_files_fqdn}=  Create List  cisco.com.pem  www.cisco.com.pem  _.cisco.com.pem
    FOR  ${cert}  IN  @{cert_files_non_fqdn}
        Restart CLI Session
        Copy File To DUT    ${CERT_FILES_DIR}/${cert}
        ...  ${CONFIG_DIR}
        ${output}=  Cert Authority Import  ${cert}  fqdn_validation=yes
        Log  ${output}
        Should Contain  ${output}  ${ERR_MSG}
    END

    FOR  ${cert}  IN  @{cert_files_fqdn}
        Copy File To DUT    ${CERT_FILES_DIR}/${cert}
        ...  ${CONFIG_DIR}
        ${output}=  Cert Authority Import  ${cert}  fqdn_validation=yes
        Commit
        Log  ${output}
        Should Not Contain  ${output}  ${ERR_MSG}
    END

Tvh1562976c
    [Documentation]  Verify custom CA with Non-FQDN/DNS names can be imported through CLI when \n
    ...  FQDN validation is disabled \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562976c \n
    [Tags]  Tvh1562976c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Run Keywords  Delete CertAuthority Certs  2
    ...  AND  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{cert_files_non_fqdn}=  Create List  Root_CA.pem  test-root.net.pem
    FOR  ${cert}  IN  @{cert_files_non_fqdn}
        Roll Over Now  logname=cli_logs
        Sleep  5s  msg=Wait for logs roll over
        Copy File To DUT    ${CERT_FILES_DIR}/${cert}
        ...  ${CONFIG_DIR}
        Cert Authority Import  ${cert}
        Commit
        Verify And Wait For Log Records
        ...  search_path=${CLI_LOGS_PATH}
        ...  wait_time=2 mins
        ...  Imported.*custom certificates successfully >= 1
    END
    ${custom_certs}=  Cert Authority Print  cert_auth_type=custom
    should contain  ${custom_certs}[0]  Root CA
    should contain  ${custom_certs}[1]  test-root.net

Tvh1562983c
    [Documentation]  Verify enabling/disabling FQDN validation works fine in GUI
    ...  (For peer certificate validation) \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562983c \n
    [Tags]  Tvh1562983c  SEC-509-FQDN-2
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Check Peer Cert FQDN Validation From GUI  Disabled

    Edit SSL Configuration Settings
    ...  Peer Certificate FQDN Validation
    ...  FQDN
    ...  True
    Commit Changes

    Check Peer Cert FQDN Validation From GUI  Enabled

    Edit SSL Configuration Settings
    ...  Peer Certificate FQDN Validation
    ...  FQDN
    ...  False
    Abandon Changes
    Check Peer Cert FQDN Validation From GUI  Enabled

    Edit SSL Configuration Settings
    ...  Peer Certificate FQDN Validation
    ...  FQDN
    ...  ${False}
    Commit Changes
    Check Peer Cert FQDN Validation From GUI  Disabled

Tvh1562982c
    [Documentation]  Verify enabling/disabling FQDN validation works fine with possible values of \n
    ...  yes/no, other strings or values ar not accepted in CLI (For peer certificate validation) \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562982c \n
    [Tags]  Tvh1562982c  SEC-509-FQDN-2
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    ${status}=  SSL Config Get Peer Cert Fqdn Status
    Should Be Equal  ${status}  Disabled

    Restart CLI Session
    SSL Config Edit Peer Cert Fqdn  enable=${True}
    Commit
    ${status}=  SSL Config Get Peer Cert Fqdn Status
    Should Be Equal  ${status}  Enabled

    Restart CLI Session
    SSL Config Edit Peer Cert Fqdn  enable=${False}
    Commit
    ${status}=  SSL Config Get Peer Cert Fqdn Status
    Should Be Equal  ${status}  Disabled

Tvh1562986c
    [Documentation]  Have certificates with Non-FQDN/DNS names, do save/reset/load config and \n
    ...  verify SMA behaviour \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562986c \n
    ...  Have certificates with Non-FQDN/DNS names, do SMA reload and verify SMA behaviour \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562987c \n
    [Tags]   Tvh1562986c  Tvh1562987c  reset
    [Setup]  DefaultTestCaseSetup
    [Teardown]  Tvh1562986c Teardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{cert_and_key}=  Create List  www.cisco.com.pem  www.cisco.com_key.pem  cisco.com.pem  cisco.com_key.pem
    Verify FQDN For Valid Certificates  ${cert_and_key}

    @{cert_and_key}=  Create List  _.com.pem  _.com_key.pem  _isco.com.pem  _isco.com_key.pem
    ...  10.10.9.12.pem  10.10.9.12_key.pem
    FOR  ${cert}  ${key}  IN  @{cert_and_key}
        ${cert_text}=  OperatingSystem.Get File  ${CERT_FILES_DIR}/${cert}
        ${cert_key_text}=  OperatingSystem.Get File  ${CERT_FILES_DIR}/${key}
        Cert Config Setup  ${cert_text}  ${cert_key_text}
        ...  one_cert=yes
        ...  intermediate=no
        ...  fqdn=No
    END
    Restart CLI Session
    ${SMA_CONF}=  Save Config
    ${config_text}=    Run On Dut  cat ${CONFIG_DIR}/${SMA_CONF}
    Log  ${config_text}
    Set Test Variable   ${config_text}

    Restart CLI Session
    Suspend  0
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Configure SSL For GUI

    ${result}=  Load Config Via Cli  ${config_text}
    Commit

    Diagnostic Reload  confirm=yes  wipedata=yes

Tvh1562989c
    [Documentation]  Verify certificates with proper FQDN/DNS names can only be imported/created/ \n
    ...  validated after upgrade \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1562989c \n
    [Tags]   Tvh1562989c  upgrade
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    @{cert_and_key}=  Create List  www.cisco.com.pem  www.cisco.com_key.pem  cisco.com.pem
    ...  cisco.com_key.pem
    Run Keyword If  '${SMA_LIB_VERSION}' >= 'zeus1400'
    ...  Verify FQDN For Valid Certificates  ${cert_and_key}
    Restart CLI Session

    #Upgrade to SMA_UPGRADE_VERSION
    ${current_build}=  Get Current Dut Version
    Should Be Equal  ${SMA_BASE_BUILD}  ${current_build}
    Update Config Dynamic Host  dynamic_host=${UPDATE_SERVER}:443
    Update Config Validate Certificates  validate_certificates=no
	Commit
    Upgrade Downloadinstall
    ...  ${SMA_UPGRADE_VERSION}
    ...  seconds=10
    ...  save_cfg=yes
    ...  email=yes
    ...  email_addr=${ALERT_RCPT}
    Sleep  1m  Compensate default reboot delay
    Wait until DUT Reboots    wait_for_ports=80,443,22
    ${current_build}=  Get Current Dut Version
    Should Be Equal  ${SMA_UPGRADE_VERSION}  ${current_build}

    #Verifying FQDN functionality after upgrade.
    Verify FQDN For Valid Certificates  ${cert_and_key}

