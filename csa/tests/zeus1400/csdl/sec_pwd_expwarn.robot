# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_pwd_expwarn.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Library      BuiltIn
Library      String
Resource     sma/global_sma.txt
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${error_message_reset_passphrase_more}          //div[@id='password_expiration_period_error_div']//following::span[text()='more']
${error_message_reset_display_reminder_more}    //div[@id='password_expiration_warning_period_error_div']//following::span[text()='more']
${error_message_reset_graceperiod_more}         //div[@id='password_grace_period_error_div']//following::span[text()='more']
${error_message_reset_passphrase_more_popup}    //div[contains(text(),'Value must be an integer from')]
${error_message_close_popup}                    //a[contains(.,'Close')]
${expiration_message_text}                      //div[@class='banner_alert_message']
${message_reset_passphrase_error}               integer from 1 to 3650.
${message_reset_display_reminder_error}         integer from 1 to 3650.
${message_reset_grace_period_error}             integer from 0 to 3650.

*** Keywords ***
Verify value range error for password reset rules
    Verify error message  ${error_message_reset_passphrase_more}  ${message_reset_passphrase_error}
    Verify error message  ${error_message_reset_display_reminder_more}  ${message_reset_display_reminder_error}
    Verify error message  ${error_message_reset_graceperiod_more}  ${message_reset_grace_period_error}

Verify error message
    [Arguments]  ${error_message_element}  ${error_message}

    Click Element  ${error_message_element}
    Sleep  3
    ${text} =  Get Text  ${error_message_reset_passphrase_more_popup}
    Should match regexp   ${text}  .*${error_message}.*
    Click Element  ${error_message_close_popup}

Verify passphrase expiration message
    [Arguments]  ${expiration_message}
    ${text} =  Get Text  ${expiration_message_text}
    Should match regexp   ${text}  .*${expiration_message}.*

*** Test Cases ***
Tvh1340969c
    [Documentation]  Tvh1340969c-SEC-PWD-EXPWARN: Warn of impending passphrase expiration
        ...  FLOW DETAILS
        ...  Login to SMA GUI
        ...  System Administration -> users.
        ...  Local User Account & Passphrase Settings -> click Edit settings.
        ...  Select checkbox - Require a passphrase reset whenever a user's passphrase is set or changed by an admin (Recommended),
        ...  Select checkbox - Require users to reset passphrases after __ days.-Select between 1 and 3650
        ...  Select checkbox - Display reminder __ days before expiration.-Select between 1 and 3650
        ...  Select checkbox - Allow a grace period of __ days to reset the passphrase after the passphrase expiry.--Between 0 and 3650
        ...  Click 'submit' button
        ...  Setting saved successfully

    [Tags]  gui  Tvh1340969c
    [Teardown]  Run keywords  Users edit reset rules disable  admin_change=off  password_expiration=off
    ...  AND  Commit Changes

    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Run keyword and ignore error  Users Edit Reset Rules  admin_change=on  password_expiration=-1  display_reminder=-5  grace_period=-5
    Verify value range error for password reset rules
    Run keyword and ignore error  Users Edit Reset Rules  admin_change=on  password_expiration=4000  display_reminder=4000  grace_period=4000
    Verify value range error for password reset rules
    Users Edit Reset Rules  admin_change=on  password_expiration=1  display_reminder=1  grace_period=0
    Commit Changes
    Users Edit Reset Rules  password_expiration=3650  display_reminder=3650  grace_period=3650
    Commit Changes
    Users Edit Reset Rules  admin_change=on  password_expiration=5  display_reminder=5  grace_period=0
    Commit Changes
    Verify passphrase expiration message  .*Your local passphrase will expire on.*At this date you will be forced to change your passphrase on log in.*