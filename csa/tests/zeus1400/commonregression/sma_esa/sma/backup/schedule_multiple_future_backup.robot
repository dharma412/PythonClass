# $Id: //prod/main/sarf_centos/tests/zeus1350/postel/regression/common/backup/schedule_multiple_future_backup/schedule_multiple_future_backup.txt#5 $ $DateTime: 2020/03/31 03:20:25 $ $Author: sarukakk $
*** Settings ***
Resource  regression.txt
Suite Setup  DefaultRegressionSuiteSetup
Suite Teardown  DefaultRegressionSuiteTeardown
Test Setup  Schedule Multiple Future Backup Test Case Setup
Test Teardown  Schedule Multiple Future Backup Test Case Teardown
Force Tags  backup.schedule_multiple_future_backup

*** Variables ***

*** Keywords ***
Schedule Multiple Future Backup Test Case Setup
    DefaultRegressionTestCaseSetup

Schedule Multiple Future Backup Test Case Teardown
    Library Order Sma
    Restart Cli Session
    Cancel All Backups
    DefaultRegressionTestCaseTeardown
    ${out}=  Run  rm -rf /tmp/*

Cancel All Backups
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is Completed
    ${out} =  Backup Config View
    FOR  ${i}  IN RANGE  10
      ${line} =  Get Line  ${out}  1
      Run Keyword If  '${line}' == 'No scheduled backups.'  Exit For Loop
      Run Keyword If  '${line}' != 'No scheduled backups.'  Cancel Backup  1
      ${out} =  Backup Config View
    END

Check If Backup Is In Progress
    [Arguments]  ${Backup_Name}
    ${out} =  Backup Config Status
    Should Contain  ${out}  Backup Name: ${Backup_Name}

Check If Backup Is Completed
    ${out} =  Backup Config Status
    Should Contain  ${out}  No backup in progress

Confirm Cancelling
    Write  Y
    ${out} =  Read Until Prompt
    Should Contain  ${out}  has been cancelled.

Cancel Backup
    [Arguments]  ${Backup_Name}
    Start CLI Session
    Backup config cancel  ${Backup_Name}
    Commit

Connect To Sma As Admin
    [Arguments]  ${DUT}
    ${timeout} =  Set SSHLib Timeout  60s
    Set SSHLib Prompt  >
    Start CLI Session
    Open Connection  ${DUT}
    Login  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

*** Test Cases ***
Tvh569936c
    [Tags]  Tvh569936c  standard
    [Documentation]  Verify that user can schedule multiple future backups\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh569936c\n
    ...  \n 1. Used the backupconfig -> schedule command to create a multiple future backups
    ...  \n 2. Enter ip address, hostname, username, and password

    Set Test Variable  ${Test_Id}  Tvh569936c
    Set Test Variable  ${Backup_Name1}  single_backup01
    Set Test Variable  ${Backup_Name2}  daily_backup01
    Set Test Variable  ${Backup_Name3}  weekly_backup01
    Set Test Variable  ${Backup_Name4}  monthly_backup01
    ${date} =  Run  echo $(date "+%m/%d/%Y %H:%M:%S" --date="6min")

    Library Order Sma
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=single
    ...  single_date=${date}
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Backup Config Schedule
    ...  job_name=${Backup_Name2}
    ...  backup_type=repeating
    ...  period=daily
    ...  rep_time=12:03
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Backup Config Schedule
    ...  job_name=${Backup_Name3}
    ...  backup_type=repeating
    ...  period=weekly
    ...  day_of_week=friday
    ...  rep_time=18:00
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Backup Config Schedule
    ...  job_name=${Backup_Name4}
    ...  backup_type=repeating
    ...  period=monthly
    ...  day_of_month=28
    ...  rep_time=6:00
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    ${out} =  Backup Config View
    Should Contain  ${out}  ${Backup_Name1}
    Should Contain  ${out}  ${Backup_Name2}
    Should Contain  ${out}  ${Backup_Name3}
    Should Contain  ${out}  ${Backup_Name4}

Tvh569622c
    [Tags]  Tvh569622c  extended
    [Documentation]  Verify that user can schedule two daily backups\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh569622c\n
    ...  \n 1. Used the backupconfig -> schedule command to create two daily backups
    ...  \n 2. Enter ip address, hostname, username, and password

    Set Test Variable  ${Test_Id}  Tvh569622c
    Set Test Variable  ${Backup_Name1}  daily_backup02_1
    Set Test Variable  ${Backup_Name2}  daily_backup02_2

    Library Order Sma
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=repeating
    ...  period=daily
    ...  rep_time=8:00
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Backup Config Schedule
    ...  job_name=${Backup_Name2}
    ...  backup_type=repeating
    ...  period=daily
    ...  rep_time=22:00
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    ${out} =  Backup Config View
    Should Contain  ${out}  ${Backup_Name1}
    Should Contain  ${out}  ${Backup_Name2}

Tvh569953c
    [Tags]  Tvh569953c  extended
    [Documentation]  Verify that scheduled future backups will execute properly at the scheduled time\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh569953c\n
    ...  \n 1. Used the backupconfig -> schedule command to create a multiple future backups
    ...  \n 2. Enter ip address, hostname, username, and password

    Set Test Variable  ${Test_Id}  Tvh569953c
    Set Test Variable  ${Backup_Name1}  single_backup03
    Set Test Variable  ${Backup_Name2}  daily_backup03
    Set Test Variable  ${Backup_Name3}  weekly_backup03
    Set Test Variable  ${Backup_Name4}  monthly_backup03

    Library Order Sma
    ${date} =  Run  echo $(date +"%m/%d/%Y %H:%M:%S")
    Set Time Set  ${date}
    Library Order Sma2
    ${date} =  Run  echo $(date +"%m/%d/%Y %H:%M:%S")
    Set Time Set  ${date}
    Library Order Sma

    ${scheduled_date} =  Run  echo $(date -v +4M "+%m/%d/%Y %H:%M")
    ${scheduled_time} =  Run  echo $(date -v +5M "+%H:%M")
    ${started_date} =  Run  date "+%d %b %Y"
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=single
    ...  single_date=${scheduled_date}:00
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Sleep  2m  #wait for scheduled time
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is In Progress  ${Backup_Name1}
    ${out} =  Backup Config Status
    Should Contain  ${out}  Begin Time: ${started_date} ${scheduled_time}
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is Completed

    ${scheduled_time} =  Run  echo $(date -v +4M "+%H:%M")
    ${started_date} =  Run  date "+%d %b %Y"
    Backup Config Schedule
    ...  job_name=${Backup_Name2}
    ...  backup_type=repeating
    ...  period=daily
    ...  rep_time=${scheduled_time}
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Sleep  2m  #wait for scheduled time
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is In Progress  ${Backup_Name2}
    ${out} =  Backup Config Status
    Should Contain  ${out}  Begin Time: ${started_date} ${scheduled_time}
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is Completed

    ${current_day_of_week} =  Run  date "+%a"
    ${scheduled_time} =  Run  echo $(date -v +4M "+%H:%M")
    ${started_date} =  Run  date "+%d %b %Y"
    Backup Config Schedule
    ...  job_name=${Backup_Name3}
    ...  backup_type=repeating
    ...  period=weekly
    ...  day_of_week=${current_day_of_week}
    ...  rep_time=${scheduled_time}
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Sleep  2m  #wait for scheduled time
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is In Progress  ${Backup_Name3}
    ${out} =  Backup Config Status
    Should Contain  ${out}  Begin Time: ${started_date} ${scheduled_time}
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is Completed

    ${current_day_month} =  Run  date "+%d"
    ${scheduled_time} =  Run  echo $(date -v +4M "+%H:%M")
    ${started_date} =  Run  date "+%d %b %Y"
    Backup Config Schedule
    ...  job_name=${Backup_Name4}
    ...  backup_type=repeating
    ...  period=monthly
    ...  day_of_month=${current_day_month}
    ...  rep_time=${scheduled_time}
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Sleep  2m  #wait for scheduled time
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is In Progress  ${Backup_Name4}
    ${out} =  Backup Config Status
    Should Contain  ${out}  Begin Time: ${started_date} ${scheduled_time}
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is Completed

Tvh569988c
    [Tags]  Tvh569988c  standard
    [Documentation]  Verify that CLI command VIEW can see all scheduled backups\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh569988c\n
    ...  \n 1. Used the backupconfig -> schedule command to create a multiple future backups
    ...  \n 2. Enter ip address, hostname, username, and password
    ...  \n 3. Used the VIEW command line to see all scheduled backups

    Set Test Variable  ${Test_Id}  Tvh569988c
    Set Test Variable  ${Backup_Name1}  single_backup04
    Set Test Variable  ${Backup_Name2}  daily_backup04
    ${date} =  Run  echo $(date "+%m/%d/%Y %H:%M:%S" --date="6min")

    Library Order Sma
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=single
    ...  single_date=${date}
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Backup Config Schedule
    ...  job_name=${Backup_Name2}
    ...  backup_type=repeating
    ...  period=daily
    ...  rep_time=12:03
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    ${out} =  Backup Config View
    Should Contain  ${out}  ${Backup_Name1}
    Should Contain  ${out}  ${Backup_Name2}

Tvh570121c
    [Tags]  Tvh570121c  standard
    [Documentation]  Verify that when one backup is in progress, any backup which tried to begin will cancelled and send a warning to admin\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh570121c\n
    ...  \n 1. Used the backupconfig -> schedule command to create a multiple future backups
    ...  \n 2. Enter ip address, hostname, username, and password
    ...  \n 3. Once one backup is in progress, start another backup immediately

    Set Test Variable  ${Test_Id}  Tvh570121c
    Set Test Variable  ${Backup_Name1}  single_backup05
    Set Test Variable  ${Backup_Name2}  weekly_backup05
    Set Test Variable  ${Alert_Email}  test_email@${CLIENT_HOSTNAME}

    Library Order Sma
    Null Smtpd Start
    ${date} =  Run  echo $(date +"%m/%d/%Y %H:%M:%S")
    Set Time Set  ${date}
    Alert Config New  ${Alert_Email}  1
    Commit

    ${scheduled_date} =  Run  echo $(date "+%m/%d/%Y %H:%M" --date="3min")
    ${scheduled_time} =  Run  echo $(date "+%H:%M" --date="3min")
    ${started_date} =  Run  date "+%d %b %Y"
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=single
    ...  single_date=${scheduled_date}:30
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    ${current_day_of_week} =  Run  date "+%a"
    Backup Config Schedule
    ...  job_name=${Backup_Name2}
    ...  backup_type=repeating
    ...  period=weekly
    ...  day_of_week=${current_day_of_week}
    ...  rep_time=${scheduled_time}
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=Yes

    Sleep  2m  #wait for scheduled time
    Wait Until Keyword Succeeds  2 min  1 sec  Check If Backup Is In Progress  ${Backup_Name2}
    Wait Until Keyword Succeeds  5 min  1 sec  Check If Backup Is Completed

    ${out} =  Backup Config View
    Should Not Contain  ${out}  ${Backup_Name1}

    FOR  ${msg}  IN RANGE  5
      ${msg} =  Null Smtpd Next Message  timeout=40  string=${True}
      ${status}  ${value} =  Run Keyword And Ignore Error  Should Contain  ${msg}  BACKUP: (${Backup_Name2}) is in progress, skipping (${Backup_Name1})
      Run Keyword If  '${status}' == 'PASS'  Exit For Loop
    END
    Run Keyword Unless  '${status}' == 'PASS'  Fail  ${value}

    Null Smtpd Stop

Tvh569636c
    [Tags]  Tvh569636c  extended
    [Documentation]  Verify that user can schedule daily backup after initial backup\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh569636c\n

    Set Test Variable  ${Test_Id}  Tvh569636c
    Set Test Variable  ${Backup_Name1}  immediate_backup06
    Set Test Variable  ${Backup_Name2}  daily_backup06

    Library Order Sma
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=now
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    Backup Config Schedule
    ...  job_name=${Backup_Name2}
    ...  backup_type=repeating
    ...  period=daily
    ...  rep_time=12:03
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    ${out} =  Backup Config View
    Should Contain  ${out}  ${Backup_Name1}
    Should Contain  ${out}  ${Backup_Name2}

Tvh569481c
    [Tags]  Tvh569481c  extended
    [Documentation]  Verify that user can cancel scheduled backup by selecting number of the backup\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh569481c\n

    Set Test Variable  ${Test_Id}  Tvh569481c
    Set Test Variable  ${Backup_Name1}  single_backup07

    Library Order Sma
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=single
    ...  single_date=1/1/2015 11:11:11
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    ${out} =  Backup Config View
    Should Contain  ${out}  ${Backup_Name1}

    Cancel Backup  1

    ${out} =  Backup Config View
    Should Not Contain  ${out}  ${Backup_Name1}

Tvh569731c
    [Tags]  Tvh569731c  extended
    [Documentation]  Verify that backup Name and IP address are displayed properly\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh569731c\n

    Set Test Variable  ${Test_Id}  Tvh569731c
    Set Test Variable  ${Backup_Name1}  weekly_backup08

    Library Order Sma
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=repeating
    ...  period=weekly
    ...  day_of_week=friday
    ...  rep_time=18:00
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    ${out} =  Backup Config View
    Should Contain  ${out}  ${Backup_Name1}
    Should Contain  ${out}  ${SMA2_IP}

Tvh569819c
    [Tags]  Tvh569819c  extended
    [Documentation]  Verify that SMA should not allow scheduling more than one backup to the same target SMA starting at the same time of the day\n
    ...  link:  http://tims.cisco.com/warp.cmd?ent=Tvh569819c\n

    Set Test Variable  ${Test_Id}  Tvh569819c
    Set Test Variable  ${Backup_Name1}  daily_backup09_1
    Set Test Variable  ${Backup_Name2}  daily_backup09_2

    Library Order Sma
    Backup Config Schedule
    ...  job_name=${Backup_Name1}
    ...  backup_type=repeating
    ...  period=daily
    ...  rep_time=12:03
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=Yes
    ...  backup_reporting=No
    ...  backup_slbl=No

    ${msg_error} =   Run Keyword And Expect Error  *  Backup Config Schedule
    ...  job_name=${Backup_Name2}
    ...  backup_type=repeating
    ...  period=daily
    ...  rep_time=12:03
    ...  ip=${SMA2_IP}
    ...  name=${SMA2}
    ...  user=${DUT_ADMIN}
    ...  passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  backup_all=No
    ...  backup_isq=No
    ...  backup_email_tracking=No
    ...  backup_web_tracking=No
    ...  backup_reporting=Yes
    ...  backup_slbl=No
    Should Contain  ${msg_error}  A repeating backup with the same schedule already exists
