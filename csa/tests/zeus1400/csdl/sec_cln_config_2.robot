# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_cln_config_2.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/global_sma.txt
Resource     regression.txt
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${test_user_admin}              admin_cln_config_2
${test_user_name}               test user
${test_user_admin_password}     Cisco12$
${test_user_group}              Administrator
${alert_email}                  admincln@config2.com
${unsubscribe_email}            unsubscribe@config.com

*** Keywords ***
Setup to create user data
    User Config New  ${test_user_admin}  ${test_user_name}  ${test_user_admin_password}  ${test_user_group}
    Alert Config New  ${alert_email}  1
    Unsubscribe new  ${unsubscribe_email}
    Commit
    ${before_reload_unsubscribe_status}=  Unsubscribe Print Options
    Should match regexp  ${before_reload_unsubscribe_status}  .*PRINT - Display all entries.*
    ${before_reload_user_status}=  User Config Print Options
    Should match regexp  ${before_reload_user_status}  .*${test_user_admin}.*
    Should match regexp  ${before_reload_user_status}  .*${test_user_name}.*
    ${before_reload_alert_status}=  Alert Config Print Alerts
    Should match regexp  ${before_reload_alert_status}  .*${alert_email}.*

Setup DUT after reboot
    Start CLI Session If Not Open
    ${is_restricted}=  Is Admin Cli Restricted
    Run Keyword If  ${is_restricted}
    ...  Passwd
    ...  old_pwd=${DUT_ADMIN_PASSWORD}
    ...  new_pwd=${DUT_ADMIN_TMP_PASSWORD}
    Load License From File

*** Test Cases ***
Tvh1340556c
    [Documentation]  Tvh1340556c-Restore factory configuration to enter clean state
        ...  FLOW DETAILS
        ...  Pre-Condition: Create some config data
        ...  cli -> Diagnostic --> Reload
        ...  Enter ""Y"" for want to continue and really wants to continue
        ...  Do you want to wipe also?[N] --> Y
        ...  Verify system goes to reboot
        ...  Verify that all the data is removed and all the configurations are set to default
        ...  Login to SMA CLI and verify that the config are erased.

    [Tags]  cli  Tvh1340556c
    [Setup]  Setup to create user data

    Diagnostic Reload  confirm=yes  wipedata=yes
    Wait until DUT Is Accessible    wait_for_ports=${DUT_PORT}    timeout=360
    Setup DUT after reboot
    ${after_reload_unsubscribe_status}=  Unsubscribe Print Options
    Should not match regexp  ${after_reload_unsubscribe_status}  .*PRINT - Display all entries.*
    ${after_reload_user_status}=  User Config Print Options
    Should not match regexp  ${after_reload_user_status}  .*${test_user_admin}.*
    Should not match regexp  ${after_reload_user_status}  .*${test_user_name}.*
    ${after_reload_alert_status}=  Alert Config Print Alerts
    Should not match regexp  ${after_reload_user_status}  .*${alert_email}.*