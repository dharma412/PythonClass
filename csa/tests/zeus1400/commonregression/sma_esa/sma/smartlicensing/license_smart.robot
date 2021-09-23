# $Id: //prod/main/sarf_centos/tests/zeus1350/license_smart/license_smart.txt#4 $
# $DateTime: 2020/05/03 10:24:33 $
# $Author: sumitada $

*** Settings ***
Resource     sma/global_sma.txt
Resource     esa/logs_parsing_snippets.txt
Resource     regression.txt
Resource     licensesmart_common.robot

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Set Appliance Under Test to SMA
...  Initialize Suite
Suite Teardown  Run Keywords
...  Finalize Suite

*** Variables ***
##REGULAR_TOKEN_ID will expire on 23rd July 2019
## Make sure that all the licenses available in the CSSM Portal
${INVALID_TOKEN_ID}=  InvalidTokenInvalidTokenInvalidTokenInvalidTokenInvalidTokenInvalidTokenInvalidTokenInvalidTokenInvalidTokenInvalidTokenInvalidTokenInvalid
${REVOKED_TOKEN_ID}=  MzgxMDM3NTEtYjcxMC00NzA4LTkwYTgtNWI0NmMyMzMzNTJlLTE1NjQwNDY5%0ANzUyMTJ8WVoxYzU3NklOM1hnY0libHg1dkVBSmZscE5mUkRMbktPcmErMVZj%0AUitPWT0%3D%0A
${EXPIRED_TOKEN_ID}=  MGViNDcxNDYtYTk2Ni00OGY1LTg0ZjUtMWJlZDRiOGRhMzAxLTE1MzI1OTc0%0AMjUyMzR8cUxSVWwrQjNybG1jdTRVZEI5YTJ2c3FPTnJUbHNJUW1tYS8wZmNt%0ATDNoWT0%3D%0A
${TC_FILTERED_SENTENCE}=  crime
${TC_FILTER_NAME}=  smart
${TG_GATEWAY_URL}=  http://gateway.com
${TG_GATEWAY_MODE}=  transport gateway / smart software manager satellite

*** Keywords ***
Initialize Suite
    global_sma.DefaultTestSuiteSetup
    Selenium Login
    Roll Over Now  smartlicense
    # Enable Smart License if not enabled
    Run Keyword If  ${USE_SMART_LICENSE} == 1
    ...  Enable Smart License

    Run Keyword and Expect Error
    ...  *Smart License has been enabled*
    ...  FeatureKeyConfig Setup    autoactivate=no

    Setup Existing User
    Null Smtpd Start

Setup Existing User
    ${summary_status}=  License Smart Summary
    Log  ${summary_status}

    #Returns -1 when no entitlements available for activation
    ${entl_list_rel}=  License Smart Get Releasesmart License List
    Log  ${entl_list_rel}

    Run Keyword If  ${entl_list_rel} != -1
    ...  Release All Entitlements

    # Request any 1 license
    @{setup_request_license}  Create List
    ...  Content Security Management Web Reporting

    Request Entitlements  @{setup_request_license}
    Set Suite Variable  @{setup_request_license}

Finalize Suite
    Null Smtpd Stop
    DefaultTestSuiteTeardown

Initialize Testcase
    DefaultTestCaseSetup
    # Enable Smart License if it is not enabled
    Enable Smart License
    # Set the URL to Direct mode
    ${mode}=  Get Smart License Transport Details  transport settings
    Run Keyword If  '${mode}'!='direct'
    ...  License Smart Url  Direct
    Commit
    Roll Over Now  smartlicense

Finalize Testcase
    DefaultTestCaseTeardown

Finalize Tvh1233779c
    Deregister DUT From SSM
    Finalize Testcase If Failed
    DefaultTestCaseTeardown

Finalize Tvh1233795c
    Finalize Testcase If Failed
    DefaultTestCaseTeardown

Finalize Testcase If Failed
    Run Keyword If Test Failed  Handle Failed Test

Handle Failed Test
    Suspend
    Reset Config
    Run Keyword And Ignore Error
    ...  Start CLI Session If Not Open
    Close All Browsers
    Configure SSL For GUI
    Selenium Close
    Selenium Login

Get Smart License Transport Details
    [Arguments]  ${mode_or_url}
    ${status}=  License Smart Status
    Log  ${status}
    ${transport_detail}=  Get From Dictionary  ${status}  ${mode_or_url}
    [Return]  ${transport_detail}

