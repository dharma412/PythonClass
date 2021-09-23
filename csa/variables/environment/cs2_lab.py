# $Id: //prod/main/sarf_centos/variables/environment/cs2_lab.py#6 $
# $DateTime: 2019/09/12 22:11:48 $
# $Author: saurgup5 $

"""
==============================================================================
                        CS2 lab Test Environment
==============================================================================
"""
import os
from environment.common import *

INET_MODE = 'ipv4'

DNS = '192.168.0.252'

FTP_SERVER = 'vm09bind0001.cs2'

#Below is the token from production portal, token will expire on 30th July 2021
SL_TOKEN_ID =  'ZmQ4ZjQwNDctZjAyZC00NGFiLTg1ZWEtMDY5ZTQwOWVjZTEzLTE2Mjc2MjYw%0AODg2ODB8RGozU2VINzFTa1JoV2U4ckJFRGdSY3ozc2labmdUb0d2WGlXQzMv%0AbmFybz0%3D%0A'

# LDAP auth variables
LDAP_AUTH_SERVER = 'vm09bsd0064.cs2'
LDAP_SERVER_TYPE = 'openldap'
LDAP_AUTH_PORT = '389'
LDAP_BASE_DN = 'dc=qa32,dc=qa'
BASE_DN = 'dc=qa32,dc=qa'
LDAP_BINDDN = 'cn=admin,%s' % (LDAP_BASE_DN,)
LDAP_PASSWORD = 'ironport'
LDAP_AUTOMATION_USER = 'automation_user'
LDAP_AUTOMATION_USER_PSW = 'Cisco123$'
LDAP_AUTOMATION_USER_GROUP = 'main_group'

BIND_SERVER = 'vm09bind0001.cs2'

RADIUS_SERVER = 'vm09radius0001.cs2'
RADIUS_SHARED_SECRET = 'testing123'

CRES_SERVER = 'res.cisco.com'
CRES_ADMIN = 'rtestuser@ironport.com'
CRES_ADMIN_PASSWORD = 'ironport123'
PXE_SERVER = 'vm30iea0004.ibqa'

MAIL_DELIVERY_SERVER = 'mail.qa.sgg.cisco.com'
STAGE_SDS = 'v2-web-intel-rest-beta.talos.cisco.com'
PROD_SDS = 'v2-web-intel-rest.talos.cisco.com'
STAGE_UPDATER = 'stage-update-manifests.ironport.com'
STAGE_SDR = 'email-sender-domain-rep-rest.talos-beta.cisco.com'
PRODUCTION_SDR = 'email-sender-domain-rep-rest.talos.cisco.com'
STAGE_SDS_SERVER = 'v2.beta.sds.cisco.com'

#Updater Servers
QA_UPDATER = 'ops-updates-vip.vega.ironport.com'
DEFAULT_UPDATER = 'update-manifests.ironport.com'
STAGING_UPDATE_SERVER_FOR_HARDWARE = 'stage-updates.ironport.com'
STAGING_UPDATE_SERVER_FOR_VIRTUAL  = 'stage-stg-updates.ironport.com'
PRODUCTION_UPDATE_SERVER_FOR_HARDWARE = 'update-manifests.ironport.com'
PRODUCTION_UPDATE_SERVER_FOR_VIRTUAL  = 'update-manifests.sco.cisco.com'
OPS_UPDATE_SERVER_FOR_HARDWARE = 'ops-updates-vip.vega.ironport.com'
OPS_UPDATE_SERVER_FOR_VIRTUAL  = 'ops-updates-cc-vip.vega.ironport.com'
LOCAL_UPDATE_SERVER_FOR_HARDWARE = 'updater01.ibqa.sgg.cisco.com'
LOCAL_UPDATE_SERVER_FOR_VIRTUAL = 'updater01.ibqa.sgg.cisco.com'
TEST_UPDATER= 'updater01.ibqa.sgg.cisco.com'
UPDATE_SERVER= 'update-manifests.ironport.com'
IBQA_UPDATER= 'updater03.ibqa.sgg.cisco.com'
SDS_SIMULATOR = 'v2.sds.cisco.com'
#AD Server variables
ADSERVER = 'iaf-w2k3-ad1.ibqa'
ADSERVER_PROXY = '10.76.68.26:3129:4'
ADSERVER_PROXYWITHOUTMASK = '10.76.68.26:3129'

