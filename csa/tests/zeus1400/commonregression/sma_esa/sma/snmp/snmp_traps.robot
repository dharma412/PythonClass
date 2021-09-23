# $Id: //prod/main/sarf_centos/tests/zeus1350/postel/regression/common/sma_general_functionalities/snmp/snmp_traps/snmp_traps.txt#2 $ $DateTime: 2020/03/30 04:14:45 $ $Author: sarukakk $
*** Settings ***
Resource          regression.txt
Suite Setup       DefaultRegressionSuiteSetup
Suite Teardown    DefaultRegressionSuiteTeardown
Test Setup        DefaultRegressionTestCaseSetup
Test Teardown     DefaultRegressionTestCaseTeardown
Force Tags  common.snmp

*** Variables ***

*** Keywords ***
Clear Environment
    Set SSHLib Prompt  ${EMPTY}
    DefaultRegressionTestCaseTeardown
    ${output}  Run  sudo rm -rf ${TEMPDIR}/snmptrapd.conf
    ${output}  Run  sudo rm -rf ${SNMP_TRAP_CONFIG_PATH}
    ${output}  Run  sudo killall -9 snmptrapd
    #Activated once feature key can't be deactiveted that's why
    #we need perform netinstall
    Netinstall  build_id_regex=${SMA_BUILD}  wait_for_ports=80

*** Test Cases ***
Tvh569758c
    [Tags]  Tvh569758c  Standard  invalid_not_applicable_for_smart_license
    [Documentation]  http://tims.cisco.com/warp.cmd?ent=Tvh569758c
    ...  Tvh569758c Verify SMA sends trap to the trap target host
    ...  \n 1. Start snmptrapd on client
    ...  \n 2. Login to the SMA.
    ...  \n 3. Enable snmpconfig and configure it to send traps to client
    ...  \n 4. Add any new feature key for 30 days.
    ...  \n 5. Switch to freebsd machine.
    ...  \n 6. Verify that machine received message about this feature key.
    [Teardown]  Clear Environment

    Set TestVariable  ${TEST_ID}  Tvh569758c

    Snmp Config Setup   enable_snmp=${SNMP_ENABLED}
    ...  ip_interface=${SNMP_IP_INTERFACE}
    ...  snmpv3_passphrase=${SNMP_V3PHRASE}
    ...  snmp_port=${SNMP_PORT}
    ...  snmpv1v2_enabled=${SNMP_V2ENABLED}
    ...  snmpv1v2_community=${SNMP_TRAP_PHRASE}
    ...  snmpv1v2_network=10.0.0.0/8
    ...  trap_target=${CLIENT_IP}
    ...  system_location_string=${SNMP_LOCATION}
    ...  system_contact_string=snmp@localhost
    ...  snmpv3_privacy_passwd=${SNMP_PRIVACY_PASSWORD}
    Commit
    # "Run" keyword can't work with snmptrapd cli command
    # so raw ssh connection is established
    Set SSHLib Timeout  10 seconds
    Set SSHLib Prompt  ${NONE}
    Open Connection  ${CLIENT_HOSTNAME}  client
    Login  ${TESTUSER}  ${TESTUSER_PASSWORD}
    Set SSHLib Prompt  $
    Write  sudo su
    Write  touch ${SNMP_TRAP_CONFIG_PATH}
    Write  echo 'disableAuthorization yes' >${SNMP_TRAP_CONFIG_PATH}
    Write  snmptrapd -m ALL -f -Le -Lf ${TEMPDIR}/snmptrap.log
    Feature Key Set Key  cloud  duration=2592000
    Sleep  4s  give a few seconds for transfering data
    ${output}  Run  cat ${TEMPDIR}/snmptrap.log
    Log  ${output}

    #verifying feature in traps
    ${lines}  Get Lines Matching Pattern    ${output}  *Cloud Administration Mode*

    ${num}   Get Line Count  ${lines}
    Should Not Be Equal As Integers  ${num}  0
    ...  msg=got bad responce. Output: ${output}
