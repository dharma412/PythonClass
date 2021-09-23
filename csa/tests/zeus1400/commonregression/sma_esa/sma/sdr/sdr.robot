*** Settings ***
Library           Collections
Resource          sma/global_sma.txt
Resource     	  sma/reports_keywords.txt
Resource          regression.txt
Resource          esa/global.txt
Resource          esa/injector.txt
Resource          esa/logs_parsing_snippets.txt
Resource          esa/backdoor_snippets.txt

Suite Setup   Run Keywords
              ...  Set Aliases For Appliance Libraries
              ...  Set Appliance Under Test to SMA
              ...  DefaultRegressionSuiteSetup
              ...  Do SDR Setup
Suite Teardown   DefaultRegressionSuiteTeardown


*** Variables ***
${DATA_UPDATE_TIMEOUT}  15m
${RETRY_TIME}  15s
${MAIL_PATH}  %{SARF_HOME}/tests/testdata/esa/

${firefox_prefs_browser.download.dir}                          %{SARF_HOME}/tmp
${firefox_prefs_browser.download.folderList}                   2
${firefox_prefs_browser.download.manager.showWhenStarting}     false
${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=       application/pdf,text/csv,application/csv
${firefox_prefs_network.http.prompt-temp-redirect}  false
${SESSION_TIMEOUT}                   1440
${PDF2TXT_PATH}                      /usr/local/bin/pdf2txt.py

${ADDRLIST1_NAME}  exception_list90080016
${SENDER1}  sender1@domain.cs27
${SENDER2}  domain@domain.cs27

${XPATH_MESSAGE_TRACKING_FIRST_ROW}   xpath=.//*[@id='resultTable']/tr[2]/td[2]/table/tbody/tr[1]/td[2]/a
${XPATH_MESSAGE_TRACKING_SECOND_ROW}  xpath=.//*[@id='resultTable']/tr[4]/td[2]/table/tbody/tr[1]/td[2]/a

${XPATH_SDR_UNKNOWN_COUNT}  xpath=.//*[@id='widget-content-ss_0_0_1']/dd/table/tbody/tr[10]/td/span/a
${XPATH_SDR_CHECK_BOX}  xpath=//input[@id="event_sdr"]
${XPATH_SDR_UNKNOWN_CHECK_BOX}  xpath= //*[@id="event_sdr_unknown"]
${XPATH_SDR_CHART_EXPORT}  xpath=//td[@id='ss_0_0_0-links']/span
${XPATH_SDR_THREAT_CATEGORY_TABLE}  xpath=.//*[@id='ss_0_2_0-links']/span[2]


${threatfeed_feeds_test_file_dir}=   /data/threatfeeds/test_stix_pkg
${threatfeed_feeds_test_file_dir}=   /data/threatfeeds/test_stix_pkg
${feeds_dir}=  %{SARF_HOME}/tests/testdata/esa/threatfeed/feeds
${threatfeed_log_fetching}=   Info: THREAT_FEEDS: 0 observables were fetched from the source:
${TIMEOUT}  90
${NO_DATA_IMAGE_MD5}=                5432ae167562581bff63ba0f6d615143
${MD5_HASH}=  e678e49e1a894f625488ba66ec8cc9bd
${FILEHASHLIST_MD5_NAME}=  list_md5
${FILEHASHLIST_MD5_DESC}=  list_md5 description
${attachments_dir}=  %{SARF_HOME}/tests/testdata/esa/threatfeed/attachments
${WEB_HOSTNAME}                      v2.beta.sds.cisco.com
${CONFIG_FILE}=    /data/pub/configuration/default_config.xml

*** Keywords ***
Do SDR Setup
    Import ESA Libraries  ESA
    ESAUtilsLibrary.Run On DUT  rm -rf ${CONFIG_FILE}
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    DefaultRegressionSuiteSetup
    Set Appliance Under Test to ESA
    Set Manifest Server
    Wait Until Keyword Succeeds  300s  30s  Check Ec Status
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    Run Keyword And Ignore Error  Log Out Of DUT
    Log Into DUT
    Spam Quarantine Enable
    Spam Quarantine SlBl Enable
    Pvo Quarantines Enable
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  ${TIMEOUT}
    Start Cli SEssion If Not Open
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes
    Commit Changes
    ${automatic_migration_settings}=  Create Dictionary
    ...  PQ Migration Mode   Automatic
    Pvo Migration Wizard Run  ${automatic_migration_settings}
    Commit Changes
    Set Appliance Under Test to ESA
    ${PUBLIC_LISTENER_IP}=  Get ESA Public IP
    ${PRIVATE_LISTENER_IP} =  Get ESA Private IP
    Set Suite Variable  ${PUBLIC_LISTENER_IP}
    Set Suite Variable  ${PRIVATE_LISTENER_IP}
    ${PUBLIC_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${PUBLIC_LISTENER_IP4}  ${PUBLIC_LISTENER.ipv4}
    ${settings}=  Create Dictionary  Web UI Inactivity Timeout  60
    Network Access Edit  ${settings}
    Commit Changes
    Message Tracking Enable  tracking=centralized
    Message Tracking Edit Settings  tracking=centralized
    EUQ Enable  ${SMA}  ${SMA_IP}  6025  enable_slbl=${True}
    Commit Changes
    Admin Access Config Timeout   timeout_webui=1440  timeout_cli=1440
    Commit
    Start Cli SEssion If Not Open
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes
    Reporting Config Setup  enable=yes
    Commit
    #Pvo Quarantines Enable
    Run Keyword and ignore Error  Commit Changes

    Roll Over Now    sdr_client
    Roll Over Now    mail_logs

    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Enable Feature Key  ETF

    Run Keyword If  ${USE_SMART_LICENSE} == 1
    ...  Threatfeedconfig setup  use_etf=yes  custom_header=yes  header_name=etf_header  header_content=false
    Admin Access Config Timeout
    ...  timeout_webui=720
    ...  timeout_cli=720
    Run On Dut   mkdir ${threatfeed_feeds_test_file_dir}
    Log Config Edit  mail_logs    log_level=4
    Log Config Edit  threatfeeds  log_level=4
    Sdr Advanced Config
    ...  sdr_lookup_timeout_value= 10
    ...  sdr_service_hostname= v2.sds.cisco.com
    ...  sdr_verify_server_certificate= No
    ...  sdr_rpc_log_level= Debug
    ...  sdr_http_client_log_level= Debug
    ...  sdr_match_exceptions_envelope_from_domain= No
    Commit
    ${list1_settings}=  Create Dictionary
    ...  Description                       ${ADDRLIST1_NAME} description
    ...  List Type                         Domains only
    ...  Addresses                         @mail.cs27
    ADDRESS Lists Add  ${ADDRLIST1_NAME}  ${list1_settings}
    @{arguments}=  Create List  domain_exception_list_name=${ADDRLIST1_NAME}
    Sender Domain Reputation Exception List  @{arguments}
    Commit Changes


Inject And Verify Message
    [Arguments]
    ...  ${test_id}
    ...  ${inject_host}
    ...  ${address}
    ...  ${num_msgs}
    ...  ${mbox_name}
    ...  ${addr_file}
    ...  @{varargs}

    Set Test Variable  ${exp_match_count}  1
    @{inject_args}=  Create List
    ...  num-msgs=${num_msgs}
    ...  inject-host=${inject_host}

    Run Keyword If  '${address}'!='None'
    ...  Append To List  ${inject_args}  mail-from=${address}

    Run Keyword If  '${mbox_name}'!='None'
    ...  Append To List  ${inject_args}  mbox-filename=${mbox_name}

    Run Keyword If  '${addr_file}'!='None'
    ...  Append To List  ${inject_args}  address-list=${addr_file}


    Inject Messages  @{inject_args}

Search By MID
    [Arguments]  ${mid}

    ${res}=  Email Message Tracking Search
    ...  ironport_mid=${mid}
    Log  ${res}
    Should Be True  ${res.result_list}

Verify Message Count
    [Arguments]  ${count}  ${sdr_type}
    Set Appliance Under Test To SMA
    ${res}=  Wait Until Keyword Succeeds   25m   15s   Reports Parse
    ...  page=Email, Reporting, Sender Domain Reputation
    ...  name=Summary of Messages handled by SDR
    Log  ${res}

    ${res1}=  Evaluate
    ...  [x for x in map(lambda x: x if not x.has_key('SDR Category') else None, ${res}) if x is not None]
    Log  ${res1}
    ${var}=   Get From List  ${res1}  8
    ${value}=  Get From Dictionary  ${var}  ${sdr_type}
    Should Be Equal  ${value}  ${count}

Verify Message Tracking

   Set Appliance Under Test To SMA
   Navigate TO  Email  Reporting  Sender Domain Reputation
   Click Element  ${XPATH_SDR_UNKNOWN_COUNT}
   Wait Until Page Contains  Message Tracking  5s
   Element Text Should Be  ${XPATH_MESSAGE_TRACKING_FIRST_ROW}       ${SENDER1}
   Element Text Should Be  ${XPATH_MESSAGE_TRACKING_SECOND_ROW}      ${SENDER2}

Disable Antivirus
    [Arguments]  ${av_name}=Sophos
    ${av_state}=  Antivirus Is Enabled  ${av_name}
    Run Keyword If  ${av_state}
    ...  Antivirus Disable  ${av_name}
    Commit Changes


Create Content Filter Through GUI
    [Arguments]  ${name}  ${listener_type}  ${should_commit}=${True}
    ${settings}=  Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${name}   ${True}
    Mail Policies Edit Content Filters  ${listener_type}  default
    ...  ${settings}
    Run Keyword If  ${should_commit}
    ...   Commit Changes

Add File Hash List
    [Arguments]  ${name}  ${description}  ${hashes}  ${type}
    ${list1_settings}=  Create Dictionary
    ...  Description                       ${description}
    ...  File Hash Type                    ${type}
    ...  File Hash                         ${hashes}
    FileHash Lists Add  ${name}  ${list1_settings}

ETF Domain Reputation Setup
    [Arguments]  ${source_name}
    Diagnostic Reporting Delete Db  confirm=yes
    Run On Dut  mkdir ${threatfeed_feeds_test_file_dir}/${source_name}
    SCP  from_location=%{SARF_HOME}/tests/testdata/esa/threatfeed/feeds/domain_reputation.xml
    ...  to_location=${threatfeed_feeds_test_file_dir}/${source_name}/
    ...  to_host=${ESA}

    Add Threatfeed Source
    ...  ${source_name}
    ...  test source
    ...  test.com
    ...  /test-data
    ...  test.ch

    ${log_value}=  Create Dictionary
    ...  Text  Malicious Domain Detected

    ${available_sources}  Create List  ${source_name}
    ${ext_threat_feeds_settings}  Create Dictionary
    ...  Available Sources  ${available_sources}
    ...  Envelope Sender  ${False}
    ...  From Header  ${True}
    ...  Reply-to  ${False}
    ${settings}  Create Dictionary
    ...  External Threat Feeds   ${ext_threat_feeds_settings}
    ${conditions}  Content Filter Create Conditions
    ...  Domain Reputation  ${settings}
    ${actions}=  Content Filter Create Actions
    ...  Add Log Entry  ${log_value}
    Content Filter Add
    ...  Incoming
    ...  my_filter
    ...  super_filter
    ...  ${actions}
    ...  ${conditions}

    ${settings}=        Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  Enable All  ${True}
    Mail Policies Edit Content Filters  incoming  default  ${settings}
    Commit Changes

ETF File Hash
    Add File Hash List  ${FILEHASHLIST_MD5_NAME}  ${FILEHASHLIST_MD5_DESC}  ${MD5_HASH}  MD5
    Commit Changes
    Run On Dut  mkdir ${threatfeed_feeds_test_file_dir}/test
    SCP  from_location=%{SARF_HOME}/tests/testdata/esa/threatfeed/feeds/STIX-MD5.xml
    ...  to_location=${threatfeed_feeds_test_file_dir}/test/
    ...  to_host=${ESA}

    Add Threat Feeds Source  test

    Log Entry Add Content Filter Via GUI  md5_cf  ${FILEHASHLIST_MD5_NAME}
    Create Content Filter Through GUI  md5_cf  Incoming
    Disable Antivirus  Sophos
    Disable Antivirus  Mcafee

ETF Url
    Url Filtering Enable
    Commit Changes

    ${status}  Url Filtering Get Details
    ${string}=  Convert To String  ${status}
    ${result}  ${msg}=  Run Keyword And Ignore Error
    ...  Should Contain  ${string}  Connected

    Run Keyword If  '${result}' == 'FAIL'  Do Websecurity Config

    Wait Until Keyword Succeeds  2 min  20 sec
    ...  Verify URL Filtering Status As Connected

    Outbreak Config Proxyconfig
    ...  proxy_template=secure-web.cisco.com/%(auth)s/%(url)s
    Outbreak Config Setup
    ...  log_urls=yes

    Commit
    Run On Dut  mkdir ${threatfeed_feeds_test_file_dir}/test1
    SCP  from_location=%{SARF_HOME}/tests/testdata/esa/threatfeed/feeds/url_reputation.xml
    ...  to_location=${threatfeed_feeds_test_file_dir}/test1/
    ...  to_host=${ESA}

    Add Threat Feeds Source  test1
    ${matched_filter_script}=  Catenate  SEPARATOR=\n
    ...  my_filter_action:
    ...  if (true) { url-etf-defang(['test1'], "", 1);
    ...  log-entry("Defang url detected"); }
    Filters New  script=${matched_filter_script}
    Commit

Chart ${name} Should Not Be Empty
    ${chart_md5}=  Email Reporting Charts Get Md5 Hash  ${name}  password=${DUT_ADMIN_SSW_PASSWORD}
    Log  ${chart_md5}
    ${result}  ${msg}=  Run Keyword And Ignore Error
    ...  Should Not Be Equal As Strings  ${chart_md5}  ${NO_DATA_IMAGE_MD5}
    # add screenshot into log if checksum of empty chart and existing one aren't equal
    Run Keyword If  '${result}' == 'FAIL'  Capture Screenshot
    Run Keyword If  '${result}' == 'FAIL'  Fail  ${msg}

Inject Message
    [Arguments]  ${inject-host}  ${extra_opts}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}
    ...  mail-from=general@${CLIENT}
    ...  extra_opts=${extra_opts}

Verify Table Data
    [Arguments]  ${table_name}  ${source}
    ...  ${col_name_1}  ${col_name_2}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  20m  10s
    ...  Email Report Table Get Data  ${table_name}
    Log  ${reporting_data}
    ${col_values}=  Get From Dictionary  ${reporting_data}
    ...  ${col_name_1}
    :FOR  ${col_value}  IN RANGE  0  3
    \  ${value} =  Get From List  ${col_values}  ${col_value}
    \  ${src} =  Get From List  ${source}  ${col_value}
    \  Should Be Equal As Strings  ${value}  ${src}
    ${col_values}=  Get From Dictionary  ${reporting_data}
    ...  ${col_name_2}
    :FOR  ${col_value}  IN RANGE  0  3
    \  ${value} =  Get From List  ${col_values}  ${col_value}
    \  ${value} =  Convert To Integer  ${value}
    \  Should Be Equal As Integers  ${value}  1

Do Websecurity Config
    Websecurityadvancedconfig  web_hostname=${WEB_HOSTNAME}
    Commit
Verify Summary Table Data Connections
    [Arguments]  ${table_name}  ${source}
    ...  ${col_name_1}  ${col_name_2}
    ${reporting_data}=  Wait Until Keyword Succeeds
    ...  20m  10s
    ...  Email Report Table Get Data  ${table_name}
    Log  ${reporting_data}
    ${col_values}=  Get From Dictionary  ${reporting_data}
    ...  ${col_name_1}
    ${value} =  Get From List  ${col_values}  0
    Should Be Equal As Strings  ${value}  ${source}
    ${col_values}=  Get From Dictionary  ${reporting_data}
    ...  ${col_name_2}
    ${value} =  Get From List  ${col_values}  0
    ${value} =  Convert To Integer  ${value}
    Should Be Equal As Integers  ${value}  1

Log Entry Add Content Filter Via GUI
    [Arguments]  ${cf_name}  ${hash_list}
    ${etf_sources}  Create List  test

    ${new_dict}  Create Dictionary
    ...   etf add categories  ${etf_sources}
    ...   use a file hash exception list  ${hash_list}

    ${new_value}  Create Dictionary
    ...   External Threat Feeds  ${new_dict}

    ${new_value1}  Create Dictionary
    ...   Text  logEntry for AttachmentFileInfo ETF

    ${conditions}  Content Filter Create Conditions
    ...  Attachment File Info  ${new_value}

    ${actions}  Content Filter Create Actions
    ...  Add Log Entry  ${new_value1}

    Content Filter Add  Incoming  ${cf_name}
    ...   Super filter  ${actions}  ${conditions}
Add Threat Feeds Source
    [Arguments]  ${source_name}
    External Threatfeeds Source Add
    ...  source_name=${source_name}
    ...  description=test source
    ...  hostname=test.com
    ...  polling_path=/test-data
    ...  collection_name=test.ch
    ...  polling_age=30
    ...  polling_interval_hour=0
    ...  polling_interval_mins=15
    ...  use_https=yes
    ...  enable_proxy=yes
    ...  configure_credentials=no
    ...  username=guest
    ...  password=guest
    Commit Changes

    Roll Over Now  logname=threatfeeds
    Verify Log Contains Records
    ...  search_path=threatfeeds
    ...  ${threatfeed_log_fetching} test ==0
Add Threatfeed Source
    [Arguments]  ${s_name}  ${desc}  ${h_name}  ${p_path}  ${c_name}
    ...  ${p_int}=15  ${f_age}=30  ${https}=N  ${port}=80
    Threatfeedconfig Sourceconfig Poll Url Add
    ...  poll_url_source_name=${s_name}
    ...  poll_url_source_description=${desc}
    ...  poll_url_host_name=${h_name}
    ...  poll_url_polling_path=${p_path}
    ...  poll_url_collection_name=${c_name}
    ...  poll_url_polling_interval=${p_int}
    ...  poll_url_feed_age=${f_age}
    ...  poll_url_poll_segment=${f_age}
    ...  poll_url_use_https=${https}
    ...  poll_url_polling_port=${port}
    ...  poll_url_configure_credentials=Y
    ...  poll_url_auth_method=1
    ...  poll_url_auth_username=guest
    ...  poll_url_auth_password=guest
    Roll Over Now  logname=threatfeeds
    Commit
    Verify Log Contains Records
    ...  search_path=threatfeeds
    ...  ${threatfeed_log_fetching} ${s_name} ==0
 
Set Manifest Server
    ${is_dut_virtual}=  Is DUT A Virtual Model
    Update Config Validate Certificates  validate_certificates=NO
    ${dynamic_host_name}   Set Variable If  ${is_dut_virtual}  ${STAGING_UPDATE_SERVER_FOR_VIRTUAL}  ${STAGING_UPDATE_SERVER_FOR_HARDWARE}
    Update Config Dynamichost  dynamic_host=${dynamic_host_name}
    Commit

Check Ec Status
    ${res}  Ecstatus
    Should Not Match Regexp  ${res}  .*Never updated.*

*** Test Cases ***
Tvh1214961c
    [Documentation]  1) Verify in the tracking details for a message, \n
    ...  sdr reputation related event is shown in the tracking details response for sdr value - unknown \n
    ...  2) To verify that user able to see the sdr verdict under  Incoming Messages by SDR \n
    ...  3) Verify counters against Incoming Messages by SDR Category for timeranges options \n
    ...  4) Verify that user able to view the columns SDR Verdict and Messages counter data.
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1214961c \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1251857c \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1194316c \n
    ...  http://tims.cisco.com/warp.cmd?ent=Tvh1194333c

    [Tags]    Tvh1214961c  Tvh1251857c  Tvh1194316c  Tvh1194333c  CSCvv63856  sdr  srts
    Set Test Variable  ${TEST_ID}  ${TEST_NAME}

    Set Appliance Under Test To SMA

    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes

    Set Aliases For Appliance Libraries
    Set Appliance Under Test To ESA
    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  ${SENDER2}  1  ${SPAM}  None
    ${mid}=  Get Mid Value  MID .*

    Wait Until Keyword Succeeds
   ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
   ...  Verify Message Count
   ...  1
   ...  Unknown

   Click Element  ${XPATH_SDR_UNKNOWN_COUNT}
   Wait Until Page Contains  Message Tracking  5s

   Checkbox Should Be Selected  ${XPATH_SDR_CHECK_BOX}
   Checkbox Should Be Selected  ${XPATH_SDR_UNKNOWN_CHECK_BOX}

   Wait Until Keyword Succeeds
    ...  10 min
    ...  20 sec
    ...  Search By MID  ${mid}

   ${msg}=  Email Message Tracking Get Message Details  ${mid}
   Log Dictionary  ${msg}
   Log Dictionary  ${msg.message_details}
   Log Dictionary  ${msg.processing_details}
   Should Contain  ${msg.message_details.get('MID')}  ${mid}
   Should Contain  ${msg.processing_details.keys()}
   ...  Message ${mid} Consolidated Sender Reputation: Unknown, Threat Category: N/A. Youngest Domain Age: unknown for domain: N/A
   Should Contain  ${msg.processing_details.keys()}   Message ${mid} Domains for which SDR is requested: reverse DNS host: d1.${CLIENT_HOSTNAME}, helo: ${CLIENT_HOSTNAME}, env-from: domain.cs27, header_from: Not Present, reply_to: Not Present


   Close Browser
   Selenium Login With Autodownload Enabled  ${firefox_prefs_browser.download.dir}  ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk} 
   Navigate To  Email  Reporting  Sender Domain Reputation
   ${start_time}=  Get Time
   Click Element  ${XPATH_SDR_CHART_EXPORT}  don't wait
   ${path}=  Wait Until Keyword Succeeds  20m  10s
   ...  Wait For Download  .csv  start_time=${start_time}  timeout=600
        ...  download_directory=%{SARF_HOME}/tmp
   Set Test Variable  ${path}
   Log  ${path}
   ${csv_data}=  Csv Parser Get Data  ${path}
   Log List  ${csv_data}
   List Should Contain Value  ${csv_data['Unknown']}  1

   Set Aliases For Appliance Libraries
   Set Appliance Under Test To SMA
   @{range_list}=  Create List  Week  30 days  90 days  Year  Day
   :FOR  ${range_time}  IN  @{range_list}
   \  ${res}=  Wait Until Keyword Succeeds   15m   15s   Reports Parse
   \  ...  page=Email, Reporting, Sender Domain Reputation
   \  ...  name=Summary of Messages handled by SDR
   \  ...  time_range=${range_time}
   \  Log  ${res}

   \  ${res1}=  Evaluate
   \  ...  [x for x in map(lambda x: x if not x.has_key('SDR Category') else None, ${res}) if x is not None]
   \  Log  ${res1}
   \  ${var}=   Get From List  ${res1}  8
   \  ${value}=  Get From Dictionary  ${var}  Unknown
   \  Should Be True  ${value}  >= 0
   \  ${start_time}=  Get Time
   \  Click Element  ${XPATH_SDR_CHART_EXPORT}  don't wait
   \  ${path}=  Wait Until Keyword Succeeds  20m  10s
   \  ...  Wait For Download  .csv  start_time=${start_time}  timeout=600
   \       ...  download_directory=%{SARF_HOME}/tmp
   \  Set Test Variable  ${path}
   \  Log  ${path}
   \  ${csv_data}=  Csv Parser Get Data  ${path}
   \  Log List  ${csv_data}
   \  List Should Contain Value  ${csv_data['Unknown']}  1

