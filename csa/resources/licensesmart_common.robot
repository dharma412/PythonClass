*** Settings ***
Library    SSHLibrary
Resource    set_sshlib_prompt.txt
Resource    utils.txt

*** Variables ***
${CMD}=  ps auxw | grep -w smart_agent | grep -v grep | awk '{print $2}'
@{imh_bv}  Mail Handling  Email Security Appliance Bounce Verification
@{imh}  Mail Handling

@{esa_complete_entitlement_list}=  Email Security Appliance Outbreak Filters
...  Email Security Appliance Advanced Malware Protection
...  Email Security Appliance Advanced Malware Protection Reputation
...  Email Security Appliance Anti-Spam License
...  Email Security Appliance Cloudmark Anti-Spam
...  Email Security Appliance PXE Encryption
...  Email Security Appliance Image Analyzer
...  Email Security Appliance Intelligent Multi-Scan
...  Email Security Appliance McAfee Anti-Malware
...  Email Security Appliance Graymail Safe-unsubscribe
...  Email Security Appliance Data Loss Prevention
...  Email Security Appliance Sophos Anti-Malware
...  Mail Handling
...  Email Security Appliance Bounce Verification
...  Email Security Appliance External Threat Feeds

@{sma_complete_entitlement_list}=  Content Security Management Config Manager
...  Content Security Management Web Reporting
...  Mail Handling
...  Content Security Management Master ISQ
...  Content Security Management Centralized Tracking
...  Content Security Management Centralized Reporting

@{wsa_complete_entitlement_list}=  Web Security Appliance Cisco Web Usage Controls
...  Web Security Appliance Anti-Virus Webroot
...  Web Security Appliance L4 Traffic Monitor
...  Web Security Appliance Cisco AnyConnect SM for AnyConnect
...  Web Security Appliance Advanced Malware Protection Reputation
...  Web Security Appliance Anti-Virus Sophos
...  Web Security Appliance Web Reputation Filters
...  Web Security Appliance Advanced Malware Protection
...  Web Security Appliance Anti-Virus McAfee
...  Web Security Appliance Web Proxy and DVS Engine
...  Web Security Appliance HTTPs Decryption

*** Keyword ***
Import Global Resource File
    Run Keyword if  '${DUT_TYPE}' == 'ESA'
    ...  Import Resource    esa/global.txt
    Run Keyword if  '${DUT_TYPE}' == 'WSA'
    ...  Import Resource    wsa/global.txt
    Run Keyword if  '${DUT_TYPE}' == 'SMA'
    ...  Import Resource    sma/global_sma.txt

Import Log Resource File
     Run Keyword if  '${DUT_TYPE}' == 'ESA'
     ...  Import Resource    esa/logs_parsing_snippets.txt
     Run Keyword if  '${DUT_TYPE}' == 'WSA'
     ...  Import Resource    wsa/logs_parsing_snippets.txt
     Run Keyword if  '${DUT_TYPE}' == 'SMA'
     ...  Import Resource    esa/logs_parsing_snippets.txt


Entitlement List Dut Type
    @{ent_list}=  Create List
    FOR  ${entl}  IN  @{sma_complete_entitlement_list}
        Run Keyword if  '${DUT_TYPE}' == 'SMA'
        ...  Append To List  ${ent_list}  ${entl}
    END

    FOR  ${ent1}  IN  @{esa_complete_entitlement_list}
        Run Keyword if  '${DUT_TYPE}' == 'ESA'
        ...  Run Keyword if  '${DUT_LIB_VERSION}' >= 'phoebe1210'
        ...  Run Keyword if  '${ent1}' != 'Email Security Appliance Cloudmark Anti-Spam'
        ...  Append To List  ${ent_list}  ${ent1}
        Run Keyword if  '${DUT_TYPE}' == 'ESA'
        ...  Run Keyword if  '${DUT_LIB_VERSION}' < 'phoebe1210'
        ...  Append To List  ${ent_list}  ${ent1}
    END
    FOR  ${ent1}  IN  @{wsa_complete_entitlement_list}
        Run Keyword if  '${DUT_TYPE}' == 'WSA'
        ...  Append To List  ${ent_list}  ${ent1}
    END
    [Return]  ${ent_list}

