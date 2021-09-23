*** Settings ***
Resource     esa/global.txt
Resource     esa/logs_parsing_snippets.txt
Resource     esa/injector.txt
Resource     regression.txt

*** Variables ***
${NETWORK_INFO_IP}=  195.66.178.61

*** Keywords  ***
Securex Suite Setup

    Set Aliases For Appliance Libraries
    Set Appliance Under Test to ESA
    Selenium Login

    DefaultTestSuiteSetup

    ${ESA_PUB_LISTENER}=  Get ESA Listener
    Set Suite Variable  ${ESA_PUB_LISTENER}
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    ${ESA_PR_LISTENER_IP}=  Get ESA Private IP
    Set Suite Variable  ${ESA_PR_LISTENER_IP}

    Interfaceconfig Edit  Management
    ...  api_http=yes  api_https=yes
    commit

    RAT Recipient Edit  InBoundMail   All  action=Accept
    Message Tracking Enable
    commit Changes

    Admin Access Config Timeout
    ...  timeout_webui=1440
    ...  timeout_cli=1440
   
    Run Keyword If  ${USE_SMART_LICENSE} == 0
    ...  Run Keywords
    ...  Feature Key Set Key  amp_file_rep  duration=2592000
    ...  AND  Feature Key Set Key  amp_file_analysis  duration=2592000

    Ampconfig Case Setup
    ...  use_malware_protection=yes
    ...  use_malware_file_analysis=yes

    ${amp_dict}=  advancedmalware params get
    ...  enable_file_analysis=YES  edit_action_file_analysis=YES
    Policyconfig Edit Advancedmalware Enable
    ...  Incoming
    ...  DEFAULT
    ...  ${amp_dict}

    ${update_server}=  Get Update Server
    Update Config Dynamichost  dynamic_host=${update_server}
    Diagnostic Reporting Delete DB  confirm=yes
    Diagnostic Tracking Delete DB  confirm=yes
    Commit

    Graymail Enable

    ${gm_settings}=  Create Dictionary
    ...  Graymail Detection  Use Graymail Detection
    ...  Enable Marketing Email Scanning            Yes
    ...  Enable Social Networking Email Scanning    Yes
    ...  Enable Bulk Email Scanning                 Yes

    Mail Policies Edit Graymail
    ...  incoming
    ...  default
    ...  ${gm_settings}

    ${dest1}  Create Dictionary  destination  /dev/null  priority  0  port  25

    Smtp Routes Edit
    ...  All Other Domains
    ...  smtproutes=${dest1}

    Commit Changes

    Null Smtpd Start

    NGGuiLibrary.Launch Dut Browser
    NGGuiLibrary.Login Into Dut
    NGGuiLibrary.Securex Login  APJC  ${APJC_CLIENT_ID}  ${APJC_CLIENT_SECRET}

Securex Suite Teardown

    NGGuiLibrary.Close Browser

    Update Config Dynamichost  dynamic_host=${DEFAULT_UPDATER}
    Ampconfig Case Setup
    ...  use_malware_protection=no
    ...  use_malware_file_analysis=no
    Smtp Routes Delete  domain=ALL
    Commit
    ${gm_settings}=  Create Dictionary
    ...  Graymail Detection  Disable Graymail Detection
    Mail Policies Edit Graymail  incoming  default  ${gm_settings}
    Graymail Disable
    Commit Changes

    DefaultTestSuiteTeardown

Securex Testcase Teardown

    NGGuiLibrary.Securex Go To Home
    NGGuiLibrary.Securex Collapse Widget
    NGGuiLibrary.Select Reports  Mail Flow Summary
    DefaultTestCaseTeardown

Get Spoof Ip Address
    [Arguments]  ${lookup_record}  ${search_path}=mail  ${timeout}=60
    [Documentation]  Return Ip Address value from record.\n
    ...  *Parameters*:\n
    ...  - `lookup_record`: The pattern to grep Ip Address value from.\n
    ...  - `search_path`: Optional. Sets the `search_path` parameter in `Log Search` keyword.\n
    ...  - `timeout`: Optional. Sets the `timeout` parameter in `Log Search` keyword.\n
    ...  *Example*:\n
    ...  ${ip_addr}=  Get Spoof Ip Address  address .* reverse dns host .* verified
    ${matches}  ${found}=  Log Search  ${lookup_record}  search_path=${search_path}  timeout=${timeout}
    Should Be True  ${matches} >= 1
    ${record}  Get From List  ${found}  0
    ${address}=  Evaluate  re.search('address (?P<address>\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3})', """${record}""").group(1)  modules=re
    ${host}=  Evaluate  re.search('host (?P<host>.*) verified', """${record}""").group(1)  modules=re
    LogMany  ${host}
    ${list}=  Evaluate  '${host}'.split(".")
    ${domain}=  Evaluate  (".").join(${list[-2:]})
    [Return]  ${address}  ${domain}

Obtain SHA From Amp Logs
    ${search_this}=  Set Variable  sha256
    ${matches}  ${output}=  Log Search  ${search_this}  search_path=amp_logs  timeout=120
    Log  ${output}
    ${matching_log_line}=  Get From List  ${output}  0
    @{log_line_split}=  Split String  ${matching_log_line}  sha256 =
    Log  ${log_line_split}

    ${log_line_split1}=  Get From List  ${log_line_split}  1
    @{log_line_split2}=  Split String  ${log_line_split1}  ,
    Log  ${log_line_split2}

    ${sha_1}=  Get From List  ${log_line_split2}  0
    ${sha}=  Replace String  ${sha_1}  ${SPACE}  ${EMPTY}

    Log  ${sha}
    [Return]  ${sha}

Enable Ip Spoofing

    ${fname}=  Smtp Session Spoof Prepare Ips File  ip_addr=${NETWORK_INFO_IP}
    Smtp Session Spoof Enable  ${ESA_PUB_LISTENER.name}  ${fname}
