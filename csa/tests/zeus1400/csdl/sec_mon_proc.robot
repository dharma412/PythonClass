# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_mon_proc.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/global_sma.txt
Resource     regression.txt
Resource     SSHLibrary
Resource     sma/csdlresource.txt

Force Tags   csdl
Suite Setup   CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${top_log_name}  top
${top_log}  /data/log/heimdall/${top_log_name}/${top_log_name}.current

*** Test Cases ***
Tvh1340821c
    [Documentation]  Tvh1340821c-Verify for debugging by TAC/engineers, user can see additional logs under -  "/data/log/heimdall/top logs" to see complete process and its memory consumption
        ...  FLOW DETAILS
        ...  SMA :Goto ->  cd /data/log/heimdall/top
        ...  Get top logs
        ...  Verify logs display complete process and its memory consumption

    [Tags]  cli  Tvh1340821c

    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${top_log}  .*last pid:.*;.*load averages:.*,.*up .*
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${top_log}  .*processes:.*running, .* sleeping.*
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${top_log}  .*Mem: .* Active, .* Inact, .* Wired, .* Buf, .* Free.*
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${top_log}  .*Swap: .* Total, .* Free.*
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${top_log}  .*PID USERNAME.*THR PRI NICE.*SIZE.*RES STATE .*C.*TIME.*WCPU COMMAND.*
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${top_log}  .*extended device statistics.*
    Wait until keyword succeeds  2 min  1 sec  Verify logs  ${top_log}  .*device.*r/s.*w/s.*kr/s.*kw/s qlen svc_t.*%b.*


