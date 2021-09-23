*** Settings ***
Resource     sma/global_sma.txt
Resource     regression.txt
Resource     sma/csdlresource.txt
Resource     sma/config_masters.txt
Library      Process
Force Tags   csdl

Suite Setup     Burp Suite Start
Suite Teardown  Burp Suite End

*** Keywords ***
Burp Suite Start
    Library Order SMA
    Set Up Selenium Environment
    Configure Proxy For Browser
    ...  http:127.0.0.1:8080, ssl:127.0.0.1:8080, ftp:127.0.0.1:8080
    Run  rm -rf Integris*.html
    ${command}=  Catenate  java -jar -Djava.awt.headless\=true
    ...  -Xmx2g /home/testuser/BurpSuitePro/burpsuite_pro.jar https ${DUT}
    ...  443 / --user-config-file=/home/testuser/carbonator/user.json
    ${handle} =  Process.Start Process  ${command}  shell=True  alias=example
    Sleep  15
    Start Burp
    Process.Process Should Be Running
    global_sma.DefaultTestSuiteSetup

Burp Suite End
    Process.Process Should Be Running
    ${result}=  Wait For Process  timeout=1800  on_timeout=kill
    Log  ${result.stdout}
    Should Contain  ${result.stdout}  Closing Burp
    ${result}=  Run  find . -name "*Integris*.html"
    ${stripped}=  Replace String  ${result}  ./  ${EMPTY}
    ${path}=  Join Path  %{SARF_HOME}  ${stripped}
    Log  ${path}
    ${high_value}=  Get High Value  ${path}
    Should Be Equal As Numbers  ${high_value}  0
    global_sma.DefaultTestSuiteTeardown

*** Test Cases ***

Tvh1319386c
    [Documentation]  Verify XSS vulnerability for all tabs in SMA GUI of http://tims.cisco.com/view-entity.cmd?ent=1301408
    [Tags]  Tvh1319386c  burp  csdl
    [Setup]  Run keywords   Centralized Web Configuration Manager Enable
    ...  AND  Commit Changes
    ...  AND  Set CMs
    ...  AND  Configuration Masters Initialize    ${sma_config_masters.${CM}}  {True}
    ...  AND  Commit Changes

    ${web_crawler_status}=  Run  cd %{SARF_HOME}/tools/sma/web_crawler/ && python web_crawler.py --dut-hostname=${DUT} --dut-username=${DUT_ADMIN} --dut-password=${DUT_ADMIN_SSW_PASSWORD} --timeout=1800 --wait-for-page-to-load=True --get-page-loading-time=True
    Log  ${web_crawler_status}