Get Smart License Transport Details From UI
    [Arguments]  ${mode_or_url}

    {status_details}=  Smart License Get Status Details
    Log  ${status_details}
    ${transport_setting_details}=  Get From Dictionary
    ...  ${status_details}  Transport Settings
    [Return]  ${transport_setting_detail}

Process Should Not Be Terminated
    [Arguments]  ${process_name}
    ${output}=  Run On DUT
    ...  ps -axww | grep -v grep | grep ${process_name} | awk '{print $3}'
    # Check status of the process
    Should Not Contain  ${output}  T

Finalize Tvh1251686c
    Tracking Config Disable
    Deregister DUT From SSM
    Finalize Testcase If Failed
    DefaultTestCaseTeardown

Finalize Tvh1233790c
    Deregister DUT From SSM
    Finalize Testcase If Failed
    DefaultTestCaseTeardown

Wait Until SL Operation Is Complete
    @{menu_option}  Create List
    ...  URL
    Wait Until Keyword Succeeds  5 min  30 sec
    ...  Verify Menu Items Under License Smart Exists  1  @{menu_option}
    Selenium Close
    Selenium Login

Get Last Renewal Attempt
    [Arguments]  ${auth_reg}
    ${last_renewal_attempt_type}=  Set Variable If  '${auth_reg.lower()}'=='auth'
    ...  last authorization renewal attempt date
    ...  last registration renewal attempt date

    ${status}=  License Smart Status
    Log  ${status}
    ${last_renewal_attempt_date}=  Get From Dictionary  ${status}  ${last_renewal_attempt_type}
    [Return]  ${last_renewal_attempt_date}

Get Last Renewal Attempt From UI
    [Arguments]  ${auth_reg}
    ${last_renewal_attempt_type}=  Set Variable If  '${auth_reg.lower()}'=='auth'
    ...  Last Authorization Renewal Date
    ...  Last Registration Renewal Date

    ${status_details}=  Smart License Get Status Details
    ${last_renewal_attempt_date}=  Get From Dictionary
    ...  ${status_details}  ${last_renewal_attempt_type}
    [Return]  ${last_renewal_attempt_date}

Verify Logs For Request And Release Licenses
    [Arguments]  ${log_message}  @{licenses_list}

    @{sma_log}=  Create List
    :FOR  ${license}  IN  @{licenses_list}
    \  Append To List  ${sma_log}  .*${license} license ${log_message}.*

    :FOR  ${log_pattern}  IN  @{sma_log}
    \  Verify And Wait For Log Records
    \  ...  search_path=smartlicense
    \  ...  wait_time=600 seconds
    \  ...  retry_time=10 seconds
    \  ...  ${log_pattern}>=1

Verify Authorization State Of Licenses
    [Arguments]  ${expected_license_auth_state}  @{licenses}

    Log Many  @{licenses}
    :FOR  ${license}  IN  @{licenses}
    \  Wait Until Keyword Succeeds  1 min  50 sec
    \  ...  Retry License State In Progress  ${license}
    \  ${license_state}  Get Entitlement State From Summary  ${license}
    \  ${actual_license_auth_state}=  Get From Dictionary  ${license_state}  ${license}
    \  Should Be Equal As Strings  ${expected_license_auth_state}  ${actual_license_auth_state}

Verify Authorization State Of Licenses From UI
    [Arguments]  ${expected_license_auth_state}  @{licenses}

    Log Many  @{licenses}
    :FOR  ${license}  IN  @{licenses}
    \  Wait Until Keyword Succeeds  1 min  50 sec
    \  ...  Retry License State In Progress  ${license}
    \  ${details}=  Smart License Get License Details
    \  ${actual_license_auth_state}=  Get From Dictionary  ${details}  ${license}
    \  Should Be Equal As Strings  ${expected_license_auth_state}  ${actual_license_auth_state}

Register DUT With SSM From UI

    @{arguments}=  Create List  token_id=${SL_TOKEN_ID}
    ...  force_register_flag=${False}
    Smart License Register  @{arguments}

    Verify And Wait For Log Records
    ...  wait_time=240 seconds
    ...  retry_time=10 seconds
    ...  search_path=smartlicense
    ...  .*The product is registered successfully.*>=1

    Wait Until SL Operation Is Complete

    ${status_details}=  Smart License Get Status Details
    ${reg_status}=  Get From Dictionary
    ...  ${status_details}  Registration Status

    Should Be Equal As Strings  ${reg_status}
    ...  Registered

    Verify And Wait For Log Records
    ...  wait_time=240 seconds
    ...  retry_time=10 seconds
    ...  search_path=smartlicense
    ...  .*Renew authorization of the product with Smart Software Manager is successful.* >=1

