# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/sec_scr_nolog_2.robot $
# $Date: 2020/10/12 $
# $Author: mrmohank $

*** Settings ***
Library      Collections
Resource     sma/csdlresource.txt
Resource     sma/saml.txt
Resource     sma/reports_keywords.txt
Variables    sma/saml_constants.py

Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown

*** Variables ***
${log_name}                   aggregatord_logs
${ftp_server_directory}       /home/user
${cli_log_path}               /data/pub/cli_logs/cli.current
${gui_log_path}               /data/pub/gui_logs/gui.current
${auth_log_path}              /data/pub/authentication/authentication.current
${test_image_server}          http://ironport.com
${ldap_server_profile}        myldap
${TEST_EUQ_SP_PROFILE}        euq_sp_profile
${TEST_EUQ_IDP_PROFILE}       euq_idp_profile
${ca_cert_path}               %{SARF_HOME}/tests/testdata/ca.crt
${ca_key_path}                %{SARF_HOME}/tests/testdata/ca.key
${inbound_cert_path}          %{SARF_HOME}/tests/testdata/sma/csdl/csdl_inbound_cert.crt
${inbound_key_path}           %{SARF_HOME}/tests/testdata/sma/csdl/csdl_inbound_cert.pem
${outbound_cert_path}         %{SARF_HOME}/tests/testdata/sma/csdl/csdl_outbound_cert.crt
${outbound_key_path}          %{SARF_HOME}/tests/testdata/sma/csdl/csdl_outbound_cert.pem
${https_cert_path}            %{SARF_HOME}/tests/testdata/sma/csdl/csdl_https_cert.crt
${https_key_path}             %{SARF_HOME}/tests/testdata/sma/csdl/csdl_https_cert.pem
${ldap_cert_path}             %{SARF_HOME}/tests/testdata/sma/csdl/csdl_ldap_cert.crt
${ldap_key_path}              %{SARF_HOME}/tests/testdata/sma/csdl/csdl_ldap_cert.pem

*** Keywords ***
Setup for Tvh1506342c

    Start CLI Session
    Roll Over Now
    Run keyword and ignore error  User Config External Setup Clear  confirm=yes
    Run keyword and ignore error  Commit

Setup for Tvh1506341c
    ${ca_certificate_file}=    OperatingSystem.Get File    ${ca_cert_path}
    Set Suite Variable  ${ca_certificate_file}
    ${ca_certificate_key}=    OperatingSystem.Get File    ${ca_key_path}
    Set Suite Variable  ${ca_certificate_key}
    ${inbound_certificate_file}=    OperatingSystem.Get File    ${inbound_cert_path}
    Set Suite Variable  ${inbound_certificate_file}
    ${inbound_certificate_key}=    OperatingSystem.Get File    ${inbound_key_path}
    Set Suite Variable  ${inbound_certificate_key}
    ${outbound_certificate_file}=    OperatingSystem.Get File    ${outbound_cert_path}
    Set Suite Variable  ${outbound_certificate_file}
    ${outbound_certificate_key}=    OperatingSystem.Get File    ${outbound_key_path}
    Set Suite Variable  ${outbound_certificate_key}
    ${https_certificate_file}=    OperatingSystem.Get File    ${https_cert_path}
    Set Suite Variable  ${https_certificate_file}
    ${https_certificate_key}=    OperatingSystem.Get File    ${https_key_path}
    Set Suite Variable  ${https_certificate_key}
    ${ldap_certificate_file}=    OperatingSystem.Get File    ${ldap_cert_path}
    Set Suite Variable  ${ldap_certificate_file}
    ${ldap_certificate_key}=    OperatingSystem.Get File    ${ldap_key_path}
    Set Suite Variable  ${ldap_certificate_key}
    Roll Over Now
    Run keyword and ignore error  Cert config clear certificates  clear=yes
    Run keyword and ignore error  Commit

