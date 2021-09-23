*** Settings ***
*** Variables ***

*** Keywords ***
Initialize DKIM DMARC Environment
    DNS Client Connect  ${BIND_SERVER}
    ${BIND_SERVER_IP}=  Get Host IP By Name  ${BIND_SERVER}
    Set Suite Variable  ${BIND_SERVER_IP}
    Set Suite Variable  ${DMARC_DOMAIN}  dmarczone.${NETWORK}

    @{dmarc_rua_and_txt_objcts}=  Create List
    ...  rua=mailto:reporter@${DMARC_DOMAIN};  DMARC_TXT_OBJ
    ...  rua=mailto:reporter@${DMARC_DOMAIN}!10;  DMARC_TXT_OBJ_REPORT_10KB

    FOR  ${rua_record}  ${variable}  IN  @{dmarc_rua_and_txt_objcts}
        ${dmarc_txt_rcrd}=  Catenate
        ...  v=DMARC1;
        ...  p=reject;
        ...  sp=reject;
        ...  adkim=s;
        ...  aspf=s;
        ...  ${rua_record}
        ...  ruf=mailto:reporter@${DMARC_DOMAIN}
        Set Suite Variable  ${${variable}}  _dmarc IN TXT "${dmarc_txt_rcrd}"
    END

Finalize DKIM DMARC Environment
    DNS Client Disconnect

Configure DKIM Verification Precondition
    [Arguments]  ${DKIM_SIGN_PROFILE_NAME}  ${DMARC_DOMAIN}  ${PRIVATE_KEY_NAME}
    Domainkeys Config Profiles Signing New
    ...  name=${DKIM_SIGN_PROFILE_NAME}
    ...  profile_type=dkim
    ...  domain_name=${DMARC_DOMAIN}
    ...  selector=default
    ...  key_method=4
    ...  key_name=${PRIVATE_KEY_NAME}
    ...  user=${DMARC_DOMAIN}
    ${DKIM_TXT_RECORD}=  Domainkeys Config Profiles Signing Dnstxt
    ...  name=${DKIM_SIGN_PROFILE_NAME}
    Set Suite Variable  ${DKIM_TXT_RECORD}
    Commit

Configure DMARC DNS Zone
    [Arguments]  ${dmarc_txtobj}  ${DMARC_DOMAIN}  ${BIND_SERVER_IP}
    ${dkim_txtobj}=  Get Txtobject From DK Dnstxt  ${DKIM_TXT_RECORD}

    ${DMARC_ZONE}=  DNS Client Create Zone  ${DMARC_DOMAIN}
    DNS Client Update Record    ${DMARC_ZONE}  recordname=@  recordtype=SOA
    ...  mname=ns.${DMARC_DOMAIN}.  rname=admin.${DMARC_DOMAIN}
    DNS Client Update Record    ${DMARC_ZONE}  recordname=ns  recordtype=A
    ...  address=${BIND_SERVER_IP}
    DNS Client Update Record    ${DMARC_ZONE}  recordname=@  recordtype=NS
    ...  target=ns
    DNS Client Update Record    ${DMARC_ZONE}  recordname=@  recordtype=A
    ...  address=${CLIENT_IP}
    DNS Client Update Record    ${DMARC_ZONE}  txtobject=${dkim_txtobj}
    DNS Client Update Record    ${DMARC_ZONE}  txtobject=${dmarc_txtobj}
    ${first_ip4_byte}=  Evaluate  '${CLIENT_IP}'.split('.')[0]
    DNS Client Update Record    ${DMARC_ZONE}
    ...  txtobject=@ IN TXT "v=spf1 +mx ip4:${first_ip4_byte}.0.0.0/8 -all"

    DNS Client Build Zones  ${DMARC_ZONE}
    DNS Client Update Zones  ${True}  ${DMARC_ZONE}

Configure DMARC Verification Precondition
    [Arguments]  ${MAIL_FLOW_POLICY_NAME}  ${DMARC_PROFILE_NAME}
    # Mail Flow Policies -> Accepted -> DMARC behaviour
    Toggle DMARC mode in Mail Flow Policy  On  ${True}  ${MAIL_FLOW_POLICY_NAME}
    ${profile_settings}=  Create Dictionary
    ...  Message action when DMARC policy is reject  Reject
    ...  Message action in case of temporary failure  Accept
    ...  Message action in case of permanent failure  Accept
    DMARC Edit Profile   ${DMARC_PROFILE_NAME}     ${profile_settings}
    Commit Changes

DKIM Signed Message Create
    [Arguments]  ${addr_from}  ${mbox_path}  ${DMARC_DOMAIN}  ${DKIM_HEADER}
    ${subj}=  Set Variable  This line is a Subject of the message
    ${msg_id}=  Message Builder Utils Make Msgid
    ${addr_to}=  Set Variable  r@${DMARC_DOMAIN}
    ${from}=  Message Builder Utils Formataddr  SARF QA, ${addr_from}
    ${to}=  Message Builder Utils Formataddr  Tester, ${addr_to}
    ${date}=  Message Builder Utils Formatdate  localtime=${True}

    ${main_message}=  Message Builder Create MIMEMultipart  subtype=related
    Message Builder Add Headers  ${main_message}
    ...  From=${addr_from}
    ...  Sender=${addr_from}
    ...  Reply-To=${addr_from}
    ...  To=${to}
    ...  Subject=${subj}
    ...  Date=${date}
    ...  Message-ID=${msg_id}

    # Custom header
    Message Builder Add Headers  ${main_message}
    ...  DKIM-Signature=${DKIM_HEADER}

    Create MBOX Containing Message  ${mbox_path}  ${main_message}
    [Return]  ${mbox_path}

Get Txtobject From DK Dnstxt
    [Arguments]  ${dnstxt}
    ${result}=  Evaluate
    ...  re.sub(r'(\\w+\\._\\w+)\\..*\\s+(IN.*)', r'''\\1 \\2''','''${dnstxt}''')  re
    [Return]  ${result}

Toggle DMARC mode in Mail Flow Policy
    [Arguments]  ${dmarc_verif_str}  ${feedback_report_status}  ${policy_name}
    ${settings}=  Mail Flow Policies Create Settings
    ...  DMARC Verification  ${dmarc_verif_str}
    ...  DMARC Feedback Reports  ${feedback_report_status}
    Mail Flow Policies Edit  ${PUBLIC_LISTENER_NAME}  ${policy_name}  ${settings}
    Commit Changes

DKIM Header Get
    Null Smtpd Start
    Inject Messages
    ...  inject-host=${ESA_PR_LISTENER_IP}
    ...  num-msgs=1
    ...  rcpt-host-list=${CLIENT}
    ...  mail-from=${TEST_ID}@${DMARC_DOMAIN}
    ${msg}=  Verify And Wait For Mail In Drain  ${TEST_ID}
    Message Load  ${msg}
    ${items}=  Message Items
    Message Unload
    Log Dictionary  ${items}

    ${dkim_header}=  Get From Dictionary  ${items}  DKIM-Signature
    Null Smtpd Stop
    [Return]  ${dkim_header}
