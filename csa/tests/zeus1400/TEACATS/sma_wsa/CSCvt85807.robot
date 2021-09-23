# $Id:
# $DateTime:
# $Author:

*** Settings ***
Library     Collections
Resource    regression.txt
Resource    sma/config_masters.txt

Suite Setup     CustomSuiteSetup
Test Setup      DefaultRegressionTestCaseSetup
Test Teardown   DefaultRegressionTestCaseTeardown
Suite Teardown  DefaultRegressionSuiteTeardown

*** Variables ***
${name}                     Publish

*** Keywords ***

CustomSuiteSetup
   DefaultRegressionSuiteSetup
   Set Suite Variable  ${SSW}  ${False}
   Add Web Appliance  ${WSA}

Add Web Appliance
   [Arguments]   ${WSA}
   Set CMs
   Library Order Sma
   Run Keyword And Ignore Error  Log Out Of DUT
   Log Into DUT
   Centralized Web Reporting Enable
   Centralized Web Configuration Manager Enable
   Centralized Upgrade Manager Enable
   ${status}  ${reason}=  Run Keyword And Ignore Error  Configuration Masters Initialize  ${sma_config_masters.${CM}}  ${True}
   Run Keyword If  '${status}' == 'FAIL'  Should Contain  ${reason}  config master is already initialized
   Wait Until Keyword Succeeds  7m  1m  Security Appliances Add Web Appliance
   ...   ${WSA}
   ...   ${WSA}
   ...   ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
   ...   config_master=${sma_config_masters.${CM}}
   Commit Changes

Publish to WSA and verify status
    [Arguments]  ${wsa_name}  ${to_cm}  ${msg}
    ${publish_result}=  Publish To Web Appliances Configuration Master Now
    ...  system-generated  ${to_cm}
    ...  ${${wsa_name}}
    Log  ${publish_result}
    Should Match Regexp  ${publish_result['${${wsa_name}}']}  .*${msg}.*

Create SMA Policies
    [Arguments]  ${cm_name}
    Set Suite Variable  ${identity_name}    Identity${name}
    Set Suite Variable  ${access_policy_All}   AccessPolicyA${name}
    Set Suite Variable  ${decryption_policy_All}  DecryptionPolicy${name}
    Security Services Display Edit Cm Settings  ${sma_config_masters.${cm_name}}
    ...  https_proxy=${True}
    ...  sophos_anti_malware=${True}
    Commit Changes
    Run Keyword  ${cm_name} Identities Add Policy
    ...  ${identity_name}
    ...  protocol=http
    Set Suite Variable  ${CUST_URL}  cust01
    Set Suite Variable  ${SITE}  site1.com, site2.com
    Run Keyword  ${cm_name} Custom Url Categories Add   ${CUST_URL}
    ...  sites=${SITE}
    Run Keyword  ${cm_name} Access Policies Add
    ...  ${access_policy_All}
    ...  identity=${identity_name}
    ...  url_categories=${CUST_URL}
    Run Keyword  ${cm_name} Decryption Policies Add  ${decryption_policy_All}
    ...  description=This policy uses ${identity_name}
    ...  identities=${identity_name}
    ...  url_categories=${CUST_URL}
    Commit Changes
    Run Keyword  ${cm_name} Access Policies Edit Protocols And User Agents
    ...  ${access_policy_All}  setting_type=disable
    Commit Changes

*** TestCases ***

CSCvt85807
   [Documentation]
   ...  \n 1. Add WSA to SMA
   ...  \n 2. Create Access Policies in SMA
   ...  \n 3. Access Policies Protocols and User Agents disable
   ...  \n 4. Verify Publish from SMA to WSA is successful

   [Tags]  CSCvt85807  teacat
   Create SMA Policies  ${CM}
   Publish to WSA and verify status  WSA  ${sma_config_masters.${CM}}  Success