Teardown for Tvh1506342c
    Close CLI session
    Start CLI session
    User Config External Setup Clear  confirm=yes
    Commit

Teardown for Tvh1506343c
    UserConfig Two Factor Privilege Delete  role=${sma_user_roles.OPERATOR}
    UserConfig Two Factor Radius Clear  confirm_delete=y
    UserConfig Two Factor Disable
    User config delete  ${RADIUS_USER}  confirm=yes
    Commit

Teardown for Tvh1506351c
    Close CLI session
    Start CLI session
    Go To  https://${SMA}
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    Users Disable External Authentication
    Commit Changes

Teardown for Tvh1506354c
    Cert config clear certificates  clear=yes
    Commit
    LDAP Delete Server Profile  ${ldap_server_profile}
    SAML DELETE SP IDP  sp_name=${TEST_SP_PROFILE}  idp_name=${TEST_IDP_PROFILE}  user_role=${USER_ROLE}
    SAML DELETE EUQ PROFILES  sp_name=${TEST_EUQ_SP_PROFILE} idp_name=${TEST_EUQ_IDP_PROFILE}
    Commit Changes

Verify sensitive informations are not captured in logs
    [Arguments]  ${log_type}  @{log_parameters}

    FOR  ${log}  IN   @{log_parameters}
        ${log_status}=  Run keyword and return status   Verify logs  ${${log_type}_log_path}  ${log}
        Should not be true  ${log_status}
    END

*** Test Cases ***
Tvh1506341c
    [Documentation]  Add certificate and its private key through CLI certconfig > certificate
    ...  Verify the related private keys are not logged
    ...  Details relevant to event/action alone logged in cli_logs
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506341

    [Setup]  Setup for Tvh1506341c
    [Tags]  cli  Tvh1506341c

    # Step 1. Login to CLI with admin credentials.
    Start CLI session

    # Step 2 . Add certificates through CLI - certconfig > certificate > setup
    #          Give Yes when it is prompted for "Do you want to use one certificate/key for
    #          receiving, delivery, HTTPS management access, and LDAPS? [Y]"
    #          Paste certificate and private key in .pem format and commit
    Cert Config Setup  ${ca_certificate_file}  ${ca_certificate_key}  intermediate=no

    # Step 3 . Commit changes
    Commit

    # Step 4. Verify cli_logs did not capture private keys pasted.
    Verify sensitive informations are not captured in logs  cli  ${ca_certificate_key}

    # Step 5. Clear exisitng certificates
    Cert config clear certificates  clear=yes
    Commit

    # Step 5 .Add certificates through CLI - certconfig > certificate > setup
    #    Give No when it is prompted for "Do you want to use one certificate/key for
    #    receiving, delivery, HTTPS management access, and LDAPS? [N]"
    #    Paste different certificates and its private keys under each option
    Cert Config Setup  ${inbound_certificate_file}  ${inbound_certificate_key}
    ...     one_cert=no
    ...     intermediate=no
    ...     rsa_cert_outbound=${outbound_certificate_file}
    ...     rsa_key_outbound=${outbound_certificate_key}
    ...     rsa_cert_https=${https_certificate_file}
    ...     rsa_key_https=${https_certificate_key}
    ...     rsa_cert_ldap=${ldap_certificate_file}
    ...     rsa_key_ldap=${ldap_certificate_key}

    # Step 6 . Commit changes
    Commit

    # Step 7 . Verify cli_logs did not capture private keys pasted.
    Verify sensitive informations are not captured in logs  cli  ${ca_certificate_key} ${outbound_certificate_key} ${https_certificate_key} ${ldap_certificate_key}

