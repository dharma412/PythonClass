# $Id:
# $DateTime:
# $Author:

*** Settings ***
Library   Collections
Resource  regression.txt
Resource  sma/reports_keywords.txt
Resource  sma/config_masters.txt
Resource  sma/global_sma.txt
Library   SmaGuiLibrary  ${SMA}  ${SMA_UPGRADE_LIB_VERSION}  with name  SmaGuiLibrary2

Suite Setup     CustomSuiteSetup
Suite Teardown  DefaultRegressionSuiteTeardown

*** Variables ***
${IDENTITY}  Identity01
${POLICY}  Policy01

*** Keywords ***

Set Manifest Server
    [Arguments]  ${validate_flag}=NO  ${server}=${UPDATE_SERVER}  ${type}=WSA
    Start CLI Session If Not Open
    Run Keyword If  '${type}' == 'SMA'
    ...  Update Config Validate Certificates  validate_certificates=${validate_flag}
    Run Keyword If  '${type}' == 'WSA'
    ...  Update Config Validate Certificates  validate=${validate_flag}
    Update Config Dynamichost  dynamic_host=${server}:443
    Commit

Check Policies
    Set CMs
    ${status}  ${reason}=  Run Keyword And Ignore Error  SmaGuiLibrary2.Configuration Masters Initialize  ${sma_config_masters.${CM}}  ${True}
    Run Keyword If  '${status}' == 'FAIL'  Should Contain  ${reason}  config master is already initialized
    SmaGuiLibrary2.Configuration Masters Import Config  ${sma_config_masters.${CM}}
    ...  ${sma_config_masters.${CM1}}  copy_roles=${True}

    ${policies}=  Run Keyword  SmaGuiLibrary2.${CM} Get Access Policies
    Log  ${policies['${POLICY}']['url_filtering']}
    Should Be Equal  ${policies['${POLICY}']['url_filtering']}  ${conf_before}

CustomSuiteSetup
    DefaultRegressionSuiteSetup  reset_appliances=${False}
    Set CMs
    DefaultReportSuiteSetup  CM=${CM}

*** Test Cases ***

CSCvs52023
   [Tags]  srts  teacat  upgrade  CSCvs52023
   [Documentation]
   ...  Create Access Policy in old CM
   ...  Upgrade SMA to new build
   ...  Verify access policy is resstored in new CM

   Set Test Variable  ${TEST_ID}  ${TEST NAME}
   Centralized Web Configuration Manager Enable
   Centralized Upgrade Manager Enable
   ${status}  ${reason}=  Run Keyword And Ignore Error  Configuration Masters Initialize  ${sma_config_masters.${CM}}  ${True}
   Run Keyword If  '${status}' == 'FAIL'  Should Contain  ${reason}  config master is already initialized
   Log  ${CM}
   Run Keyword  ${CM} Identities Add Policy  ${IDENTITY}
   ...  description=Create Identity Profile
   ...  protocol=http

   Run Keyword  ${CM} Access Policies Add  ${POLICY}
   ...  description=Custom access policy with Custom identity ${IDENTITY}
   ...  identity=${IDENTITY}
   Commit Changes

   ${policies}=  Run Keyword  ${CM} Access Policies Get List
   Log  ${policies}
   Log  ${policies['${POLICY}']['url_filtering']}
   Set Test Variable  ${conf_before}  ${policies['${POLICY}']['url_filtering']}

   #Do upgrade in SMA and check it succeeds
   Set Manifest Server   validate_flag=NO  server=${UPDATE_SERVER}
   ...  type=SMA
   Upgrade Downloadinstall
   ...  ${SMA_UPGRADE_VERSION}
   ...  seconds=10
   ...  save_cfg=yes
   ...  email=yes
   ...  email_addr=${ALERT_RCPT}
   Sleep  1m  Compensate default reboot delay
   Wait until DUT Reboots    wait_for_ports=443
   Wait Until Keyword Succeeds  5m  30s  Selenium Login
   Restart Cli Session
   ${output}  Version
   Should Contain  ${output}  ${SMA_UPGRADE_VERSION}

   Set Test Variable  ${SMA_BASE_LIB_VERSION}  ${SMA_LIB_VERSION}
   Run Keyword If  '${SMA_UPGRADE_LIB_VERSION}' > '${SMA_BASE_LIB_VERSION}'
   ...   Check Policies
   Selenium Close

CSCvo87355
    [Documentation]
    ...  Upgrade SMA to new build
    ...  Verify in User Reports authenticated users are displayed
    [Tags]  srts  teacat  upgrade  CSCvo87355

    Library Order Sma
    Selenium Login
    Web Reporting Open
    ...  Users
    Web Reporting Check Cell Value
    ...  Users
    ...  ${LDAP_REPORTING_USER}
    ...  Transactions Completed
    ...  >0
    Web Reporting Check Cell Value
    ...  Users
    ...  ${LDAP_REPORTING_USER}
    ...  Bandwidth Used
    ...  >0
    Selenium Close
