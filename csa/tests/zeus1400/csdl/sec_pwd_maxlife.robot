# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_pwd_maxlife.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      BuiltIn
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${error_message_reset_passphrase_more}          //div[@id='password_expiration_period_error_div']//following::span[text()='more']
${error_message_reset_passphrase_more_popup}    //div[contains(text(),'Value must be an integer from')]
${error_message_close_popup}                    //a[contains(.,'Close')]
${expiration_message_text}                      //div[@class='banner_alert_message']
${message_reset_display_reminder_error}         integer from 1 to 3650.
${default_reset_passphrase_days}                90

*** Keywords ***
Verify value range error for password reset rules
    Click Element  ${error_message_reset_passphrase_more}
    Sleep  3
    ${text} =  Get Text  ${error_message_reset_passphrase_more_popup}
    Should match regexp   ${text}  .*${message_reset_display_reminder_error}.*
    Click Element  ${error_message_close_popup}

Verify passphrase expiration message
    [Arguments]  ${expiration_message}
    ${text} =  Get Text  ${expiration_message_text}
    Should match regexp   ${text}  .*${expiration_message}.*

*** Test Cases ***
Tvh1340973c
    [Documentation]  Tvh1340973c-SEC-PWD-MAXLIFE: Allow administrative passphrase lifetime limit
        ...  FLOW DETAILS
        ...  Login to SMA GUI
        ...  System Administration -> users.
        ...  Local User Account & Passphrase Settings -> click Edit settings.
        ...  Select checkbox - Require a passphrase reset whenever a user's passphrase is set or changed by an admin (Recommended),
        ...  Verify default value of 'Require users to reset passphrases after __ days' as 90
        ...  Verify boundary value of 'Require users to reset passphrases after __ days'
        ...  Select checkbox - Require users to reset passphrases after __ days.-Select between 1 and 3650
        ...  Click 'submit' button
        ...  Setting saved successfully

    [Tags]  gui  Tvh1340973c
    [Teardown]  Run keywords  Users Edit Reset Rules  password_expiration=${default_reset_passphrase_days}
    ...  AND  Commit Changes
    ...  AND  Users edit reset rules disable  admin_change=off  password_expiration=off
    ...  AND  Commit Changes

    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ${actual_default_passphrase_days}=  Users get reset passphrase days
    Should be equal  ${actual_default_passphrase_days}  ${default_reset_passphrase_days}
    Run keyword and ignore error  Users Edit Reset Rules  password_expiration=-1
    Verify value range error for password reset rules
    Run keyword and ignore error  Users Edit Reset Rules  password_expiration=0
    Verify value range error for password reset rules
    Run keyword and ignore error  Users Edit Reset Rules  password_expiration=4000
    Verify value range error for password reset rules
    Users Edit Reset Rules  password_expiration=3650
    Users Edit Reset Rules  password_expiration=1
    Commit Changes
    Verify passphrase expiration message  .*Your local passphrase will expire on.*At this date you will be forced to change your passphrase on log in.*