Tvh1506342c
    [Documentation]  Configure Radius server through CLI - Userconfig > External command with server's
    ...              shared secret and login to CLI as Radius user.
    ...  Verify shared secrets/user credentials are not logged in to cli_logs/authentication on configuration and communication
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506342

    [Setup]  Setup for Tvh1506342c
    [Teardown]  Teardown for Tvh1506342c
    [Tags]  cli  Tvh1506342c

    # Step 1. Login to CLI with admin credentials.
    Start CLI session

    # Step 2. Enable External authentication and map RADIUS server profile to it under CLI - userconfig > external
    # Step 3. Provide server's details and shared secret, Map group of users to
    #         role or map all users to admin role by default.
    User Config External Setup New  ${RADIUS_SERVER}  ${RADIUS_SECRET}  reply_timeout=10
    ...  create_mapping=yes
    ...  group_name=${RADIUS_CLASS_ATTRIBUTE}
    ...  role=Administrator

    # Step 4. Submit and Commit changes
    Commit

    # Step 5.Login to SMA CLI as Radius user and verify login credentials are not captured
    Close CLI session
    Start CLI session   user=${RADIUS_USER}  password=${RADIUS_USER_PASSWORD}

    # Step 6. Verify the Password configured for Radius server is not captured anywhere in cli_logs
    Verify sensitive informations are not captured in logs  cli  ${RADIUS_SECRET}  ${RADIUS_USER_PASSWORD}

Tvh1506343c
    [Documentation]  	Configure Radius server through CLI - userconfig > external command with server's
    ...                 shared secret and login to CLI using 2FA
    ...  Verify shared secrets/user credentials are not logged in to cli_logs/authentication on
    ...  configuration and communication
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506343

    [Setup]  Setup for Tvh1506342c
    [Teardown]  Teardown for Tvh1506343c
    [Tags]  cli  Tvh1506343c

    # Step 1. Login to CLI with admin credentials.
    Start CLI session

    # Step 2. Configure Local user "user1" under userconfig > new.
    User Config New  ${RADIUS_USER}  ${RADIUS_USER}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  ${sma_user_roles.OPERATOR}

    # Step 3.  Enable Two Factor authentication and map RADIUS server profile to it under cli > userconfig > twofactorauth
    #          Provide server's details and shared secret.
    #          Configure Two-Factor Authentication based on User Role Privileges.
    UserConfig Two Factor Radius New   ${RADIUS_SERVER}  ${RADIUS_SECRET}  port=1812  timeout=5  auth_type=2
    UserConfig Two Factor Privilege Add  role=${sma_user_roles.OPERATOR}

    # Step 4. Commit the changes
    Commit

    # Step 5. Verify shared secret is not captured in cli_logs
    Verify sensitive informations are not captured in logs  cli  ${cli_log_path}  ${RADIUS_SECRET}

    # Step 6. Login to SMA CLI as local user give radius passcode as second factor for authentication
    Establish SSH Connection To  ${CLIENT_HOSTNAME}  ${TESTUSER}  ${TESTUSER_PASSWORD}  $
    Enter option ssh -4 ${RADIUS_USER}@${SMA} and read
    Enter option yes and read
    ${passcode_logs}=  Enter option ${DUT_ADMIN_SSW_PASSWORD} and read
    Should contain  ${passcode_logs}  Passcode:
    ${login_success_logs}=  Enter option ${RADIUS_USER_PASSWORD} and read
    Should contain  ${login_success_logs}  Welcome to the Cisco

    # Step 7. Verify login credentials are not captured in cli_logs/authentication logs.
    Verify sensitive informations are not captured in logs  cli  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}
    Verify sensitive informations are not captured in logs  auth  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}

