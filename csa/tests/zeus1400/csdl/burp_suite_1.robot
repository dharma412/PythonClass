*** Settings ***
Library      Collections
Library      Process
Resource     sma/global_sma.txt
Resource     regression.txt
Force Tags   csdl

Suite Setup  Burp Suite Start
Suite Teardown  Burp Suite End

*** Variables ***

${RADIUS_GROUP_ADMINS}  radadmins
${LDAP_USER_NAME}       ldap_1
${LDAP_CLASS}           ldap_group
${LDAP_PROFILE_NAME}    mainldapprofile
${PWD_ERR_XPATH}        //div[@id="service_hosts[0][shared_secret]_error_div"]/span
${GUEST_NAME}           user1
${GUEST_USER}           user1
${GUEST_PASS}           Ab#124578
${WEB_STATUS_LINK}      //dl[@class="box"]/dd/div/a
${INPUT_USERNAME}       //input[@name='username']
${INPUT_PASSWORD}       //input[@name='password']
${INPUT_LOGIN}          //input[@name='action:Login']

*** Keywords ***

Burp Suite Start
#    Radius Client Connect   ${RADIUS_SERVER}
#    ...  default_secret_str=${RADIUS_SECRET}
#    Radius Client Update Basic User    ${RADIUS_USER}
#    ...  ${RADIUS_USER_PASSWORD}  ${RADIUS_GROUP_ADMINS}

    LDAP Client Connect  ${LDAP_AUTH_SERVER}
    ...  ldap_server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  basedn=${LDAP_BASEDN}
    ...  binddn=${LDAP_BINDDN}
    ...  password=${LDAP_PASSWORD}
    Run Keyword and Ignore Error  Ldap Client Add User
    ...  uid=${LDAP_USER_NAME}
    ...  password=${LDAP_PASSWORD}
    ...  objectclass=inetOrgPerson,inetLocalMailRecipient
    ...  posixAccount=${True}
    ...  mail=${LDAP_USER_NAME}@${CLIENT}

    Run Keyword and Ignore Error  Ldap Client Add Group
    ...  ${LDAP_CLASS}
    ...  members=${LDAP_USER_NAME}
    ...  basedn=${LDAP_BASEDN}

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
#    Radius Client Delete User   ${RADIUS_USER}
#    Radius Client Disconnect
    Ldap Client Delete Group   ${LDAP_CLASS}
    Ldap Client Delete User   ${LDAP_USER_NAME}
    Ldap Client Disconnect
    global_sma.DefaultTestSuiteTeardown

Login As
    [Arguments]  ${user_name}  ${password}
    Log Out Of DUT
    Login To DUT  ${user_name}  ${password}

*** Test Cases ***

Tvh1301408c
    [Documentation]  Verify save and load configurtaion using burp suite tool
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301408
    [Tags]  Tvh1301408c
    Set Appliance Under Test To SMA
    Configuration File Save Config

Tvh1301412c
    [Documentation]  Verify load configuration with malicious data in xml file
    ...  using burp suite tool.
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301412
    [Tags]  Tvh1301412c
    ${config_file}=  Configuration File Save Config  mask_passwd=${False}
    ${saveconfig_content}=  Run On DUT
    ...  cat "/data/pub/configuration/${config_file}"  host=${SMA}
    ${new_config_file}=  Set Variable  %{SARF_HOME}/tmp/config.xml
    OperatingSystem.Create File  ${new_config_file}  ${saveconfig_content}
    OperatingSystem.Run  echo "abcxyz" >> ${new_config_file}
    Copy File To DUT   %{SARF_HOME}/tmp/config.xml   /data/pub/configuration/
    Run Keyword And Expect Error
    ...  GuiValueError: *  Configuration File Load Config  config.xml

Tvh1301417c
    [Documentation]  Verify SMA login with  different credential which returns
    ...  a true value using burp suite tool.
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301417
    [Tags]  Tvh1301417c
    Run Keyword And Expect Error
    ...  GuiError: *  Login As  ' or '1' = '1   ' or '1' = '1"

Tvh1378197c
    [Documentation]  Verify LDAP authentication with  different credential
    ...  which returns a true value using burp suite tool.
    ...  http://tims.cisco.com/view-entity.cmd?ent=1378197
    [Tags]  Tvh1378197c

    Login To DUT  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    LDAP Add Server Profile
    ...  ${LDAP_PROFILE_NAME}
    ...  ${LDAP_AUTH_SERVER}
    ...  ' or 1=1 or ''=':' or 1=1 or ''='
    ...  OpenLDAP
    ...  ${LDAP_AUTH_PORT}
    ...  ${LDAP_BASE_DN}
    ${result}=  LDAP Run Server Profile Test  ${LDAP_PROFILE_NAME}
    Should Contain  ${result}  failed

