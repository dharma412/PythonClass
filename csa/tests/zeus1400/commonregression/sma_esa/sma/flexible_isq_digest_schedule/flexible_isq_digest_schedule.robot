# $Id: //prod/main/sarf_centos/tests/zeus1350/feature_acceptance_tests/flexible_isq_digest_schedule/flexible_isq_digest_schedule.txt#2 $ $DateTime: 2020/07/23 03:24:33 $ $Author: vsugumar $

*** Settings ***
Resource     esa/global.txt
Resource     sma/global_sma.txt
Resource     esa/injector.txt
Resource     esa/logs_parsing_snippets.txt
Resource     esa/backdoor_snippets.txt
Resource     regression.txt
Variables    esa/mbox.py

Suite Setup  Run Keywords
...  Set Aliases For Appliance Libraries
...  Set Appliance Under Test to ESA
...  Initialize Suite
Suite Teardown  Run Keywords
...  Teardown Suite

*** Variables ***
@{ALL_DAYS}=     Mon  Tue  Wed  Thu  Fri  Sat  Sun

*** Keywords ***
Initialize Suite
    Set Appliance Under Test to ESA
    global.DefaultTestSuiteSetup
    ${ESA_PUB_LISTENER_IP}=  Get ESA Public IP
    Set Suite Variable  ${ESA_PUB_LISTENER_IP}
    Euq Enable  ${SMA}  ${SMA_IP}  6025
    Commit Changes

    Set Appliance Under Test to SMA
    global_sma.DefaultTestSuiteSetup
    Spam Quarantine Enable
    ...  interface=Management
    ...  port=6025
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=None
    Security Appliances Add Email Appliance
    ...  ${ESA}
    ...  ${ESA_IP}
    ...  isq=${True}
    ...  ssh_credentials=${DUT_ADMIN}:${DUT_ADMIN_SSW_PASSWORD}
    Commit Changes

    ${ALL_HOURS}=  Evaluate  map('{0:02d}'.format, xrange(24))
    Set Suite Variable  ${ALL_HOURS}

Teardown Suite
    Set Appliance Under Test to SMA
    Security Appliances Delete Email Appliance
    ...  ${ESA}
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${False}
    Spam Quarantine Disable
    Commit Changes
    Clean EUQ
    global_sma.DefaultTestSuiteTeardown

    Set Appliance Under Test to ESA
    Selenium Login
    Euq Disable
    Commit Changes
    global.DefaultTestSuiteTeardown


Get Most Close Schedule Datetime
    [Arguments]  ${min_distance}=2
    ${current_datetime_str}=  EsaCliLibrary.Set Time
    ${current_datetime}=  Evaluate
    ...  datetime.datetime.strptime('${current_datetime_str}', '${GETDTIME_FMT}')
    ...  datetime
    ${current_min_value}=  Set Variable  ${current_datetime.minute}
    ${current_sec_value}=  Set Variable  ${current_datetime.second}
    ${next_hour_expr}=  Catenate
    ...  datetime.datetime.strptime('${current_datetime_str}', '${GETDTIME_FMT}') +
    ...  datetime.timedelta(hours=1) -
    ...  datetime.timedelta(minutes=${current_min_value}, seconds=${current_sec_value})
    ${next_hour_datetime}=  Evaluate  ${next_hour_expr}  datetime
    ${next_2hours_expr}=  Catenate
    ...  datetime.datetime.strptime('${current_datetime_str}', '${GETDTIME_FMT}') +
    ...  datetime.timedelta(hours=2) -
    ...  datetime.timedelta(minutes=${current_min_value}, seconds=${current_sec_value})
    ${next_2hours_datetime}=  Evaluate  ${next_2hours_expr}  datetime
    ${schedule_datetime}=  Set Variable If
    ...  ${current_min_value} + ${min_distance} >= 60
    ...  ${next_2hours_datetime}
    ...  ${next_hour_datetime}
    [Return]  ${schedule_datetime}

Dictionary Should Contain Item
    [Arguments]  ${src_dict}  ${key}  ${value}
    Dictionary Should Contain Key  ${src_dict}  ${key}
    ${src_value}=  Get From Dictionary  ${src_dict}  ${key}
    Should Be Equal  ${src_value}  ${value}

Verify Msg Headers
    [Arguments]  ${msg}  @{headers_and_values}
    Message Load  ${msg}
    ${items}=  Message Items
    Message Unload
    ${items}=  Evaluate
    ...  dict(map(lambda kv: (kv[0], email.header.decode_header(kv[1])[0][0]), ${items}.iteritems()))
    ...  email
    Log Dictionary  ${items}
    FOR  ${header_name}  ${header_value}  IN  @{headers_and_values}
      Dictionary Should Contain Item  ${items}  ${header_name}  ${header_value}
    END

