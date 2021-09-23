# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_log_limit.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
@{invalid_set_time_limit_values}         %  a  0  61  -1
@{valid_set_time_limit_values}           1  2  25  59  60
@{invalid_events_limit_values}           %  a  9  5001  -1
@{valid_events_limit_values}             10  11  2500  4999  5000
${default_event_limit}                   10
${default_time_limit}                    10
${time_limit}                            60
${events_limit_popup_message}            Value must be an integer from 10 to 5000.
${time_limit_popup_message}              Value must be an integer from 1 to 60.
${xpath_event_limit_error_more}          //div[@id='rl_event_limit_error_div']//following::span[@class='bubble-link-errormsg']
${xpath_time_limit_error_more}           //div[@id='rl_time_limit_error_div']//following::span[@class='bubble-link-errormsg']
${gui_log_name}                          gui
${authentication_log_name}               authentication
${authentication_log_location}           authentication
${log_files_path}                        /data/pub
${authentication_log_path}               ${log_files_path}/${authentication_log_location}
${authentication_log_file}               ${authentication_log_path}/${authentication_log_name}.current
${more_popup_message_element}            //div[contains(text(),'Value must be an integer from')]

*** Keywords ***
Precondition for Tvh1340624c
    [Arguments]  @{log_names}
    @{log_subscription}=  Create List  @{log_names}[0]  ${sma_log_types.AUTH}
    ...  @{log_names}[1]  ${sma_log_types.HTTP}
    FOR  ${logname}  ${log_type}  IN  @{log_subscription}
      Run keyword and continue on failure  Log config delete  ${logname}
      Log config new  name=${logname}   log_file=${log_type}
      Commit
    END

Verify invalid rate limit value error in CLI
    [Arguments]  ${log_name}  ${type}  @{invalid_limit_values}
    FOR  ${invalid_set_limit}  IN  @{invalid_limit_values}
      ${rate_limit_error}=  Run keyword if  '${type}'=='time_limit'  Run keyword and expect error  *  Log config edit  ${log_name}  rate_limit=Y  time_range=${invalid_set_limit}  number_of_events=${default_event_limit}
      ...  ELSE IF   '${type}'=='event_limit'  Run keyword and expect error  *  Log config edit  ${log_name}  rate_limit=Y  time_range=${default_time_limit}  number_of_events=${invalid_set_limit}
      Should match regexp  ${rate_limit_error}  .*IafCliValueError: ${invalid_set_limit}.*
    END

Verify valid rate limit values in CLI
    [Arguments]  ${log_name}  ${type}  @{valid_limit_values}
    FOR  ${set_limit}  IN  @{valid_limit_values}
      Run keyword if  '${type}'=='time_limit'  Log config edit  ${log_name}  rate_limit=Y  time_range=${set_limit}  number_of_events=${default_event_limit}
      ...  ELSE IF  '${type}'=='event_limit'  Log config edit  ${log_name}  rate_limit=Y  time_range=${default_time_limit}  number_of_events=${set_limit}
      ...  ELSE  Run keywords  Should be equal as strings  ${type}  time_limit  AND  Should be equal as strings  ${type}  event_limit
      Commit
    END

Verify invalid rate limit event limit value error in GUI
    [Arguments]  ${log_name}  @{invalid_events_limit_values}
    FOR  ${invalid_max_event_value}  IN  @{invalid_events_limit_values}
      Run keyword and ignore error  Log Subscriptions Edit Log  ${log_name}  logged_events=${invalid_max_event_value}  time_limit=${default_time_limit}
      Click Element  ${xpath_event_limit_error_more}
      Sleep  3
      ${text}=  Get Text  ${more_popup_message_element}
      Should match regexp   ${text}  .*${events_limit_popup_message}.*
    END

Verify invalid rate limit time limit value error in GUI
    [Arguments]  ${log_name}  @{invalid_time_limit_values}
    FOR  ${invalid_set_time_limit}  IN  @{invalid_time_limit_values}
      Run keyword and ignore error  Log Subscriptions Edit Log  ${log_name}  logged_events=${default_event_limit}  time_limit=${invalid_set_time_limit}
      Click Element  ${xpath_time_limit_error_more}
      Sleep  3
      ${text}=  Get Text  ${more_popup_message_element}
      Should match regexp   ${text}  .*${time_limit_popup_message}.*
    END

Check log count based on rate limit set
    [Arguments]  ${keyword}  ${log_file}  ${rate_limit_set}
    ${current_time_plus_timelimit}=  Add time to current time  seconds=${time_limit}
    FOR  ${index}  IN RANGE  ${time_limit}
      ${current_time}=  Get current time
      Exit For Loop If   '${current_time}' > '${current_time_plus_timelimit}'
      Run keyword  ${keyword}
      ${auth_log}  ${auth_log_count}=  Filter Log  ${log_file}  skip_patterns='.*Begin Logfile.*','.*Version.*','.*Time offset.*'
      Should Be True  ${auth_log_count} <= ${rate_limit_set}
    END

Disable log subscription rate limit
    [Arguments]  @{lognames}
    FOR  ${logname}  IN  @{lognames}
      Log config edit  ${log_name}  rate_limit=N
      Commit
    END

*** Test Cases ***
Tvh1340624c
    [Documentation]  Tvh1340624c-SEC-LOG-LIMIT: Control log rates and resource utilization

    [Tags]      cli  gui Tvh1340624c
    [Setup]     Precondition for Tvh1340624c  ${authentication_log_name}  ${gui_log_name}
    [Teardown]  Disable log subscription rate limit  ${authentication_log_name}  ${gui_log_name}

     # Step 1. Goto SMA CLI
     # Step 2. logconfig -> edit ->logname
     # Step 3. Input invalid values in time limit and event limit values
     # Step 4. Verify error messages for invalid ipnputs
     Verify invalid rate limit value error in CLI  ${gui_log_name}  time_limit  @{invalid_set_time_limit_values}
     Verify invalid rate limit value error in CLI  ${authentication_log_name}  event_limit  @{invalid_events_limit_values}

     # Step 5. Goto SMA CLI
     # Step 6. logconfig -> edit ->logname
     # Step 7. Input valid values in time limit and event limit values
     # Step 8. Verify values are getting saved successfully
     Verify valid rate limit values in CLI  ${authentication_log_name}  time_limit  @{valid_set_time_limit_values}
     Verify valid rate limit values in CLI  ${gui_log_name}  event_limit  @{valid_events_limit_values}

     # Step 9. Go to page System Administrator -> Log Subscription
     # Step 10. Select a specific log
     # Step 11. Enable Rate Limit
     # Step 12. Input invalid values in time limit and event limit values
     # Step 13. Press Submit button
     # Step 14. Verify error messages for invalid ipnputs
     Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
     Verify invalid rate limit event limit value error in GUI  ${authentication_log_name}  @{invalid_events_limit_values}
     Verify invalid rate limit time limit value error in GUI  ${gui_log_name}  @{invalid_set_time_limit_values}

     # Step 15. Input valid values in time limit and event limit values
     # Step 16. Verify value is saved is successfully
     Log Subscriptions Edit Log  ${authentication_log_name}  logged_events=${default_event_limit}  time_limit=${time_limit}
     Commit Changes

     # Step 17. Check log count is less than the rate limit set by tailing the .current logs
     Sleep  300
     Start CLI Session
     Roll Over Now
     Run On DUT  cd ${authentication_log_path} && rm -rf *.s
     Check log count based on rate limit set  Start CLI Session  ${authentication_log_file}  ${default_event_limit}