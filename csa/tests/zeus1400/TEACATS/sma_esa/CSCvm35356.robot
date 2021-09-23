*** Settings ***
Resource        regression.txt
Resource        esa/injector.txt
Library         BuiltIn
Library         OperatingSystem
Suite Setup     Custom Suite Setup
Suite Teardown  DefaultRegressionSuiteTeardown

*** variables ***
${Listeners_names}  Test_Listeners
${Listeners_type}  public
${Listeners_port}  25
${Listeners_interface}  Management
${Listeners_bounce_profile}  Default
${RAT_action}  Accept
${security_email_name}  ESA_SMA
${REPORTING_GROUP}  testgroup

*** Keywords ***

AMP Test Case Setup
     Centralized Email Reporting Enable
     Listeners Add
     ...  listener_name=${Listeners_names}
     ...  type=${Listeners_type}
     ...  port=${Listeners_port}
     ...  interface=${Listeners_interface}
     ...  bounce_profile=${Listeners_bounce_profile}
     ...  submit=${True}
     RAT Recipient Add
     ...  ${Listeners_names}
     ...  address=${CLIENT}
     ...  action=${RAT_action}
     ${settings}=  Create Dictionary
     ...  Advanced Malware Protection  Yes
     ...  Enable File Analysis  ${True}
     ${settings_antispam}=  Create Dictionary
     ...  Anti-Spam Scanning  Disabled
     ${settings_antivirus}=  Create Dictionary
     ...  Anti-Virus Scanning  No
     Mail Policies Edit Antispam
     ...  Incoming
     ...  Default
     ...  ${settings_antispam}
     Mail Policies Edit Antivirus
     ...  Incoming
     ...  Default
     ...  ${settings_antivirus}
     Commit Changes
     Advancedmalware Enable
     Mail Policies Edit Advanced Malware Protection
     ...  Incoming
     ...  default
     ...  ${settings}
     Message Tracking Enable
     ...   tracking=centralized
     Commit Changes
     Start Cli Session If Not Open
     Diagnostic Reporting Delete Db  confirm=yes
     Wait Until Ready
     Roll Over Now  mail_logs

Custom Suite Setup
     DefaultRegressionSuiteSetup
     @{appliances}  Create List  ESA  ESA2
     FOR  ${appliance}  IN  @{appliances}
        Library Order ${appliance}
        Run Keyword If  ${USE_SMART_LICENSE} == 0
        ...  Add AMP Feature Key
     END
     Threatgrid Rekey Esa Sma
     FOR  ${dut}  IN  ESA  ESA2
        Library Order ${dut}
        AMP Test Case Setup
     END
     Library Order SMA
     ${ESA_IP}=  Get Host IP By Name  ${ESA}
     ${ESA2_IP}=  Get Host IP By Name  ${ESA2}
     Library Order Sma
     Run Keyword And Ignore Error  Log Out of DUT
     Log Into DUT
     Centralized Email Reporting Enable
     Centralized Email Message Tracking Enable
     PVO Quarantines Enable
     Security Appliances Add Email Appliance
     ...  ${security_email_name}
     ...  ${ESA_IP}
     ...  reporting=${True}
     ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
     Security Appliances Add Email Appliance
     ...  ${ESA2}
     ...  ${ESA2_IP}
     ...  reporting=${True}
     ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
     Centralized Email Reporting Group Add  ${REPORTING_GROUP}  ${ESA2}
     Commit Changes
     Start Cli Session If Not Open
     Diagnostic Reporting Delete Db  confirm=yes
     Wait Until Ready
     Diagnostic Tracking Delete Db   confirm=yes
     Wait Until Ready
     ${automatic_migration_settings}=  Create Dictionary
     ...  PQ Migration Mode   Automatic
     Pvo Migration Wizard Run  ${automatic_migration_settings}
     Commit Changes
     ${settings}=  Create Dictionary
     ...  Advanced Malware Protection  Yes
     ...  Enable File Analysis  ${True}
     ...  Include an X-header  ${True}
     ...  Unscannable Actions on Message Errors Apply Action  Quarantine
     ...  Unscannable Actions on Rate Limit Apply Action  Quarantine
     ...  Unscannable Actions on AMP Service Not Available Apply Action  Quarantine
     ...  Messages with File Analysis Pending Apply Action  Quarantine
     ...  Messages with File Analysis Pending Apply Action  Quarantine
     ...  Messages with File Analysis Pending Archive Original  No
     ...  Messages with File Analysis Pending Modify Subject  No
     ...  Messages with File Analysis Pending Add Custom Header  No
     FOR  ${esa}  IN  @{esa_appliances}
       Library Order ${esa}
       Selenium Login
       Wait Until Keyword Succeeds  5m  1m  Pvo Quarantines Enable
       Run Keyword And Ignore Error  Commit Changes
       Mail Policies Edit Advanced Malware Protection  incoming  default  ${settings}
       Commit Changes
     END

Add AMP Feature Key
     ${amp_file_rep_fkey}=  Generate DUT Feature Key  amp_file_rep
     ${amp_file_analysis_fkey}=  Generate DUT Feature Key  amp_file_analysis
     Start Cli Session If Not Open
     Feature Key Activate  ${amp_file_rep_fkey}
     Restart CLI Session
     Feature Key Activate  ${amp_file_analysis_fkey}
     Restart CLI Session

Generate File
     [Arguments]  ${source_file}  ${dest_file}
     ${random}=  Generate Random String
     Log  ${random}
     Convert To String  ${random}
     Run  cat ${source_file} > ${dest_file}
     Run  echo ${random} >> ${dest_file}
     [Return]  ${dest_file}

