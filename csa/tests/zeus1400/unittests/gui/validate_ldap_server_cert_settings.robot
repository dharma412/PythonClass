*** Settings ***
Library      String
Resource     sma/csdlresource.txt
Suite Setup     Selenium Login
suite Teardown  Selenium Close
Documentation   Validate LDAP Server Certificate.


*** Test Cases ***
Enable Validate LDAP Server Certificates
   [Tags]  ut1
   Ldap Edit Global Settings  interface=Management  validate_ldap_server=${True}
   commit changes

Disable Validate LDAP Server Certificates
   [Tags]  ut2
   Ldap Edit Global Settings  interface=Auto  validate_ldap_server=${False}
   commit changes

Edit Ldap Global Settings
   [Tags]  ut3
   Ldap Edit Global Settings  Management
   Commit changes

