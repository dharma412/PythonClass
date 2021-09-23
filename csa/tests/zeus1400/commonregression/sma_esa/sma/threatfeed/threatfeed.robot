*** Settings ***
Resource     esa/injector.txt
Resource     regression.txt
Resource     sma/esasma.txt
Resource     esa/global.txt
Resource     sma/global_sma.txt
Resource     sma/reports_keywords.txt
Resource     esa/logs_parsing_snippets.txt

Suite Setup  Initialize Suite
Suite Teardown  Finalize Suite

*** Variables ***

${threatfeed_feeds_test_file_dir}=   /data/threatfeeds/test_stix_pkg
${feeds_dir}=  %{SARF_HOME}/tests/testdata/esa/threatfeed/feeds
${threatfeed_log_fetching}=   Info: THREAT_FEEDS: 0 observables were fetched from the source:
${TIMEOUT}  90
${http_source}=         hailataxii
${http_hostname}=       hailataxii.com
${http_pollpath}=       /taxii-data
${http_collection}=     guest.Abuse_ch
${http_port}=           80
${NO_DATA_IMAGE_MD5}=                5432ae167562581bff63ba0f6d615143
${firefox_prefs_browser.download.dir}=                          %{SARF_HOME}/tmp
${firefox_prefs_browser.download.folderList}=                   2
${firefox_prefs_browser.download.manager.showWhenStarting}=     false
${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}=        application/pdf,text/csv
${MD5_HASH}=  e678e49e1a894f625488ba66ec8cc9bd
${FILEHASHLIST_MD5_NAME}=  list_md5
${FILEHASHLIST_MD5_DESC}=  list_md5 description
${attachments_dir}=  %{SARF_HOME}/tests/testdata/esa/threatfeed/attachments
${WEB_HOSTNAME}                      v2.beta.sds.cisco.com

*** Keywords ***

Initialize Suite
    DefaultRegressionSuiteSetup

    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Enable Feature Key  ETF

    Run Keyword If  ${USE_SMART_LICENSE} == 1
    ...  Threatfeedconfig setup  use_etf=yes  custom_header=yes  header_name=etf_header  header_content=false
	
    Set Appliance Under Test to ESA
    Set Manifest Server
    Wait Until Keyword Succeeds  300s  30s  Check Ec Status
    Common SetUp

    ${is_enabled}=  External Threatfeeds Is Enabled
    Run Keyword If  not ${is_enabled}
    ...  External Threatfeeds Enable
    Commit Changes

    Null Smtpd Start

    Admin Access Config Timeout
    ...  timeout_webui=720
    ...  timeout_cli=720
    Log Config Edit  mail_logs    log_level=4
    Log Config Edit  threatfeeds  log_level=4
    Commit
    Run On Dut   mkdir ${threatfeed_feeds_test_file_dir}

Common SetUp
    Set Aliases For Appliance Libraries
    Set Appliance Under Test to SMA
    Run Keyword And Ignore Error  Log Out Of DUT
    Log Into DUT
    Centralized Email Reporting Enable
    Centralized Email Message Tracking Enable
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  reporting=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Network Access Edit Settings  ${TIMEOUT}
    Commit Changes
    Start Cli Session If Not Open
    Run keyword And Ignore Error  Diagnostic Tracking Delete DB  confirm=yes
    Run keyword And Ignore Error  Diagnostic Reporting Delete DB  confirm=yes
    Commit

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
    Commit Changes
    Start Cli Session If Not Open
    Run keyword And Ignore Error  Diagnostic Tracking Delete DB  confirm=yes
    Run keyword And Ignore Error  Diagnostic Reporting Delete DB  confirm=yes
    Reporting Config Setup  enable=yes
    Commit

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

ETF IP Spoofing
    Library Order Esa
    Initialize Spoof
    Run On Dut  mkdir ${threatfeed_feeds_test_file_dir}/hailataxii
    SCP  from_location=%{SARF_HOME}/tests/testdata/esa/threatfeed/feeds/iphat.xml
    ...  to_location=${threatfeed_feeds_test_file_dir}/hailataxii/
    ...  to_host=${ESA}

    Add Threatfeed Source
    ...  ${http_source}
    ...  ip source
    ...  ${http_hostname}
    ...  ${http_pollpath}
    ...  ${http_collection}

    Sender Group ETF Config
    Listenerconfig Edit Hostaccess Edit Sendergroup Move  InboundMail
    ...  BLOCKED_LIST  etf-source: hailataxii  1
    Commit

