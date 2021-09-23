# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/sec_ntp_auth3.txt#3 $
# $Date: 2020/11/06 $
# $Author: mrmohank $

*** Settings ***
Library         Collections
Resource        sma/global_sma.txt
Resource        sma/csdlresource.txt

Force Tags          csdl
Suite Setup         CSDL Suite Setup
Suite Teardown      CSDL Suite Teardown

*** Variables ***
${WRONG_NTP_KEY_ID}         2
${WRONG_NTP_KEY_VALUE}      Wrongpass
${sntpd_log_path}           /data/pub/sntpd_logs/sntpd.current

*** Test Cases ***
Tvh1340823c
    [Documentation]  Tvh1340823c-Support NTPv3 authentication
    [Tags]  gui  cli  Tvh1340823c

    #    1. Login to GUI
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    #    2. Go to System Administration > Time Settings.
    #    3. Click on Edit Settings > Select Radio button "Use Network Time Protocol"
    #    4. Enter the wrong details for Key Number,Key Value for NTP server
    Time Settings Edit Settings  ntp  ntp_servers=${NTP_SERVER}  ntp_authentication=True  key_numbers=${WRONG_NTP_KEY_ID}  key_passes=${WRONG_NTP_KEY_VALUE}

    #    5. Click on Submit and Commit the changes.
    Commit Changes

    #    6. Verify in logs for failure- Packet truncated
    Wait until keyword succeeds  5 min  1 min  Verify logs  ${sntpd_log_path}  .*Warning: network error during ntp query IP ${NTP_SERVER_IP}: packet truncated.*

    #    7. Go to System Administration > Time Settings.
    #    8. Click on Edit Settings > Select Radio button "Use Network Time Protocol"
    #    9. Enter the correct details for NTP Server,Key Number,Key Value
    Time Settings Edit Settings  ntp  ntp_servers=${NTP_SERVER}  ntp_authentication=True  key_numbers=${NTP_KEY_ID}  key_passes=${NTP_KEY_VALUE}

    #   10. Click on Commit the Changes.
    Commit Changes

    #    11. Verify in logs /data/pub/sntpd_logs/sntpd_logs.current.
    Wait until keyword succeeds  5 min  1 sec  Verify logs  ${sntpd_log_path}  .*sntp authentication host ${NTP_SERVER_IP} key number ${NTP_KEY_ID}.*
    Wait until keyword succeeds  5 min  1 sec  Verify logs  ${sntpd_log_path}  .*adjust: time_const: [0-9]+ offset: .*[0-9]+us next_poll: [0-9]+.*