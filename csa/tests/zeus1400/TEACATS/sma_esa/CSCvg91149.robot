*** Settings ***
Resource     sma/global_sma.txt
Resource     regression.txt

Suite Setup  Do Suite Setup
Suite Teardown  DefaultTestSuiteTeardown

*** Keywords ***

Do Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup

*** Test Cases ***

Tvh1157624c
    [Documentation]  Checking ssh keys are not regenerated
    ...     and showlicense are working after upgrade
    ...     http://tims/view-entity.cmd?ent=1157624
    [Tags]  srts  teacat  CSCvg91149  Tvh1157624c
    [Setup]  DefaultTestCaseSetup
    [Teardown]  DefaultTestCaseTeardown

    Set SSHLib Timeout  10 seconds
    Open Connection  ${CLIENT_HOSTNAME}  client
    Login  ${TESTUSER}  ${TESTUSER_PASSWORD}
    Write  ssh ${DUT_ADMIN}@${SMA}
    ${out}=  Read Until Regexp  .*\\(yes\\/no\\)\\?|.*assword\\:
    ${add_to_known_hosts}=  Set Variable If  '${out.find('yes')}' !='-1'  yes  ${EMPTY}
    Run Keyword If  '${add_to_known_hosts}' != '${EMPTY}'  Write  ${add_to_known_hosts}
    Sleep  3s
    ${is_dut_virtual}  Is DUT A Virtual Model
    Set Suite Variable  ${is_dut_virtual}
    Update Config Dynamichost  dynamic_host=${UPDATE_SERVER}
    Update Config Validate Certificates  validate_certificates=No
    Commit
    ${sma_version}=  Get Dut Build
    Upgrade And Wait  ${sma_version}  timeout=1200
    Open Connection  ${CLIENT_HOSTNAME}  client
    Login  ${TESTUSER}  ${TESTUSER_PASSWORD}
    Write  ssh ${DUT_ADMIN}@${SMA}
    ${out}=  Read Until Regexp  .*\\(yes\\/no\\)\\?|.*assword\\:
    Run Keyword If  '${out.find('yes')}' !='-1'  Fail
    Sleep  3s
    Restart CLI Session
    ${license_status}=  Run Keyword If  ${is_dut_virtual} is ${TRUE}
    ...  ShowLicense
    Log  ${license_status}
    Run Keyword If  ${is_dut_virtual} is ${TRUE}
    ...  Should Contain  ${license_status}  license_version