CLOUD_DOMAIN = 'a.immunet.com'
FILE_ANALYSIS_SERVER_URL = 'https://intel.api.sourcefire.com'
FILE_ANALYSIS_SERVER= 'AMERICAS (https://panacea.threatgrid.com)'
CLOUD_SERVER_PRODUCTION = 'cloud-sa.amp.sourcefire.com'
TG_SERVER1 = 'https://tgif-01-clean.ibqa.sgg.cisco.com'
TG_SERVER2 = 'https://tgif-02-clean.ibqa.sgg.cisco.com'
FILE_ANALYSIS_URL = 'https://panacea.threatgrid.com'
FILE_ANALYSIS_URL_SELECT = 'https://panacea.threatgrid.com'
CLOUD_SERVER_POOL = 'cloud-sa.amp.cisco.com'
REPUTATION_SERVER=  'AMERICAS (cloud-sa.amp.cisco.com)'

#Proxy servers
HTTP_PROXY = 'http://64.102.255.40:80'
HTTPS_PROXY = 'https://64.102.255.40:443'
CISCO_PROD_HTTP_PROXY = 'http://proxy.esl.cisco.com:80'
CISCO_PROD_HTTPS_PROXY = 'https://proxy.esl.cisco.com:80'

#Stunnel Proxy Server for ESA
WSA_PROXY = '10.76.70.198'
PROXY_PORT = '3128'
PROXY_USERNAME = 'admin'
PROXY_PASSWORD = 'ironport'

THIRD_PARTY_TOOLS_UPDATE_SERVER = 'qa-updater2.vega.ironport.com:443'

#File Analysis Proxy Server for ESA
FA_PROXY_SERVER = 'proxy.esl.cisco.com'
FA_PROXY_PORT = '80'
FA_PROXY_USERNAME = 'admin2'
FA_PROXY_PASSWORD = 'Cisco1234'
# cpt snmp variables
SNMP_ENABLED      = 'yes'           # Specify whether to enable or disable snmp: 'yes' or 'no'
SNMP_IP_INTERFACE = 'Management'    # Specify an interface for SNMP requests: 'Management', 'P1', 'P2'
SNMP_V3PHRASE     = 'ironport'      # Specify SNMPv3 passphrase which must be at least 8 chars
SNMP_PORT         = '161'           # Specify port that SNMP daemon listens on
SNMP_V2ENABLED    = 'yes'           # Specify whether to service SNMP v1/v2 requests: 'yes' or 'no'
SNMP_V2PHRASE     = 'ironport'      # specify v1/v2 community string
SNMP_TRAP_PHRASE  = 'ironport'      # Specify trap community string
SNMP_CHANGE_TRAP_STATUS  = 'no'     # Specify whether to change current settings for enterprise trap status: 'yes' or 'no'
SNMP_LOCATION     = 'San Bruno, CA USA'   # Specify location string
SNMP_CONTACT      = 'admin@system.com'    # Specify contact string
SNMP_MIBS         = '+ASYNCOS-MAIL-MIB'   # Included MIB module
SNMP_VERSION      = '3'                   # SNMP version - 3 or 2c
SNMP_SECNAME      = 'v3get'               # Security name - corresponds to -u option in snmpwalk
SNMP_AUTH_PROTOCOL = 'MD5'                # Snmp authentication protocol - SHA | MD5
SNMP_V3_SECLEVEL   = 'authNoPriv'         # SNMP version 3 security level - coresponds to -l option
SNMP_NET_MIB_DIR   = '/usr/local/share/snmp/mibs'   # Net snmp standard mib directory
SNMP_IRONPORT_MIB_DIR = '/home/www/mibs/main'       # Ironport standard mib directory

# Harpe Tool Machine for parsing Rewritten URLs
HARPE_TOOL_HOST = 'vm09harpe0001.cs2'
HARPE_HOST_USERNAME = 'root'
HARPE_HOST_PASSWD = 'cisco123'

# CS2 lab VCenter is u32c01p09-vc.cisco.com
VSPHERES = (('10.196.152.79', 'CISCO\\cs.autobot.gen', 'Cisco456!'),)