Deregister DUT From UI
    @{arguments}=  Create List  sl_action=Deregister
    Smart License Perform Action
    ...  @{arguments}

    ${details}=  Smart License Get Status Details
    ${reg_status}=  Get From Dictionary
    ...  ${details}  Registration Status
    Should Be Equal As Strings  ${reg_status}  Unregistered

*** Test Cases ***

Tvh1233748c
    [Documentation]  Verify 'URL' can be configured:
    ...  Direct and Transport Gateway\n
    ...  Tvh1233748c-Configure Transport setup\n
    ...  Tvh1233771c-Configure Transport setup - Transport Gateway\n
    ...  Tvh1251687c-Configure Transport setup -
    ...  Transport Gateway - invalid/empty\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233748\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233771\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1251687
    [Tags]   Tvh1233748c  Tvh1233771c  Tvh1251687c  srts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Testcase
    Set Test Variable  ${TEST_ID}  Tvh1233748c

    ${mode}=  Get Smart License Transport Details  transport settings
    Should Be Equal As Strings  ${mode}  direct

    # Configure invalid transport gateway
    Run Keyword And Expect Error
    ...  *Entered Invalid Gateway URL*
    ...  License Smart Url  transport_gateway  gateway

    Run Keyword And Expect Error
    ...  *Entered Invalid Gateway URL*
    ...  License Smart Url  transport_gateway  ${EMPTY}

    Roll Over Now  smartlicense

    # Configure transport gateway
    License Smart Url  transport_gateway  ${TG_GATEWAY_URL}
    Commit
    Verify And Wait For Log Records
    ...  search_path=smartlicense
    ...  wait_time=300 seconds
    ...  retry_time=30 seconds
    ...  .*transport settings is successful to transport_gateway option.* >= 1

    ${url}=  Get Smart License Transport Details  transport_url
    ${mode}=  Get Smart License Transport Details  transport settings

    Should Be Equal As Strings  ${mode}  ${TG_GATEWAY_MODE}
    Should Be Equal As Strings  ${url}  ${TG_GATEWAY_URL}

    # Configure direct url
    License Smart Url  direct
    Commit

    Verify And Wait For Log Records
    ...  search_path=smartlicense
    ...  wait_time=300 seconds
    ...  retry_time=60 seconds
    ...  .*transport settings is successful to direct option.* >= 1

    ${mode}=  Get Smart License Transport Details  transport settings
    Should Be Equal As Strings  ${mode}  direct