Close SSH connection
   Set SSHLib Prompt  ${Empty}
   SSHLibrary.Close Connection

Finalize Tvh1231020c
   FOR  ${dut}  IN  ESA  ESA2
      Library Order ${dut}
      Run Keyword And Ignore Error  Log Out Of DUT
      Log Into DUT
      PVO Quarantines Disable
      Commit Changes
   END

***Test Cases***

Tvh1231020c
     [Documentation]  Amp viral emails from SMA, get delivered
     ...   1.  Attach 2 ESA to SMA
     ...   2.  Send AMP Mail to ESA1
     ...   3.  Verify AMP Mail reaches SMA
     ...   4.  Check AMP Mail is not queued for delivery in ESA1
     ...   5.  Verify AMP Mail is not released to  ESA2
     ...   http://tims/view-entity.cmd?ent=1231020
     [Tags]  srts  teacat  CSCvm35356  CSCvq35114  Tvh1231020c  CSCvo71592
     [Teardown]  Finalize Tvh1231020c

     Set Test Variable  ${TEST_ID}  ${TEST NAME}

     ${source}=  Set Variable  %{SARF_HOME}/tests/testdata/esa/advancedmalware/win32server.exe
     ${dest}=  Set Variable  /tmp/file_unknown.exe

     ${exe_file}=  Generate File  ${source}  ${dest}

     Inject Messages
     ...  attach-filename=${exe_file}
     ...  num-msgs=1
     ...  inject-host=${ESA_IP}
     ...  rcpt-host-list=${CLIENT}

     Inject Messages
     ...  attach-filename=${exe_file}
     ...  num-msgs=1
     ...  inject-host=${ESA2_IP}
     ...  rcpt-host-list=${CLIENT}
     Sleep  10s

     Import Library  UtilsLibrary  ${ESA}  WITH NAME  UtilsLibraryESA
     Roll Over Now  mail_logs
     ${matches}  ${found}=  UtilsLibraryESA.Log Search  .*AMP file reputation verdict.*  search_path=mail  timeout=15
     ${mid_esa}=  Run Keyword If  ${matches}!=0  Evaluate  re.search('MID ([0-9]+)', '''${found}''').group(1)  re

     ${matches}  ${found}=  UtilsLibraryESA.Log Search  .*MID ${mid_esa}.*Message.*accepted.*  search_path=mail  timeout=60
     ${mid_smaesa}=  Run Keyword If  ${matches}!=0  Evaluate  re.search('Message ([0-9]+) accepted', '''${found}''').group(1)  re

     Import Library  UtilsLibrary  ${ESA2}  WITH NAME  UtilsLibraryESA2
     Roll Over Now  mail_logs
     ${matches}  ${found}=  UtilsLibraryESA2.Log Search  .*AMP file reputation verdict.*  search_path=mail  timeout=15
     ${mid_esa2}=  Run Keyword If  ${matches}!=0  Evaluate  re.search('MID ([0-9]+)', '''${found}''').group(1)  re

     ${matches}  ${found}=  UtilsLibraryESA2.Log Search  .*MID ${mid_esa2}.*Message.*accepted.*  search_path=mail  timeout=60
     ${mid_smaesa2}=  Run Keyword If  ${matches}!=0  Evaluate  re.search('Message ([0-9]+) accepted', '''${found}''').group(1)  re

     Import Library  UtilsLibrary  ${SMA}  WITH NAME  UtilsLibrarySMA
     Roll Over Now  mail_logs

     Sleep  1m
     Library Order Sma

     ${status}  ${value}=  Run Keyword And Ignore Error
     ...  Pvo Release Policy Message  File Analysis  esa_ip=${ESA_IP}
     Run Keyword If  '${status}'=='FAIL'
     ...  Pvo Release Policy Message  Policy  esa_ip=${ESA_IP}

     ${matches}  ${found}=  UtilsLibrarySMA.Log Search  .*MID ${mid_smaesa} released from quarantine.*  search_path=mail  timeout= 60
     Should Be Equal As Numbers  ${matches}  1
     ${matches}  ${found}=  UtilsLibrarySMA.Log Search  .*MID ${mid_smaesa2} released from quarantine.*  search_path=mail  timeout= 60
     Should Be Equal As Numbers  ${matches}  0

     ${matches}  ${found}=  UtilsLibraryESA.Log Search  .*received from the SMA ${SMA_IP} \\(MID originally ${mid_esa}\\) on release from central quarantine.*  search_path=mail  timeout=15
     Should Be Equal As Numbers  ${matches}  1
     ${matches}  ${found}=  UtilsLibraryESA.Log Search  .*received from the SMA ${SMA_IP} \\(MID originally ${mid_esa2}\\) on release from central quarantine.*  search_path=mail  timeout=15
     Should Be Equal As Numbers  ${matches}  0

     ${matches}  ${found}=  UtilsLibraryESA2.Log Search  .*received from the SMA ${SMA_IP} \\(MID originally ${mid_esa}\\) on release from central quarantine.*  search_path=mail  timeout=15
     Should Be Equal As Numbers  ${matches}  0
     ${matches}  ${found}=  UtilsLibraryESA2.Log Search  .*received from the SMA ${SMA_IP} \\(MID originally ${mid_esa2}\\) on release from central quarantine.*  search_path=mail  timeout=15
     Should Be Equal As Numbers  ${matches}  0

