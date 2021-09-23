*** Settings ***
Library         String
Resource        sma/csdlresource.txt
Suite Setup     Restart CLI Session
Documentation   verifying FQDN command in CLI.

*** Variables ***
${INBOUND_CERTIFICATE}=       %{SARF_HOME}/tests/testdata/sma/csdl/csdl_inbound_cert.crt
${INBOUND_CERTIFICATE_KEY}=   %{SARF_HOME}/tests/testdata/sma/csdl/csdl_inbound_cert.pem
${OUTBOUND_CERTIFICATE}=      %{SARF_HOME}/tests/testdata/sma/csdl/csdl_outbound_cert.crt
${OUTBOUND_CERTIFICATE_KEY}=  %{SARF_HOME}/tests/testdata/sma/csdl/csdl_outbound_cert.pem
${HTTPS_CERTIFICATE}=         %{SARF_HOME}/tests/testdata/sma/csdl/csdl_https_cert.crt
${HTTPS_CERTIFICATE_KEY}=     %{SARF_HOME}/tests/testdata/sma/csdl/csdl_https_cert.pem
${LDAP_CERTIFICATE}=          %{SARF_HOME}/tests/testdata/sma/csdl/csdl_ldap_cert.crt
${LDAP_CERTIFICATE_KEY}=      %{SARF_HOME}/tests/testdata/sma/csdl/csdl_ldap_cert.pem

*** keywords ***
Set Variables For Certificates
    ${inbound_cert}=       OperatingSystem.Get File  ${INBOUND_CERTIFICATE}
    Set Test Variable      ${inbound_cert}
    ${inbound_cert_key}=   OperatingSystem.Get File  ${INBOUND_CERTIFICATE_KEY}
    Set Test Variable      ${inbound_cert_key}
    ${outbound_cert}=      OperatingSystem.Get File  ${OUTBOUND_CERTIFICATE}
    Set Test Variable      ${outbound_cert}
    ${outbound_cert_key}=  OperatingSystem.Get File  ${OUTBOUND_CERTIFICATE_KEY}
    Set Test Variable      ${outbound_cert_key}
    ${https_cert}=         OperatingSystem.Get File  ${HTTPS_CERTIFICATE}
    Set Test Variable      ${https_cert}
    ${https_cert_key}=     OperatingSystem.Get File  ${HTTPS_CERTIFICATE_KEY}
    Set Test Variable      ${https_cert_key}
    ${ldap_cert}=          OperatingSystem.Get File  ${LDAP_CERTIFICATE}
    Set Test Variable      ${ldap_cert}
    ${ldap_cert_key}=      OperatingSystem.Get File  ${LDAP_CERTIFICATE_KEY}
    Set Test Variable      ${ldap_cert_key}

*** Test Cases **
Test1
    #With fqdn validation
    ${fqdn}=  Cert Authority Import  csdl_CA.pem  fqdn_validation=yes 
    Log  ${fqdn}
    Should Contain  ${fqdn}  A valid domain name is a string that must match the following rules

    #Without fqdn validation
    ${fqdn}=  Cert Authority Import  csdl_CA.pem
    Log  ${fqdn}
    Should Contain  ${fqdn}  Imported 1 custom certificates successfully


Test2
    SSL Config Edit Peer Cert Fqdn  enable=${True}
    Commit
    ${fqdn_status}=  SSL Config Get Peer Cert Fqdn Status
    Log  ${fqdn_status}
    Should Contain  ${fqdn_status}  Enabled

Test3
    Set Variables For Certificates
    #with fqdn
    Run Keyword And Expect Error  *failed due to certificate pair with invalid FQDN
    ...  Cert Config Setup
    ...  ${inbound_cert}
    ...  ${inbound_cert_key}
    ...  intermediate=no
    ...  fqdn=yes
    
    #without fqdn
    Cert Config Setup
    ...  ${inbound_cert}
    ...  ${inbound_cert_key}
    ...  intermediate=no

Test4
    Set Variables For Certificates
    #with fqdn
    Run Keyword And Expect Error  *failed due to certificate pair with invalid FQDN
    ...  Cert Config Setup  ${inbound_cert}  ${inbound_cert_key}
    ...  one_cert=no
    ...  intermediate=no
    ...  fqdn=yes
    ...  rsa_cert_outbound=${outbound_cert}
    ...  rsa_key_outbound=${outbound_cert_key}
    ...  rsa_cert_https=${https_cert}
    ...  rsa_key_https=${https_cert_key}
    ...  rsa_cert_ldap=${ldap_cert}
    ...  rsa_key_ldap=${ldap_cert_key}
    
    #without fqdn
    Cert Config Setup  ${inbound_cert}  ${inbound_cert_key}
    ...  one_cert=no
    ...  intermediate=no
    ...  rsa_cert_outbound=${outbound_cert}
    ...  rsa_key_outbound=${outbound_cert_key}
    ...  rsa_cert_https=${https_cert}
    ...  rsa_key_https=${https_cert_key}
    ...  rsa_cert_ldap=${ldap_cert}
    ...  rsa_key_ldap=${ldap_cert_key}