Tvh1233757c
    [Documentation]   Merged multiple test cases\n
    ...  a) Requests multiple licenses in eval mode and verifies
    ...     Eval mode is started\n
    ...  b) Verifes the logs for license activation and summary
    ...     output for correct authorization state\n
    ...  c) Registers DUT with SSM and verifies
    ...     authorization state of all the licenses\n
    ...     License state should change from
    ...     Eval to proper authoriziation state \n
    ...  d) Releases the license in registered mode\n
    ...  e) Deregisters the DUT from SSM, verifies the license
    ...     authorization state changes to Eval.\n
    ...  Tvh1233757c-Device Registration- Evaluation period
    ...  is on - In Direct Mode\n
    ...  Tvh1233759c-Activate  Multiple entitlements - Authorized\n
    ...  Tvh1233761c-Display entitlements with status\n
    ...  Tvh1233762c-Deactivate entitlement\n
    ...  Tvh1233752c-Activate entitlement when Registration Status
    ...  is "Unregistered" and Evaluation period is on and then register\n
    ...  Tvh1233751c-Activate multiple entitlements when Registration Status
    ...  is "Unregistered" - Evaluation Period On\n
    ...  Tvh1233752c-Activate multiple entitlements when Registration Status
    ...  is "Unregistered" and Evaluation period is on and then
    ...  register\n
    ...  Tvh1233764c-Device Deregistration - Evaluation period is not
    ...    yet expired and De-register releases licenses\n
    ...  Tvh1233760c-Verify  smart agent Status output - all fields and
    ...   values are correct\n
    ...  Tvh1238088c-Evaluation  - count down continues only when atleaset
    ...   one license is in Requested state\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233757\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233759\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233761\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233762\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233752\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233751\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233752\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233764\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233760\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1238088\n

    [Tags]  Tvh1233757c  Tvh1233759c   Tvh1233761c  Tvh1233762c  Tvh1233752c  Tvh1233751c  Tvh1233752c  Tvh1233764c  Tvh1233760c  Tvh1238088c  srts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Tvh1233795c
    Set Test Variable  ${TEST_ID}  Tvh1233757c

    @{request_licenses_list}  Create List
     ...  Content Security Management Config Manager
     ...  Content Security Management Master ISQ

    # Request 2 licenses and verify the logs
    Request Entitlements  @{request_licenses_list}

    Verify Logs For Request And Release Licenses
    ...  in eval mode is requested successfully on the appliance
    ...  @{request_licenses_list}

    Verify Authorization State Of Licenses
    ...  Eval
    ...  @{request_licenses_list}

    # Verify eval mode should be on
    ${eval_usage}  ${eval_period}  Get Smart License Evaluation Period
    Should Be Equal As Strings  ${eval_usage}  in use

    # Register the DUT, verify status of the requested license
    Wait Until Keyword Succeeds  5 min  30 sec
    ...  Register DUT With SSM

    Verify And Wait For Log Records
    ...  wait_time=240 seconds
    ...  retry_time=10 seconds
    ...  search_path=smartlicense
    ...  .*Renew authorization of the product with Smart Software Manager is successful.* >=1

    Verify Logs For Request And Release Licenses
    ...  has been moved to In Compliance successfully
    ...  @{request_licenses_list}

    Verify Authorization State Of Licenses
    ...  In Compliance
    ...  @{request_licenses_list}

    # Release 1 license
    @{release_licenses_list}  Create List
    ...  Content Security Management Config Manager

    Release Entitlements  @{release_licenses_list}

    Verify And Wait For Log Records
    ...  wait_time=240 seconds
    ...  retry_time=10 seconds
    ...  search_path=smartlicense
    ...  .*Renew authorization of the product with Smart Software Manager is successful.* >=1

    Verify Logs For Request And Release Licenses
    ...  is released successfully from the appliance
    ...  @{release_licenses_list}

    Verify Authorization State Of Licenses
    ...  Not requested
    ...  @{release_licenses_list}

    # Deregister the DUT, verify status of the requested license
    # It should be in "Eval" state
    Deregister DUT From SSM

    @{release_licenses_list}  Create List
     ...  Content Security Management Master ISQ

    Verify Logs For Request And Release Licenses
    ...  in eval mode is requested successfully on the appliance
    ...  @{release_licenses_list}

    Verify Authorization State Of Licenses
    ...  Eval
    ...  @{release_licenses_list}

    # Release remaining 1 license
    Release Entitlements  @{release_licenses_list}
    Verify Logs For Request And Release Licenses
    ...  is released successfully from the appliance
    ...  @{release_licenses_list}

    Verify Authorization State Of Licenses
    ...  Not requested
    ...  @{release_licenses_list}

    ## Eval period is in use as 1 license is still requested
    ${summary_status}=  License Smart Summary
    Log  ${summary_status}
    ${eval_usage}  ${eval_period}  Get Smart License Evaluation Period
    Should Be Equal As Strings  ${eval_usage}  in use

    Release Entitlements  @{setup_request_license}
    Verify Logs For Request And Release Licenses
    ...  is released successfully from the appliance
    ...  @{setup_request_license}

    ## All licenses are released, but eval mode will be in use
    ##as product based licenses will be still in requested state
    ${summary_status}=  License Smart Summary
    Log  ${summary_status}
    ${eval_usage}  ${eval_period}  Get Smart License Evaluation Period
    Should Be Equal As Strings  ${eval_usage}  in use