Finalize Suite
    Library Order Esa
    Run On Dut  rm -r ${threatfeed_feeds_test_file_dir}/test2
    Run On Dut  rm -r ${threatfeed_feeds_test_file_dir}/hailataxii
    Run On Dut  rm -r ${threatfeed_feeds_test_file_dir}/test
    Run On Dut  rm -r ${threatfeed_feeds_test_file_dir}/test1
    Listenerconfig Edit Hostaccess Reset  InboundMail
    Run Keyword And Ignore Error  Filters Delete  filter=my_filter_action
    Commit
    Content Filter Delete  Incoming  my_filter
    Delete File Hash List  ${FILEHASHLIST_MD5_NAME}
    Delete Content Filter Through GUI  md5_cf  Incoming
    Delete Content Filter Via GUI  md5_cf
    External Threatfeeds Source Delete   test2
    External Threatfeeds Source Delete   hailataxii
    External Threatfeeds Source Delete   test
     Run Keyword And Ignore Error  External Threatfeeds Source Delete   test1
    Url Filtering Disable
    Commit Changes
    Uninitialize Spoof
    DefaultRegressionSuiteTeardown

Inject Message
    [Arguments]  ${inject-host}  ${extra_opts}
    Inject Messages  inject-host=${inject-host}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}
    ...  mail-from=general@${CLIENT}
    ...  extra_opts=${extra_opts}

Do Common Testcase Setup
    [Arguments]  ${dest_hosts}=${CLIENT_IP}
    Library Order Esa
    DefaultTestCaseSetup

    EsaCliLibrary.Smtp Routes New  domain=.${NETWORK}
    ...  dest_hosts=${dest_hosts}
    Commit

    Null Smtpd Start  max-msgs-per-conn=5
    Roll Over Now  mail_logs

Do Common Testcase Teardown
    Library Order Esa
    Start CLI Session If Not Open
    EsaCliLibrary.Smtp Routes Delete  domain=.${NETWORK}
    Commit

    Null Smtpd Stop

    DefaultTestCaseTeardown

Initialize Spoof
    SCP  from_location=%{SARF_HOME}/tests/testdata/esa/threatfeed/spoof/ipspoof
    ...  to_location=/data/pub/
    ...  to_host=${ESA}
    @{set_spoof_script}=  Create List
    ...  import spoof_smtp_session as I
    ...  I.read_ips("","ipspoof")
    ...  I.install()
    Backdoor Run  hermes  ${set_spoof_script}

Uninitialize Spoof
    @{set_spoof_script}=  Create List
    ...  import spoof_smtp_session as U
    ...  U.remove_ips()
    Backdoor Run  hermes  ${set_spoof_script}

Chart ${name} Should Not Be Empty
    ${chart_md5}=  Email Reporting Charts Get Md5 Hash  ${name}  password=${DUT_ADMIN_SSW_PASSWORD}
    Log  ${chart_md5}
    ${result}  ${msg}=  Run Keyword And Ignore Error
    ...  Should Not Be Equal As Strings  ${chart_md5}  ${NO_DATA_IMAGE_MD5}
    # add screenshot into log if checksum of empty chart and existing one aren't equal
    Run Keyword If  '${result}' == 'FAIL'  Capture Screenshot
    Run Keyword If  '${result}' == 'FAIL'  Fail  ${msg}

Sender Group ETF Config
    ${sources_list}  Create List  hailataxii
    HAT Sender Group Edit Settings  InBoundMail  BLOCKED_LIST
    ...  etf_add_sources=${sources_list}
    Commit Changes

Parse Report
    ${res}=  Reports Parse
    ...  page=Monitor, External Threat Feeds
    ...  name=Summary of External Threat Feed Sources by incoming mail connections
    ...  result_as_dictionary=${True}
    ...  use_normalize=${True}
    Log Dictionary  ${res}
    ${res}=  Reports Parse  name=Summary of External Threat Feed Sources by incoming mail connections
    ${var} =  Get From List  ${res}  0
    ${value} =  Get From Dictionary  ${var}  Total Connections
    Log  ${value}
    Should Be Equal  ${value}  1

