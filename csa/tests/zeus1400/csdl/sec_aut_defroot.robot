# $Id: //prod/main/sarf_centos/tests/zeus1381/csdl/sec_aut_defroot.txt#2 $
# $Date: 2020/08/25 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/csdlresource.txt

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown
Test Setup      Defroot Test Case Setup
Test Teardown   Defroot Test Case Teardown

*** Variables ***
${demo_certificate_expected_message}             (?s)You are currently using a demo certificate/key for receiving, delivery, HTTPS(.*?)management access, and LDAPS.(.*?)Cisco recommends using a CA trusted certificate.(.*?)Use the certconfig CLI command to import the certificate.
${certconfig_certificate_expected_message}       (?s)Currently using the demo certificate/key for receiving, delivery, HTTPS(.*?)management access, and LDAPS. Cisco recommends using a CA trusted(.*?)certificate.
${welcome_message}                               Welcome
${demo_certificate_popup}                        id=democert_dialog_c
${demo_certificate_message}                      xpath=//div[@id='democert_dialog']/div[2]/div
${demo_certificate_popup_ok}                     xpath=//*[@type="button" and contains(text(), "OK")]
${welcome_message_popup}                         id=confirmation_dialog_h
${welcome_message_popup_ok}                      id=yui-gen24-button
${welcome_popup_message}                         xpath=//div[@id='confirmation_dialog']/div[2]/div
${ca_cert_path}                                  %{SARF_HOME}/tests/testdata/ca.crt
${ca_key_path}                                   %{SARF_HOME}/tests/testdata/ca.key
${username_element}                              name=username
${password_element}                              name=password
${loginbutton_element}                           name=action:Login

*** Keywords ***
Defroot Test Case Setup
    ${certconfig_options}=  Cert config options
    ${certconfig_clearstatus}=  Run keyword and return status  Should not match regexp  ${certconfig_options}  .*CLEAR.*
    Run keyword if  '${certconfig_clearstatus}'=='False'  Run keywords  Cert config clear certificates  clear=yes  AND  Commit
    Get certificate file and key file  ${ca_cert_path}  ${ca_key_path}
    Admin access config welcome message  message=${welcome_message}
    Commit

Get certificate file and key file
    [Arguments]  ${cert_file_path}  ${cert_key_path}
    ${cert_file}=    OperatingSystem.Get File    ${cert_file_path}
    Set Suite Variable  ${cert_file}
    ${cert_key}=    OperatingSystem.Get File    ${cert_key_path}
    Set Suite Variable  ${cert_key}

Login to SMA
    [Arguments]  ${username}  ${password}

    Input Text  ${username_element}  ${username}
    Input Text  ${password_element}  ${password}
    Click Button  ${loginbutton_element}  Don't wait
    Sleep  5

Defroot Test Case Teardown
    Admin access clear welcome message
    Commit
    Set SSHLib Prompt  ${empty}

Get demo certificate popup status and welcome message status
    [Arguments]  ${username}  ${password}

    Login to SMA  ${username}  ${password}
    ${certificate_popup_status}=  Run keyword and return status  Page Should Contain Element  ${demo_certificate_popup}
    ${certificate_popup_message}=  Run keyword if  '${certificate_popup_status}'=='True'  Get Text  ${demo_certificate_message}
    Run keyword if  '${certificate_popup_status}'=='True'  Click Element  ${demo_certificate_popup_ok}
    ${welcome_message_status}=  Run keyword and return status  Page Should Contain Element  ${welcome_message_popup}
    ${welcome_popup_message}=  Run keyword if  '${welcome_message_status}'=='True'  Get Text  ${welcome_popup_message}
    Run keyword if  '${welcome_message_status}'=='True'  Click Element  ${welcome_message_popup_ok}
    [Return]  ${certificate_popup_message}  ${welcome_popup_message}  ${certificate_popup_status}