Tvh1233790c
    [Documentation]  Tvh1233790c- Saveconfig/loadconfig - Loading a config
    ...  which is saved after enabling SL after registration\n
    ...  Tvh1233791c-Saveconfig/loadconfig - Loading a config which
    ...  is saved after enabling SL, activating entitlements\n
    ...  Tvh1233768c- Deactivate multiple entitlements\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233790\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233791\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233768
    [Tags]  Tvh1233790c  Tvh1233791c  Tvh1233768c  srts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Tvh1233790c

    Set Test Variable  ${TEST_ID}  Tvh1233790c

    @{licenses_list}  Create List
    ...  Content Security Management Config Manager
    ...  Content Security Management Master ISQ

    #Request 2 licenses and verify the logs
    Request Entitlements  @{licenses_list}

    Verify Logs For Request And Release Licenses
    ...  in eval mode is requested successfully on the appliance
    ...  @{licenses_list}

    Verify Authorization State Of Licenses
    ...  Eval
    ...  @{licenses_list}

    # Register the DUT
    Wait Until Keyword Succeeds  5 min  30 sec
    ...  Register DUT With SSM
	
    Set Appliance Under Test to SMA
    Selenium Login
    ${conf}=  Configuration File Save Config  mask_passwd=${False}

    # Load the configuration which was saved
    Configuration File Load Config  ${conf}
    Commit Changes

    # Verify that save/load config , has no impact on
    # Smart licensing,registration and licenses states
    Verify Registration Status On Appliance  registered

    Verify Authorization State Of Licenses
    ...  In Compliance
    ...  @{licenses_list}

    #Release licenses
    Release Entitlements  @{licenses_list}
    Verify Logs For Request And Release Licenses
    ...  is released successfully from the appliance
    ...  @{licenses_list}

    Verify Authorization State Of Licenses
    ...  Not requested
    ...  @{licenses_list}

Tvh1251686c
    [Documentation]  Tvh1251686c-Post smartagent process
    ...  restart smartlicense is activated automatically\n
    ...  Tvh1251685c-Restart smart agent process -
    ...  Features are not impacted\n
    ...  Tvh1238532c-Restart smart agent process -
    ...  Verify Smart license status\n
    ...  Tvh1238538c-Enable feature when the corresponding
    ...  entitlement is not activated\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1251686\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1251685\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1238532\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1238538

    [Tags]  Tvh1251686c  Tvh1251685c  Tvh1238532c  Tvh1238538c  erts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Tvh1251686c

    Set Test Variable  ${TEST_ID}  Tvh1251686c

    Wait Until Keyword Succeeds  5m  30s
    ...  Register DUT With SSM

    @{licenses_list}  Create List
    ...  Content Security Management Centralized Tracking

    #Request 2 licenses
    Request Entitlements  @{licenses_list}

    Verify Logs For Request And Release Licenses
    ...  has been moved to In Compliance successfully
    ...  @{licenses_list}

    Verify Authorization State Of Licenses
    ...  In Compliance
    ...  @{licenses_list}
	
    Restart CLI Session
    Tracking Config Enable

    #Restart smart_agent
    Run On DUT  /data/bin/heimdall_svc -r smart_agent

    ${daemon_name}=  Set Variable  smart_agent
    # Wait till process is up and running
    Wait Until Keyword Succeeds  10 min  30 sec
    ...  Verify If Smart Agent Process Is Ready

    # Verify SL is enabled after agent restart
    Verify Smart License Status Enabled

    # Verify registration status is intact
    Verify Registration Status On Appliance  registered

    #Verify license status
    Verify Authorization State Of Licenses
    ...  In Compliance
    ...  @{licenses_list}

    Release Entitlements  @{licenses_list}
    Verify Logs For Request And Release Licenses
    ...  is released successfully from the appliance
    ...  @{licenses_list}

    Verify Authorization State Of Licenses
    ...  Not requested
    ...  @{licenses_list}

    #After releasing license checking if feature is disabled
    Navigate To  Management Appliance   Centralized Services  Centralized Message Tracking
    ${result}=  Get Text  xpath=//*[@id='page_title']
    Should Contain  ${result}  License Unavailable

Tvh1233786c
    [Documentation]  Tvh1233786c-Verify forceful manual update of
    ...  smart_agent-After SL enable\n
    ...  Tvh1233749c-Show smart license agent version\n
    ...  Tvh1251688c-smart agent update testing on virtual SMA\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233786\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233749\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1251688
    [Tags]  Tvh1233786c  Tvh1233749c  Tvh1251688c  erts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Testcase
    Set Test Variable  ${TEST_ID}  Tvh1233786c
    Update Config Dynamic Host  dynamic_host=${IBQA_UPDATER}
    Update Config Validate Certificates  validate_certificates=No
    Commit
    Roll Over Now  updater_logs
    License Smart Agent Update  force=${True}
    ${status}  ${value}=  Run Keyword And Ignore Error
    ...  Verify And Wait For Log Records
    ...  search_path=updater
    ...  wait_time=500
    ...  smart license is up to date >= 1

    Run Keyword If  '${status}' == 'FAIL'  Verify And Wait For Log Records
    ...  search_path=updater
    ...  wait_time=500
    ...  smart_agent update completed >= 1
    Wait Until Keyword Succeeds  5 min  30 sec
    ...  Verify If Smart Agent Process Is Ready

    ${res}=  License Smart Agent Status
    Log Dictionary  ${res}
    ${last_update}  Get From Dictionary  ${res}  Last Updated
    Run Keyword If  '${status}' == 'FAIL'
    ...  Should Not Be Equal As Strings  ${last_update}  Never updated

