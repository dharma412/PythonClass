*** Settings ***
Library      String
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown
Test Setup      DefaultTestCaseSetup
Test Teardown   DefaultTestCaseTeardown


*** Variables ***
${CONFIG_DIR}=                /data/pub/configuration/
${CUSTOM_CA_CERT}=            %{SARF_HOME}/tests/testdata/sma/csdl/csdl_custom_ca.pem
${CUSTOM_CA_CERT_1}=          %{SARF_HOME}/tests/testdata/sma/csdl/csdl_custom_ca_1.pem
${CHAIN_CERT}=                %{SARF_HOME}/tests/testdata/sma/csdl/csdl_chain_ca.pem
${PK12_CERT}=                 %{SARF_HOME}/tests/testdata/sma/csdl/csdl_custom_ca.p12
${INVALID_CERT}=              %{SARF_HOME}/tests/testdata/sma/csdl/csdl_invalid_ca_cert.pem
${IMPORT_ERROR}=              Imported an Invalid Certificate
${CERT_NAME}=                 csdl_custom_ca


*** Keywords ***
Reset Configuration
    ${config_file}=  Configuration File Save Config  mask_passwd=${False}
    Set Test Variable  ${config_file}
    Configuration File Reset
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Selenium Close
    Selenium Login


*** Test Cases ***
Tvh1494729c
    [Documentation]  Verify usage of Trusted root CAs can be enabled/disabled at CLI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494729c
    [Tags]  Tvh1494729c

    ${status}=  Cert Authority Enable Disable  cert_auth_type=system  enable=${False}
    Log  ${status}
    Commit
    should contain  ${status}  System list disabled

    ${status}=  Cert Authority Enable Disable  cert_auth_type=system  enable=${True}
    Log  ${status}
    Commit
    should contain  ${status}  System list enabled

Tvh1494733c
    [Documentation]  Verify Custom-CAs can be enabled/disabled at CLI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494733c
    [Tags]  Tvh1494733c

    ${status}=  Cert Authority Enable Disable  cert_auth_type=custom  enable=${True}
    Log  ${status}
    Commit
    should contain  ${status}  Custom list enabled

    ${status}=  Cert Authority Enable Disable  cert_auth_type=custom  enable=${False}
    Log  ${status}
    Commit
    should contain  ${status}  Custom list disabled

Tvh1494734c
    [Documentation]  Verify Custom-CAs can be imported through CLI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494734c
    ...  Verify Custom-CAs can be displayed at CLI .\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494735c
    ...  Verify Custom-CAs can be exported/downloaded through CLI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494736c
    [Tags]  Tvh1494734c  Tvh1494735c  Tvh1494736c
    [Teardown]  Run Keywords  Cert Authority Delete  1  y
    ...  AND  Commit

    Copy File To DUT  ${CUSTOM_CA_CERT}  ${CONFIG_DIR}
    Set Test Variable  ${FILE_NAME}  csdl_custom_ca.pem
    Cert Authority Import  ${FILE_NAME}
    Commit

    ${custom_certs}=  Cert Authority Print  cert_auth_type=custom
    should contain  ${custom_certs}[0]  ${CERT_NAME}

    Cert Authority Export  1  custom.txt  cert_type=custom  export_all=${True}
    ${output}=  Run On DUT  ls ${CONFIG_DIR}
    should contain  ${output}  custom.txt


Tvh1494742c
    [Documentation]  Enable & Import Custom-CAs through CLI, save configuration and reset
    ...  the configuration. Load saved configuration and verify Custom-Cas are loaded back.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494742c
    [Tags]  Tvh1494742c
    [Teardown]  Run Keywords  Cert Authority Enable Disable  cert_auth_type=custom  enable=${False}
    ...  AND  Commit

    ${status}=  Cert Authority Enable Disable  cert_auth_type=custom  enable=${True}
    Commit
    should contain  ${status}  Custom list enabled

    ${status}=  Cert Authority Enable Disable  cert_auth_type=system  enable=${True}
    should contain  ${status}  Already Enabled

    Restart CLI Session

    ${CONFIG_FILE}=  Save Config  yes

    Suspend
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_TMP_PASSWORD}

    ${status}=  Cert Authority Enable Disable  cert_auth_type=custom  enable=${False}
    should contain  ${status}  Already Disabled

    Restart CLI Session

    Load Config From File   ${CONFIG_FILE}
    commit

    ${status}=  Cert Authority Enable Disable  cert_auth_type=custom  enable=${True}
    should contain  ${status}  Already Enabled

Tvh1494745c
    [Documentation]  Verify usage of Trusted root CAs can be enabled/disabled at GUI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494745c
    ...  Verify Custom-CAs can be enabled/disabled at GUI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494750c
    [Tags]  Tvh1494745c  Tvh1494750c

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Enabled
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled

    Edit Certificate Authorities  custom_list_enable=${True}  system_list_enable=${False}
    Commit Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Enabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Disabled

    Edit Certificate Authorities  custom_list_enable=${False}  system_list_enable=${True}
    Commit Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Enabled