Check demo certificate warning message in certconfig
    [Arguments]  ${warning}=${None}
    ${demo_certificate_message}=  Cert config options
    Run keyword if  '${warning}'=='True'  Should match regexp  ${demo_certificate_message}  ${certconfig_certificate_expected_message}
    ...  ELSE  Should not match regexp  ${demo_certificate_message}  ${certconfig_certificate_expected_message}

*** Test Cases ***
Tvh1435225c
    [Documentation]
    ...  Tvh1435225c- Check whether correct warning message is getting displayed when we login to cli for the first time login(ATTACH TEST REPORT)
    ...  Tvh1435229c- Check whether correct welcome message and warning message  is getting displayed when we login to cli for the first time login

    [Tags]  cli  Tvh1435225c  Tvh1435229c

    # Step 1. Connect to SMA
    # Step 2. Enter CLI mode
    # Step 3. Check demo certificate warning message
    # Step 4. Check demo certificate welcome message
    Connect to SMA  ${RTESTUSER}  ${RTESTUSER_PASSWORD}
    ${cli_session_user_message}=  Enter option and wait till expected condition  cli  >
    Should match regexp  ${cli_session_user_message}  ${demo_certificate_expected_message}
    Should match regexp  ${cli_session_user_message}  (?s)${welcome_message}

Tvh1435226c
    [Documentation]
    ...  Tvh1435226c- Check whether demo certification warning is seen when 'certconfig' command is entered
    ...  Tvh1435228c- Check whether after addition of the custom certificate from the certconfig command via cli, we are getting the warning message or not
    ...  Tvh1435300c- Check whether after clearing custom certificate from the Setup section in cli we get demo certificate message again
    ...  Tvh1435236c- Check that proper warning message is displayed
    ...  Tvh1435227c- Check whether after addition of the custom certificate from the certconfig command via gui, we are getting the warning message or not
    ...  Tvh1435306c- Check whether after clearing custom certificate we get demo certificate message again
    ...  Tvh1435234c- Check whether correct welcome message and warning message  is getting displayed when we login to gui for the first time login
    ...  Tvh1435239c- Check whether after addition of the custom certificate from the certconfig command via cli, we are getting the warning message or not

    [Tags]  cli  Tvh1435226c  Tvh1435228c  Tvh1435300c  Tvh1435236c  Tvh1435227c  Tvh1435306c  Tvh1435234c Tvh1435239c

    # Step 1. Go to the CLI prompt of SMA -> cli->certconfig
    # Step 2.  Check demo certificate warning message
    Check demo certificate warning message in certconfig  True

    # Step 3. Add a custom certificate and key using 'Setup' option
    # Step 4. Check Warning message - Warning message for demo certificate should not be displayed.
    Cert Config Setup  ${cert_file}  ${cert_key}  intermediate=no
    Commit
    Check demo certificate warning message in certconfig  False

    # Step 5.  Login to SMA GUI
    # Step 6.  Check demo certificate warning message pop up is not displayed and welcome message is displayed
    ${postsetup_certificate_message}  ${postsetup_welcome_message}  ${postsetup_certificate_popup}=  Get demo certificate popup status and welcome message status  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Should not be true  ${postsetup_certificate_popup}
    Should match regexp  ${postsetup_welcome_message}  ${welcome_message}
    Log Out Of Dut

    # Step 7. Clear the certificate added using the certconfig option
    # Step 8.  Check demo certificate warning message
    Cert config clear certificates  clear=yes
    Commit
    Check demo certificate warning message in certconfig  True

    # Step 9.  Login to SMA GUI
    # Step 10. Check demo certificate warning message pop up is displayed after clearing the certificates
    # Step 11. Check correct welcome message on GUI login
    ${clearsetup_certificate_message}   ${clearsetup_welcome_message}  ${clearsetup_certificate_popup}=  Get demo certificate popup status and welcome message status  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Should be true  ${clearsetup_certificate_popup}
    Should match regexp  ${clearsetup_certificate_message}  ${demo_certificate_expected_message}
    Should match regexp  ${clearsetup_welcome_message}  ${welcome_message}