*** Settings ***
Resource  regression.txt
Resource  wsa/global.txt
Resource  sma/global_sma.txt
Resource  sma/config_masters.txt

Suite Setup	Custom Suite Setup
Suite Teardown	DefaultRegressionSuiteTeardown

*** Variables ***
${IP1}        10.10.7.0/24
${IP2}        10.10.7.1/24
${IP3}        10.10.7.0/24,10.10.8.0/24


*** Keywords ***
Custom Suite Setup
    DefaultRegressionSuiteSetup
    Set CMs
    Selenium Close
    Set Suite Variable  ${SSW}  ${False}

Enable Configuration Master And Add Web Appliance
    Library Order SMA
    Selenium Login
    Centralized Web Reporting Enable
    Centralized Web Configuration Manager Enable
    @{Configuration_Master}  Create List  ${sma_config_masters.${CM}}
    ...  ${sma_config_masters.${CM1}}
    FOR  ${ConfigMaster}  IN  @{Configuration_Master}
      Configuration Masters Initialize  ${ConfigMaster}  ${True}
    END
    ${WSA_IP}=   Get Host IP By Name    ${WSA}
    ${WSA2_IP}=   Get Host IP By Name    ${WSA2}

    @{Add_Appliance}  Create List  ${WSA}  ${WSA_IP}  ${sma_config_masters.${CM}}
    ...  ${WSA2}  ${WSA2_IP}  ${sma_config_masters.${CM1}}

    FOR  ${applaince_name}  ${wsa_ip}  ${sma_cm}  IN  @{Add_Appliance}
      Wait Until Keyword Succeeds  7m  1m  Security Appliances Add Web Appliance
      ...  ${applaince_name}
      ...  ${wsa_ip}
      ...  iccm=${True}
      ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
      ...  config_master=${sma_cm}
    END
    Commit Changes

*** Test Cases ***
CSCvn57479
    [Tags]  CSCvn57479  CSCvn40552  teacat
    [Documentation]
    ...  \n  1. Install SMA with 11.5.1-105
    ...  \n  2. Run SSW
    ...  \n  3	Login to SMA through CLI
    ...  \n  4.Give the command saveconfig
    ...  \n  5.Give N when asked Do you want to mask the password? Files with masked passwords cannot be loaded using loadconfig command. [Y]>
    ...  \n  traceback is seen with "KeyError: 'LoginGraceTime'"

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    #Save Config through CLI
    ${result}=  Save Config
    Log  ${result}

CSCvn33303
    [Tags]  CSCvn33303  CSCvm5313  teacat
    [Documentation]
    ...  \n  1. Install SMA with 11.5.1-105
    ...  \n  2. Run SSW
    ...  \n  3. Enable Centralized Web Reporting and Centralized Configuration Management
    ...  \n  4. Join a WSA to the SMA
    ...  \n  5. Enable the 11.0 and 10.5 config masters
    ...  \n  6. Commit changes
    ...  \n  7. Go on the CLI and run saveconfig.  It should traceback with an error of "ValueError: webtapd"

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Enable Configuration Master And Add Web Appliance

    #Save config through UI-As per the TEACATs this step is not required but adding it as extra validation
    ${filename}  Configuration File Save Config
    Log  Saved as ${filename}

    Selenium Close

    #Save Config through CLI
    Start CLI Session If Not Open
    ${result}=  Save Config
    Log  ${result}


CSCvp18612
    [Tags]  CSCvp18612  teacat
    [Documentation]  Modifying subnets in Identities of CM can cause
    ...  subnets in policies membership to be removed
    ...  \n  1. Install SMA with 12.5.0.428
    ...  \n  2. Run SSW
    ...  \n  3. Enable Centralized Configuration Management
    ...  \n  5. Enable the 11.8 config masters
    ...  \n  6. Add an Identification Policy with a subnet.
    ...  \n  7. Create Access Policy using the Identification Policy
    ...  \n  created earlier. Add a specific subnet to the Access Policy.
    ...  \n  8. Commit changes
    ...  \n  9. Add another subnet to the Identification Profile created earlier.
    ...  \n  10. Commit changes
    ...  \n  11. Check the Access policy's subnet have old values

    Set Test Variable  ${TEST_ID}  ${TEST NAME}
    Library Order SMA
    Selenium Login
    Centralized Web Configuration Manager Enable
    FOR  ${sma_cm}  IN  ${CM}  ${CM1}
      Configuration Masters Initialize  ${sma_config_masters.${sma_cm}}  ${True}
      Run Keyword  ${sma_cm} Identities Add Policy
      ...  ${IDENTITY}
      ...  subnet=${IP1}
      ...  protocol=http
      Run Keyword  ${sma_cm} Access Policies Add
      ...  ${IDENTITY_01}
      ...  identity=${IDENTITY}
      ...  subnets=${IP2}
      Commit Changes
      Run Keyword  ${sma_cm} Identities Edit Policy
      ...  ${IDENTITY}
      ...  subnet=${IP3}
      Commit Changes
      Navigate To  Web   ${sma_config_masters.${sma_cm}}  Access Policies
      Page Should Contain  Subnets: ${IP2}
    END