Verify Smart License Status Enabled
    [Documentation]  Verifies the Smart license status as enabled
    ${status}  License Smart Status
    ${enabled_status}  Get From Dictionary  ${status}  smart licensing status
    Should Be Equal As Strings  ${enabled_status}  enabled

Get Smart Agent Process Id
    [Documentation]  Fetches the smart agent process ID
    ${pid} =  Run On Dut  ${CMD}
    [Return]  ${pid}

Get Smart License Evaluation Period
    [Documentation]  Fetches the evaluation mode from license_smart->status
    ...  command. Returns two values 'Evaluation Period' and 'Evaluation Mode'.
    ${status}  License Smart Status
    ${eval_mode_in_use}  Get From Dictionary  ${status}  evaluation period
    ${eval_period_remaining}  Get From Dictionary  ${status}  evaluation period remaining
    [Return]  ${eval_mode_in_use}  ${eval_period_remaining}

Verify Eval Period Counter Started
    [Documentation]  It verifies that evaluation period has been started
    ...  it should not be equal to 90 days. When evaluation mode is 'in use'
    ${eval_90_days}=  Set Variable  90 days 0 hours 0 minutes 0 seconds
    ${eval_in_use}  ${eval_period}  Get Smart License Evaluation Period
    Should Be Equal As Strings  ${eval_in_use}  in use
    Should Not Be Equal As Strings  ${eval_period}  ${eval_90_days}

Verify Eval Period Counter Not Started
    [Documentation]  Verifies that evaluation period has not been started.
    ...  it should be equal to 90 days.
    ${eval_90_days}=  Set Variable  90 days 0 hours 0 minutes 0 seconds
    ${eval_in_use}  ${eval_period}  Get Smart License Evaluation Period
    Should Be Equal As Strings  ${eval_in_use}  not in use
    Should Be Equal As Strings  ${eval_period}  ${eval_90_days}

Verify Deregistered Successfully
    [Documentation]  1.Gets the entitlement status before and after deregistration
    ...  2.For Physical device logs will not get generated for product based licenses.
    ...  3.For Virtual device logs gets generated for product based licenses.
    ...  4.Removed product based licenses from logs if the device is physical
    ...  5.Post deregistration verifies the log for successful deregistration.
    ...  6.If the status of the device is in eval mode then verifies the log message
    ...  for all entitlements getting activated in eval mode post deregistration.
    ${pre_summary_status}  Remove Product License Keys From License Summary
    @{entl_list_reg_mode}  Get Dictionary Keys  ${pre_summary_status}
    License Smart Deregister

    Run Keyword if  '${DUT_TYPE}' != 'WSA'
    ...  Verify And Wait For Log Records
         ...  wait_time=240 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*The product is deregistered successfully from Smart Software Manager.* >= 1

    Run Keyword if  '${DUT_TYPE}' == 'WSA'
    ...  Verify And Wait For Wsa Log Records
         ...  wait_time=240 seconds
         ...  retry_time=10 seconds
	 ...  search_path=smartlicense
         ...  .*The product is deregistered successfully from Smart Software Manager.* >= 1

    FOR  ${eval_entl}  IN  @{entl_list_reg_mode}
        Run Keyword if  '${DUT_TYPE}' != 'WSA' and '${eval_usage}' == 'in use'
        ...  Verify And Wait For Log Records
             ...  wait_time=240 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  .*${eval_entl} license in eval mode is requested successfully on the appliance.*>=1
    END

    FOR  ${eval_entl}  IN  @{entl_list_reg_mode}
        Run Keyword if  '${DUT_TYPE}' == 'WSA' and '${eval_usage}' == 'in use'
        ...  Verify And Wait For Wsa Log Records
             ...  wait_time=240 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  .*${eval_entl} license in eval mode is requested successfully on the appliance.*>=1
    END

Get Registration Status
    [Documentation]  Gets the registration status details under license_smart->status
    ...  command. Status would be returned as 'REGISTERED' or 'UNREGISTERED'
    ${status}  License Smart Status
    ${reg_val}  Get From Dictionary  ${status}  registration status
    Log  ${reg_val}
    [Return]  ${reg_val}

