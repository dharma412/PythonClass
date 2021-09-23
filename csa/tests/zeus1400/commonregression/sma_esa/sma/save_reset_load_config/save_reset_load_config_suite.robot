# $Id: //prod/main/sarf_centos/tests/zeus1350/postel/regression/common/sma_general_functionalities/save_reset_load_config/save_reset_load_config_suite.txt#3 $ $DateTime: 2020/02/11 01:44:48 $ $Author: kathirup $

*** Settings ***
Resource     	  sma/reports_keywords.txt
Resource          regression.txt
Suite Setup       Run Keywords
...  DefaultRegressionSuiteSetup
...  Ignore SSW In Test Case Setup
...  Library Order SMA
Suite Teardown    Run Keywords  DefaultRegressionSuiteTeardown
Test Setup        Run Keywords  DefaultRegressionTestCaseSetup
Test Teardown     Run Keywords  Abandon Changes  DefaultRegressionTestCaseTeardown
Force Tags  common.save_reset_load_config

*** Variables ***
${XML_STR}   <?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE config SYSTEM "config.dtd"><config><update_interval>600</update_interval></config>
${DUT_CONFIG_PATH}   /data/pub/configuration

*** Keywords ***
Ignore SSW In Test Case Setup
    Set Suite Variable   ${SSW}   ${FALSE}

Enable SLBL
    Run Keyword And Ignore Error   Spam Quarantine Enable   port=6025
    Run Keyword And Ignore Error   Spam Quarantine Slbl Enable
    Run Keyword And Ignore Error   Commit Changes

*** Test Cases ***
Tvh569507c
    [Tags]  Tvh569507c   standard
    [Documentation]   Verify that save configuration file works on the appliance via WebUI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh569507c
    ...  \n 1. Navigate to Management Appliance > System Administration > Configuration File page
    ...  \n 2. Save configuration file locally
    ...  \n 3. Save configuration file to the appliance
    ...  \n 4. Email configuration file

    Set TestVariable  ${TEST_ID}    ${TEST NAME}

    #  2. Save configuration file locally
    Selenium Login With Autodownload Enabled   %{SARF_HOME}/tmp   text/xml
    ${start_time}=   Get Time
    Configuration File Download Config
    ${saved_config}  Wait For Download   .xml   start_time=${start_time}  download_directory=%{SARF_HOME}/tmp
    OperatingSystem.File Should Exist   ${saved_config}

    #  3. Save configuration file to the appliance
    ${saved_config_filename}  Configuration File Save Config
    ...   mask_passwd=${True}

    ${out}=     DUT File Exists     ${DUT_CONFIG_PATH}/${saved_config_filename}
    Should Be True     ${out}

    #  4. Email configuration file
    Null Smtpd Start
    Configuration File Email Config
    ...   testuser@${CLIENT_HOSTNAME}
    ${msg} =  Null Smtpd Next Message
    Null Smtpd Stop
    Should Match  "${msg}"  *.xml*

Tvh570222c
    [Tags]  Tvh570222c   standard
    [Documentation]   Verify that save configuration file works on the appliance via CLI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh570222c
    ...  \n 1. Save configuration file to the appliance via CLI

    Set TestVariable  ${TEST_ID}   ${TEST NAME}

    ${saved_config_filename}   Save Config

    ${out}=     DUT File Exists     ${DUT_CONFIG_PATH}/${saved_config_filename}
    Should Be True     ${out}

Tvh569976c
    [Tags]  Tvh569976c   standard
    [Documentation]   Verify that reset configuration works on the appliance via WebUI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh569976c
    ...  \n 1. Navigate to Management Appliance > System Administration > Configuration File page
    ...  \n 2. Preset Reset button

    Set TestVariable   ${TEST_ID}   ${TEST NAME}
    Selenium Login
    Configuration File Reset

Tvh569535c
    [Tags]  Tvh569535c   standard
    [Documentation]   Verify that reset configuration works on the appliance via CLI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh569535c
    ...  \n 1. Run suspend command
    ...  \n 2. Run resetconfig command

    Set TestVariable   ${TEST_ID}   ${TEST NAME}
    Configure SSL For GUI
    Suspend   10
    Reset Config   yes
    Configure SSL For GUI