# SAML Parameters
ADFS_IDP_HOSTNAME = 'vm30win0009.ibqa'
ADFS_IDP_USER_DOMAIN = 'postx.sgg.cisco.com'
ADFS_IDP_USERNAME = 'aminath@postx.sgg.cisco.com'
ADFS_IDP_PASSWORD = 'cisco@123'

WSA_IDP_HOSTNAME = 'vm30wsa0007.ibqa.sgg.cisco.com'

# FIPS Compliant Certificate
FIPS_CERT_PATH = '{0}/tests/testdata/fips_cert/'.format(os.environ['SARF_HOME'])
FIPS_COMPLIANT_CA_FILE = 'fips_compliant_ca.pem'
FIPS_COMPLIANT_CA_NAME = 'ESA_AUTOMATION_FIPS_CA'
FIPS_COMPLIANT_CERT_FILE = 'fips_compliant_certificate.p12'
FIPS_COMPLIANT_CERT_PASSWD = 'cisco123'
FIPS_COMPLIANT_CERT_NAME = 'ESA_AUTOMATION_FIPS_DEVICE_CERT'


# SNMP server details for snmp ipv6 test cases
SNMP_SERVER_HOST = 'DUMMY_TO_BE_FILLED'
SNMP_SERVER_IPV4 = 'DUMMY_TO_BE_FILLED'
SNMP_SERVER_IPV6 = 'DUMMY_TO_BE_FILLED'
SNMP_SERVER_USER = 'DUMMY_TO_BE_FILLED'
SNMP_SERVER_PWD = 'DUMMY_TO_BE_FILLED'


#CDA Variables
CDA_IP                     =  'DUMMY_TO_BE_FILLED'
CDA_URL                    =  'DUMMY_TO_BE_FILLED'
CDA_USERNAME               =  'DUMMY_TO_BE_FILLED'
CDA_PASSWORD               =  'DUMMY_TO_BE_FILLED'
KERBROSE_CLIENT_IP         =  'DUMMY_TO_BE_FILLED'
ADMIN_USER                 =  'DUMMY_TO_BE_FILLED'
KERBROSE_CLIENT_PASSWORD   =  'DUMMY_TO_BE_FILLED'
KERBROSE_CLIENT_USER       =  'DUMMY_TO_BE_FILLED'

#Local DNS server IP for DANE
DANE_DNS = '10.10.2.184'

#DANE Testing Domains
DANE_MTA = 'vm09esa0197.cs2'
DANE_SUCCESS_DOMAIN = 'test-dane.net'
TLSA_BOGUS_DOMAIN = 'test-tlsabogus.net'
NO_TLSA_DOMAIN = 'test-notlsa.net'
TLSA_INSEC_DOMAIN = 'test-tlsainsec.net'
INCORRECT_MATCH_FIELD_DOMAIN = 'test-tlsamatch.net'
WRONG_TLSA_DOMAIN = 'test-tlsalength.net'
INCORRECT_CERTIFICATE_USAGE_DOMAIN = 'test-tlsausage.net'
MXINSEC_AINSEC_DOMAIN = 'testunsign.net'
CNAME_SUCCESS_DOMAIN = 'test-cname.net'
CNAME_TLSAINSEC = 'test-mxcasectinsec.net'
CNAME_NOTLSA = 'test-cname6.net'
CNAME_INSECA = 'test-cname2.net'
CNAME_INSEC = 'test-cnameunsign.net'
CERT_FAIL_DOMAIN = 'test-certfail.net'
CERT_FAIL_TRY_NEXT_MX = 'test-certfail2.net'
MXBOGUS_DOMAIN = 'test-mxbogus.net'
MXSEC_ABOUGS_DOMAIN = 'mxsecabogus.net'
MXSEC_AINSEC_DOMAIN = 'mxsecainsec.net'
MXSEC_AINSEC_NOTLSA_DOMAIN = 'mxsecainsecnotlsa.net'
MXSEC_ASEC_TLSABOGUS_DOMAIN = 'test-tlsabogusfail.net'

#OnPrem2013 Variables
ONPREM_USER_2013 = 'administrator'
ONPREM_PASSWORD_2013 = 'Exchange@2013'
EXCHANGE_IP_2013 = '10.10.2.149'