Tvh1494751c
    [Documentation]  Verify Custom-CAs (.pem format) can be imported through GUI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494751c
    ...  Verify Custom-CAs can be displayed at GUI, verify individual certificate
    ...  details can be viewed.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494752c
    ...  Disable Custom-CA and verify already uploaded certificates are still
    ...  available and it is not.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494766c
    ...  Verify Custom-CAs can be deleted through GUI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494754c
    [Tags]  Tvh1494751c  Tvh1494752c  Tvh1494754c  Tvh1494766c

    Edit Certificate Authorities  custom_list_enable=${True}
    ...  system_list_enable=${True}  custom_list_cert_path=${CUSTOM_CA_CERT}
    Commit Changes

    ${custom_list}=  Get All Custom Trusted Root Cert
    Log  ${custom_list}
    should contain  ${custom_list}  ${CERT_NAME}

    ${details}=  Get Custom Trusted Root Cert Detail  ${CERT_NAME}
    Log  ${details}
    ${value}=  Get Dictionary Values  ${details}
    Log  ${value}
    should contain  ${value}  ${CERT_NAME}

    Edit Certificate Authorities  custom_list_enable=${False}  system_list_enable=${True}
    Commit Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled

    ${custom_list}=  Get All Custom Trusted Root Cert
    Log  ${custom_list}
    should contain  ${custom_list}  ${CERT_NAME}

    Delete Custom Trusted Root Cert  ${CERT_NAME}
    Commit Changes

    ${custom_list}=  Get All Custom Trusted Root Cert
    Log  ${custom_list}
    should not contain  ${custom_list}  ${CERT_NAME}

Tvh1494755c
    [Documentation]  Upload Custom-CA in .p12 or .der format and verify it is rejected.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494755c
    [Tags]  Tvh1494755c

    Roll Over Now  logname=gui_logs

    Run Keyword And Expect Error  GuiValueError: *  Edit Certificate Authorities  custom_list_enable=${True}
    ...  system_list_enable=${True}  custom_list_cert_path=${PK12_CERT}
    Page Should Contain  ${IMPORT_ERROR}

    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  ${IMPORT_ERROR} >=1

Tvh1494762c
    [Documentation]  Enable Custom-CA and click  on cancel or Abandon changes verify changes are cancelled,
    ...  Enable Custom-CA and click on submit and commit verify the changes are reflected,
    ...  repeat the check for disabling Custom-CA.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494762c
    ...  Enable System-CA and click on cancel or Abandon changes verify changes are cancelled,
    ...  Enable System-CA and click on submit and commit verify the changes are reflected,
    ...  repeat the check for disabling System-CA.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494763c
    [Tags]  Tvh1494762c  Tvh1494763c

    Edit Certificate Authorities  custom_list_enable=${True}  system_list_enable=${False}
    Abandon Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Enabled

    Edit Certificate Authorities  custom_list_enable=${True}  system_list_enable=${False}
    Commit Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Enabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Disabled

    Edit Certificate Authorities  custom_list_enable=${False}  system_list_enable=${True}
    Abandon Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Enabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Disabled

    Edit Certificate Authorities  custom_list_enable=${False}  system_list_enable=${True}
    Commit Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Enabled

    # Enable Custom-CA and Disable System-CA and click on cancel
    Edit Certificate Authorities  custom_list_enable=${True}  system_list_enable=${False}
    Cancel Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Enabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Disabled


Tvh1494775c
    [Documentation]  Enable Custom & System CA, Import Custom-CAs through GUI, Save configuration
    ...  file and reset configuration, load saved configuration file and verify custom CA , System CA
    ...  are enabled. Repeat this check for disabling Custom & System CA\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494775c
    [Tags]  Tvh1494775c

    # Enable Custom & System CA
    Edit Certificate Authorities  custom_list_enable=${True}  system_list_enable=${True}
    Commit Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Enabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Enabled

    Reset Configuration
    #Default Configuration status
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Enabled

    Load Config From File   ${config_file}
    commit

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Enabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Enabled

    # Disable Custom & System CA
    Edit Certificate Authorities  custom_list_enable=${False}  system_list_enable=${False}
    Commit Changes
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Disabled

    Reset Configuration

    #Default Configuration status
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Enabled

    Load Config From File  ${config_file}
    commit

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ${custom_status}=  Get Certificate Authority Status  custom
    should contain  ${custom_status}  Disabled
    ${system_status}=  Get Certificate Authority Status  system
    should contain  ${system_status}  Disabled

Tvh1494759c
    [Documentation]  Upload invalid/corrupted CAs under Custom-CA and verify that are rejected.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494755c
    [Tags]  Tvh1494759c

    Roll Over Now  logname=gui_logs

    Run Keyword And Expect Error  GuiValueError: *  Edit Certificate Authorities  custom_list_enable=${True}
    ...  system_list_enable=${True}  custom_list_cert_path=${INVALID_CERT}

    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  User admin has performed custom CA certificate related operation which has failed due to Invalid X.509 format >=1