Tvh1233796c
    [Documentation]  Tvh1233796c-Register with invalid idtoken\n
    ...  Tvh1233797c-Register using revoked token\n
    ...  Tvh1238534c-Register- Using 'Expired' token idRegister without token\n
    ...  Tvh1233795c-SMA-Register without idtoken\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233796\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233797\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1238534\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233795
    [Tags]  Tvh1233796c  Tvh1233797c  Tvh1238534c  Tvh1233795c  srts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Tvh1233795c
    Set Test Variable  ${TEST_ID}  Tvh1233796c

    @{menu_option}  Create List
    ...  DEREGISTER

    @{reg_token_data}=  Create List
    ...  revoked_token_id     ${REVOKED_TOKEN_ID}
    ...  expired_token_id     ${EXPIRED_TOKEN_ID}
    ...  invalid_token_id     ${INVALID_TOKEN_ID}

    :FOR  ${token_type_desc}  ${token_id}  IN  @{reg_token_data}
    \  Log  ${token_type_desc}
    \  Roll Over Now  smartlicense
    \  Sleep  3s  reason=Wait for log rollover
    \  Wait Until Keyword Succeeds  3 min  30 sec
    \  ...  License Smart Register  token=${token_id}  reregister=yes
    \  Wait Until Keyword Succeeds  3 min  30 sec
    \  ...  Verify Menu Items Under License Smart Exists  0  @{menu_option}
    \  Verify And Wait For Log Records
    \  ...  search_path=smartlicense
    \  ...  wait_time=120 seconds
    \  ...  retry_time=30 seconds
    \  ...  .*registration of the product with Smart Software Manager failed.* >= 1

    #Try to register without any token
    Run Keyword And Expect Error  *Token cannot be empty*
    ...  License Smart Register  token=${EMPTY}  reregister=yes

Tvh1251689c
    [Documentation]  Tvh1251689c - UI : Verify transport_setup works as expected
    ...   after SL enable\n
    ...  Tvh1251684c - UI : Register- Using 'Expired' token id\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1251689\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1251684
    [Tags]  Tvh1251689c  Tvh1251684c  srts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Testcase

    Set Test Variable  ${TEST_ID}  Tvh1251689c
    @{arguments}=  Create List  transport_settings=transport_gateway
    ...  url=https://example.com:1234

    Smart License Configure URL  @{arguments}
    Commit Changes

    ${details}=  Smart License Get Status Details
    ${transport_settings}=  Get From Dictionary
    ...  ${details}  Transport Settings
    Should Be Equal As Strings  ${transport_settings}
    ...  Transport Gateway / Smart Software Manager Satellite

    @{arguments}=  Create List  transport_settings=direct
    Smart License Configure URL  @{arguments}
    Commit Changes

    ${details}=  Smart License Get Status Details
    ${transport_settings}=  Get From Dictionary
    ...  ${details}  Transport Settings
    Should Be Equal As Strings  ${transport_settings}
    ...  Direct

    @{menu_option}  Create List
    ...  DEREGISTER

    @{arguments}=  Create List  token_id=${EXPIRED_TOKEN_ID}
    ...  force_register_flag=${False}
    Roll Over Now  smartlicense
    Sleep  3s  reason=Wait for log rollover
    Wait Until Keyword Succeeds  3 min  30 sec
    ...  Smart License Register  @{arguments}
    Wait Until Keyword Succeeds  3 min  30 sec
    ...  Verify Menu Items Under License Smart Exists  0  @{menu_option}
    Verify And Wait For Log Records
    ...  search_path=smartlicense
    ...  wait_time=120 seconds
    ...  retry_time=30 seconds
    ...  .*registration of the product with Smart Software Manager failed.* >= 1