Add File Hash List
    [Arguments]  ${name}  ${description}  ${hashes}  ${type}
    ${list1_settings}=  Create Dictionary
    ...  Description                       ${description}
    ...  File Hash Type                    ${type}
    ...  File Hash                         ${hashes}
    FileHash Lists Add  ${name}  ${list1_settings}

Delete File Hash List
    [Arguments]  ${name}
    FileHash Lists Delete  ${name}

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

Create Content Filter Through GUI
    [Arguments]  ${name}  ${listener_type}  ${should_commit}=${True}
    ${settings}=  Create Dictionary
    ...  Content Filters  Enable Content Filters (Customize settings)
    ...  ${name}   ${True}
    Mail Policies Edit Content Filters  ${listener_type}  default
    ...  ${settings}
    Run Keyword If  ${should_commit}
    ...   Commit Changes

Delete Content Filter Through GUI
    [Arguments]  ${name}  ${listener_type}
    ${settings}=  Create Dictionary
    ...  Content Filters  Disable Content Filters
    Mail Policies Edit Content Filters  ${listener_type}  default
    ...  ${settings}
    Commit Changes

Delete Content Filter Via GUI
    [Arguments]  ${cf_name}
    Content Filter Delete  Incoming  ${cf_name}

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

Disable Antivirus
    [Arguments]  ${av_name}=Sophos
    ${av_state}=  Antivirus Is Enabled  ${av_name}
    Run Keyword If  ${av_state}
    ...  Antivirus Disable  ${av_name}
    Commit Changes

Do Tvh1197579c Teardown
    Library Order Esa
    Delete File Hash List  ${FILEHASHLIST_MD5_NAME}
    Run On Dut  rm -r ${threatfeed_feeds_test_file_dir}/test
    Delete Content Filter Through GUI  md5_cf  Incoming
    Delete Content Filter Via GUI  md5_cf
    External Threatfeeds Source Delete   test
    Commit Changes
    Do Common Testcase Teardown

Verify Drill Down Table
    [Arguments]  ${table_name}  ${col_name_1}  ${ioc_list}
    ${reporting_link}=  Email Report Get Content Link  ${table_name}
    ${col_values}=  Get From Dictionary  ${reporting_link}
    ...  ${col_name_1}
    Log  ${reporting_link}
    :FOR  ${col_value}  IN RANGE  0  3
    \  ${value} =  Get From List  ${col_values}  ${col_value}
    \  ${head} =  Get From List  ${ioc_list}  ${col_value}
    \  Click Element  ${value}
    \  ${attr}=  Evaluate  ${col_value} + 2
    \  ${header} =  Get Text  //table[@class=\'pairs\']/tbody/tr[${attr}]/th
    \  Should Be Equal As Strings  ${header}  ${head}
    \  ${value} =  Get Text  //table[@class=\'pairs\']/tbody/tr[${attr}]/td/span
    \  Should Be Equal As Integers  ${value}  1
    \  Navigate To  Email  Reporting  External Threat Feeds

Verify Redirected Table
    [Arguments]  ${table_name}  ${col_name_1}  ${col_list}  ${src_list}
    ${reporting_link}=  Email Report Get Content Link  ${table_name}
    ${col_values}=  Get From Dictionary  ${reporting_link}
    ...  ${col_name_1}
    Log  ${reporting_link}
    :FOR  ${col}  IN RANGE  0  3
    \  ${value} =  Get From List  ${col_values}  ${col}
    \  Click Element  ${value}
    \  ${ioc_value} =  Get From List  ${col_list}  ${col}
    \  Sleep  5s
    \  ${value} =  Get Text  //table[@class='report_subsection']//div[@id='ss_0_0_0']//table[@summary]/tbody[2]/tr[1]/td[1]/div/span
    \  ${count} =  Get Text  //table[@class='report_subsection']//div[@id='ss_0_0_0']//table[@summary]/tbody[2]/tr[1]/td[2]/div/span
    \  Should Be Equal As Strings  ${value}  ${ioc_value}
    \  Should Be Equal As Integers  ${count}  1
    \  ${src_value} =  Get From List  ${src_list}  ${col}
    \  ${value} =  Get Text  //table[@class='report_subsection']//div[@id='ss_0_2_0']//table[@summary]/tbody[2]/tr[1]/td[1]/div/span
    \  ${count} =  Get Text  //table[@class='report_subsection']//div[@id='ss_0_2_0']//table[@summary]/tbody[2]/tr[1]/td[2]/div/span
    \  Should Be Equal As Strings  ${value}  ${src_value}
    \  Should Be Equal As Integers  ${count}  1
    \  Verify Export Data For Charts  ${col}
    \  Navigate To  Email  Reporting  External Threat Feeds

