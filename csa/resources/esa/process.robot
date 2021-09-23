*** Settings ****

*** Keywords ***
Get File Analysis Client ID And Generate Analysis Key
    Navigate To  Security Services  File Reputation and Analysis
    Click Button  //*[@type='submit' and @value='Edit Global Settings...']
    Click Element  //div[@id='analysis_arrow_closed']  don't wait
    ${out}=  Get Text  //div[@id='analysis_advanced']/table/tbody/tr[2]/td
    Log  ${out}
    Run On DUT  cd /data/fire_amp/db/preserve && python TG_Registration.py ${out}
    Restart Service And Check Status  amp
    Restart Service And Check Status  thirdparty

Check Process Status
    [Arguments]  ${process_name}
    ...  ${process_id}=False
    ${out}=  Run On Dut  /data/bin/heimdall_svc -s ${process_name}
    Should Contain
    ...  ${out}
    ...  'up': True
    ...  Error: Service did not come up after ${process_name} restart
    Should Contain
    ...  ${out}
    ...  'ready': True
    ...  Error: Service did not come up after ${process_name} restart
    Run Keyword If  ${process_id}
    ...  Return From Keyword  ${out}  

Restart Service And Check Status
    [Arguments]  ${service}  ${time_out}=1 min
    Run On DUT  /data/bin/heimdall_svc -r ${service}
    Wait Until Keyword Succeeds  ${time_out}  5 sec
    ...  Check Process Status  ${service}

Clear Heimdall Log
    [Arguments]  ${service_name}
    Run On DUT  echo "" > /data/log/heimdall/${service_name}/${service_name}.current
