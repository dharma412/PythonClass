*** Settings ***
Resource    sma/reports_keywords.txt
Resource    sma/config_masters.txt

Suite Setup     CustomSuiteSetup
Test Setup      DefaultReportTestCaseSetup
Test Teardown   DefaultReportTestCaseTeardown
Suite Teardown  DefaultReportSuiteTeardown

*** Variables ***
${report_tool}  xpath=//td[@id='report_toolbar']/a

*** Keywords ***
CustomSuiteSetup
    DefaultRegressionSuiteSetup  reset_appliances=${False}
    Set CMs
    DefaultReportSuiteSetup  CM=${CM}

*** Test Cases ***
Tvh1157625c
    [Documentation]  Check pdf links for Users Websites URL.\n
    ...  http://tims/view-entity.cmd?ent=1157625
    [Tags]  srts  teacat  CSCvg91080  Tvh1157625c

    Library Order Sma
    Roll Over Now  gui_logs
    Selenium Login
    @{chklst}  Create List  Users  Web Sites  URL Categories  Application Visibility
    FOR  ${elm}  IN  @{chklst}
         Navigate To  Web  Reporting  ${elm}
         Run Keyword And Ignore Error  Log Into DUT
         Click Element  ${report_tool}  don't wait
         ${out}=  Run on DUT  grep "application fault" /data/pub/gui_logs/gui.current
         Should Be Empty  ${out}
    END
    Selenium Close