Tvh1233814c
    [Documentation]   Merged multiple UI test cases\n
    ...  Tvh1233814c-UI: Verify Request, Release License works
    ...  as expected in eval mode\n
    ...  Tvh1233809c-UI: Verify Register works as expected\n
    ...  Tvh1233816c-UI: Verify Request, Release License works
    ...   as expected after registration\n
    ...  Tvh1251690c-UI: Display entitlements with status\n
    ...  Tvh1233811c-UI: Verify Deregister works as expected\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233814\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233809\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233816\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1251690\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233811\n
    [Tags]  Tvh1233814c  Tvh1233809c  Tvh1233816c  Tvh1251690c  Tvh1233811c  srts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Testcase
    Set Test Variable  ${TEST_ID}  Tvh1233814c

    #### Request licenses in Eval mode
    ${summary}=  License Smart Summary
    Log  ${summary}

    @{request_licenses_list_eval}  Create List
     ...  Content Security Management Config Manager
     ...  Content Security Management Master ISQ

    # Request 3 licenses in eval mode and verify the logs
    Smart License Request Licenses  ${request_licenses_list_eval}

    Verify Logs For Request And Release Licenses
    ...  in eval mode is requested successfully on the appliance
    ...  @{request_licenses_list_eval}

    Verify Authorization State Of Licenses From UI
    ...  Eval
    ...  @{request_licenses_list_eval}

    # Verify eval mode should be on
    ${status_details}=  Smart License Get Status Details
    ${eval_period}=  Get From Dictionary
    ...  ${status_details}
    ...  Evaluation Period
    Should Be Equal As Strings  ${eval_period}  In Use

    #### Release licenses in Eval mode
    @{release_licenses_list_eval}  Create List
     ...  Content Security Management Master ISQ

    Smart License Release Licenses  ${release_licenses_list_eval}

    Verify Logs For Request And Release Licenses
    ...  is released successfully from the appliance
    ...  @{release_licenses_list_eval}

    Verify Authorization State Of Licenses From UI
    ...  Not requested
    ...  @{release_licenses_list_eval}

    #### Register DUT with SSM
    # Register the DUT, verify status of the requested license
    Wait Until Keyword Succeeds  15 min  30 sec
    ...  Register DUT With SSM From UI

    @{licenses_list_eval_to_reg}  Create List
     ...  Content Security Management Config Manager

    Verify Logs For Request And Release Licenses
    ...  has been moved to In Compliance successfully
    ...  @{licenses_list_eval_to_reg}

    Verify Authorization State Of Licenses From UI
    ...  In Compliance
    ...  @{licenses_list_eval_to_reg}

    #### Request license after registration
    # Request 2 licenses and verify the logs
    @{request_licenses_list_reg}  Create List
     ...  Content Security Management Centralized Tracking
     ...  Content Security Management Centralized Reporting

    Smart License Request Licenses  ${request_licenses_list_reg}

    Verify Logs For Request And Release Licenses
    ...  has been moved to In Compliance successfully
    ...  @{request_licenses_list_reg}

    Verify Authorization State Of Licenses From UI
    ...  In Compliance
    ...  @{request_licenses_list_reg}

    #### Release 2 licenses after registration
    @{release_licenses_list_reg}  Create List
     ...  Content Security Management Config Manager

    Smart License Release Licenses  ${release_licenses_list_reg}
    Verify And Wait For Log Records
    ...  wait_time=240 seconds
    ...  retry_time=10 seconds
    ...  search_path=smartlicense
    ...  .*Renew authorization of the product with Smart Software Manager is successful.* >=1

    Verify Logs For Request And Release Licenses
    ...  is released successfully from the appliance
    ...  @{release_licenses_list_reg}

    Verify Authorization State Of Licenses From UI
    ...  Not requested
    ...  @{release_licenses_list_reg}

    #### Deregister the DUT, verify status of the requested license
    # It should be in "Eval" state
    Deregister DUT From UI

    @{release_licenses_list_dereg}  Create List
     ...  Content Security Management Centralized Tracking
     ...  Content Security Management Centralized Reporting

    Verify Logs For Request And Release Licenses
    ...  in eval mode is requested successfully on the appliance
    ...  @{release_licenses_list_dereg}

    Verify Authorization State Of Licenses From UI
    ...  Eval
    ...  @{release_licenses_list_dereg}

    # Release remaining  licenses
    Release Entitlements  @{release_licenses_list_dereg}
    Verify Logs For Request And Release Licenses
    ...  is released successfully from the appliance
    ...  @{release_licenses_list_dereg}

    Verify Authorization State Of Licenses From UI
    ...  Not requested
    ...  @{release_licenses_list_dereg}