Verify Export Data For Charts
    [Arguments]  ${col}
    ${start_time}=  Get Time
    Click Element  xpath=//td[@id='ss_0_1_0-links']/span  don't wait
    ${path}=  Wait Until Keyword Succeeds  10m  10s
    ...  Wait For Download  .csv  start_time=${start_time}  timeout=180
    ...  download_directory=%{SARF_HOME}/tmp
    Set Test Variable  ${path}
    Log  ${path}
    Find And Verify CSV Report  %{SARF_HOME}/tmp  *Threat*
    ...  @{expected_value${col}}
    Remove File  ${path}

Find And Verify CSV Report
    [Arguments]  ${dir}  ${file_pattern}  @{key_value_pairs}
    ${file_names}=  OperatingSystem.List Files In Directory
    ...  ${dir}  ${file_pattern}
    Log  ${file_names}
    ${csv_report_file_path}=  OperatingSystem.Join Path
    ...  ${dir}  ${file_names[0]}
    ${csv_data}=  Csv Parser Get Data  ${csv_report_file_path}
    Log  ${csv_data}
    :FOR  ${key}  ${value}  IN  @{key_value_pairs}
    \   List Should Contain Value  ${csv_data['${key}']}  ${value}

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

ETF Url
    Url Filtering Enable
    Commit Changes

    ${status}  Url Filtering Get Details
    Log  ${status}
    ${result}  ${msg}=  Run Keyword And Ignore Error
    ...  Should Contain  ${status}  Connected
    ${string}=  Convert To String  ${status}
    Log  ${string}
    ${result}  ${msg}=  Run Keyword And Ignore Error
    ...  Should Contain  ${string}  Connected
    
    Log  ${result}
    Log  ${msg}

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

Do Tvh1197582c Teardown
    Library Order Esa
    Run On Dut  rm -r ${threatfeed_feeds_test_file_dir}/test
    Filters Delete  filter=my_filter_action
    Commit
    External Threatfeeds Source Delete   test
    Commit Changes
    Url Filtering Disable
    Commit Changes
    Do Common Testcase Teardown

Do Websecurity Config
    Websecurityadvancedconfig  web_hostname=${WEB_HOSTNAME}
    Commit
    
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

Tvh1197571c
    [Documentation]  ETF for Domain Reputation
    ...  http://tims.cisco.com/view-entity.cmd?ent=1197571
    [Tags]  Tvh1197571c  standard
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    ETF Domain Reputation Setup  test2
    ETF File Hash
    ETF Url
    Roll Over Now  mail_logs

    Inject Message  ${PUBLIC_LISTENER_IP4}
    ...  --custom-header=myheader:general@${CLIENT},from:general@suppcrt-seourity.esy.es

    Verify Log Contains Records
    ...  search_path=mail
    ...  Info: MID .* Threat feeds source 'test2' detected malicious domain: 'suppcrt-seourity.esy.es' in: Friendly From ==1
    ...  Info: MID .* Custom Log Entry: Malicious Domain Detected ==1

    Inject Messages
    ...  attach-filename=${attachments_dir}/atch_md5_file_1
    ...  num-msgs=1
    ...  inject-host=${PUBLIC_LISTENER_IP4}
    ...  rcpt-host-list=${CLIENT}

    Verify Log Contains Records
    ...  search_path=mail
    ...  Info: MID.*Threat feeds source 'test' detected malicious file with MD5: 'e678e49e1a894f625488ba66ec8cc9bd', filename: atch_md5_file_1. Condition: File Hash External Threat Feeds Rule ==1
    ...  MID.*Custom Log Entry: logEntry for AttachmentFileInfo ETF ==1

    Inject Messages  inject-host=${PUBLIC_LISTENER_IP4}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=Tvh1196124c@${CLIENT}
    ...  mbox-filename=${attachments_dir}/url_action.mbox

    Verify Log Contains Records
    ...  search_path=mail
    ...  Info: MID.*Threat feeds source 'test1' detected malicious URL:.*mecrob.cc\\/bot\\/gate.php.* in message body. Action: URL defanged ==1
    ...  Info: MID .* Custom Log Entry: Defang url detected ==3

    Library Order Sma
    Selenium Login
    @{source_list}=  Create List  test  test1  test2
    @{ioc_list}=  Create List  File Hash  URL  Domain

    :FOR  ${table}  ${source}  ${col1}  ${col2}  IN
    ...  Summary of External Threat Feeds  ${source_list}  External Threat Feed Sources  Number of Threats Detected
    ...  Indicator of Compromise (IOC) Matches  ${ioc_list}  Indicator of Compromise (IOC)  Number of Threats Detected
    \  Verify Table Data  ${table}  ${source}  ${col1}  ${col2}

    :FOR  ${chart_name}  IN
    ...   Top External Threat Feed Sources
    ...   Top Indicator of Compromise (IOC) Matches
    \   Email Reporting Check Chart Presence  ${chart_name}
    Selenium Close