Tvh1214938c

    [Documentation]  User able to see the results(enteries) in ascending order with proper data \n
    ...  link: http://tims.cisco.com/warp.cmd?ent=Tvh1214938c
    [Tags]    Tvh1214938c  sdr  srts

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Set Aliases For Appliance Libraries
    Set Appliance Under Test To SMA

    Restart CLI Session
    Wait Until Keyword Succeeds   5m   15s   Diagnostic Reporting Delete DB
    Diagnostic Reporting Delete DB      confirm=yes


    Set Appliance Under Test To ESA


    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  ${SENDER2}  1  ${SPAM}  None

    Set Appliance Under Test To ESA
    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  ${SENDER1}  1  ${SPAM}  None

    Wait Until Keyword Succeeds
   ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
   ...  Verify Message Count
   ...  2
   ...  Unknown

    Wait Until Keyword Succeeds
   ...  ${DATA_UPDATE_TIMEOUT}  ${RETRY_TIME}
   ...  Verify Message Tracking


Tvh1194336c

    [Documentation]  Verify that user able to view the columns SDR Category, \n
    ...  desc and Messages counter data under "Summary of Messages by SDR Threat Category" chart. \n
    ...  link: http://tims.cisco.com/warp.cmd?ent=Tvh1194336c
    [Tags]    Tvh1194336c  sdr  srts

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Set Aliases For Appliance Libraries
    Set Appliance Under Test To SMA
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes

    Set Aliases For Appliance Libraries
    Set Appliance Under Test To ESA

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  domain@aechk.com  1  ${SPAM}  None

    Set Aliases For Appliance Libraries
    Set Appliance Under Test To SMA
    ${res}=  Wait Until Keyword Succeeds   25m   15s   Reports Parse
    ...  page=Email, Reporting, Sender Domain Reputation
    ...  name=Summary of Messages handled by SDR
    Log  ${res}

   Navigate To  Email  Reporting  Sender Domain Reputation
   ${start_time}=  Get Time
   Click Element  ${XPATH_SDR_THREAT_CATEGORY_TABLE}  don't wait
   ${path}=  Wait Until Keyword Succeeds  20m  10s
   ...  Wait For Download  .csv  start_time=${start_time}  timeout=600
        ...  download_directory=%{SARF_HOME}/tmp
   Log  ${path}
   ${csv_data}=  Csv Parser Get Data  ${path}
   ${keys_coloumn}=  Get Dictionary Keys  ${csv_data}
   List Should Contain Value  ${keys_coloumn}  Description
   List Should Contain Value  ${keys_coloumn}  Messages
   List Should Contain Value  ${keys_coloumn}  SDR Threat Category
   List Should Contain Value  ${csv_data['SDR Threat Category']}  Spam

