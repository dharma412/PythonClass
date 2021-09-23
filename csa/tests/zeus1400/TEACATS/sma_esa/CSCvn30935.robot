# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/TEACATS/sma_esa/CSCvn30935.txt#2 $ $DateTime: 2020/04/30 21:33:26 $ $Author: sumitada $

*** Settings ***
Library    SmaGuiLibrary
Library    Collections
Library    String
Resource   sma/global_sma.txt
Resource   regression.txt
Resource   licensesmart_common.txt

Suite Setup          global_sma.DefaultTestSuiteSetup
Suite Teardown       global_sma.DefaultTestSuiteTeardown

*** Variables ***

*** Keywords ***

Close SSH connection
   Set SSHLib Prompt  ${Empty}
   SSHLibrary.Close Connection

*** Test Cases ***

Tvh1256663c
    [Documentation]  Diagnostic deletedb does not delete enough
    ...  http://tims/view-entity.cmd?ent=1256663
    ...  Go to sma reporting/incoming_queue
    ...  Generate data files in that folder
    ...  Run diagnostic deletedb
    ...  Check if there are no files present in data/pub/reporting/incoming_queue
    ...  Check if there are no files present in data/db/reporting/export_files
    [Tags]  srts  teacat  Tvh1256663c
    [Teardown]  Close SSH connection

    Set Test Variable  ${TEST_ID}  Tvh1256663c
    Selenium Login
    Centralized Email Reporting Enable
    Commit Changes
    Copy File To DUT  %{SARF_HOME}/tests/testdata/sma/file_gen.sh  /data/pub/reporting/incoming_queue/
    ${crtl_c}   Evaluate    chr(int(3))
    ${address}=  Get Host IP By Name  ${DUT}
    SSHLibrary.Open Connection  ${address}
    Set SSHLib Prompt  ]
    SSHLibrary.Login    ${RTESTUSER}    ${RTESTUSER_PASSWORD}
    Write  chmod 777 /data/pub/reporting/incoming_queue/file_gen.sh
    Read Until Prompt
    Write  cd /data/pub/reporting/incoming_queue
    Read Until Prompt
    Write  ./file_gen.sh
    Sleep  20s
    Write Bare  ${crtl_c}
    Read Until Prompt
    Write  ls | wc -l
    ${out}=  Read Until Prompt
    ${match}=   Evaluate  re.search('(\\d+)', '''${out}''').group(1)  re
    Should Be True  ${match} > 5000
    Diagnostic Reporting Delete DB  confirm=yes
    Write  ls | wc -l
    ${out}=  Read Until Prompt
    ${match}=   Evaluate  re.search('(\\d+)', '''${out}''').group(1)  re
    Should Be True  ${match} == 0
    Write  cd /data/db/reporting/export_files
    Read Until Prompt
    Write  ls | wc -l
    ${out}=  Read Until Prompt
    ${match}=   Evaluate  re.search('(\\d+)', '''${out}''').group(1)  re
    Should Be True  ${match} == 0
    Set SSHLib Prompt  ${EMPTY}