Catch Next Msg And Verify Headers
    [Arguments]  ${timeout}=120  @{headers_and_values}
    ${msg}=  Null Smtpd Next Message  timeout=${timeout}
    Should Not Be Equal As Strings  ${msg}  ${None}
    ...  Notification message has not been received within ${timeout} seconds timeout
    Verify Msg Headers  ${msg}  @{headers_and_values}

Initialize Tvh703549c
    DefaultTestCaseSetup

    ${PREVIOUS_SPEED}=  Set Selenium Speed  0
    Set Test Variable  ${PREVIOUS_SPEED}

Finalize Tvh703549c
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${False}
    Commit Changes

    Set Selenium Speed  ${PREVIOUS_SPEED}

    DefaultTestCaseTeardown

Initialize Tvh703548c
    DefaultTestCaseSetup

    Set Test Variable  ${NOTIFICATION_TITLE}  SQ Notification
    Set Test Variable  ${MIN_DISTANCE}  2

    EsaCliLibrary.Smtp Routes New  domain=.${NETWORK}  dest_hosts=${CLIENT}
    EsaCliLibrary.Commit
    SmaCliLibrary.Smtp Routes New  .${NETWORK}  ${CLIENT}
    SmaCliLibrary.Commit

    Null Smtpd Start

    EsaUtilsLibrary.Sync Time
    SmaUtilsLibrary.Sync Time

    ${settings}=    Create Dictionary
    ...  Anti-Spam Scanning           Use IronPort Anti-Spam service
    ...  Positive Spam Apply Action   Spam Quarantine
    EsaGuiLibrary.Mail Policies Edit Antispam  incoming  default  ${settings}
    EsaGuiLibrary.Commit Changes
    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_fname=From ${SMA}
    ...  spam_notif_subject=${NOTIFICATION_TITLE}
    ...  spam_notif_title=${NOTIFICATION_TITLE}n
    ...  spam_notif_username=supermario
    ...  spam_notif_domain=${CLIENT}
    ...  spam_notif_baddr=mario@${CLIENT}
    ...  spam_notif_freq=daily
    ...  spam_notif_days=${ALL_DAYS}
    ...  spam_notif_hours=${ALL_HOURS}
    ...  submit=${False}
    Commit Changes

    ${notification_datetime}=  Get Most Close Schedule Datetime
    ...  ${MIN_DISTANCE}
    ${notification_year}=  Set Variable  ${notification_datetime.year}
    ${notification_month}=  Set Variable  ${notification_datetime.month}
    ${notification_day}=  Set Variable  ${notification_datetime.day}
    ${notification_hour}=  Set Variable  ${notification_datetime.hour}
    ${datetime_to_set_expr}=  Catenate
    ...  datetime.datetime(year=${notification_year},
    ...  month=${notification_month},
    ...  day=${notification_day},
    ...  hour=${notification_hour}) -
    ...  datetime.timedelta(minutes=${MIN_DISTANCE})
    ${datetime_to_set}=  Evaluate
    ...  ${datetime_to_set_expr}  datetime
    ${datetime_to_set_str}=  Call Method  ${datetime_to_set}
    ...  strftime  ${SETDTIME_FMT}
    EsaCliLibrary.Set Time  ${datetime_to_set_str}
    SmaCliLibrary.Set Time Set  ${datetime_to_set_str}

    ${current_datetime_str}=  EsaCliLibrary.Set Time
    Log  ${current_datetime_str}

    Inject Messages
    ...  mail-from=test@${CLIENT}
    ...  rcpt-host-list=${CLIENT}
    ...  mbox-filename=${mbox.SPAM}
    ...  num-msgs=1
    ...  inject-host=${ESA_PUB_LISTENER_IP}

Finalize Tvh703548c
    Quarantines Spam Edit Notifications
    ...  spam_notif_enable=${False}
    Commit Changes
    ${settings}=  Create Dictionary
    ...  Anti-Spam Scanning   Disabled
    EsaGuiLibrary.Mail Policies Edit Antispam  incoming  default  ${settings}
    EsaGuiLibrary.Commit Changes

    EsaCliLibrary.Smtp Routes Clear
    EsaCliLibrary.Commit
    SmaCliLibrary.Smtp Routes Clear
    SmaCliLibrary.Commit

    EsaUtilsLibrary.Sync Time
    SmaUtilsLibrary.Sync Time

    Null Smtpd Stop

    DefaultTestCaseTeardown

Initialize Tvh703546c
    DefaultTestCaseSetup

    ${PREVIOUS_SPEED}=  Set Selenium Speed  0
    Set Test Variable  ${PREVIOUS_SPEED}

    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_fname=From ${SMA}
    ...  spam_notif_subject=SQ Notification
    ...  spam_notif_title=SQ Notification
    ...  spam_notif_username=supermario
    ...  spam_notif_domain=${CLIENT}
    ...  spam_notif_baddr=mario@${CLIENT}
    ...  spam_notif_freq=daily
    ...  spam_notif_days=Mon
    ...  spam_notif_hours=00
    ...  submit=${False}

