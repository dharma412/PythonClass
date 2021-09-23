*** Settings ***
Library      String
Resource     sma/csdlresource.txt
Suite Setup     Selenium Login
suite Teardown  Selenium Close
Documentation   verifying FQDN command in GUI.

*** Variables ***
${CUSTOM_CA_CERT}=            %{SARF_HOME}/tests/testdata/sma/csdl/csdl_custom_ca.pem

*** Test Cases ***
Test1
    Edit SSL Configuration Settings
    ...  Peer Certificate FQDN Validation
    ...  FQDN
    ...  enable
    Commit changes

Test2
    Run Keyword And Expect Error  *
    ...  Edit Certificate Authorities  custom_list_enable=${True}
    ...  custom_list_cert_path=${CUSTOM_CA_CERT}  fqdn_validation=${True}

Test3
    Edit Certificate Authorities  custom_list_enable=${True}
    ...  custom_list_cert_path=${CUSTOM_CA_CERT}