Tvh1197573c
    [Documentation]
    ...  http://tims.cisco.com/view-entity.cmd?ent=1197573
    [Tags]  Tvh1197573c  standard
    [Setup]  Do Common Testcase Setup
    [Teardown]  Do Common Testcase Teardown

    ETF IP Spoofing
    Roll Over Now  mail_logs
    Inject Messages  inject-host=${PUBLIC_LISTENER_IP4}  num-msgs=1
    ...  rcpt-host-list=${CLIENT}  mail-from=Tvh1197571c@${CLIENT}

    Verify Log Contains Records
    ...  search_path=mail
    ...  Info: ICID .* REJECT SG BLOCKED_LIST match etf-source: hailataxii SBRS .* ==1

    Wait Until Keyword Succeeds
    ...  3 min
    ...  30 sec
    ...  Parse Report

    Library Order Sma
    Selenium Login
    Verify Summary Table Data Connections
    ...  Summary of External Threat Feed Sources by incoming mail connections  hailataxii  External Threat Feed Sources  Total Connections
    Email Reporting Check Chart Presence
    ...  Top External Threat Feed Sources by incoming mail connections
    Selenium Close

Tvh1197579c
    [Documentation]
    ...  http://tims/view-entity.cmd?ent=1197579
    [Tags]  Tvh1197579c  standard

    Library Order Sma
    Selenium Login

    @{ioc_list}=  Create List  File Hash  URL  Domain
    Wait until keyword succeeds  10m  2m  Verify Drill Down Table  Summary of External Threat Feeds  External Threat Feed Sources  ${ioc_list}
    Selenium Close

Tvh1197582c
    [Documentation]
    ...  http://tims/view-entity.cmd?ent=1197582
    [Tags]  Tvh1197582c  standard

    Library Order Sma
    Close Browser
    Selenium Login With Autodownload Enabled  ${firefox_prefs_browser.download.dir}  ${firefox_prefs_browser.helperApps.neverAsk.saveToDisk}

    @{expected_value0}=  Create List
    ...  External Threat Feed Sources  test
    ...  Number of Threats Detected    1

    @{expected_value1}=  Create List
    ...  External Threat Feed Sources  test1
    ...  Number of Threats Detected    1

    @{expected_value2}=  Create List
    ...  External Threat Feed Sources  test2
    ...  Number of Threats Detected    1

    Set Test Variable  @{expected_value0}
    Set Test Variable  @{expected_value1}
    Set Test Variable  @{expected_value2}

    @{col_list}=  Create List  ${MD5_HASH}  http://mecrob.cc/bot/gate.php  suppcrt-seourity.esy.es        
    @{src_list}=  Create List  test  test1  test2
    Wait until keyword succeeds  10m  2m  Verify Redirected Table  Indicator of Compromise (IOC) Matches  Indicator of Compromise (IOC)  ${col_list}  ${src_list}
    Selenium Close
