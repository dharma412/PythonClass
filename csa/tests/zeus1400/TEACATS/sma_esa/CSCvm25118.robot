# $Id: //prod/main/sarf_centos/tests/zeus1350/common_regression_tests/TEACATS/sma_esa/CSCvm25118.txt#2 $ $DateTime: 2020/04/30 21:33:26 $ $Author: sumitada $

*** Settings ***
Library           SmaGuiLibrary
Library           Collections
Resource          sma/global_sma.txt
Resource          regression.txt

Suite Setup   Run Keywords
              ...  Set Aliases For Appliance Libraries
              ...  Set Appliance Under Test to SMA
              ...  global_sma.DefaultTestSuiteSetup

Suite Teardown   global_sma.DefaultTestSuiteTeardown

*** Variables ***

*** Keywords ***

Close SSH connection
   Set SSHLib Prompt  ${Empty}
   SSHLibrary.Close Connection

*** Test Cases ***

Tvh1231017c
    [Documentation]  Hermes crash during checkpoint start
    ...  1. Generate Hermes cores
    ...  2. Check if core files contain memcpy and not fpickle
    ...  http://tims/view-entity.cmd?ent=1231017
    [Tags]  srts  teacat  CSCvm25118  Tvh1231017c
    [Teardown]  Close SSH connection

    Set Test Variable  ${TEST_ID}  Tvh1231017c
    Set TestVariable   ${mthd}     import _fpickle\ndef test_room():\n${SPACE*4}data = 'a'\n${SPACE*4}while True:\n${SPACE*8}print len(data)\n${SPACE*8}_fpickle.fpickle(data)\n${SPACE*8}data = data + data\ntest_room()
    ${address} =  Get Host IP By Name  ${DUT}
    Copy File To DUT  %{SARF_HOME}/tests/testdata/sma/gdb  /data
    SSHLibrary.Open Connection    ${address}
    Set SSHLib Prompt  ]
    SSHLibrary.Login    ${RTESTUSER}    ${RTESTUSER_PASSWORD}
    Set SSHLib Prompt  >
    Write  telnet /tmp/hermes.bd
    Read Until Prompt
    Write  ${mthd}\n
    Set SSHLib Prompt  ]
    Set SSHLib Timeout  60 seconds
    Write  \n\n
    Read Until Prompt
    ${out}=  SSHLibrary.Execute Command    ls /data/cores
    ${out1}=  CATENATE  SEPARATOR=  /data/cores/  ${out}
    ${out2}=  SSHLibrary.Execute Command    find /data -name hermes | head -n 1
    ${output}=  CATENATE  ${out2}  ${out1}
    Write  chmod 777 /data/gdb
    Write  /data/gdb ${output}
    Set SSHLib Prompt  (gdb)
    Read Until Prompt
    Write  set pagination off
    Read Until Prompt
    Write  bt
    ${backtrace}  Read Until Prompt
    Should Contain  ${backtrace}  fpickle
    Should Not Contain  ${backtrace}  memcpy
    Write  q
    Set SSHLib Prompt  ]
    Write  rm -rf ${out1}
    Read Until Prompt
    Set SSHLib Prompt  ${EMPTY}
