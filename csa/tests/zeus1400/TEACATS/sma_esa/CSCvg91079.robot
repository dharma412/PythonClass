*** Settings ***
Resource     sma/global_sma.txt
Resource     regression.txt

*** Keywords ***

Test Setup  DefaultTestCaseSetup
Test Teardown  DefaultTestCaseTeardown

*** Test Cases ***

Tvh1157623c
    [Documentation]  Raid_log_watch crashes on startup
    ...  http://tims/view-entity.cmd?ent=1157623
    [Tags]  srts  teacat  CSCvg91079  Tvh1157623c

    Set Appliance Under Test To SMA
    Update Config Dynamichost  dynamic_host=${UPDATE_SERVER}
    Update Config Validate Certificates  validate_certificates=no
    Commit

    ${sma_version}=  Get Dut Build
    Upgrade And Wait  ${sma_version}  timeout=1200
    ${output}=  Run on DUT  echo "test" | /data/bin/raid_log_watch
    Should Not Contain  ${output}  raid_log_watch
    ${output}=  Run on DUT  grep "syslogd" /var/log/messages
    Should Not Contain  ${output}  raid_log_watch
