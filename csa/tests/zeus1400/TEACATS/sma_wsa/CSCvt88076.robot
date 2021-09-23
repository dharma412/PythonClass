*** Settings ***
Resource  amp.txt
Resource  regression.txt
Resource  wsa/backdoor_snippets.txt
Resource  sma/config_masters.txt
Suite Setup     Custom Suite Setup
Suite Teardown  DefaultRegressionSuiteTeardown
Test Setup      DefaultTestCaseSetup
Test Teardown   DefaultTestCaseTeardown

*** Variables ***
${custom_amp_policy}  amppolicy
${custom_exe_location}  %{SARF_HOME}/tests/testdata/wsa/amp/${AMP_FILE_NAME}
${custom_file_url}  http://${HTTP_SERVER}/test-data/amp/eicar.com
${AMP_FILE_NAME}    eicar.com
${AMP_FILE_256}     275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f
${AMP_File_Unknown}  %{SARF_HOME}/tests/testdata/wsa/amp/unknown.exe
${AMP_Server_Unknown}   http://${HTTP_SERVER}/test-data/amp/unknown.exe
${AMP_File_name1}   unknown.exe
${PUBLISH_CONFIG}  publish_config.xml
${TEMP_DIR}  /tmp
${CONFIG_PATH}      /data/pub/configuration
${Malicious_path}   //td[@align='left']/table/tbody/tr/td[2]
${custom_blacklist_file}   http://rbms.info/files/dcrm/ms-word-versions/wg6.doc
*** Keyword ***
Custom Suite Setup
     DefaultRegressionSuiteSetup
     Set CMs
     Run Keyword If  ${USE_SMART_LICENSE} == 0
     ...  Add AMP Feature Key
     Threatgrid Rekey Wsa Sma
     Copy File For AMP File Analysis  ${custom_exe_location}
     Reporting Edit  center
     Anti Malware And Reputation Edit Settings
     ...  amp_file_rep=${True}
     ...  amp_file_analysis=${True}
     ...  mcafee=${False}
     ...  sophos=${False}
     ...  webroot=${False}
     #   Edit Global Policy
     Access Policies Add  ${custom_amp_policy}
     Access Policies Edit Anti Malware And Reputation  ${custom_amp_policy}
     ...  amp_file_rep_setting=enable
     ...  amp_known_malicious_action=block
     Commit Changes

     ${WSA_IP}=  Get Host IP By Name  ${WSA}
     Set Suite Variable   ${WSA_IP}
     Library Order SMA
     Selenium Login
     Centralized Web Configuration Manager Enable
     Centralized Web Reporting Enable
     Configuration Masters Initialize    ${sma_config_masters.${CM}}  {True}
     Security Appliances Add Web Appliance
     ...  ${WSA}
     ...  ${WSA_IP}
     ...  reporting=${True}
     ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
     Commit Changes

     Library Order WSA
     Web Proxy Clear Cache

     Clear Reporting Data

Add AMP Feature Key
     ${amp_file_rep_fkey}=  Generate DUT Feature Key  amp_file_rep
     ${amp_file_analysis_fkey}=  Generate DUT Feature Key  amp_file_analysis
     Start Cli Session If Not Open
     Feature Key Activate  ${amp_file_rep_fkey}
     Restart CLI Session
     Feature Key Activate  ${amp_file_analysis_fkey}
     Restart CLI Session

Clear Reporting Data

     Library Order Sma
     Start Cli Session If Not Open
     Diagnostic Reporting Delete Db  confirm=yes
     Diagnostic Tracking Delete Db  confirm=yes
     Wait Until Ready
     Library Order Wsa
     Start Cli Session If Not Open
     Diagnostic Reporting Delete Db  confirm=yes
     Diagnostic Tracking Delete Db  confirm=yes
     Wait Until Ready

Get Amp Summary

     Web Reporting Open   Advanced Malware Protection
     ${table}=   Web Reporting Get Table
                 ...   Incoming files handled by AMP Summary
     log   ${table}
     ${table_length}=  Get Length  ${table}
     Run Keyword If  ${table_length} == 82  Fail
     [Return]   ${table}

Get File Analysis Table

     Web Reporting Open  File Analysis
     ${table}=   Web Reporting Get Table
                  ...   Completed Analysis Requests from This Appliance
     log   ${table}
     ${table_length}=  Get Length  ${table}
     Run Keyword If  ${table_length} == 92  Fail
     [Return]   ${table}

Check Reporting Chart
     Web Reporting Open   Advanced Malware Protection
     Web Reporting Check Chart Presence
     ...   Malicious Files By Category

*** Test Cases ***

CSCvt88076
     [Documentation]    Verify that WSA erroneous data are not displaying indexerror in SMA
     ...   \n 1.Enable Access policy on wsa
     ...   \n 2.Enable  Anti Malware And Reputation on wsa
     ...   \n 3.Enable centralized reporting on wsa
     ...   \n 4.Enable centralized reporting on Sma
     ...   \n 5.Add wsa on the sma
     ...   \n 6.Run the curl command
     ...   \n 7.Verify that Web Tracking Detail displays detect file name, content type, malware name
     ...   \n 8.Copy Wsa erroneous export files to sma
     ...   \n 9.Verify reportd logs does not display Indexerror

     [Tags]   CSCvt88076  teacat
     Set Test Variable  ${TEST_ID}   ${TEST NAME}

     Clear Reporting Data
     Make Requests  proxy=${WSA_IP}:3128  url=${custom_file_url}

     Library Order Sma
     Web Reporting Open   Advanced Malware Protection
     ${table_amp}=   Wait Until Keyword Succeeds
                     ...  30m
                     ...  10s
                     ...  Get Amp Summary
     log   ${table_amp}

     ${result_tracking}=   Web Tracking Search
                           ...   time_range=Day
                           ...   transaction_type=All
     log   ${result_tracking}

     ${tracking_1}=  Get From List  ${result_tracking}  0
     log   ${tracking_1}
     Should Match Regexp  ${tracking_1}  Filename:
     Should Match Regexp  ${tracking_1}  AMP File Verdict: Malicious
     Should Match Regexp  ${tracking_1}  Content Type:
     Should Match Regexp  ${tracking_1}  Malware Threat:

     Import Library  UtilsLibrary  ${SMA}  WITH NAME  UtilsLibrarySMA
     Set Test Variable  ${fpath}  %{SARF_HOME}/tests/testdata/sma/export_files/
     UtilsLibrarySMA.Run On DUT  mkdir -p /data/db/reporting/export_files/1minute
     UtilsLibrarySMA.Copy File To DUT  ${fpath}  /data/db/reporting/export_files/1minute/  -r
     ${matches}  ${found}=  UtilsLibrarySMA.Log Search  .*IndexError.* list index out of range.*  search_path=reportd  timeout=15
     Should Be Equal As Numbers  ${matches}  0