Get Entitlement State From Summary
    [Documentation]  Fetched the list of entitlement state
    ...  returns dictionary containing entitlement and its state from license_smart->summary
    ...  command.
    [Arguments]  @{entitlement_list}
    ${entitlement_dict}=  Create Dictionary
    ${summary_status}  License Smart Summary
    FOR  ${entl}  IN  @{entitlement_list}
        ${entl_status}  Get From Dictionary  ${summary_status}  ${entl}
        ${entl_state}  Get From Dictionary  ${entl_status}  Status
        Set To Dictionary  ${entitlement_dict}  ${entl}  ${entl_state}
    END
    Log  ${entitlement_dict}
    [Return]  ${entitlement_dict}

Verify Registration Status On Appliance
    [Documentation]  Verifies the registration status. under license_smart->status command.
    ...  should be equal to the status passed as argument.
    [Arguments]  ${reg_status_to_verify}
    ${reg_status}  Get Registration Status
    Should Be Equal As Strings  ${reg_status}  ${reg_status_to_verify}

Verify Product Base License In Eval
    [Documentation]  Verifies product base license based on DUT type is in eval.
    ...  For ESA 'IMH' and 'BV' are the product based licenses.
    ${imh_eval}  Create Dictionary  Mail Handling  Eval
    ${bv_eval}  Create Dictionary  Email Security Appliance Bounce Verification  Eval
    ${entl_status_esa}=  Run Keyword if  '${DUT_TYPE}' == 'ESA'
    ...  Get Entitlement State From Summary  @{imh_bv}
    ${entl_status_sma}=  Run Keyword if  '${DUT_TYPE}' == 'SMA'
    ...  Get Entitlement State From Summary  @{imh}
    Run Keyword if  '${DUT_TYPE}' == 'ESA'
    ...  Dictionary Should Contain Sub Dictionary  ${entl_status_esa}  ${imh_eval}
    Run Keyword if  '${DUT_TYPE}' == 'SMA'
    ...  Dictionary Should Contain Sub Dictionary  ${entl_status_sma}  ${imh_eval}
    Run Keyword if  '${DUT_TYPE}' == 'ESA'
    ...  Dictionary Should Contain Sub Dictionary  ${entl_status_esa}  ${bv_eval}

Verify Menu Items Under License Smart Exists
    [Documentation]  Verifies the list of menu items exists under 'license_smart'.
    ...  command.
    ...    Parameters:
    ...    - ${should_exist}: Pass as 1 if menu item should be listed else pass 0
    ...    - @{menu_items}: Create a list and pass a list of menu items to be checked under license_smart command
    [Arguments]  ${should_exist}  @{menu_items}
    FOR  ${menu}  IN  @{menu_items}
        ${exists}  License Smart Menu Item Check  ${menu}
        Log  ${exists}
        Run Keyword if  ${should_exist} == 1  Should Be True  ${exists}
        Run Keyword if  ${should_exist} == 0  Should Not Be True  ${exists}
    END

Entitlements Not Activated
    [Documentation]  Returns actual list of entitlements listed in 'request_license' command.
    ${status}  License Smart Get License List Available For Request
    [Return]  ${status}

Remove Product License Keys From License Summary
    [Documentation]  Removes product based licenses from license_smart->.
    ...  Summary command. For physical device log message will not be generated.
    ...  for product based licenses.
    ${summary_status}  License Smart Summary
    Run Keyword If  '${DUT_TYPE}' == 'ESA' or 'SMA'
    ...  Remove From Dictionary  ${summary_status}  Mail Handling
    Run Keyword If  '${DUT_TYPE}' == 'ESA'
    ...  Remove From Dictionary  ${summary_status}  Email Security Appliance Bounce Verification
    [Return]  ${summary_status}

Verify If Smart Agent Process Is Ready
    ${output}=  Run On DUT  /data/bin/heimdall_svc status smart_agent
    ${output}=  Evaluate  ${output}
    ${pid}=  Get From Dictionary  ${output}  pid
    ${enabled}=  Get From Dictionary  ${output}  enabled
    ${ready}=  Get From Dictionary  ${output}  ready
    Should Not Be Equal As Strings  ${pid}  -1
    Should Be True  ${enabled}
    Should Be True  ${ready}