Tvh1506344c
    [Documentation]  Configure Radius server under GUI - System Administration > Users > External Authentication
    ...              with server's shared secret and login to GUI as Radius user
    ...  Verify shared secrets/user credentials are not logged in to gui_logs on configuration and communication
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506344

    [Setup]  Setup for Tvh1506342c
    [Teardown]  Teardown for Tvh1506342c
    [Tags]  gui  Tvh1506344c

    # Step 1. Login to UI with admin credentials.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    # Step 2. Enable External authentication and map RADIUS server profile to it under System Administration > Users
    # Step 3. Provide server's details and shared secret, Map group of users to specific role or map all users
    #         admin role by default.
    Users Edit External Authentication   RADIUS
    ...  radius_servers=${RADIUS_SERVER}:${RADIUS_PORT}:${RADIUS_SECRET}:10
    ...  auth_cache_timeout=20
    ...  group_mapping=${RADIUS_CLASS_ATTRIBUTE}:${sma_user_roles.ADMIN}

    # Step 4. Submit and Commit changes
    Commit Changes

    # Step 5.Login to SMA UI as Radius user
    Login to SMA via GUI  ${RADIUS_USER}  ${RADIUS_USER_PASSWORD}

    # Step 6. Verify shared secret is not captured in gui_logs
    #         Verify login credentials are not captured in gui_logs/authentication logs.
    Verify sensitive informations are not captured in logs  gui  ${RADIUS_SECRET}  ${RADIUS_USER_PASSWORD}
    Verify sensitive informations are not captured in logs  auth  ${RADIUS_SECRET}  ${RADIUS_USER_PASSWORD}

Tvh1506345c
    [Documentation]  Configure Radius server under GUI - System Administration > Users > Two Factor Authentication
    ...              with server's shared secret
    ...   Login to GUI using 2FA, verify shared secrets/user credentials are not logged in to gui_logs
    ...   on configuration and communication
    ...   TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506345

    [Setup]  Setup for Tvh1506342c
    [Teardown]  Teardown for Tvh1506343c
    [Tags]  cli  Tvh1506345c

    # Step 1. Login to UI with admin credentials.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    # Step 2. Configure Local user "user1" under System Administration > Users > Add user.
    Users Add user  ${RADIUS_USER}  ${RADIUS_USER}  ${DUT_ADMIN_SSW_PASSWORD}  ${sma_user_roles.OPERATOR}

    # Step 3. Enable Two Factor authentication and map RADIUS server profile to it under System Administration > Users
    #         Provide server's details and shared secret.
    @{radius_servers}=  Create List
    ...  ${RADIUS_SERVER},,${RADIUS_SECRET},,
    ${radius_tf_auth_settings}=  Create Dictionary
    ...  Authentication Type  RADIUS
    ...  RADIUS Server Information  ${radius_servers}
    Users twofactor auth enable  ${radius_tf_auth_settings}

    # Step 4. Enable Two factor authentica
    ${privileges_map}=  Create Dictionary
    ...  ${sma_user_roles.OPERATOR}  ${True}
    Users twofactor auth privileges  ${privileges_map}

    # Step 5. Commit the changes
    Commit Changes

    # Step 6. Login to SMA UI as local user, give radius passcode as second factor for authentication
    Log Out Of Dut
    Login To DUT  ${RADIUS_USER}  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}

    # Step 7. Verify login credentials are not captured in gui_logs/authentication logs.
    Verify sensitive informations are not captured in logs  gui  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}
    Verify sensitive informations are not captured in logs  auth  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}

Tvh1506346c
    [Documentation]  Configure SNMP with authentication and encryption passwords using CLI - snmpconfig
    ...  Verify passwords are not logged in cli_logs
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506346

    [Setup]  Roll Over Now
    [Teardown]  Run keywords  Snmp Config Setup  enable_snmp=no
    ...  AND  Commit
    [Tags]  cli  Tvh1506346c

    # Step 1. Login to CLI with admin credentials.
    Start CLI session

    # Step 2. Configure SNMP with authentication and encryption passwords using CLI
    Snmp Config Setup  enable_snmp=yes  ip_interface=Management
    ...  snmp_port=${SNMP_PORT}  snmpv3_passphrase=${DUT_ADMIN_TMP_PASSWORD}
    ...  snmpv3_privacy_passwd=${DUT_ADMIN_SSW_PASSWORD}
    ...  snmpv1v2_enabled=yes  snmpv1v2_community=snmptest
    ...  system_location_string=San Bruno
    ...  system_contact_string=localhost

    # Step 3. Submit and Commit changes
    Commit

    # Step 4. Verify the Password configured for SNMP server is not captured anywhere in cli_logs
    Verify sensitive informations are not captured in logs  cli  ${DUT_ADMIN_TMP_PASSWORD}  ${DUT_ADMIN_SSW_PASSWORD}

