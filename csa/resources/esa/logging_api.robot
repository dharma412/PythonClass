*** Settings ***

Library      robot.libraries.DateTime
Resource     esa/global.txt
Resource     esa/injector.txt
Resource     esa/logs_parsing_snippets.txt
Resource     regression.txt

*** Keywords  ***

Api Suite Setup
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA

    DefaultTestSuiteSetup
    Interfaceconfig Edit  Management
    ...  api_http=yes  api_https=yes
    commit

Api Suite Teardown
    DefaultTestSuiteTeardown

Edit Mail Flow Policy TLS Settings
    [Arguments]  ${listener_name}  ${policy_name}  ${opt}
    ${settings}=  Mail Flow Policies Create Settings  TLS  ${opt}
    Mail Flow Policies Edit  ${listener_name}  ${policy_name}  ${settings}
    Commit Changes

Get Date From Filename
    [Arguments]  ${filename}
    ...          ${time}
    ...          ${end_dt}=${False}
    Log Many  ${filename}
    Log Many  ${time}

    ${date_time}=  Evaluate
    ...  re.search('.*@([\\w]*)','${filename}').group(1)  modules=re
    ${year}=  Evaluate  '${date_time[0:4]}'
    ${year}=  Convert To Integer  ${year}  base=10
    ${time}=  Split String  ${time}
    ${month}=  Evaluate  time.strptime('${time[1]}','%b').tm_mon  modules=time
    ${date}=  Set Variable  ${time[0]}
    ${date}=  Convert To Integer  ${date}  base=10
    ${hour}=  Evaluate  '${time[2][0:2]}'
    ${hour}=  Convert To Integer  ${hour}  base=10
    ${mins}=  Evaluate  '${time[2][3:5]}'
    ${mins}=  Convert To Integer  ${mins}  base=10

    ${pdt_date}=  Evaluate
    ...  datetime.datetime(${year}, ${month}, ${date}, ${hour}, ${mins}, 00)
    ...  modules=datetime
    Log Many  ${pdt_date}
    ${timezone}=  Get Time Zone From DUT
    ${gmt_date}=  Run Keyword If  '${timezone}' == 'PST'  Add Time To Date  ${pdt_date}  8 hours
    ...  ELSE  Add Time To Date  ${pdt_date}  7 hours
    ${gmt_date}=  Run Keyword If  ${end_dt}==${True}  Add Time To Date       ${gmt_date}         1 minute
    ...  ELSE  Subtract Time From Date       ${gmt_date}         2 minute
    Log Many  ${gmt_date}

    ${dt}=  Convert Date  ${gmt_date}  result_format=%Y-%m-%dT%H:%M:00.000Z

    [Return]  ${dt}

Get Logs Info From DUT
    [Arguments]    ${logname}

    ${out}=  Run On Dut  cd /data/pub/${logname};ls -lrt *.{s,gz}
    Log Many  ${out}
    @{lines}=  Split String  ${out}  \n
    Reverse List  ${lines}
    Log Many  ${lines}
    ${len}=  Get Length  ${lines}
    ${newlist}=  Create List
    ${logdict}=  Create Dictionary
    ${log}=  Create List
    FOR  ${val}  IN RANGE  ${len}
       ${li}=  Split String  ${lines[${val}]}
       Append To List  ${newlist}  ${li}
       Log Many  ${newlist}
    END
    FOR  ${val}  IN  @{newlist}
       Set To Dictionary  ${logdict}  Size  ${val[4]}
       Set To Dictionary  ${logdict}  Name  ${val[8]}
       ${date}=  Catenate  ${val[6]}  ${val[5]}  ${val[7]}
       Set To Dictionary  ${logdict}  Date  ${date}
       ${sha256}=  Get SHA256 OF File  ${val[8]}  ${logname}
       Set To Dictionary  ${logdict}  Filehash  ${sha256}
       ${moddat}=  Get Last Modification Date OF File  ${val[8]}  ${logname}
       Set To Dictionary  ${logdict}  ModificationDate  ${moddat}
       ${dict}=  Copy Dictionary  ${logdict}
       Log Many  ${logdict}
       Append To List  ${log}  ${dict}
       Log Many  ${log}
    END
    [Return]  ${log}

