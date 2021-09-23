# $Id: //prod/main/sarf_centos/tests/zeus1380/csdl/sec_ssh_v2.txt#1 $
# $Date: 2020/09/07 $
# $Author: mrmohank $

*** Settings ***
Library         Collections
Resource        sma/csdlresource.txt
Force Tags      csdl
Suite Setup     CSDL Suite Setup
Suite Teardown  CSDL Suite Teardown
Test Teardown   SSH V2 and SSL3 Test teardown

*** Variables ***
@{ssh_command_log}  (?s)debug1: Reading configuration data /etc/ssh/ssh_config(.*?)
    ...  (?s)debug1: Connecting to .* port 22.(.*?)
    ...  (?s)debug1: Connection established.(.*?)
    ...  (?s)debug1: identity file /home/testuser/.ssh/id_rsa type (.*?)
    ...  (?s)debug1: identity file /home/testuser/.ssh/id_dsa type -1(.*?)
    ...  (?s)debug1: Remote protocol version 2.0, remote software version OpenSSH.*(.*?)
    ...  (?s)debug1: match: OpenSSH_.* FreeBSD-.* pat OpenSSH.* compat .*(.*?)
    ...  (?s)debug1: Local version string SSH-2.0-OpenSSH_.* FreeBSD-.*(.*?)
    ...  (?s)debug1: Enabling compatibility mode for protocol 2.0(.*?)
    ...  (?s)debug1: Local version string SSH-2.0-OpenSSH_.*(.*?)
    ...  (?s)debug1: SSH2_MSG_KEXINIT sent(.*?)
    ...  (?s)debug1: SSH2_MSG_KEXINIT received(.*?)
    ...  (?s)The authenticity of host '.*' can't be established.(.*?)
    ...  (?s)Are you sure you want to continue connecting (yes/no)?(.*?)
    #    Missing Logs - To be updated after confirmation from CSDL functional team
    #    debug1: identity file /home/testuser/.ssh/identity type -1
    #    debug1: kex: server->client aes128-cbc hmac-md5 none
    #    debug1: kex: client->server aes128-cbc hmac-md5 none
    #    debug1: SSH2_MSG_KEX_DH_GEX_REQUEST(1024<1024<8192) sent
    #    debug1: expecting SSH2_MSG_KEX_DH_GEX_GROUP
    #    debug1: SSH2_MSG_KEX_DH_GEX_INIT sent
    #    debug1: expecting SSH2_MSG_KEX_DH_GEX_REPLY
    #    DSA key fingerprint is 1a:0e:c1:49:d5:6e:ad:4d:f6:a3:e6:2f:1d:31:0e:34.

@{ssh_authenticity_log}  (?s)debug1: SSH2_MSG_NEWKEYS sent(.*?)
    ...  (?s)debug1: expecting SSH2_MSG_NEWKEYS(.*?)
    ...  (?s)debug1: SSH2_MSG_NEWKEYS received(.*?)
    ...  (?s)debug1: SSH2_MSG_SERVICE_ACCEPT received(.*?)
    ...  (?s)debug1: Authentications that can continue: publickey,password,keyboard-interactive(.*?)
    ...  (?s)debug1: Next authentication method: publickey(.*?)
    ...  (?s)debug1: Trying private key: /home/testuser/.ssh/id_dsa(.*?)
    ...  (?s)debug1: Next authentication method: keyboard-interactive(.*?)
    #   Missing Logs - To be updated after confirmation from CSDL functional team
    #   Offering RSA public key: /home/testuser/.ssh/id_rsa
    #   debug1: ssh_dss_verify: signature correct
    #   debug1: SSH2_MSG_SERVICE_REQUEST sent
    #   debug1: Trying private key: /home/testuser/.ssh/identity

@{ssh_password_log}  (?s)debug1: Authentication succeeded .*keyboard-interactive(.*?)
     ...  (?s)debug1: channel 0: new [client/-session](.*?)
     ...  (?s)debug1: Requesting no-more-sessions@openssh.com(.*?)
     ...  (?s)debug1: Entering interactive session.(.*?)
     ...  (?s)client_input_global_request: rtype hostkeys-00@openssh.com want_reply 0(.*?)