*** Test Cases ***
Tvh703548c
    [Documentation]  Verify if notification message is sent at
    ...  correct time as configured under daily spam notification
    [Tags]  Tvh703548c  fat
    [Setup]  Initialize Tvh703548c
    [Teardown]  Finalize Tvh703548c
    Set Test Variable  ${TEST_ID}  Tvh703548c

    Catch Next Msg And Verify Headers  ${${MIN_DISTANCE}*60+90}
    ...  Subject  ${NOTIFICATION_TITLE}

Tvh703549c
    [Documentation]  Verify ISQ_digest notificaton
    ...  can be scheduled for any hour of the day
    [Tags]  Tvh703549c  fat
    [Setup]  Initialize Tvh703549c
    [Teardown]  Finalize Tvh703549c
    Set Test Variable  ${TEST_ID}  Tvh703549c

    @{hours}=  Evaluate  random.sample(${ALL_HOURS}, 3)  random
    FOR  ${hour}  IN  @{hours}
      Spam Quarantine Edit Notification
      ...  spam_notif_enable=${True}
      ...  spam_notif_fname=From ${SMA}
      ...  spam_notif_subject=SQ Notification
      ...  spam_notif_title=SQ Notification
      ...  spam_notif_username=supermario
      ...  spam_notif_domain=${CLIENT}
      ...  spam_notif_baddr=mario@${CLIENT}
      ...  spam_notif_freq=daily
      ...  spam_notif_days=Mon
      ...  spam_notif_hours=${hour}
    END

Tvh703546c
    [Documentation]  Verify if daily option of notification schedule
    ...  has all 24 Hours populated as checkboxes for the user to choose from
    [Tags]  Tvh703546c  fat
    [Setup]  Initialize Tvh703546c
    [Teardown]  Finalize Tvh703549c
    Set Test Variable  ${TEST_ID}  Tvh703546c

    FOR  ${hour}  IN RANGE  24
      ${checkbox_xpath}=  Evaluate
      ...  "xpath=//input[@id='time_picker_{0:02d}00']".format(${hour})
      Page Should Contain Element  ${checkbox_xpath}
      ...  ${hour}-hour checkbox is not present on page but should be present
    END

Tvh703547c
    [Documentation]  Verify if daily option of notification schedule has
    ...  all 7 days of the week listed and user can choose multiple days at once
    [Tags]  Tvh703547c  fat
    [Setup]  Initialize Tvh703549c
    [Teardown]  Finalize Tvh703549c
    Set Test Variable  ${TEST_ID}  Tvh703547c

    FOR  ${sample_number}  IN RANGE  3
      ${days_count_to_sample}=  Evaluate
      ...  random.randint(2, len(${ALL_DAYS}))  random
      ${days_to_select}=  Evaluate
      ...  random.sample(${ALL_DAYS}, ${days_count_to_sample})  random
      Spam Quarantine Edit Notification
      ...  spam_notif_enable=${True}
      ...  spam_notif_fname=From ${SMA}
      ...  spam_notif_subject=SQ Notification
      ...  spam_notif_title=SQ Notification
      ...  spam_notif_username=supermario
      ...  spam_notif_domain=${CLIENT}
      ...  spam_notif_baddr=mario@${CLIENT}
      ...  spam_notif_freq=daily
      ...  spam_notif_days=${days_to_select}
      ...  spam_notif_hours=00
    END

Tvh706494c
    [Documentation]  Verify daily spam notification schedule without any hour selected
    ...  can't be submitted, error message is displayed
    [Tags]  Tvh706494c  srts
    [Setup]  Initialize Tvh703549c
    [Teardown]  Finalize Tvh703549c
    Set Test Variable  ${TEST_ID}  Tvh706494c

    Run Keyword And Expect Error
    ...  *The Settings were not changed*Please select at least one time.
    ...  Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_subject=From ${DUT}
    ...  spam_notif_title=SQ Notification
    ...  spam_notif_username=supermario
    ...  spam_notif_domain=${CLIENT}
    ...  spam_notif_baddr=mario@${CLIENT}
    ...  spam_notif_freq=daily
    ...  spam_notif_days=Mon
    ...  submit=${True}

Tvh706499c
    [Documentation]  Verify all 24 Hrs can be selected at once under daily spam notification schedule
    [Tags]  Tvh706499c  srts
    [Setup]  Initialize Tvh703549c
    [Teardown]  Finalize Tvh703549c
    Set Test Variable  ${TEST_ID}  Tvh706499c

    Spam Quarantine Edit Notification
    ...  spam_notif_enable=${True}
    ...  spam_notif_subject=From ${DUT}
    ...  spam_notif_title=SQ Notification
    ...  spam_notif_username=supermario
    ...  spam_notif_domain=${CLIENT}
    ...  spam_notif_baddr=mario@${CLIENT}
    ...  spam_notif_freq=daily
    ...  spam_notif_days=Mon
    ...  spam_notif_hours=${ALL_HOURS}
    ...  submit=${True}