Tvh1233810c
    [Documentation]  Tvh1233810c - UI: Verify Re-register works as expected\n
    ...  Tvh1233813c - UI: Verify auth renew works as expected\n
    ...  Tvh1233812c - UI: Verify idcert renew works as expected\n
    ...  Tvh1233819c - UI: Verify status output is as expected in
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233810\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233813\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233812\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233819\n
    [Tags]  Tvh1233810c  Tvh1233813c  Tvh1233812c  Tvh1233819c  srts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Testcase
    Set Test Variable  ${TEST_ID}  Tvh1233810c

    ## Register DUT with SSM
    # Register the DUT, verify status of the requested license
    Wait Until Keyword Succeeds  10 min  30 sec
    ...  Register DUT With SSM From UI

    ####Reregister DUT with SSM
    @{arguments}=  Create List  sl_action=Reregister
    ...  token_id=${SL_TOKEN_ID}
    Smart License Perform Action  @{arguments}

    Verify And Wait For Log Records
    ...  wait_time=240 seconds
    ...  retry_time=10 seconds
    ...  search_path=smartlicense
    ...  .*The product is registered successfully.*>=1

    Wait Until SL Operation Is Complete

    ${status_details}=  Smart License Get Status Details
    ${reg_status}=  Get From Dictionary
     ...  ${status_details}  Registration Status
    Should Be Equal As Strings  ${reg_status}  Registered

    ${last_auth_renewal_date1}=  Get Last Renewal Attempt From UI  Auth
    Log  ${last_auth_renewal_date1}

    @{arguments}=  Create List  sl_action=Renew Authorization Now
    Smart License Perform Action  @{arguments}

    ${last_auth_renewal_date2}=  Get Last Renewal Attempt From UI  Auth
    Log  ${last_auth_renewal_date2}

    Should Not Be Equal As Strings
    ...  ${last_auth_renewal_date1}
    ...  ${last_auth_renewal_date2}

    ${last_reg_renewal_date1}=  Get Last Renewal Attempt From UI  Registration
    Log  ${last_reg_renewal_date1}

    @{arguments}=  Create List  sl_action=Renew Certificates Now
    Smart License Perform Action  @{arguments}

    ${last_reg_renewal_date2}=  Get Last Renewal Attempt From UI  Registration
    Log  ${last_reg_renewal_date2}

    Should Not Be Equal As Strings
    ...  ${last_reg_renewal_date1}
    ...  ${last_reg_renewal_date2}

Tvh1233779c
    [Documentation]  Tvh1233779c-Auth-Renew - Manual\n
    ...  Tvh1233780c-idcert-renew - Manual\n
    ...  Tvh1233758c-Device reregistration\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233779\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233780\n
    ...  http://tims.cisco.com/view-entity.cmd?ent=1233758

    [Tags]  Tvh1233779c  Tvh1233780c  Tvh1233758c  srts  smart_license
    [Setup]  Initialize Testcase
    [Teardown]  Finalize Tvh1233779c

    Set Test Variable  ${TEST_ID}  Tvh1233779c

    Wait Until Keyword Succeeds  5 min  30 sec
    ...  Register DUT With SSM

    Roll Over Now  smartlicense

    Wait Until Keyword Succeeds  5 min  30 sec
    ...  Reregister DUT With SSM

    #Testing renew auth
    # Renewauth 1st time
    License Smart Renewauth
    Verify And Wait For Log Records
    ...  search_path=smartlicense
    ...  .*Renew authorization of the product with Smart Software Manager is successful.* >= 1

    Verify Registration Status On Appliance  registered

    ${last_auth1}=  Get Last Renewal Attempt  Auth
    Log  ${last_auth1}

    Roll Over Now  smartlicense

    # Not able to avoid Sleep
    Sleep  60s

    # Renewauth 2nd time
    License Smart Renewauth
    Verify And Wait For Log Records
    ...  search_path=smartlicense
    ...  .*Renew authorization of the product with Smart Software Manager is successful.* >= 1

    # Not able to avoid Sleep
    Sleep  60s

    ${last_auth2}=  Get Last Renewal Attempt  Auth
    Log  ${last_auth2}

    Should Not Be Equal As Strings  ${last_auth1}  ${last_auth2}

    #Testing renew cert
    ${last_renew_cert1}=  Get Last Renewal Attempt  Registration
    Log  ${last_renew_cert1}

    License Smart Renewid

    ${last_renew_cert2}=  Get Last Renewal Attempt  Registration
    Log  ${last_renew_cert2}

    Should Not Be Equal As Strings  ${last_renew_cert1}  ${last_renew_cert2}