@{tls_information_expected_log}  (?s)CONNECTED(.*?)
    ...  (?s)depth=0 C = --, ST = .*, L = .*, O = .*, OU = .*, CN = .*, emailAddress = .*(.*?)
    ...  (?s)verify return:1(.*?)
    ...  (?s)Certificate chain(.*?)
    ...  (?s)0 s:/C=--/ST=.*/L=.*/O=.*/OU=.*/CN=.*/emailAddress=.*(.*?)
    ...  (?s)i:/C=--/ST=.*/L=.*/O=.*/OU=.*/CN=.*/emailAddress=.*(.*?)
    ...  (?s)Server certificate(.*?)
    ...  (?s)-----BEGIN CERTIFICATE-----(.*?)
    ...  (?s)-----END CERTIFICATE-----(.*?)
    ...  (?s)Server public key is 2048 bit(.*?)
    ...  (?s)Secure Renegotiation IS supported(.*?)
    ...  (?s)Compression: NONE(.*?)
    ...  (?s)Expansion: NONE(.*?)
    ...  (?s)Protocol  : TLSv1(.*?)
    ...  (?s)No ALPN negotiated(.*?)
    ...  (?s)Cipher    : (.*?)
    #    To be clarified- The below are mising inactual logs as expected in TIMS
    #    verify error:num=18

*** Keywords ***
Verify Logs
    [Arguments]  ${actual_logs}  @{expected_logs}

    FOR  ${expected_log}  IN  @{expected_logs}
       Should match regexp  ${actual_logs}  ${expected_log}
    END

SSH V2 and SSL3 Test setup

    # Remove known host to get authenticity question
    Run on Host  ${CLIENT_IP}  ${TESTUSER}  ${TESTUSER_PASSWORD}  rm ~/.ssh/known_hosts
    # Establish SSH connection to client
    Establish SSH Connection To  ${CLIENT_HOSTNAME}  ${TESTUSER}  ${TESTUSER_PASSWORD}  $

SSH V2 and SSL3 Test teardown

    # Close SSH connection to client
    Close Connection
    Set SSHLib Prompt  ${empty}

*** Test Cases ***
Tvh1435408c
    [Documentation]  Tvh1435408c- Check whether we are able to login to SMA with ssh version 2 with username:admin
    [Tags]  cli  Tvh1435408c
    [Setup]  SSH V2 and SSL3 Test setup

    # Step 1. Do a ssh version 2 to SMA with 'admin' user from client and verify logs
    ${ssh_command_output}=  Enter option ssh -v -l ${DUT_ADMIN} ${SMA_IP} and read
    Verify Logs   ${ssh_command_output}  @{ssh_command_log}

    # Step 2. Enter 'yes' for authenticity question and verify logs
    ${ssh_authenticity_output}=  Enter option yes and read
    Verify Logs  ${ssh_authenticity_output}  @{ssh_authenticity_log}

    # Step 3. Enter password for user and verify logs
    ${ssh_password_output}=  Enter option ${DUT_ADMIN_SSW_PASSWORD} and read
    Verify Logs  ${ssh_password_output}  @{ssh_password_log}

Tvh1435401c
    [Documentation]  Tvh1435401c- Check whether we are able to login to SMA with ssh version 2 with username:rtestuser
    [Tags]  cli  Tvh1435401c
    [Setup]  SSH V2 and SSL3 Test setup

    # Step 1. Do a ssh version 2 to SMA with 'rtestuser' user from client and verify logs
    ${ssh_command_output}=  Enter option ssh -v -l ${RTESTUSER} ${SMA_IP} and read
    Verify Logs   ${ssh_command_output}  @{ssh_command_log}

    # Step 2. Enter 'yes' for authenticity question and verify logs
    ${ssh_authenticity_output}=  Enter option yes and read
    Verify Logs  ${ssh_authenticity_output}  @{ssh_authenticity_log}

    # Step 3. Enter password for user and verify logs
    ${ssh_password_output}=  Enter option ${RTESTUSER_PASSWORD} and read
    Verify Logs  ${ssh_password_output}  @{ssh_password_log}

Tvh1435946c
    [Documentation]  Tvh1435946c- To verify whether there is support of TLS for HTTP in SMA box
    [Tags]  cli  Tvh1435946c

    #1. Run openssl command in SMA and get output
    Connect to SMA  ${RTESTUSER}  ${RTESTUSER_PASSWORD}
    ${tls_support_information}=  Enter option openssl s_client -connect ${CLIENT_IP}:443 and read

    #2. Verify the output logs for TLS support
    Verify Logs   ${tls_support_information}   @{tls_information_expected_log}