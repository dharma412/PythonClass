*** Settings ***
Resource           sma/csdlresource.txt

Force Tags         csdl
Suite Setup        Initialize Suite
Suite Teardown     CSDL Suite Teardown


*** Variables ***
${USER_NAME}=                    testuser
${PASSWORD}=                     Fdsag12$
${USER_ROLE}=                    Administrator
${USERS_PII_INFORMATION}=        9000000009
${ALERTS_PII_INFORMATION}=       sample@cisco.com
${SYSTEM_USERS_PATH}=            /data/db/config/system.users/data.cfg
${SYSTEM_ALERTS_PATH}=           /data/db/config/system.alert/data.cfg

*** Keywords ***
Initialize Suite
    CSDL Suite Setup 
    Log Into Dut

*** Test Cases ***
Tvh1556321c
    [Documentation]  Verify collected PII data in SMA [Email address, sender/recipient \n
    ...  addresses, Mail headers, etc] are deleted when un-needed. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1556321c
    [Tags]      Tvh1556321c  SEC-PRV-ERASE  reset
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Users Add User  ${USER_NAME}  ${USERS_PII_INFORMATION}  ${PASSWORD}  ${USER_ROLE}
    Commit Changes

    ${data_cfg}=  Run On Dut  cat ${SYSTEM_USERS_PATH}
    Log  ${data_cfg}
    Should Contain  ${data_cfg}  ${USERS_PII_INFORMATION}

    Users Delete User  ${USER_NAME}
    Commit Changes
 
    ${data_cfg}=  Run On Dut  cat ${SYSTEM_USERS_PATH}
    Log  ${data_cfg}
    Should Not Contain  ${data_cfg}  ${USERS_PII_INFORMATION}

Tvh1556322c
    [Documentation]  Verify PII data in sma are deleted after reset configuration. \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1556322c
    [Tags]      Tvh1556322c  SEC-PRV-ERASE  reset
    [Setup]     DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Users Add User  ${USER_NAME}  ${USERS_PII_INFORMATION}  ${PASSWORD}  ${USER_ROLE}
    Alerts Add Recipient  ${ALERTS_PII_INFORMATION}  all-all
    Commit Changes

    ${users_data_cfg}=  Run On Dut  cat ${SYSTEM_USERS_PATH}
    Log  ${users_data_cfg}
    Should Contain  ${users_data_cfg}  ${USERS_PII_INFORMATION}

    ${alerts_data_cfg}=  Run On Dut  cat ${SYSTEM_ALERTS_PATH}
    Log  ${alerts_data_cfg}
    Should Contain  ${alerts_data_cfg}  ${ALERTS_PII_INFORMATION}

    Suspend
    Reset Config
    Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_SSW_PASSWORD}

    ${users_data_cfg}=  Run On Dut  cat ${SYSTEM_USERS_PATH}
    Log  ${users_data_cfg}
    Should Not Contain  ${users_data_cfg}  ${USERS_PII_INFORMATION}

    ${alerts_data_cfg}=  Run On Dut  cat ${SYSTEM_ALERTS_PATH}
    Log  ${alerts_data_cfg}
    Should Not Contain  ${alerts_data_cfg}  ${ALERTS_PII_INFORMATION}