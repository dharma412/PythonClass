*** Settings ***
Resource  regression.txt
Resource  wsa/global.txt
Resource  sma/config_masters.txt


Suite Setup	Custom Suite Setup
Suite Teardown	DefaultRegressionSuiteTeardown

*** Variables ***
${CATEGORY_NAME}  SMACategory
${ACCESS_POLICY_NAME}  SMAPolicies
${IDENTITY}  SMAIdentity

*** Keywords ***

Custom Suite Setup
    DefaultRegressionSuiteSetup
    Set CMs
    Selenium Close
    Set Suite Variable  ${SSW}  ${False}

    Enable and Initalize Configuration Master


Add and Edit Access Policies with Custom URL Categories
    @{configuration_masters}  Create List  ${CM}
    FOR  ${cm}  IN  @{configuration_masters}
      Run Keyword  ${cm} Custom Url Categories Add  ${CATEGORY_NAME}  google.com  order=1
      Run Keyword  ${cm} Identities Add Policy  ${IDENTITY}  description=Identity Profile  protocol=http
      Run Keyword  ${cm} Access Policies Add  ${ACCESS_POLICY_NAME}  description=Policies  identity=${IDENTITY}  url_categories=${CATEGORY_NAME}
      Commit Changes
      Run Keyword  ${cm} Access Policies Edit  ${ACCESS_POLICY_NAME}  identity=${IDENTITY}  proxy_ports=3128  user_agents=ie7, ie8
      Run Keyword  ${cm} Access Policies Edit Protocols And User Agents  ${ACCESS_POLICY_NAME}  block_protocols=http
      Run Keyword  ${cm} Access Policies Edit Objects  ${ACCESS_POLICY_NAME}  setting_type=custom  ftp_size=1024
      Run Keyword  ${cm} Access Policies Edit Applications  ${ACCESS_POLICY_NAME}
      Run Keyword  ${cm} Access Policies Edit Anti Malware And Reputation  ${ACCESS_POLICY_NAME}  wbrs_setting=disable
      Commit Changes
    END

Verify Access Policies List
   @{configuration_masters}  Create List  ${CM}
   FOR  ${cm}  IN  @{configuration_masters}
     ${policies}=  Run Keyword  ${cm} Access Policies Get List
     Log  ${policies}
     ${filtering_policy}=  Get From Dictionary  ${policies}  ${ACCESS_POLICY_NAME}
     ${proto_user}=  Get From Dictionary  ${filtering_policy}  protocols_and_user_agents
     ${url_filter}=  Get From Dictionary  ${filtering_policy}  url_filtering
     ${application}=  Get From Dictionary  ${filtering_policy}  applications
     ${objects}=  Get From Dictionary  ${filtering_policy}  objects
     ${amp}=  Get From Dictionary  ${filtering_policy}  anti-malware_and_reputation
     Log  ${proto_user}
     Log  ${url_filter}
     Log  ${application}
     Log  ${objects}
     Log  ${amp}
     Should Be Equal As Strings  Block: 1 Protocol  ${proto_user}
     Should Be Equal As Strings  Monitor: 1  ${url_filter}
     Should Be Equal As Strings  Monitor: 204  ${application}
     Should Be Equal As Strings  Web Reputation: Disabled\nAdvanced Malware Protection: Enabled\nAnti-Malware Scanning: Enabled  ${amp}
     Should Be Equal As Strings  No blocked items\nFTP Max Size: 1 GB  ${objects}
   END

Enable and Initalize Configuration Master
    Library Order SMA
    Selenium Login
    Centralized Web Reporting Enable
    Centralized Web Configuration Manager Enable
    Centralized Upgrade Manager Enable
    @{Configuration_Master}  Create List  ${sma_config_masters.${CM}}
    FOR  ${ConfigMaster}  IN  @{Configuration_Master}
      Configuration Masters Initialize  ${ConfigMaster}  ${True}
      Commit Changes
    END

*** Test Cases ***

CSCvn26076
    [Tags]  CSCvn26076  CSCve95724  teacat
    [Documentation]
    ...  Install the SMA version 11.0.0-145 and run SSW.
    ...  \n  Navigate to  Management Appliances>>  Centralized services >>  Web  >> Centralized Configuration Manager
    ...  \n  and enable Centralized Configuration Manager
    ...  \n  Navigate to Web>> Utilities >> Configuration Masters  and Initialize the 11.0 version of Configuration Master and commit changes.
    ...  \n  Navigate to  Web>> Configuration master 11.0 >> Custom Policy Elements >> Custom And External URL Categories.
    ...  \n  Add URL Category . Commit and submit changes.
    ...  \n  Navigate to  Web>> Configuration master 11.0 >> Web policies >> Access Policies and then click on Add policy
    ...  \n  Add SMAAccessPolicy. Change the values for Protocols and User Agents and URL Filtering .
    ...  \n  In SMAAccessPolicy click on  URL filtering and select Custom Category
    ...  \n  add new category named as SMACategory and select include it in policy and commit changes
    ...  \n  After addition of new policy named as my policy by default all fields (URL Filtering, Applications and Objects) have value as global policy

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Add and Edit Access Policies with Custom URL Categories

    Verify Access Policies List

    Selenium Close