Tvh1266519c
    [Documentation]  In SDR reporting, cover all the verdicts.\n
    ...  link:http://tims.cisco.com/warp.cmd?ent=Tvh1266519c

    [Tags]  Tvh1266519c  sdr  srts

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Set Appliance Under Test To SMA

    Restart CLI Session
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes

    Set Aliases For Appliance Libraries
    Set Appliance Under Test To ESA

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  user@ihavebadreputation.com  1  ${SPAM}  None

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  user1@domain.com  1  ${SPAM}  None

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  weak@roughbros.com  1  ${SPAM}  None

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  weak@example.com  1  ${SPAM}  None

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...   Tainted@soften.ktu.lt  1  ${SPAM}  None

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  user123@001sh.net  1  ${SPAM}  None

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  user1@domain.cs27  1  ${SPAM}  None


    Set Appliance Under Test To SMA
    ${res}=  Wait Until Keyword Succeeds   25m   15s   Reports Parse
    ...  page=Email, Reporting, Sender Domain Reputation
    ...  name=Summary of Messages handled by SDR
    Log  ${res}

    ${res1}=  Evaluate
    ...  [x for x in map(lambda x: x if not x.has_key('SDR Category') else None, ${res}) if x is not None]
    Log  ${res1}

    ${var}=   Get From List  ${res1}  2
    ${value}=  Get From Dictionary  ${var}  Poor
    Should Be True  ${value}  >= 0

     ${var}=   Get From List  ${res1}  4
    ${value}=  Get From Dictionary  ${var}  Tainted
    Should Be True  ${value}  >= 0

    ${var}=   Get From List  ${res1}  6
    ${value}=  Get From Dictionary  ${var}  Weak
    Should Be True  ${value}  >= 0

    ${var}=   Get From List  ${res1}  8
    ${value}=  Get From Dictionary  ${var}  Unknown
    Should Be True  ${value}  >= 0

    ${var}=   Get From List  ${res1}  10
    ${value}=  Get From Dictionary  ${var}  Neutral
    Should Be True  ${value}  >= 0

    ${var}=   Get From List  ${res1}  18
    ${value}=  Get From Dictionary  ${var}  Total Message Count
    Should Be True  ${value}  >= 0