Tvh1378200c
    [Documentation]  Verify RADIUS authentication with  different credential
    ...  which returns a true value using burp suite tool.
    ...  http://tims.cisco.com/view-entity.cmd?ent=1378200
    [Tags]  Tvh1378200c

    Set Test Variable  ${RADIUS_SECRET1}  ' or 1=1 or ''='
    Run Keyword And Ignore Error
    ...  Users Edit External Authentication  RADIUS
    ...  radius_servers=${RADIUS_SERVER}:${RADIUS_PORT}:${RADIUS_SECRET1}:45
    ...  group_mapping=${RADIUS_CLASS_ATTRIBUTE}:${sma_user_roles.ADMIN}
    Click Element  ${PWD_ERR_XPATH}
    Page Should Contain  Shared secret can not contain whitespaces
    Commit Changes
    Log Out of DUT
    Run Keyword And Expect Error
    ...  GuiError: ${RADIUS_USER} * FAILED
    ...  Log Into DUT   ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}
    ${title}=  Get Title
    Should Contain  ${title}  Welcome

Tvh1397768c
    [Documentation]  Check while logging in changing the xpath
    ...  for username, and check whether it logs errors in burp
    ...  http://tims.cisco.com/view-entity.cmd?ent=1397768
    [Tags]  Tvh1397768c

    @{ip_user_list}  Create List  //label[@name='username']  ${EMPTY}
    Log  ${ip_user_list}
    FOR  ${user}  IN  @{ip_user_list}
      Input Text  ${INPUT_USERNAME}  //label[@name='username']
      Input Text  ${INPUT_PASSWORD}  ${DUT_ADMIN_SSW_PASSWORD}
      Click Element  ${INPUT_LOGIN}
      ${title}=  Get Title
      Should Contain  ${title}  Welcome
    END

Tvh1397767c
    [Documentation]  Check whether non-admin user not
    ...  having access is able to modify the xpath or not
    ...  http://tims.cisco.com/view-entity.cmd?ent=1397767
    [Tags]  Tvh1397767c

    Start Cli Session If Not Open
    User Config New  ${GUEST_USER}  ${GUEST_NAME}  ${GUEST_PASS}
    ...  ${sma_user_roles.GUEST}
    Commit
    Log Into DUT  ${GUEST_USER}  ${GUEST_PASS}
    Navigate To  Web  Utilities  Web Appliance Status
    Click Element  ${WEB_STATUS_LINK}
    ${title} =  Get Title
    Should Be Equal  ${title}  Access Denied
    Selenium Close

Tvh1301420c
    [Documentation]  Verify modifying element id using inspect
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301420
    [Tags]  Tvh1301420c

    ${value}=  Change Id For Login Button
    Log  ${value}
    Should Be True  ${value}

Tvh1301423c
    [Documentation]  Verify modifying the xpath for SMA login page
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301423
    [Tags]  Tvh1301423c

    ${value}=  Change Name For Login Button
    Log  ${value}
    Should Be True  ${value}

Tvh1301437c
    [Documentation]  Verify modifying xpath by removing
    ...  and adding some element so that it remains a valid xpath
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301437
    [Tags]  Tvh1301437c

    ${not_removed}=  Remove Element In Login Page  text_login_model
    Should Be True  ${not_removed}
    ${not_added}=  Add Element In Login Page  text_login_model
    Should Be True  ${not_added}

Tvh1301438c
    [Documentation]  Verify modifying header title and groupindex in xpath
    ...  in firefox for SMA Configuration page
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301438
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301513
    [Tags]  Tvh1301438c  Tvh1301513c

    Modify Title And Groupindex In Configuration File

Tvh1397773c
    [Documentation]  Change the xpath name of a field and try to submit
    ...  http://tims.cisco.com/view-entity.cmd?ent=1397773
    [Tags]  Tvh1397773c

    Update Netmask Name In Ip Interface

Tvh1301543c
    [Documentation]  Verify modifying the cookies
    ...  http://tims.cisco.com/view-entity.cmd?ent=1301543
    [Tags]  Tvh1301543c

    ${bool_val}=  Modify Cookies For Dut Url
    Should Be True  ${bool_val}