Tvh1506347c
    [Documentation]  Configure update server with password and url information under GUI - System Administration
    ...  Update Settings and verify credentials are not logged and details relevant
    ...  Details relevant to event/action alone logged in gui_logs
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506347

    [Setup]  Roll Over Now
    [Teardown]  Run keywords  Update settings edit settings  image_server=ironport
    ...  AND  Commit Changes
    [Tags]  gui  Tvh1506347c

    # Step 1. Login to GUI with admin credentials.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    # Step 2. Configure Local Update Servers
    #         GUI > System Amin > Settings > Use own server with required details
    ${image_server}=  Update Settings Set Service Params
    ...  url=${UPDATE_SERVER}
    ...  port=80
    ...  username=${DUT_ADMIN}
    ...  password=${DUT_ADMIN_PASSWORD}
    ...  asyncos_url=ironport.com:80
    Update settings edit settings  image_server=${image_server}

    # Step 3. Submit and Commit changes
    Commit Changes

    # Step 4. Verify Authentication password provided are not captured in gui_logs.
    Verify sensitive informations are not captured in logs  gui  ${DUT_ADMIN_PASSWORD}

Tvh1506348c
    [Documentation]  Configure update server with password and url information using CLI
    ...  Updateconfig and verify credentials are not logged
    ...  Details relevant to event/action alone logged in cli_logs
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506348

    [Setup]  Roll Over Now
    [Tags]  cli  Tvh1506348c

    # Step 1. Login to CLI with admin credentials.
    Start CLI session

    # Step 2. Configure Local Update Servers
    #         CLI > Updateconfig > setup > Use own server with required details
    Update Config Setup  update_from=Use own  update_server=http://${DUT_ADMIN}:${DUT_ADMIN_TMP_PASSWORD}@${UPDATE_SERVER}/home/

    # Step 3. Submit and Commit changes
    Commit

    # Step 4. Verify Authentication password provided are not captured in gui_logs.
    Verify sensitive informations are not captured in logs  cli  ${DUT_ADMIN_TMP_PASSWORD}

Tvh1506349c
    [Documentation]  Edit Log Subscription for any of the logs through CLI to configure FTP push, provide
    ...              remote servers credentials under config command.
    ...  Verify the credentials are not logged and details relevant to event/action alone logged in cli_logs
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506349

    [Setup]  Roll Over Now
    [Teardown]  Run keywords  Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  AND  Log subscriptions set retrieval method to manually download   ${log_name}
    ...  AND  Commit Changes
    [Tags]  cli  Tvh1506349c

    # Step 1. Login to CLI with admin credentials.
    Start CLI session

    # Step 2. Edit Log Subscription for any of the logs through CLI - logconfig > edit > <select log>
    # Step 3. Enable FTP log push and configure remote server's details including username and password.
    Log Config Edit  ${log_name}
    ...  retrieval=FTP Push  hostname=${FTP_SERVER}  username=${FTPUSER}
    ...  password=${FTPUSER_PASSWORD}  directory=${ftp_server_directory}  filename=agg_files
    Commit

    # Step 4. Verify the Password configured for FTP server is not captured anywhere in cli_logs
    Verify sensitive informations are not captured in logs  cli  ${FTPUSER_PASSWORD}

