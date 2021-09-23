*** Settings ***

Resource     regression.txt
Resource     web_reporting_preparation.txt
Resource     sma/global_sma.txt
Resource     wsa/global.txt
Resource     sma/config_masters.txt

Suite Setup    Do Suite Setup
Suite Teardown    Do Suite Teardown


*** Variables ***

${IDENTITY_01}  Identity01
${IDENTITY_02}  Identity02
${ACCESS_POLICY_NAME_1}  SMAAccPolicy1
${ACCESS_POLICY_NAME_2}  SMAAccPolicy2
${WSA_CONF}   sma_wsa.xml
${AD_REALM}	 ADRealm01
${AUTH_SCHEME}  Kerberos or NTLMSSP or Basic
${CONFIG_PATH}     /data/pub/configuration


*** Keywords ***
Do Suite Setup

    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    Set CMs
    Run Keywords  DefaultRegressionSuiteSetup  Enable SSW
    Disable SSW In Test Setup
    Add Web Appliance and assign CM

Disable SSW In Test Setup
    Set Suite Variable  ${SSW}  ${False}

Do Suite Teardown
    Selenium Close
    DefaultRegressionSuiteTeardown

Enable SSW
    Set Suite Variable  ${SKIP_SSW}  False

Add Web Appliance and assign CM
    Set Appliance Under Test to SMA
    ${WSA_IP}=  Get Host IP By Name  ${WSA}
    Enable Web Services
    Centralized Upgrade Manager Enable
    Security Appliances Add Web Appliance  ${WSA}  ${WSA_IP}  config_master=${sma_config_masters.${CM}}  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes

Setup Authentication Realm on WSA
    [Arguments]
    ...  ${REALM_NAME}
    ...  ${ADSERVER}
    ...  ${AD_DOMAIN}
    ...  ${DOMAIN_USER}
    ...  ${DOMAIN_PWD}
    ...  ${JOIN_DOMAIN}

    Authentication Add Ntlm Realm   ${REALM_NAME}
    ...  ${ADSERVER}
    ...  ${AD_DOMAIN}
    ...  domain_user=${DOMAIN_USER}
    ...  domain_pw=${DOMAIN_PWD}
    ...  join_domain=${JOIN_DOMAIN}

    Commit Changes  ADREALM

Save Wsa Config File
    [Arguments]  ${config_file}
    Run Keyword And Ignore Error  Run On DUT  rm -rf ${CONFIG_PATH}/${config_file}
    Configuration File Save  filename=${config_file}
    Copy File From Dut To Remote Machine  ${CLIENT_HOSTNAME}  ${CONFIG_PATH}/${config_file}  ${TEMPDIR}
    Run  sudo chmod a+r ${TEMPDIR}/${config_file}

*** Test Cases ***
CSCvo78466

    [Documentation]  Netinstall an SMA (M680 was used here) to version 8.4.0-150 \n
    ...  -Add a security appliance with an authentication realm configured and activate configuration master 11.8. \n
    ...  -Go to configuration master 12.5 and add an identity that requires authentication, and an access policy.
    ...  -Add a group that listed. [ As per Teacat, couldnt add the group.]

    [Tags]  srts  teacat  CSCvo78466

    Set Appliance Under Test to WSA
    Setup Authentication Realm on WSA
    ...  ${AD_REALM}
    ...  ${AD1_SERVER}
    ...  ${AD1_DOMAIN}
    ...  ${AD1_JOIN_USER}
    ...  ${AD1_JOIN_PW}
    ...  False
    Identities Add Policy  ${IDENTITY_01}   auth_method=requires  auth_realm=${AD_REALM}  auth_scheme=${AUTH_SCHEME}  protocol=http
    Access Policies Add  ${ACCESS_POLICY_NAME_1}  description=Policies  identity=${IDENTITY_01}:selected::${AD1_NET_DOMAIN}\\Account Operators
    Commit Changes
    Save Wsa Config File  ${WSA_CONF}

    Set Appliance Under Test to SMA
    Configuration Masters Import Config  ${sma_config_masters.${CM}}  ${sma_config_source.CONFIG_FILE}  filepath=${TEMPDIR}/${WSA_CONF}
    Commit Changes

    Run Keyword  ${CM} Identities Add Policy  ${IDENTITY_02}  auth_method=requires  auth_realm=${AD_REALM}  auth_scheme=${AUTH_SCHEME}
    Commit Changes
    Run Keyword  ${CM} Access Policies Add  ${ACCESS_POLICY_NAME_2}  description=Policies  identity=${IDENTITY_02}:selected::${AD1_NET_DOMAIN}\\Account Operators
    Commit Changes