Get SHA256 OF File
    [Arguments]  ${file_name}  ${log_name}

    ${sha256}=  Run On Dut
    ...  python -c "import hashlib; print hashlib.sha256(open('/data/pub/${log_name}/${file_name}','rb').read()).hexdigest()"
    [Return]  ${sha256}

Get Last Modification Date OF File
    [Arguments]  ${file_name}  ${log_name}

    ${moddate}=  Run On Dut
    ...  python -c "import os.path; print os.path.getmtime('/data/pub/${log_name}/${file_name}')"
    ${mod}=  Split String  ${moddate}  .
    ${moddate}=  Convert To Integer  ${mod[0]}  base=10
    [Return]  ${moddate}

Get Access Token

    ${adfs_data}=  Create Dictionary
    ...  adfs_auth_url      ${ADFS_AUTH_URL}
    ...  adfs_resource      ${ADFS_RESOURCE}
    ...  adfs_username      ${ADFS_USERNAME}
    ...  adfs_password      ${ADFS_PASSWORD}
    ...  adfs_client_id     ${ADFS_CLIENT_ID}
    ...  adfs_scope         ${ADFS_SCOPE}
    ...  adfs_grant_type    ${ADFS_GRANT_TYPE}
    ${response}=  Get Adfs Access Token  ${adfs_data}
    Log  ${response}
    ${body}=  Get Response Body  ${response}
    Log Dictionary  ${body}
    ${access_token}=  Get From Dictionary  ${body}  access_token
    Log  ${access_token}
    [Return]  ${access_token}

Comparision OF API and Log
    [Arguments]  ${api_resp}
    ...  ${log}
    ...  ${logname}
    ...  ${computehash}=${FALSE}

    LogMany  ${api_resp}
    LogMany  ${log}
    ${moddate}=  Set Variable  ${EMPTY}
    ${count}=  Set Variable  ${api_resp['meta']['totalCount']}
    FOR  ${value}  IN RANGE  ${count}
       Should Be Equal As Strings  ${log[${value}]['Name']}  ${api_resp['data'][${value}]['name']}
       Should Be Equal As Strings   ${api_resp['data'][${value}]['downloadUrl']}  ${api_base_url}/${logname}/${log[${value}]['Name']}
       Should Be Equal As Numbers   ${api_resp['data'][${value}]['size']}  ${log[${value}]['Size']}
       Should Be Equal As Numbers   ${api_resp['data'][${value}]['modificationDate']}  ${log[${value}]['ModificationDate']}
       Run Keyword If  ${computehash} == ${TRUE}  Should Be Equal As Strings  ${api_resp['data'][${value}]['fileHash']}  ${log[${value}]['Filehash']}
    END

Write Data In File
    [Arguments]  ${data}
    ...  ${log_name}

    OperatingSystem.Create File    %{HOME}/Downloads/${log_name}_response_log.txt       ${data}

Download And Compare File
    [Arguments]  ${log_name}
    ...  ${file_name}
    ...  ${data}

    Log Subscriptions Download File  ${log_name}  ${file_name}
    Write Data In File  ${data}  ${log_name}
    ${csvA} =  OperatingSystem.Get File    %{HOME}/Downloads/${file_name}
    ${csvB} =  OperatingSystem.Get File    %{HOME}/Downloads/${log_name}_response_log.txt
    Should Be Equal As Strings   ${csvA}    ${csvB}

Get Time Zone From DUT
    ${date}=  Run on DUT  date
    ${date_split}=  Split String  ${date}
    ${timezone}=  Get From List  ${date_split}  4
    [Return]  ${timezone}