Tvh1506350c
    [Documentation]  Edit Log Subscription for any of the logs through GUI to configure FTP push, provide
    ...              remote servers credentials under config command.
    ...  Verify the credentials are not logged and details relevant to event/action alone logged in gui_logs
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506350

    [Setup]  Roll Over Now
    [Teardown]  Run keywords  Log subscriptions set retrieval method to manually download   ${log_name}
    ...  AND  Commit Changes
    [Tags]  gui  Tvh1506350c

    # Step 1. Login to UI with admin credentials.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    #.Step 2. Edit Log Subscription for any of the logs through GUI - System Administration > Log Subscriptions > <Log name> >
    # Step 3. Enable FTP log push and configure remote server's details including username and password.
    Log subscriptions set retrieval method to ftp push  ${log_name}  ${FTP_SERVER}  ${ftp_server_directory}  ${FTPUSER}  ${FTPUSER_PASSWORD}
    Commit Changes

    # Step 4. Verify the Password configured for FTP server is not captured anywhere in cli_logs
    Verify sensitive informations are not captured in logs  gui  ${FTPUSER_PASSWORD}

Tvh1506351c
    [Documentation]  Login to SMA CLI and GUI with  valid & invalid LDAP user credentials
    ...  Login to EUQ with  valid & invalid LDAP user credentials
    ...  Verify credentials are not logged and details relevant to event/action alone logged in cli_logs/gui_logs/authentication
    ...  logs on both events
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506351
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506352

    [Setup]  Roll Over Now
    [Teardown]  Teardown for Tvh1506351c
    [Tags]  gui  cli  Tvh1506351c  Tvh1506352c

    # Step 1. Login to UI with admin credentials.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    # Step 2. Configure LDAP server under System Administration > LDAP with required server details
    #         Enable external authentication queries.
    LDAP Add Server Profile  ${ldap_server_profile}  ${LDAP_AUTH_SERVER}
    ...  server_type=${LDAP_SERVER_TYPE}
    ...  port=${LDAP_AUTH_PORT}
    ...  base_dn=${LDAP_BASE_DN}
    LDAP Edit External Authentication Queries  ${ldap_server_profile}
    ...  user_base_dn=${LDAP_BASE_DN}
    ...  group_base_dn=${LDAP_BASE_DN}
    Commit Changes

    # Step 3. Enable External authentication and map LDAP server profile to it under System Administration > Users
    #         Map group of users to certain roles within External authentication configuration.
    Edit External Authentication LDAP User Role  ${ldap_server_profile}  ${LDAP_SMA_USER_GROUP}  ${sma_user_roles.ADMIN}
    Commit Changes

    # Step 4 . Try to access SMA GUI as LDAP user with incorrect password.
    Run keyword and expect error  GuiError: ${LDAP_SMA_USER} user login with password ${RADIUS_USER_PASSWORD} FAILED  Login to SMA via GUI  ${LDAP_SMA_USER}  ${RADIUS_USER_PASSWORD}

    # Step 5. Access SMA GUI as LDAP user with correct password.
    Login to SMA via GUI  ${LDAP_SMA_USER}  ${LDAP_SMA_USER_PASS}

    # Step 5. Try to access SMA CLI as LDAP user with incorrect password.
    Close CLI Session
    Start CLI session   user=${LDAP_SMA_USER}  password=${RADIUS_USER_PASSWORD}

    # Step 7. Access SMA CLI as LDAP user with correct password.
    Close CLI Session
    Start CLI session   user=${LDAP_SMA_USER}  password=${LDAP_SMA_USER_PASS}

    # Step 8. Verify login successful and password is not logged to cli_logs/authentication logs.
    Verify sensitive informations are not captured in logs  cli  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}  ${LDAP_SMA_USER_PASS}
    Verify sensitive informations are not captured in logs  gui  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}  ${LDAP_SMA_USER_PASS}
    Verify sensitive informations are not captured in logs  auth  ${DUT_ADMIN_SSW_PASSWORD} ${RADIUS_USER_PASSWORD} ${LDAP_SMA_USER_PASS}

    # Step 9. Enable End-User Quarantine Access with "End-User Authentication" method - LDAP under GUI -
    #         Centralized Services > Email > Spam Quarantine.
    Enable Spam Quarantine On SMA
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=LDAP
    Commit Changes

    # Step 10. Launch EUQ GUI portal
    Log Out Of Dut
    Go To  https://${SMA}:83

    #Step 11. Try to access SMA EUQ UI as LDAP user with incorrect password.
    Run keyword and expect error  GuiError: ${LDAP_SMA_USER} user login with password ${RADIUS_USER_PASSWORD} FAILED  Log Into DUT  user=${LDAP_SMA_USER}  password=${RADIUS_USER_PASSWORD}

    # Step 12. Try to access SMA EUQ UI as LDAP user with correct password.
    Log Into DUT  user=${LDAP_SMA_USER}  password=${LDAP_SMA_USER_PASS}
    Log Out Of Dut

    # Step 13. Verify login failed and is password not logged to cli_logs/authentication logs.
    Verify sensitive informations are not captured in logs  cli  ${DUT_ADMIN_SSW_PASSWORD} ${RADIUS_USER_PASSWORD} ${LDAP_SMA_USER_PASS}
    Verify sensitive informations are not captured in logs  gui  ${DUT_ADMIN_SSW_PASSWORD} ${RADIUS_USER_PASSWORD} ${LDAP_SMA_USER_PASS}
    Verify sensitive informations are not captured in logs  auth  ${DUT_ADMIN_SSW_PASSWORD} ${RADIUS_USER_PASSWORD} ${LDAP_SMA_USER_PASS}