Enable Smart License
    [Documentation]  1. Smart license will be enabled if smart agent process.
    ...  is not up.
    ...  2. Once smart license is enabled. Verifies smart agent process should not be
    ...  empty.
    ...  3. Verifies log message once smart license is enabled.
    ...  4. Under license_smart->status. Checks that smartlicense status is 'enabled'.
    ${sa_process_enabled}  Get Smart Agent Process Id
    Set Suite Variable  ${sa_process_enabled}

    @{simulate_new_user}  Create List
    ...  rm -f /var/db/godspeed/features/*.feature
    ...  rm -f /data/db/features/*.feature

    FOR  ${cmds}  IN  @{simulate_new_user}
        Run Keyword if  '${sa_process_enabled}' == '${EMPTY}' and ${SMART_LICENSE_NEW_USER} == 1
        ...  Run On Dut  ${cmds}
    END

    Roll Over Now  smartlicense
    Run Keyword if  '${sa_process_enabled}' == '${EMPTY}'  Run Keywords
    ...  License Smart Enable
    ...  Commit

    #Verifying whether the  smart agent process is up and ready
    Wait Until Keyword Succeeds  5 min  10 sec
    ...  Verify If Smart Agent Process Is Ready

    #Below verifies mail log immediately after enabling smart license.
    Run Keyword if  '${DUT_TYPE}' != 'WSA' and '${sa_process_enabled}' == '${EMPTY}'
    ...  Verify And Wait For Log Records
         ...  wait_time=180 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*Smart Licensing is enabled.* >= 1

    Run Keyword if  '${DUT_TYPE}' == 'WSA' and '${sa_process_enabled}' == '${EMPTY}'
    ...  Verify And Wait For Wsa Log Records
         ...  wait_time=180 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*Smart Licensing is enabled.* >= 1

    #Verifies under license_smart->status. That smartlicense is enabled.
    @{menu_option}  Create List
    ...  STATUS
    Wait Until Keyword Succeeds  3 min  30 sec
    ...  Verify Menu Items Under License Smart Exists  1  @{menu_option}

    Verify Smart License Status Enabled
    ${sa_process_id}  Get Smart Agent Process Id
    Should Not Be Empty  ${sa_process_id}
    @{complete_entitl_list}=  Entitlement List Dut Type

    #No Licenses should be in "Request In Progress" State
    ${status}  ${msg}=  Run Keyword And Ignore Error  Check Entitlement State
    Run Keyword If  '${status}' == 'FAIL'  Check Status And Perform Registeration
    Run Keyword If  '${status}' == 'FAIL'  Check Entitlement State

Check Status And Perform Registeration
    ${registration_status}=  Get Registration Status
    Run Keyword If  '${registration_status}' == 'registered'
    ...  Reregister DUT With SSM
    Run Keyword If  '${registration_status}' == 'unregistered'
    ...  Register DUT With SSM

Check Entitlement State
    @{complete_entitl_list}=  Entitlement List Dut Type
    FOR  ${entitlement}  IN  @{complete_entitl_list}
        Wait Until Keyword Succeeds  3 min  30 sec  Retry License State In Progress  ${entitlement}
    END

Register And Verify Logs
    [Documentation]  Registers and verifies the log message.
    License Smart Register  token=${SL_TOKEN_ID}  reregister=yes
    Run Keyword if  '${DUT_TYPE}' != 'WSA'
    ...  Verify And Wait For Log Records
         ...  wait_time=240 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*The product is registered successfully.*>=1
         ...  .*Renew authorization of the product with Smart Software Manager is successful.* >= 1

    Run Keyword if  '${DUT_TYPE}' == 'WSA'
    ...  Verify And Wait For Wsa Log Records
         ...  wait_time=240 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*The product is registered successfully.*>=1
         ...  .*Renew authorization of the product with Smart Software Manager is successful.* >= 1

Register DUT With SSM
    [Documentation]  Registers device if not registered with smart software manager.
    ...  Verifies the registration log message. Verifies product based licenses
    ...  requested successfully for virtual devices.
    ${registration_status}=  Get Registration Status

    Run Keyword If  '${registration_status}' == 'unregistered' or '${registration_status}' == 'unregistered - registration failed'  Run Keywords
    ...  Register And Verify Logs

    #Giving 5min max for registration. Sometimes registration may take long time.
    Wait Until Keyword Succeeds  5 min  10 sec  Verify Registration Status On Appliance  registered

    #Verifies post register following menu items exists
    @{register_menu_option}=  Create List
    ...  DEREGISTER
    ...  REREGISTER
    Verify Menu Items Under License Smart Exists  1  @{register_menu_option}

Reregister DUT With SSM
    [Documentation]  Reregisters the product with force register option set as 'yes'.

    ${registration_status}=  Get Registration Status
    License Smart Register  token=${SL_TOKEN_ID}  remove_register=yes
    Run Keyword if  '${DUT_TYPE}' != 'WSA'
    ...  Verify And Wait For Log Records
         ...  wait_time=240 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*The product is registered successfully.*>=1

     Run Keyword if  '${DUT_TYPE}' == 'WSA'
     ...  Verify And Wait For Wsa Log Records
          ...  wait_time=240 seconds
          ...  retry_time=10 seconds
          ...  search_path=smartlicense
          ...  .*The product is registered successfully.*>=1

    #Verifies post register following menu items exists
    @{register_menu_option}=  Create List
    ...  DEREGISTER
    ...  REREGISTER
    Verify Menu Items Under License Smart Exists  1  @{register_menu_option}

Deregister DUT From SSM
    [Documentation]  Deregisters the DUT and verifies the Log message.
    ${registration_status}=  Get Registration Status
    Run Keyword If  '${registration_status}' == 'registered'
    ...  License Smart Deregister
    Run Keyword If  '${DUT_TYPE}' != 'WSA' and '${registration_status}' == 'registered'
    ...  Verify And Wait For Log Records
         ...  wait_time=240 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*The product is deregistered successfully from Smart Software Manager.* >= 1

    Run Keyword If  '${DUT_TYPE}' == 'WSA' and '${registration_status}' == 'registered'
    ...  Verify And Wait For Wsa Log Records
         ...  wait_time=240 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*The product is deregistered successfully from Smart Software Manager.* >= 1
    @{deregister_menu_option}=  Create List
    ...  DEREGISTER
    Verify Menu Items Under License Smart Exists  0  @{deregister_menu_option}

Verify All Entitlements Are Activated
    [Documentation]  It verifies that all the entitlements are activated
    ...  successfully. And are present under license_smart -> summary.
    ...  It also checks that no entitlements should be listed under license_smart->
    ...  request license command.

    ${not_requested}=  Set Variable  Not requested
    ${summary_status}  License Smart Summary
    @{complete_entitl_list}=  Entitlement List Dut Type
    FOR  ${entitlement}  IN  @{complete_entitl_list}
        ${entl_state_summary}  Get Entitlement State From Summary  ${entitlement}
        ${entl_state}  Get From Dictionary  ${entl_state_summary}  ${entitlement}
        Should Not Be Equal As Strings  ${not_requested}  ${entl_state}
    END

    #Returns -1 when no entitlements available for activation
    ${entl_not_activated}  Entitlements Not Activated
    Should Be Equal As Integers  ${entl_not_activated}  -1

Enable Smart License On Appliance
    [Documentation]  Following checks are done in this keyword :
    ...    1. Product based licenses should get activated automatically while enabling smartlicense
    ...    for existing user
    ...    2. verifies Classic license CLI's will not be able to execute post SL enable.
    ...    3. If evaluation mode-> in use. Then evaluation period should kick start.
    # Below are the scenarios covered as part of enable smart license keyword.
    #------------------------------------------------------------------------------------------
    #
    #       | Device Type |  User Types |        Eval Period Scenarios verifications           |
    #
    #------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------
    #       | Virtual     |  New        |  release_license & request_license will not be listed|
    #                                   |  Eval mode -> will be 'not in use'                   |
    #-------------------------------------------------------------------------------------------
    #       | Physical    |  Existing   |  Eval Counter starts                                 |
    #-----------------------------------|  Product base license -> In Eval State               |
    #                                   |
    #-------------------------------------------------------------------------------------------
    #       | Virtual     |  Existing   |  Eval Counter starts                                 |
    #-----------------------------------|  Product base license -> In Eval State               |
    #                                   |
    #-------------------------------------------------------------------------------------------
    Import Global Resource File
    Import Log Resource File
    ${is_dut_virtual}=  Is Virtual Machine  vmname=${DUT}

    Enable Smart License

    @{simulate_new_user}  Create List
    ...  rm -f /var/db/godspeed/features/*.feature
    ...  rm -f /data/db/features/*.feature

    FOR  ${cmds}  IN  @{simulate_new_user}
        Run Keyword if  '${sa_process_enabled}' == '${EMPTY}' and ${SMART_LICENSE_NEW_USER} == 1
        ...  Run On Dut  ${cmds}
    END

    #Verifying that classic license CLI's like featureconfig not working
    Run Keyword if  '${DUT_TYPE}' == 'ESA'
    ...  Run Keyword and Expect Error  *Smart License has been enabled. Use license_smart to manage license*  Feature Key List    Dormant

    ${eval_usage}  ${eval_period}  Get Smart License Evaluation Period

    Run Keyword if  ${SMART_LICENSE_NEW_USER} == 0 and '${eval_usage}' == 'in use'
    ...  Wait Until Keyword Succeeds  120 sec  10 sec  Verify Eval Period Counter Started

    @{imh_bv_eval_logs}=  Create List
    ...  .*Mail Handling license in eval mode is requested successfully on the appliance.*
    ...  .*Email Security Appliance Bounce Verification license in eval mode is requested successfully on the appliance.*

    @{imh_eval_logs}=  Create List
    ...  .*Mail Handling license in eval mode is requested successfully on the appliance.*

    #Verifies log message for product based licenses getting activated in SL mode
    #For existing User

    FOR  ${Log}  IN  @{imh_bv_eval_logs}
        Run Keyword if  '${DUT_TYPE}' == 'ESA' and ${SMART_LICENSE_NEW_USER} == 0 and '${sa_process_enabled}' == '${EMPTY}'
        ...  Verify And Wait For Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  ${Log}>=1
    END

    FOR  ${Log}  IN  @{imh_eval_logs}
        Run Keyword if  '${DUT_TYPE}' == 'SMA' and ${SMART_LICENSE_NEW_USER} == 0 and '${sa_process_enabled}' == '${EMPTY}'
        ...  Verify And Wait For Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  ${Log}>=1
    END

    Run Keyword if  ${SMART_LICENSE_NEW_USER} == 0 and '${eval_usage}' == 'in use'
    ...  Verify Product Base License In Eval

    ${registration_status}=  Get Registration Status

    @{vesa_new_user_menu}=  Create List
    ...  REQUESTSMART_LICENSE
    ...  RELEASESMART_LICENSE

    Run Keyword if  ${SMART_LICENSE_NEW_USER} == 1 and '${is_dut_virtual}' == 'True'
    ...  Verify Menu Items Under License Smart Exists  0  @{vesa_new_user_menu}

    Run Keyword if  ${SMART_LICENSE_NEW_USER} == 1
    ...  Should Be Equal As Strings  ${eval_usage}  not in use

Request Entitlements
    [Documentation]  Requests whichever entitlements has been passed .
    [Arguments]  @{entl_list}
    License Smart Request Smart Entitlement  ${entl_list}

Release Entitlements
    [Documentation]  Releases whichever entitlement/entitlements has been passed.
    [Arguments]  @{entl_list}
    License Smart Release Smart Entitlement  ${entl_list}

Retry License State In Progress
    [Documentation]  Entitlement state should not get stuck in 'request in progress'.
    ...  this keyword checks this.
    [Arguments]  ${entl}
    ${entl_state_sum}  Get Entitlement State From Summary  ${entl}
    ${entl_state}  Get From Dictionary  ${entl_state_sum}  ${entl}
    Should Not Be Equal As Strings  ${entl_state}  Request in progress

Retry License State Change
    [Documentation]  Waits untill state entitlement changed to the appropriate
    ...  states.
    [Arguments]  ${entl}  ${entl_state}
    ${entl_state_sum}  Get Entitlement State From Summary  ${entl}
    ${entl_status}  Get From Dictionary  ${entl_state_sum}  ${entl}
    Should Be Equal As Strings  ${entl_status}  ${entl_state}

Request All Entitlements
    [Documentation]  Requests all entitlements only those
    ...  which are available for activation out of the entitlment list passed.
    ...  verifies corresponding mail log and summary for this successfull activation
    ...  Successfully activated entitlements states are checked in summary.
    ...  Product based licenses activation along with other license is checked as part of
    ...  registration.

    ${available_entl_list}  Entitlements Not Activated
    Log  ${available_entl_list}
    @{keys}  Get Dictionary Keys  ${available_entl_list}
    Run Keyword If  '${DUT_TYPE}' == 'ESA'
    ...  List Should Not Contain Value  ${keys}  ${imh_bv}
    Run Keyword If  '${DUT_TYPE}' == 'SMA'
    ...  List Should Not Contain Value  ${keys}  ${imh}
    Request Entitlements   @{keys}
    ${eval_usage}  ${eval_period}  Get Smart License Evaluation Period
    @{eval_log}=  Create List
    FOR  ${enl}  IN  @{keys}
        Append To List  ${eval_log}  .*${enl} license in eval mode is requested successfully on the appliance.*
    END

    FOR  ${eval_entl_logs}  IN  @{eval_log}
        Run Keyword If  '${DUT_TYPE}' != 'WSA' and '${eval_usage}' == 'in use'
        ...  Verify And Wait For Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  ${eval_entl_logs}>=1
    END

    FOR  ${eval_entl_logs}  IN  @{eval_log}
        Run Keyword If  '${DUT_TYPE}' == 'WSA' and '${eval_usage}' == 'in use'
        ...  Verify And Wait For Wsa Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  ${eval_entl_logs}>=1
    END

    @{reg_log}=  Create List
    FOR  ${enl_reg}  IN  @{keys}
        Append To List  ${reg_log}  .*${enl_reg} license has been moved to.*
    END

    FOR  ${reg_entl_logs}  IN  @{reg_log}
        Run Keyword If  '${DUT_TYPE}' != 'WSA' and '${eval_usage}' == 'not in use'
        ...  Verify And Wait For Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  ${reg_entl_logs}>=1
    END

    FOR  ${reg_entl_logs}  IN  @{reg_log}
        Run Keyword If  '${DUT_TYPE}' == 'WSA' and '${eval_usage}' == 'not in use'
        ...  Verify And Wait For Wsa Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  ${reg_entl_logs}>=1
    END

    #Verify product based licenses are activated as part of registration
    @{imh_bv_reg_logs}=  Create List
    ...  .*Mail Handling license has been moved to.*
    ...  .*Email Security Appliance Bounce Verification license has been moved to.*

    FOR  ${prod_reg_logs}  IN  @{imh_bv_reg_logs}
        Run Keyword If  '${DUT_TYPE}' == 'ESA' and '${eval_usage}' == 'not in use'
        ...  Verify And Wait For Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  ${prod_reg_logs}>=1
    END

    Run Keyword If  '${DUT_TYPE}' == 'SMA' and '${eval_usage}' == 'not in use'
    ...  Verify And Wait For Log Records
         ...  wait_time=180 seconds
         ...  retry_time=10 seconds
         ...  search_path=smartlicense
         ...  .*Mail Handling license has been moved to.*>=1

    #Check all the licenses in Summary displayed with proper entitlements states

    @{complete_entitl_list}=  Entitlement List Dut Type
    FOR  ${entitlement}  IN  @{complete_entitl_list}
        Wait Until Keyword Succeeds  1 min  50 sec  Retry License State In Progress  ${entitlement}
    END

    ${summary_status}  License Smart Summary
    FOR  ${entitlement}  IN  @{complete_entitl_list}
        ${entl_state_sum}  Get Entitlement State From Summary  ${entitlement}
        ${entl_state}  Get From Dictionary  ${entl_state_sum}  ${entitlement}
        Run Keyword If  '${eval_usage}' == 'in use'
        ...  Should Be Equal As Strings  Eval  ${entl_state}
        Run Keyword If  '${eval_usage}' == 'not in use'
        ...  Should Not Be Equal As Strings  Eval  ${entl_state}
    END

Release All Entitlements
    [Documentation]  Releases all entitlements on appliance.
    ...  Following are the checks made in this keyword,
    ...  1. Fetches list of entitlements available in release_license
    ...  command.
    ...  2. releases all the entitlements under release_license and verifies the log messages
    ...  for the same.
    ...  3. Released entitlements states should be 'Not requested' under summary command.
    ...  4. If the registration status is unregistered.Verifies
    ...  eval mode should be 'in use' for virtual device. But for physical should be 'not in use'

    #Fetch the list of entitlements available for releasing
    ${entl_list_rel}  License Smart Get Releasesmart License List
    Log  ${entl_list_rel}
    @{release_list}  Get Dictionary Keys  ${entl_list_rel}

    Release Entitlements  @{release_list}

    FOR  ${entitlement}  IN  @{release_list}
        Run Keyword if  '${DUT_TYPE}' != 'WSA'
        ...  Verify And Wait For Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  .*${entitlement} license is released successfully from the appliance.* >= 1
    END

    FOR  ${entitlement}  IN  @{release_list}
        Run Keyword if  '${DUT_TYPE}' == 'WSA'
        ...  Verify And Wait For Wsa Log Records
             ...  wait_time=180 seconds
             ...  retry_time=10 seconds
             ...  search_path=smartlicense
             ...  .*${entitlement} license is released successfully from the appliance.* >= 1
    END

    FOR  ${entlments}  IN  @{release_list}
        Wait Until Keyword Succeeds  1 min  50 sec  Retry License State Change  ${entitlement}  Not requested
    END

    ${registration_status}=  Get Registration Status
    ${is_dut_virtual}=  Is Virtual Machine  vmname=${DUT}
    ${eval_usage}  ${eval_period}  Get Smart License Evaluation Period
    Run Keyword If  '${registration_status}' == 'unregistered' and '${DUT_TYPE}' != 'WSA'
    ...  Should Be Equal As Strings  ${eval_usage}  in use

Deregister Appliance From SSM
    [Documentation]  Deregisters the appliance from smart soft manager.
    ...  Verifies the log for succesfull deregistration. Post deregistration
    ...  registration status should change to UNREGISTERED.
    ...  If the device is virtual and evaluation status returned 'not in use'
    ...  No entitlements should be activated in this virtual device.
    ${eval_usage}  ${eval_period}  Get Smart License Evaluation Period
    ${registration_status}=  Get Registration Status
    Run Keyword If  '${eval_usage}' == 'not in use' and '${registration_status}' == 'registered'
    ...  Verify Deregistered Successfully
    ${is_dut_virtual}=  Is Virtual Machine  vmname=${DUT}
    ${eval_post_deg}  ${eval_post_deg_period}  Get Smart License Evaluation Period
    #If all entitlements are activated it would take some time to deactivate given 5min for
    # status to change to UNREGISTERED.
    Wait Until Keyword Succeeds  5 min  10 sec  Verify Registration Status On Appliance  unregistered

Wait Until SL Operation Is Complete
    @{menu_option}  Create List
    ...  URL
    Wait Until Keyword Succeeds  5 min  30 sec
    ...  Verify Menu Items Under License Smart Exists  1  @{menu_option}

Enable Smart License And Verify
    ${sl_is_enabled}=  Smart License Is Enabled
    Run Keyword If  not ${sl_is_enabled}  Run Keywords
    ...  Smart License Enable
    ...  Commit Changes

    Run Keyword If  not ${sl_is_enabled}
    ...  Wait Until Keyword Succeeds  5 min  30 sec
    ...  Verify If Smart Agent Process Is Ready

    Run Keyword if  not ${sl_is_enabled}
    ...  Verify And Wait For Log Records
    ...  wait_time=120 seconds
    ...  retry_time=10 seconds
    ...  search_path=smartlicense
    ...  .*Smart Licensing is enabled.* >= 1


Register Option
    License Smart Register
    ...  token=${SL_TOKEN_ID}
    ...  reregister=yes

Reregister Option
    License Smart Register
    ...  token=${SL_TOKEN_ID}
    ...  remove_register=yes

Register SL
    ${details}=  Smart License Get Status Details
    ${reg_status}=  Get From Dictionary
    ...  ${details}  Registration Status
    Run Keyword if  '${reg_status}' == 'Unregistered'  Register Option
    ...  ELSE  Reregister Option

    Verify And Wait For Log Records
    ...  wait_time=240 seconds
    ...  retry_time=10 seconds
    ...  search_path=smartlicense
    ...  .*The product is registered successfully.*>=1

    Wait Until SL Operation Is Complete
    ${details}=  Smart License Get Status Details
    ${reg_status}=  Get From Dictionary
    ...  ${details}  Registration Status

    Should Be Equal  ${reg_status}  Registered

Check Status And Deregister SL
    ${registration_status}=  Get Registration Status
    Log  ${registration_status}
    Run Keyword If  '${registration_status}' == 'registered'
    ...  License Smart Deregister