Tvh1494787c
    [Documentation]  Verify Custom-Cas imported through GUI are reflected and can be viewed, deleted at CLI\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494787c
    [Tags]  Tvh1494787c

    Edit Certificate Authorities  custom_list_enable=${True}
    ...  system_list_enable=${True}  custom_list_cert_path=${CUSTOM_CA_CERT}
    Commit Changes

    ${custom_list}=  Get All Custom Trusted Root Cert
    Log  ${custom_list}
    should contain  ${custom_list}  ${CERT_NAME}

    ${custom_list_cli}=  Cert Authority Print  cert_auth_type=custom
    should contain  ${custom_list_cli}[0]  ${CERT_NAME}

    Cert Authority Delete  1  y
    Commit

    ${custom_list}=  Get All Custom Trusted Root Cert
    should not contain  ${custom_list}  ${CERT_NAME}

Tvh1494786c
    [Documentation]  Verify Custom-Cas that are imported through CLI can be deleted through GUI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494786c
    ...  Verify multiple Custom-CAs can be imported through CLI one by one
    ...  and are appended not overwritten
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494744c
    [Tags]  Tvh1494786c  Tvh1494744c

    Copy File To DUT  ${CUSTOM_CA_CERT}  ${CONFIG_DIR}
    Copy File To DUT  ${CUSTOM_CA_CERT_1}  ${CONFIG_DIR}
    Set Test Variable  ${CERT_NAME_1}  csdl_custom_ca_1
    Set Test Variable  ${FILE_NAME}  csdl_custom_ca.pem
    Set Test Variable  ${FILE_NAME_1}  csdl_custom_ca_1.pem

    Cert Authority Import  ${FILE_NAME}
    Cert Authority Import  ${FILE_NAME_1}
    Commit
    ${custom_list_cli}=  Cert Authority Print  cert_auth_type=custom
    should contain  ${custom_list_cli}[0]  ${CERT_NAME}
    should contain  ${custom_list_cli}[1]  ${CERT_NAME_1}

    ${custom_list_gui}=  Get All Custom Trusted Root Cert
    should contain  ${custom_list_gui}  ${CERT_NAME}
    should contain  ${custom_list_gui}  ${CERT_NAME_1}

    Delete Custom Trusted Root Cert  ${CERT_NAME}
    Delete Custom Trusted Root Cert  ${CERT_NAME_1}
    Commit Changes

    ${custom_list}=  Get All Custom Trusted Root Cert
    should not contain  ${custom_list}  ${CERT_NAME}
    should not contain  ${custom_list}  ${CERT_NAME_1}

Tvh1494788c
    [Documentation]  Verify logs have been added when certificates imported/appended/deleted through GUI.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494788c
    [Tags]  Tvh1494788c

    Roll Over Now  logname=gui_logs

    Edit Certificate Authorities  custom_list_enable=${True}
    ...  system_list_enable=${True}  custom_list_cert_path=${CUSTOM_CA_CERT}
    Commit Changes

    Delete Custom Trusted Root Cert  ${CERT_NAME}
    Commit Changes

    Verify And Wait For Log Records
    ...  wait_time=180 seconds
    ...  retry_time=10 seconds
    ...  search_path=${GUI_LOGS}
    ...  Certificate successfully uploaded >=1
    ...  Certificate is updated with.*common_name ${CERT_NAME} >=1
    ...  Certificate profile is deleted with name ${CERT_NAME} >=1

Tvh1494756c
    [Documentation]  Upload Custom-CA certificate chain and verify it is accepted
    ...  and displayed properly\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494756c
    [Tags]  Tvh1494756c
    [Teardown]  Run Keywords  Delete Custom Trusted Root Cert  cisco.com
    ...  AND  Delete Custom Trusted Root Cert  mail.cisco.com
    ...  AND  Commit Changes

    Edit Certificate Authorities  custom_list_enable=${True}
    ...  system_list_enable=${True}  custom_list_cert_path=${CHAIN_CERT}
    Commit Changes

    ${custom_list}=  Get All Custom Trusted Root Cert
    Log  ${custom_list}
    should contain  ${custom_list}  cisco.com
    should contain  ${custom_list}  mail.cisco.com

Tvh1494776c
    [Documentation]  Override trust for few certificates under Trusted Root certificates,
    ...  Save configuration file and reset configuration, load saved configuration file
    ...  and verify Certificates override status remains same after loading configuration file.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1494776c
    [Tags]  Tvh1494776c
    [Teardown]  Run Keywords  Override Trusted Root Certificate  1  ${False}
    ...  AND  Override Trusted Root Certificate  2  ${False}
    ...  AND  Commit Changes

    Override Trusted Root Certificate  1  ${True}
    Override Trusted Root Certificate  2  ${True}
    Page Should Contain  2 trusted root certificates in the Cisco list have been overridden
    Commit changes

    Reset Configuration
    #Default Configuration status
    Navigate To  Network  Certificates
    Page Should Not Contain  2 trusted root certificates in the Cisco list have been overridden

    Load Config From File   ${config_file}
    commit

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Navigate To  Network  Certificates
    Page Should Contain  2 trusted root certificates in the Cisco list have been overridden