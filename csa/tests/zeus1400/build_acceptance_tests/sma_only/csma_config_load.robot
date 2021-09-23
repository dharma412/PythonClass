*** Settings ***
Resource    sma/global.txt
Resource    regression.txt

Suite Setup  Initialize Suite
Suite Teardown  Finalize Suite

*** Variables ***
${BASE_CONFIG_XML_FILE}=  sma_base_config_14.0.0.xml
${BASE_DIR}=  %{SARF_HOME}/tools/ces/config_builder/
${CES_LICENSE_NAME}=  ces_sma_license.xml
${CONFIG_DIR}=  /data/pub/configuration
${LICENSE_PATH}=  %{SARF_HOME}/tests/testdata/virtual/
${VSMA_LICENSE_NAME}=  smalicense.xml


***Keywords***
Initialize Suite
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    # DefaultTestSuiteSetup is not needed for this test
    # as it requires a CES license to be loaded before
    # loading the CES zero day config. Since this test
    # will run as part of regular BATS in Jenkins hence
    # doing a resetconfig just to clean everything.

    Suspend  0
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}

    # Copy CES license and on prem SMA license to SMA
    Copy To DUT  ${LICENSE_PATH}/${CES_LICENSE_NAME}
    Copy To DUT  ${LICENSE_PATH}/${VSMA_LICENSE_NAME}

    # Load CES license
    Load License From File  ${CES_LICENSE_NAME}


Finalize Suite
    DefaultTestSuiteTeardown

Copy To DUT
    [Arguments]  ${file_name}
    Copy File To Dut
    ...  ${file_name}
    ...  ${CONFIG_DIR}
    ...  from_user=testuser
    ...  from_password=iropnort

Load License From File
    [Arguments]  ${file_name}
    ${license_paste_return}=  Load License  conf=file  conf_file=${file_name}
    Log  ${license_paste_return}

Get SMA Version
    ${_build_installed} =  Version
    Log  ${_build_installed}
    ${_sma_version} =  Evaluate
    ...  re.search('Version: ([0-9]+\.[0-9]+\.[0-9]+-[0-9]+)', '''${_build_installed}''').group(1)
    ...  re
    Log  ${_sma_version}
    [Return]  ${_sma_version}

Do Tvh1583688c Setup
    DefaultTestCaseSetup

    # Delete existing config on the client (if exists)
    Run  rm -vf ${BASE_DIR}/${BASE_CONFIG_XML_FILE}

    # Delete existing config on the SMA (if exists)
    Run On Dut  rm -vf ${CONFIG_DIR}/${BASE_CONFIG_XML_FILE}

    # Take backup of original config_builder.conf
    Run  cp -vf ${BASE_DIR}/config_builder.conf ${BASE_DIR}/config_builder_bk.conf

    # Get ESA serial number
    Set Appliance Under Test to ESA
    ${version_output}=  Version
    ${serial_number}=  Get Lines Matching Pattern  ${version_output}  Serial \#:*
    ${serial_number}=  Fetch From Right  ${serial_number}  :
    Set Variable  ${serial_number}
    ${serial}=  Strip String  ${serial_number}

    Set Appliance Under Test to SMA
    ${SMA_build}=  Get SMA Version

    # Replace primary_ip_interface, instance_external_name, alert_email_address,
    # sma_instance_external_name, sma_euq_url, smamodelname,
    # sma_primary_ip_interface, sma_primary_netmask, sma_primary_gateway,
    # serial_number, sma_ext_name with proper values in config_builder.conf
    Run  sed -i s/^sma_version=.*/sma_version=${SMA_build}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^primary_ip_interface=.*/primary_ip_interface=${ESA_IP}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^instance_external_name=.*/instance_external_name=${ESA}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^alert_email_address=.*/alert_email_address=testuser@mail.sgg.cisco.com/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^sma_instance_external_name=.*/sma_instance_external_name=${SMA}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^sma_euq_url=.*/sma_euq_url=${SMA}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^smamodelname=M100V=.*/smamodelname=${SMA_MODEL}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^sma_primary_ip_interface=.*/sma_primary_ip_interface=${SMA_IP}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^sma_primary_netmask=.*/sma_primary_netmask=${DUT_NETMASK}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^sma_primary_gateway=.*/sma_primary_gateway=${DUT_GW}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^serial_number=.*/serial_number=${serial}/ ${BASE_DIR}/config_builder.conf
    Run  sed -i s/^sma_ext_name=.*/sma_ext_name=${SMA}/ ${BASE_DIR}/config_builder.conf

    # Replace template_path value with current client's
    # workspace path
    ${TEMPLATE_PATH}=  Replace String Using Regexp  ${BASE_DIR}  \\/  \\\\\\\\/
    Run  sed -i s/^template_path=.*/template_path=${TEMPLATE_PATH}/ ${BASE_DIR}/config_builder.conf

    # Run config_builder.py script to generate Zero day config XML
    ${output}=  Run  cd ${BASE_DIR} && python config_builder.py
    Log  ${output}

    # Copy Zero day XML to SMA and verify copy was successful
    Copy To DUT  ${BASE_DIR}/${BASE_CONFIG_XML_FILE}
    ${result}=  Run On Dut  ls ${CONFIG_DIR}
    Should Contain  ${result}  ${BASE_CONFIG_XML_FILE}

Do Tvh1583688c Teardown
    # If anything fails or SMA crashes during config load or config save
    # then CLI session will break. Open a new one if needed.
    Start CLI Session If Not Open

    # Restore SMA's default admin ssw password
    Suspend  0
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}

    # Load on prem SMA license
    Load License From File  ${VSMA_LICENSE_NAME}

    # Restore original config_builder.conf
    # and delete generated base config from client
    Run  cp -vf ${BASE_DIR}/config_builder_bk.conf ${BASE_DIR}/config_builder.conf
    Run  rm -vf ${BASE_DIR}/config_builder_bk.conf
    Run  rm -vf ${BASE_DIR}/${BASE_CONFIG_XML_FILE}

    DefaultTestCaseTeardown

*** Test Cases ***
Tvh1583688c
    [Documentation]  Load CES Zeroday config xml to 14.0 SMA \n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1583688 \n
    [Tags]  Tvh1583688c  autobat
    [Setup]  Do Tvh1583688c Setup
    [Teardown]  Do Tvh1583688c Teardown

    # Load CES zero day config
    ${result}=  Load Config From File  ${BASE_CONFIG_XML_FILE}
    Commit

    Selenium Login
    Configuration File Save Config  mask_passwd=${False}