Tvh1214952c
    [Documentation]  Verify while doing tracking summary search, \n
    ...  sdr Reputation param in combination with other message events, \n
    ...  results returned should be combination of both message events \n
    ...  To verify the SDR groups/counters with reporting group enabled.
    ...  link: http://tims.cisco.com/warp.cmd?ent=Tvh1214952c
    ...  link: http://tims.cisco.com/warp.cmd?ent=Tvh1194961c
    [Tags]    Tvh1214952c  Tvh1194961c  sdr  srts

    Set Test Variable  ${TEST_ID}  ${TEST_NAME}
    Set Aliases For Appliance Libraries
    Set Appliance Under Test To SMA

    Restart CLI Session
    Diagnostic Tracking Delete DB  confirm=yes
    Diagnostic Reporting Delete DB  confirm=yes
    Centralized Email Reporting Group Add  sdr_group  ${ESA}
    Commit Changes

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  ${SENDER2}  1  ${TESTVIRUS}  None

    Inject And Verify Message   ${TEST_ID}   ${PUBLIC_LISTENER_IP}
    \  ...  ${SENDER1}  1  ${SPAM}  None

   Set Aliases For Appliance Libraries
   Set Appliance Under Test To SMA
   ${res}=  Wait Until Keyword Succeeds   25m   15s   Reports Parse
   ...  page=Email, Reporting, Sender Domain Reputation
   ...  name=Summary of Messages handled by SDR
   Log  ${res}
   ${result_list}=  Email Message Tracking Search
   Log  ${result_list}
   Element Text Should Be  ${XPATH_MESSAGE_TRACKING_FIRST_ROW}       ${SENDER1}
   Element Text Should Be  ${XPATH_MESSAGE_TRACKING_SECOND_ROW}       ${SENDER2}

   Set Aliases For Appliance Libraries
   Set Appliance Under Test To ESA
   Start Cli Session If Not Open
   ${is_enabled}=  External Threatfeeds Is Enabled
   Run Keyword If  not ${is_enabled}
   ...  External Threatfeeds Enable
   Commit Changes
   ETF Domain Reputation Setup  test2
   ETF File Hash
   ETF Url
   Commit Changes

   Null Smtpd Start
   Inject Message  ${PUBLIC_LISTENER_IP}
   ...  --custom-header=myheader:general@${CLIENT},from:general@suppcrt-seourity.esy.es

   Verify Log Contains Records
   ...  search_path=mail
   ...  Info: MID .* Threat feeds source 'test2' detected malicious domain: 'suppcrt-seourity.esy.es' in: Friendly From ==1
   ...  Info: MID .* Custom Log Entry: Malicious Domain Detected ==1

   Inject Messages
   ...  attach-filename=${attachments_dir}/atch_md5_file_1
   ...  num-msgs=1
   ...  inject-host=${PUBLIC_LISTENER_IP}
   ...  rcpt-host-list=${CLIENT}

   Verify Log Contains Records
   ...  search_path=mail
   ...  Info: MID.*Threat feeds source 'test' detected malicious file with MD5: 'e678e49e1a894f625488ba66ec8cc9bd', filename: atch_md5_file_1. Condition: File Hash External Threat Feeds Rule ==1
   ...  MID.*Custom Log Entry: logEntry for AttachmentFileInfo ETF ==1

   Inject Messages  inject-host=${PUBLIC_LISTENER_IP}  num-msgs=1
   ...  rcpt-host-list=${CLIENT}  mail-from=${TEST_NAME}@${CLIENT}
   ...  mbox-filename=${attachments_dir}/url_action.mbox

   Verify Log Contains Records
   ...  search_path=mail
   ...  Info: MID.*Threat feeds source 'test1' detected malicious URL:.*mecrob.cc\\/bot\\/gate.php.* in message body. Action: URL defanged ==1
   ...  Info: MID .* Custom Log Entry: Defang url detected ==3

   Set Appliance Under Test To SMA
   @{source_list}=  Create List  test  test1  test2
   @{ioc_list}=  Create List  File Hash  URL  Domain

   :FOR  ${table}  ${source}  ${col1}  ${col2}  IN
   ...  Summary of External Threat Feeds  ${source_list}  External Threat Feed Sources  Number of Threats Detected
   ...  Indicator of Compromise (IOC) Matches  ${ioc_list}  Indicator of Compromise (IOC)  Number of Threats Detected
   \  Verify Table Data  ${table}  ${source}  ${col1}  ${col2}

   Start Cli Session If Not Open
   SSL Config Gui  versions=All Services  ssl_method=TLSv1.0  confirm=Enable for all services
   Commit

   :FOR  ${chart_name}  IN
   ...   Top External Threat Feed Sources
   ...   Top Indicator of Compromise (IOC) Matches
   \   Email Reporting Check Chart Presence  ${chart_name}

   Navigate To  Email  Message Tracking  Message Tracking

   @{message_event}=  Create List  sender domain reputation  External Threat Feeds
   Run Keyword And Ignore Error  Log Into DUT
   ${results}=  Email Message Tracking Search
   ...  message_event=${message_event}
   Log  ${results}
   ${result_count}=  Email Message Tracking Get Total Result Count
   ...   ${results}
   Should Be True  ${result_count} >= 3