#OnPrem2016 Variables
ONPREM_USER_2016 = 'administrator'
ONPREM_PASSWORD_2016 = 'Cisco123$'
EXCHANGE_IP_2016 = '10.10.2.150'

#proxy url
CISCO_STAGE_URL = 'http://stage.secure-web.sco.cisco.com'
CISCO_HTTPS_STAGE_URL = 'https://stage.secure-web.sco.cisco.com'
CISCO_STAGE_URL_FOR_VIRTUAL = 'http://stage.secure-web.sco.cisco.com'
CISCO_STAGE_URL_FOR_HARDWARE = 'http://secure-web.cisco.com'

#ClamAV Variables
CLAMAV_CLOUD_SERVER_POOL = 'cloud-sa.amp.cisco.com'
CLAMAV_FILE_ANALYSIS_URL = 'https://panacea.threatgrid.com'
CLAMAV_FILE_ANALYSIS_URL_SELECT = 'https://panacea.threatgrid.com'
CLAMAV_FILE_ANALYSIS_SERVER = '4.14.36.148'
CLAMAV_FILE_REP_SERVER = '52.21.117.50'

#Search And Remediate Variable
SAR_DOMAIN = 'scale.com'
SAR_IP = '10.10.2.148'
SAR_ONPREM_USER = 'administrator'
SAR_ONPREM_PASSWORD = 'Cisco123$'

#Stage portal SSE Variables
PORTAL_SSE_URL = "https://stage-portal.sse.itd.cisco.com/login"
PORTAL_SSE_USER_NAME = "testuser@ironport.com"
PORTAL_SSE_PASS_WORD = "Cisco123$"
CSN_USER = 'testcsn'
CSN_USER_PASSWORD = 'Ironport153$'

# Beaker Gripmock Server details
GRIPMOCK_SERVER = '10.10.4.103'
GRIPMOCK_USERNAME = 'testuser'
GRIPMOCK_PASSWORD = 'ironport'
GRIPMOCK_DOCKER_CONTAINER='containers.cisco.com/talos_onbox/gripmock'
GRIPMOCK_BASE_DIR='/home/testuser/gripmock'
GRIPMOCK_PBUF_FILE='{}/tests/testdata/esa/gripmock/pbufs/cs2_mock_server.pbuf'.format(os.environ['SARF_HOME'])

#Cisco AD Details
CISCO_TEST_USER_NAME = 'testuser'
CISCO_TEST_USER_MAIL = 'testuser@cisco.com'
CISCO_TEST_PASSWORD = 'Ironport678$'
CISCO_TEST_USER_GROUP = 'lys-alpha-users'
CISCO_AD_SERVER = '173.36.12.198'
CISCO_AD_PORT = '3269'
CISCO_AD_BASEDN = 'dc=cisco, dc=com'

#CSA Token
CSA_TOKEN= 'N5N4PQRpPkmWWokHTyRPgw=='
CSA_TERRANOVA_SERVER= 'https://secat.cisco.com/portal/api/data/report/2020'

# OIDC ADFS Parameters
ADFS_IP = '10.10.4.105'
ADFS_HOSTNAME = 'WIN-BL0P4116VDB.onpremesa.com'
ADFS_AUTH_URL = 'https://u32c01p09-vrouter.cisco.com:40543/adfs/oauth2/token'
ADFS_RESOURCE = 'https://u32c01p21-vrouter.cisco.com'
ADFS_USERNAME = 'onpremesa.com\\administrator'
ADFS_PASSWORD = 'Cisco123$'
ADFS_CLIENT_ID = 'ab762716-544d-4aeb-a526-687b73838a36'
ADFS_SCOPE = 'openid'
ADFS_GRANT_TYPE = 'password'

OIDC_METADATA_URL = 'https://WIN-BL0P4116VDB.onpremesa.com/adfs/.well-known/openid-configuration'
OIDC_ISSUER = 'http://WIN-BL0P4116VDB.onpremesa.com/adfs/services/trust'
OIDC_AUIDENCE = 'https://u32c01p21-vrouter.cisco.com'

#Mar Details
MAR_THUMBPRINT = 'uwvQDDvN0MRH3UbBCriH1MrDlh0='