Tvh1506353c
    [Documentation]  Login to SMA GUI/EUQ with valid & invalid SAML users' credentials
    ...  Verify credentials are not logged and details relevant to event/action alone logged in gui_logs
    ...  and authentication logs on both events
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506353

    [Setup]  Roll Over Now
    [Tags]  gui  cli  Tvh1506353c

    # Step 1.  Login to UI with admin credentials.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}

    # Step 2 . Configure SAML for UI login under System Administration > SAML with required SP and IDP server details.
    Add Customer SAML Config Azure
    Commit Changes
    Userconfig External Setup Saml
    ...  cache_time=0
    ...  group_name=${SAML_GROUP_Azure}
    ...  role=${SAML_GROUP_ROLE_ADMIN}
    Commit

    # Step 3.  Enable External authentication and map SAML server profile to it under System Administration > Users
    # Step 4.  Map group of users (Configured in IDP) to certain roles (e.g, Operator) within External auth configuration.
    Users Edit External Authentication  SAML
    ...  extauth_attribute_name_map=
    ...  group_mapping=${SAML_GROUP_Azure}:Administrator
    Commit Changes
    Log Out Of Dut

    # Step 5. Try to access SMA GUI as SAML user with incorrect password.
    Run keyword and ignore error  SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${RADIUS_USER_PASSWORD}  azure

    #Step 6. Try to access SMA GUI as SAML user with correct password.
    Go To  https://${SMA}
    SSO Log Into Dut    ${USER_ROLE_CUSTOMER}  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}  azure

    # Step 7. Verify login failed and is password not logged to gui_logs/authentication logs
    Verify sensitive informations are not captured in logs  gui  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}
    Verify sensitive informations are not captured in logs  auth  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}

    # Step 8. Configure SAML for EUQ login under System Administration > SAML with required SP and IDP server details.
    Login to SMA via GUI  ${DUT_ADMIN}  ${DUT_ADMIN_SSW_PASSWORD}
     ${settings}=  Create Dictionary
    ...  User Role                          ${USER_ROLE}
    ...  SP Entity ID                       ${SP_ENTITY_ID}
    ...  SP Certificate                     ${CERT_FILE_SP_Azure}
    ...  Private Key                        ${CERT_FILE_KEY_SP_Azure}
    ...  Organization Name                  ${ORGANIZATION_NAME}
    ...  Organization Display Name          ${ORGANIZATION_DISPLAY_NAME}
    ...  Organization URL                   ${ORGANIZATION_URL}
    ...  Organization Technical Contact     ${ORGANIZATION_TECHNICAL_CONTACT}
    ...  Configuration Mode                 ${CONFIGURATION_MODE}
    ...  Import IDP Metadata                ${IDP_Metadata_Azure}
    SAML ADD SP AND IDP FOR EUQ  ${TEST_EUQ_SP_PROFILE}  ${TEST_EUQ_IDP_PROFILE}  ${settings}
    Commit Changes

    # Step 9. Enable End-User Quarantine Access with "End-User Authentication" method - SAML 2.0 under GUI - Centralized Services > Email > Spam Quarantine
    Enable Spam Quarantine On SMA
    Spam Quarantine Edit Enduser Access
    ...  end_user_access_enable=${True}
    ...  end_user_auth=SAML 2.0
    Commit Changes
    Log Out Of Dut

    #Step 10 Try to access SMA EUQ UI as SAML user with incorrect password.
    Go To  https://${SMA}:83
    Run keyword and ignore error  Do AZURE LOGIN TO DUT  ${SAML_AZUR_USER}  ${RADIUS_USER_PASSWORD}

    #Step 11. Try to access SMA EUQ UI as SAML user with correct password.
    Go To  https://${SMA}:83
    Run keyword and ignore error  Do AZURE LOGIN TO DUT  ${SAML_AZUR_USER}  ${SAML_AZUR_USER_PASSWORD}

    #Step 12. Verify login successful and password is not logged to gui_logs/authentication logs.
    Verify sensitive informations are not captured in logs  gui  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}
    Verify sensitive informations are not captured in logs  auth  ${DUT_ADMIN_SSW_PASSWORD}  ${RADIUS_USER_PASSWORD}

