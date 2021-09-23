# $ Id: $
# $ DateTime:  $
# $ Author: $

import os

Certificate                     =      os.environ['SARF_HOME'] + '/tests/testdata/sma/saml/sample_cert.pem'
USER_ROLE                       =      'admin'
USER_ROLE_DEVOPS                =      'devops'
SP_ENTITY_ID                    =      'sp_entity_id'
ASSERTION_CONSUMER_URL          =      'http://${DUT}'
ASSERTION_CONSUMER_URL_DEVOPS   =      'http://${DUT}/devops_sso'
CERT_FILE                       =      os.environ['SARF_HOME'] + '/tests/testdata/sma/saml/sample_cert.pem'
CERT_KEY                        =      os.environ['SARF_HOME'] + '/tests/testdata/sma/saml/sample_key.key'
CERTIFICATE_PASSPHRASE          =      'ironport'
SIGN_REQUEST                    =      str(1)
ORGANIZATION_NAME               =      'cisco'
ORGANIZATION_DISPLAY_NAME       =      'Cisco Systems'
TEST_SP_PROFILE                 =      'test_sp_customer'
TEST_IDP_PROFILE                =      'test_idp_customer'
ORGANIZATION_URL                =      'http://www.cisco.com/'
ORGANIZATION_TECHNICAL_CONTACT  =      'test@cisco.com'
CONFIGURATION_MODE              =      'Import IDP Metadata'
IDP_METADATA                    =      os.environ['SARF_HOME'] + '/tests/testdata/sma/saml/sample_idp_metadata.xml'
IDP_ENTITY_ID                   =      'wsa.saas.com'
CONFIGURATION_MODE_MANUAL       =      'Configure Keys Manually'
SSO_URL                         =      'http://mus.cisco.com/SSOURL/SMA'
CERT_FILE_OTH_FORMAT            =      os.environ['SARF_HOME'] + '/tests/testdata/sma/saml/test_cerificate_ext.txt'
CERT_KEY_OTH_FORMAT             =      os.environ['SARF_HOME'] + '/tests/testdata/sma/saml/test_cert_key_format.txt'
IDP_METADATA_OTH_FORMAT         =      os.environ['SARF_HOME'] + '/tests/testdata/sma/saml/test_format_metadata.txt'
IDP_METADATA_ACTION_PASTE       =      'PASTE'
IDP_METADATA_ACTION_ENTER       =      'ENTER'
SAML_GROUP                      =      'my_group'
SAML_GROUP_NEW                  =      'samlgroup_new'
SAML_GROUP_ATTRIB               =      'memberof'
SAML_GROUP_ROLE_ADMIN           =      1
SAML_GROUP_ROLE_OPERATOR        =      2
SAML_GROUP_ROLE_CLOUD           =      3
SAML_GROUP_ROLE_READONLY        =      4
SAML_GROUP_ROLE_GUEST           =      6
TEST_SP_PROFILE_EDIT            =      'sp_profile_edit'
TEST_IDP_PROFILE_EDIT           =      'idp_profile_edit'
TEST_SP_DEVOPS_PROFILE          =      'sp_devops_profile'
TEST_IDP_DEVOPS_PROFILE         =      'idp_devops_profile'
SAML_AZUR_USER                  =      'testuser@maresa.onmicrosoft.com'
SAML_AZUR_USER_PASSWORD         =      'Ironport123$'
USER_ROLE_CUSTOMER              =      'customer'

#SAML UI LOGIN VARIABLES
SP_ENTITY_ID_Azure              =        'cs33_sso_entity_id'
SAML_GROUP_Azure                =        'ea6064aa-d6fc-48d3-abb8-1728e1f39e0b'
CERT_FILE_SP_Azure              =        os.environ['SARF_HOME'] + '/tests/testdata/sma/azure_idp/sp_cert.crt'
CERT_FILE_KEY_SP_Azure          =        os.environ['SARF_HOME'] + '/tests/testdata/sma/azure_idp/sp_cert_key.pem'
IDP_Metadata_Azure              =        os.environ['SARF_HOME'] + '/tests/testdata/sma/azure_idp/azure_metadata.xml'

#SAML EUQ LOGIN VARIABLES
EUQ_SP_ENTITY_ID                   =        'entity_id'
EUQ_SAML_GROUP                     =        'e2b9c376-395c-4b81-a93e-65d4296e26a8'
EUQ_CERT_FILE_SP_Azure             =        os.environ['SARF_HOME'] + '/tests/testdata/sma/azure_idp/sp_cert.crt'
EUQ_CERT_FILE_KEY_SP_Azure         =        os.environ['SARF_HOME'] + '/tests/testdata/sma/azure_idp/sp_cert_key.pem'
EUQ_IDP_Metadata_Azure             =        os.environ['SARF_HOME'] + '/tests/testdata/sma/azure_idp/azure_metadata.xml'
