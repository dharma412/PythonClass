# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_log_statchg.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/csdlresource.txt

Force Tags   csdl
Suite Setup   CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${mail_log_location}            mail_logs
${mail_log_name}                mail
${gui_log_name}                 gui
${gui_log_location}             gui_logs
${authentication_log_name}      authentication
${authentication_log_location}  authentication
${log_files_path}               /data/pub

*** Keywords ***
Pre condition for deleting and adding logs subscription
    [Arguments]  @{log_names}

    FOR  ${logname}  IN  @{log_names}
      Run keyword and ignore error  Log subscriptions delete  ${logname}
    END
    Run keyword and ignore error  Log Subscriptions Add Log  ${sma_log_types.AUTH}  ${authentication_log_name}
    Run keyword and ignore error  Log Subscriptions Add Log  ${sma_log_types.MAIL}  ${mail_log_name}
    Run keyword and ignore error  Log Subscriptions Add Log  ${sma_log_types.HTTP}  ${gui_log_name}

Get log file contents
    [Arguments]  ${log_files_list}  ${logname}  ${log_location}

    ${log_file_name}=  Evaluate  re.search('${logname}..*T[0-9]+.s', """${log_files_list}""").group(0)  modules=re
    ${log_file_cat_command}=  Catenate  cat  ${log_file_name}
    ${log_file_detail_contents}=  Run On DUT  cd ${log_files_path}/${log_location} && ${log_file_cat_command}
    [Return]  ${log_file_detail_contents}

Roll over logs and get log files list
    [Arguments]  ${log_location}  ${log_name}

    Run On DUT  cd ${log_files_path}/${log_location} && rm -rf *.s
    Roll Over Now
    Sleep  2
    ${log_files}=  Run On DUT  cd ${log_files_path}/${log_location} && ls -lrt
    Should match regexp  ${log_files}  .*.s
    [Return]  ${log_files}

Verify log file start and stop messages
    [Arguments]  ${file_contents}

    Should match regexp  ${file_contents}  .*Info: Begin Logfile.*
    Should match regexp  ${file_contents}  .*Info: Version.*
    Should match regexp  ${file_contents}  .*Info: Time offset from UTC.*
    Should match regexp  ${file_contents}  .*Info: Logfile rolled over.*
    Should match regexp  ${file_contents}  .*Info: End Logfile.*

*** Test Cases ***
Tvh1340631c
    [Documentation]  Tvh1340631c-Verify logs are shown to indicate start/stop of a log when a process starts/stops
        ...  FLOW DETAILS
        ...  Start and Stop Logs - Mail logs, Gui logs, Authentication logs
        ...  Verify start and stop of logs in the log files with details like Begin profile, End profile and details

    [Tags]  cli  Tvh1340631c
    [Setup]  Run keywords  Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  AND  Pre condition for deleting and adding logs subscription  ${authentication_log_name}  ${mail_log_name}  ${gui_log_name}
    ...  AND  Commit Changes

    ${authentication_log_files}=  Roll over logs and get log files list  ${authentication_log_location}  ${authentication_log_name}
    ${authentication_log_file_contents}=  Get log file contents  ${authentication_log_files}  ${authentication_log_name}  ${authentication_log_location}
    Verify log file start and stop messages  ${authentication_log_file_contents}
    ${mail_log_files}=  Roll over logs and get log files list  ${mail_log_location}  ${mail_log_name}
    ${mail_log_file_contents}=  Get log file contents  ${mail_log_files}  ${mail_log_name}  ${mail_log_location}
    Verify log file start and stop messages  ${mail_log_file_contents}
    ${gui_log_files}=  Roll over logs and get log files list  ${gui_log_location}  ${gui_log_name}
    ${gui_log_file_contents}=  Get log file contents  ${gui_log_files}  ${gui_log_name}  ${gui_log_location}
    Verify log file start and stop messages  ${gui_log_file_contents}