Tvh1506354c
    [Documentation]  	Verify SMA does not capture any critical configuration information
    ...  it logs only information related to events/action
    ...  Passwords/Private keys are not captured and logged in gui_logs/cli_logs while
    ...  loading configuration files through GUI/CLI.
    ...  TIMS link - http://tims.cisco.com/view-entity.cmd?ent=1506354

    [Setup]  Setup for Tvh1506341c
    [Tags]  gui  cli  Tvh1506354c

    #Step 1 .Login to UI with admin credentials
    Selenium Login
    Start CLI Session
    User Config New  ${RADIUS_USER}  ${RADIUS_USER}  ${DUT_ADMIN_SSW_PASSWORD}
    ...  ${sma_user_roles.OPERATOR}
    Commit

    # Step 2. Save configuration file GUI - System Administration > Configuration File > Save Configuration.
    ${sma_config_file}=  Configuration File Save Config  mask_passwd=${False}

    # Step 3. Load configuration file through GUI - System Administration > Configuration File > Load Configuration.
    Configuration File Load Config   ${sma_config_file}
    Commit Changes

    # Step 4. Verify Passwords/Private keys are not captured and logged in gui_logs
    Verify sensitive informations are not captured in logs  gui  ${ca_certificate_key} ${FTPUSER_PASSWORD} ${DUT_ADMIN_SSW_PASSWORD} ${RADIUS_USER_PASSWORD} ${CISCO_TEST_PASSWORD}

    # Step 5. Login to CLI, Load configuration file through CLI - loadconfig.
    ${sma_config_file}=  Save Config
    Load Config From File  ${sma_config_file}
    Commit

    # Step 6. Verify Passwords/Private keys are not captured and logged in cli_logs.
    Verify sensitive informations are not captured in logs  cli  ${ca_certificate_key} ${FTPUSER_PASSWORD} ${DUT_ADMIN_SSW_PASSWORD} ${RADIUS_USER_PASSWORD} ${CISCO_TEST_PASSWORD}