Tvh570129c
    [Tags]  Tvh570129c   standard
    [Documentation]   Verify that load configuration works on the appliance via WebUI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh570129c
    ...  \n 1. Navigate to Management Appliance > System Administration > Configuration File page
    ...  \n 2. Load configuration file from local computer
    ...  \n 3. Save configuration file to the appliance
    ...  \n 4. Paste configuration in the web form

    Set TestVariable   ${TEST_ID}   ${TEST NAME}

    ${config_filename}   Save Config

    #  2. Load configuration file from local computer
    Copy File From Dut To Remote Machine  ${CLIENT_HOSTNAME}  ${DUT_CONFIG_PATH}/${config_filename}  ${TEMPDIR}
    Run   sudo chmod a+r ${TEMPDIR}/${config_filename}
    Run Keyword And Ignore Error  Selenium Close
    Selenium Login
    Configuration File Upload Config   ${TEMPDIR}/${config_filename}
    Run   sudo rm ${TEMPDIR}/${config_filename}

    #  3. Load configuration file from the appliance
    Configuration File Load Config   ${config_filename}

    #  4. Paste configuration in the web form
    Configuration File Paste Config
    ...   ${XML_STR}

Tvh569518c
    [Tags]  Tvh569518c   standard
    [Documentation]   Verify that load configuration file works on the appliance via CLI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh569518c
    ...  \n 1. Navigate to Management Appliance > System Administration > Configuration File page
    ...  \n 2. Load configuration file to the appliance via CLI

    Set TestVariable   ${TEST_ID}  ${TEST NAME}

    ${config_filename}   Save Config

    Load Config From File   ${config_filename}

    Load Config Via Cli
    ...   ${XML_STR}


Tvh569613c Verify that End-User Safelist/Blocklist Database can be saved via WebUI
    [Tags]  Tvh569613c  extended
    [Documentation]   Verify that End-User Safelist/Blocklist Database can be saved via WebUI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh569613c
    ...  \n 1. Navigate to Management Appliance > System Administration > Configuration File page
    ...  \n 2. Press Backup Now button in SLBL Database section

    Set TestVariable   ${TEST_ID}    Tvh569613c

    Enable SLBL

    ${slbl_backup}   Configuration File Backup Slbl

    ${out}=     DUT File Exists     ${DUT_CONFIG_PATH}/${slbl_backup}
    Should Be True     ${out}

Tvh569735c Verify that End-User Safelist/Blocklist Database can be saved via CLI
    [Tags]  Tvh569735c  extended
    [Documentation]   Verify that End-User Safelist/Blocklist Database can be saved via CLI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh569735c
    ...  \n 1. Run slblconfig command to export all entries to csv file

    Set TestVariable   ${TEST_ID}    Tvh569735c

    Enable SLBL

    ${slbl_export}   Slbl Config Export
    Run Keyword If   '${slbl_export}'=='${None}'   Fail   Export of SlBl database was not finished successfully.

    ${out}=     DUT File Exists     ${DUT_CONFIG_PATH}/${slbl_export}
    Should Be True     ${out}

Tvh570171c Verify that End-User Safelist/Blocklist Database can be restored via WebUI
    [Tags]  Tvh570171c  extended
    [Documentation]   Verify that End-User Safelist/Blocklist Database can be restored via WebUI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh570171c
    ...  \n 1. Navigate to Management Appliance > System Administration > Configuration File page
    ...  \n 2. Press Select File to restore button in SLBL Database section

    Set TestVariable   ${TEST_ID}    Tvh570171c

    Enable SLBL

    Set Test Variable  ${slbl_filename}   slbl.csv

    Copy File To DUT   %{SARF_HOME}/tests/testdata/${slbl_filename}   ${DUT_CONFIG_PATH}

    Configuration File Restore Slbl   ${slbl_filename}

Tvh570247c Verify that End-User Safelist/Blocklist Database can be restored via CLI
    [Tags]  Tvh570247c  extended
    [Documentation]   Verify that End-User Safelist/Blocklist Database can be restored via CLI
    ...  \n link: http://tims.cisco.com/warp.cmd?ent=Tvh570247c
    ...  \n 1. Run slblconfig command to import all entries from csv file

    Set TestVariable   ${TEST_ID}    Tvh570247c

    Enable SLBL

    Set Test Variable  ${slbl_filename}   slbl.csv

    Copy File To DUT   %{SARF_HOME}/tests/testdata/${slbl_filename}   ${DUT_CONFIG_PATH}

    Slbl Config Import   ${slbl_filename}
