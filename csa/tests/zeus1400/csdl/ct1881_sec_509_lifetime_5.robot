*** Settings ***
Resource           sma/csdlresource.txt

Force Tags         csdl
Suite Setup        Initialize Suite
Suite Teardown     Finalize Suite
Test Setup         DefaultTestCaseSetup
Test Teardown      DefaultTestCaseTeardown


*** Variables ***
${EUQ_PORT}=      83
${NGUI_PORT}=     4431


*** Keywords ***
Initialize Suite
    Set Aliases For Appliance Libraries
    CSDL Suite Setup
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Spam Quarantine Enable
    Commit Changes

Finalize Suite
    Spam Quarantine Disable
    Commit Changes
    CSDL Suite Teardown

Verify Default SMA Certificate Validity
    [Arguments]  ${port}
    ${rc}  ${cmd_out}=  Run And Return Rc And Output
    ...  echo | openssl s_client -connect ${SMA_IP}:${port} 2>/dev/null | openssl x509 -text
    Log  ${cmd_out}
    Should Be Equal As Integers  ${rc}  0

    # Getting certificate created year
    ${certificate_from_date}=  Get Lines Containing String  ${cmd_out}  Not Before
    @{certificate_from_date_list}=  Split String  ${certificate_from_date}
    ${valid_from_year}=  Get From List  ${certificate_from_date_list}  5

    # Getting certificate expired year
    ${certificate_to_date}=  Get Lines Containing String  ${cmd_out}  Not After
    @{certificate_to_date_list}=  Split String  ${certificate_to_date}
    ${valid_to_year}=  Get From List  ${certificate_to_date_list}  6

    ${validity_period}=  Evaluate  ${valid_to_year} - ${valid_from_year}
    Log  ${validity_period}
    Should Be True	2 < ${validity_period} < 5


*** Test Cases ***
Tvh1548719c
    [Documentation]  Verify default SMA Certificate (End entity certificate) for GUI HTTPS
    ...  service does not have validity greater than 2 years and less than 5 years.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1548719c
    [Tags]  Tvh1548719c

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Verify Default SMA Certificate Validity  ${DUT_PORT}

Tvh1548720c
    [Documentation]  Verify default SMA Certificate (End entity certificate) for Spam Quarantine
    ...  HTTPS service does not have validity greater than 2 years and less than 5 years.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1548720c
    [Tags]  Tvh1548720c

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    Go To  https://${DUT}:83
    Login To Spam Quarantine  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Verify Default SMA Certificate Validity  ${EUQ_PORT}

Tvh1548721c
    [Documentation]  Verify default SMA Certificate (End entity certificate) for NGUI
    ...  service does not have validity greater than 2 years and less than 5 years.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1548721c
    [Tags]  Tvh1548721c

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    SMANGGuiLibrary.Launch Dut Browser
    SMANGGuiLibrary.Login Into Dut
    Verify Default SMA Certificate Validity  ${NGUI_PORT}
    SMANGGuiLibrary.Close Browser

Tvh1548730c
    [Documentation]  VVerify SMA's default certificate's validity after save, reset/reload
    ...  and load configuration.\n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1548730c
    [Tags]  Tvh1548730c

    Set Test Variable  ${TEST_ID}  ${TEST NAME}

    ${SMA_ORIG_CONFIG}=  Save Config
    Set Test Variable  ${SMA_ORIG_CONFIG}
    Suspend  0
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}
    Restart CLI Session
    Load Config From File  ${SMA_ORIG_CONFIG}
    Commit
    Close Browser
    Selenium Login
    Verify Default SMA Certificate Validity  ${DUT_PORT}
    
    Go To  https://${DUT}:83
    Login To Spam Quarantine  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Verify Default SMA Certificate Validity  ${EUQ_PORT}
    
    SMANGGuiLibrary.Launch Dut Browser
    SMANGGuiLibrary.Login Into Dut
    Verify Default SMA Certificate Validity  ${NGUI_PORT}
    SMANGGuiLibrary.Close Browser