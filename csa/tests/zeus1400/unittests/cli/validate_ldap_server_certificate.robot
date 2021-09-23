*** Settings ***
Library         SmaCliLibrary
Suite Setup     Restart CLI Session
Documentation   Validate LDAP server certificate.


*** Test Cases **
Enable Validate LDAP Server Certificates
    [Tags]    ut1
    LDAP Config Setup  ldap_server_certificate=Yes
    commit
    
Disable Validate LDAP Server Certificates
    [Tags]    ut2
    LDAP Config Setup  Auto  No  No
    commit
