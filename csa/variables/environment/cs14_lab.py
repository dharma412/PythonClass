# $Id: //prod/main/sarf_centos/variables/environment/cs14_lab.py#1 $
# $DateTime: 2019/04/01 01:50:17 $
# $Author: sarukakk $

"""
==============================================================================
 cs14 PCloud lab Test Environment
==============================================================================
Robot variable file for .cs14 lab.
This file depents on two environment variables:
 WSA - should contain hostname of the WSA appliance under test
 SLICE_SERVER - should contain hostname of the FreeBSD server reserved for
 the slice (this variable is used in 'default' module)
"""

import os
import socket
from environment.common import *

INET_MODE = 'ipv4'
IPV_PARAM = '-4'

DNS = '192.168.0.252'
"""
==============================================================================
 cs14 PCloud lab Test Environment for WSA
==============================================================================
"""
REGION = 'America'
COUNTRY = 'United States'
TIME_ZONE = 'Los_Angeles'

SLICE_SERVER = os.environ.get("SLICE_SERVER")

IIS_SERVER = 'ad1.cs14'
#IIS_SERVER_UNIX_FORMAT = 'ad2.cs14'

# Tools Server - that's a box to run such tools as icaptestd.py
# It should be different from DUT, Client, and HTTP_SERVER
TOOLS = 'tools.cs14'

# HTTP Server
HTTP_SERVER = SLICE_SERVER
HTTP_SERVER_NEW = TOOLS


# server with special test files (badware, files by types etc)
SERVICE_SERVER = TOOLS

# HTTPS server that had expired certificate
# locate under /usr/local/etc/apache22/ssl/expired.crt
EXPIRED_HTTPS = TOOLS

# HTTPS server that had certificate with no CN defined
# locate under /usr/local/etc/apache22/ssl/nocn.crt
NOCN_HTTPS = TOOLS

# HTTPS server that had certificate with NULL character in CN
# locate under /usr/local/etc/apache22/ssl/nullincn.crt
NULLINCN_HTTPS = TOOLS

# Upstream proxy
#UPSTRM_PROX1 = "squid-server01.cs14"

# SSW
SSW_MODE = 'M1'         # M1 is an alias for Management Interface
# P1 - another option for Data Interface
ALERT_RCPT =   'testuser@mail.qa.sgg.cisco.com'

# Active Directory Server 1
AD1_SERVER = 'ad1.ad01.cs14'
AD1_SERVER_IP = '10.10.13.221'
AD1_DOMAIN = 'AD01.CS14'
AD1_NET_DOMAIN = 'AD01'
AD1_USER = 'user1'
AD1_USER_PW = 'pass1'
AD1_BASE_DN = 'cn=Users,dc=ad01,dc=cs14'
AD1_BIND_BASE_DN = 'cn=user1,cn=Users,dc=ad01,dc=cs14'
AD1_BIND_BASE_PW = 'pass1'
AD1_JOIN_USER = 'administrator'
AD1_JOIN_PW = 'Cisco1234$'
AD_JOIN_USER = 'administrator'
AD_JOIN_USER_PASSWORD = 'Cisco1234$'
AD1_SECRET = 'ironport'

# Windows 2008 Active Directory server
#WIN2K8_AD_SERVER = 'ad1.cs14'
#WIN2K8_AD_DOMAIN = 'AD01.CS3'
#WIN2K8_AD_JOIN_USER = 'administrator'
#WIN2K8_AD_JOIN_PW = 'Cisco1234$'

# NTLM auth variables
NTLM_AUTH_SERVER = AD1_SERVER
AD_DOMAIN = AD1_DOMAIN
AD_NET_DOMAIN = AD1_NET_DOMAIN
AD_SERVER1 = AD1_SERVER

# RADIUS auth variables
RADIUS_SERVER = 'radius-server01.cs14'
RADIUS_PORT = '1812'
RADIUS_SECRET = 'cisco123'
RADIUS_USER = 'user1'
RADIUS_USER_PASSWORD = 'user1pass'

# ex DLP server conf variable
EX_DLP_SERVER = SLICE_SERVER
EX_DLP_SERVER_PORT = '1344'
EX_DLP_RECONNECTIONS = '2'
EX_DLP_SERVICE_URL = 'icap://%s:%s/reqmod' % (EX_DLP_SERVER, EX_DLP_SERVER_PORT,)


# symantec
#SY_DLP_SERVER = 'symantecdlp.auto.sgg.cisco.com'
#SY_DLP_SERVER_PORT = '4000'
#SY_DLP_RECONNECTIONS = '2'
#SY_DLP_SERVICE_URL = 'icap://%s:%s/reqmod' % (SY_DLP_SERVER, SY_DLP_SERVER_PORT)

# FTP server
FTP_SERVER = SLICE_SERVER
FTP_SERVER_IP = socket.gethostbyname(FTP_SERVER)

FTP_SERVER_ROOT_DIR = '/home/ftpuser'
DIR_FOR_UPLOADS = 'uploads'

FTP_UPSTREAM_PROXY = SLICE_SERVER

FTP_UPSTREAM_DUT_PROXY_PORT = '8021'
FTP_UPSTREAM_PROXY_PORT = '8081'
DUT_FTP_PROXY_PORT = '8021'
DUT_HTTP_PROXY_PORT = '3128'

DIR_WITH_FILES_FOR_UPLOAD = '/home/testuser/files_for_upload'

# cpt snmp variables
#SNMP_ENABLED = 'yes'   # Specify whether to enable or disable snmp: 'yes' or 'no'
#SNMP_IP_INTERFACE = 'Management'    # Specify an interface for SNMP requests: 'Management', 'P1', 'P2'
#SNMP_V3PHRASE = 'ironport'    # Specify SNMPv3 passphrase which must be at least 8 chars
#SNMP_PORT = '161'    # Specify port that SNMP daemon listens on
#SNMP_V2ENABLED = 'yes'    # Specify whether to service SNMP v1/v2 requests: 'yes' or 'no'
#SNMP_V2PHRASE = 'ironport'  # specify v1/v2 community string
#SNMP_V2NETWORK = '10.92.147.0/24'    # Specify networks that v1/v2 requests are allowed
#SNMP_TRAP_TARGET = '10.92.145.222'    # Specify trap target ip
#SNMP_TRAP_PHRASE = 'ironport'  # Specify trap community string
#SNMP_TRAP_CONFIG_PATH = '/usr/local/etc/snmp/snmptrapd.conf'    # Specify trap configuration file path
#SNMP_CHANGE_TRAP_STATUS = 'no'    # Specify whether to change current settings for enterprise trap status: 'yes' or 'no'
#SNMP_LOCATION = 'San Bruno, CA USA'   # Specify location string
#SNMP_CONTACT = 'admin@system.com'    # Specify contact string
#SNMP_MIBS = '+ASYNCOS-MAIL-MIB'   # Included MIB module
#SNMP_VERSION = '3'   # SNMP version - 3 or 2c
#SNMP_SECNAME_v1 = 'v1get'   # Security name - corresponds to -u option in snmpwalk ver. 1
#SNMP_SECNAME_v2 = 'v2get'   # Security name - corresponds to -u option in snmpwalk ver. 2
#SNMP_SECNAME = 'v3get'   # Security name - corresponds to -u option in snmpwalk ver. 3
#SNMP_AUTH_PROTOCOL = 'MD5'    # Snmp authentication protocol - SHA | MD5
#SNMP_V3_SECLEVEL = 'authNoPriv'    # SNMP version 3 security level - coresponds to -l option
#SNMP_NET_MIB_DIR = '/usr/local/share/snmp/mibs'   # Net snmp standard mib directory
#SNMP_IRONPORT_MIB_DIR = '/home/www/mibs/main'   # Ironport standard mib directory

# Feature Key update server
FEATURE_KEY_UPDATES_SERVER = 'qa10.qa.sgg.cisco.com'
FEATURE_KEY_BASE_PATH = '/home/upgrades/fkey/data'
FK_UPDATES_SERVER = FEATURE_KEY_UPDATES_SERVER
UPDATE_SERVER = 'update-manifests.ironport.com'

AD_JOIN_USER_01 = 'administrator'
AD_JOIN_USER_PASS_01 = 'Cisco1234$'
AD_JOIN_USER_PASS_WRONG = 'ironport'

#DNS_IP_01 = '10.10.201.12'
#DNS_IP_02 = '10.10.201.13'
#DNS_IP_03 = '10.10.201.14'
#DNS_IP_04 = '10.10.201.15'
#DNS_IP_05 = '10.10.201.16'
#DNS_IP_06 = '10.10.201.17'
#DNS_IP_07 = '10.10.201.18'
#DNS_IP_08 = '10.10.201.19'
#DNS_IP_09 = '10.10.201.20'
#DNS_IP_10 = '10.10.201.21'

# FEEDS_SERVERS
#FEED_SERVER = 'ad1.cs14'
#NGINX_SERVER = 'nginx-server01.cs14'
#LIGHTTPD_SERVER = 'lighttpd-server01.cs14'

# WCCP ROUTER IP. This IP Adrress belongs to cs14 Lab
#WCCP_ROUTER_IP_M1 = 'SET:WCCP_ROUTER_IP_M1'
#WCCP_ROUTER_IP_P1 = 'SET:WCCP_ROUTER_IP_P1'

# x509 OCSP Responder
#X509_OCSP_RESPONDER = TOOLS
#OCSP_SERVER = TOOLS

#WBNP_SERVER = 'wbnp01.cs14.devit.ciscolabs.com'

#ISE Server Details
ISE_SERVER_HOST_NAME = 'ISESErver.cs14.devit.ciscolabs.com'
ISE_SERVER_IP = '10.10.13.227'
ISE_SERVER_USER = 'admin'
ISE_SERVER_USER_PWD = 'Ironport1'
ERS_ADMIN_USER = 'ERSAdmin'
ERS_ADMIN_USER_PWD = 'Ironport1'

#Kerberos Client Details
KERBEROSE_CLIENT_HOST = 'Kerberos-client02.cs14'
KERBEROSE_CLIENT_IP = '10.10.13.226'
KERBROSE_CLIENT_USER = 'iseuser'
KERBROSE_CLIENT_USER_PWD = 'Ironport1'

"""
==============================================================================
 cs14 PCloud lab Test Environment for ESA
==============================================================================
"""

#Commenting this variable since its common for WSA and ESA
#FTP_SERVER = CLIENT_HOSTNAME

# LDAP auth variables is common for WSA and ESA
LDAP_AUTH_SERVER = 'LdapServer.cs14'
LDAP_SERVER_TYPE = 'openldap'
LDAP_AUTH_PORT = '389'
LDAP_BASE_DN = 'dc=qa32,dc=qa'
USER_NAME_ATTR = 'uid'
BASE_DN = 'dc=qa32,dc=qa'
LDAP_BINDDN = 'cn=admin,%s' % (LDAP_BASE_DN,)
LDAP_PASSWORD = 'ironport'
#LDAP_ADMIN_DN = 'cn=administrator,cn=Users,dc=ad1,dc=cs14'
#LDAP_ADMIN_PASS = 'Cisco1234$'
LDAP_BIND_BASE_DN = 'cn=administrator,cn=Users,dc=ad1,dc=cs14'
LDAP_BIND_BASE_PW = 'Cisco1234$'

BIND_SERVER = 'vm30bsd0149.ibqa'

#RADIUS_SERVER = 'vm30bsd0149.ibqa'

CRES_SERVER = 'res.cisco.com'
CRES_ADMIN = 'rtestuser@ironport.com'
CRES_ADMIN_PASSWORD = 'ironport123'
PXE_SERVER = 'vm30iea0004.ibqa'

MAIL_DELIVERY_SERVER = 'mail.qa.sgg.cisco.com'
STAGE_SDS = 'v2.beta.sds.cisco.com'
PROD_SDS = 'v2.sds.cisco.com'
STAGE_UPDATER = 'stage-update-manifests.ironport.com'
SYSLOG_SERVER = TOOLS

#Updater Servers
QA_UPDATER = 'ops-updates-vip.vega.ironport.com'
DEFAULT_UPDATER = 'update-manifests.ironport.com'
STAGING_UPDATE_SERVER_FOR_HARDWARE = 'stage-updates.ironport.com'
STAGING_UPDATE_SERVER_FOR_VIRTUAL  = 'stage-stg-updates.ironport.com'
PRODUCTION_UPDATE_SERVER_FOR_HARDWARE = 'update-manifests.ironport.com'
PRODUCTION_UPDATE_SERVER_FOR_VIRTUAL  = 'update-manifests.sco.cisco.com'
OPS_UPDATE_SERVER_FOR_HARDWARE = 'ops-updates-vip.vega.ironport.com'
OPS_UPDATE_SERVER_FOR_VIRTUAL  = 'ops-updates-cc-vip.vega.ironport.com'
TEST_UPDATER= 'updater01.ibqa.sgg.cisco.com'
UPDATE_SERVER= 'update-manifests.ironport.com'
IBQA_UPDATER= 'updater03.ibqa.sgg.cisco.com'
SDS_SIMULATOR = 'v2.sds.cisco.com'
#AD Server variables
ADSERVER = 'iaf-w2k3-ad1.ibqa'
ADSERVER_PROXY = '10.76.68.26:3129:4'
ADSERVER_PROXYWITHOUTMASK = '10.76.68.26:3129'

CLOUD_DOMAIN = 'a.immunet.com'
CLOUD_SERVER_POOL = 'amp-cloud-sa-ext.qa.immunet.com'
FILE_ANALYSIS_SERVER_URL = 'https://intel.api.sourcefire.com'
CLOUD_SERVER_PRODUCTION = 'cloud-sa.amp.sourcefire.com'

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

# cpt snmp variables
SNMP_ENABLED      = 'yes'           # Specify whether to enable or disable snmp: 'yes' or 'no'
SNMP_IP_INTERFACE = 'Management'    # Specify an interface for SNMP requests: 'Management', 'P1', 'P2'
SNMP_V3PHRASE     = 'ironport'      # Specify SNMPv3 passphrase which must be at least 8 chars
SNMP_PORT         = '161'           # Specify port that SNMP daemon listens on
SNMP_V2ENABLED    = 'yes'           # Specify whether to service SNMP v1/v2 requests: 'yes' or 'no'
SNMP_V2PHRASE     = 'ironport'      # specify v1/v2 community string
SNMP_TRAP_PHRASE  = 'ironport'      # Specify trap community string
SNMP_TRAP_CONFIG_PATH = '/usr/local/etc/snmp/snmptrapd.conf'    # Specify trap configuration file path
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
SNMP_PRIVACY_PASSWORD = 'Cisco123$'
SNMP_SECNAME_v1 = 'v1get'   # Security name - corresponds to -u option in snmpwalk ver. 1

# ssh tunnel variables
SSH_TUNNEL_HOST = 'tunnels-int.cisco.com'

# Harpe Tool Machine for parsing Rewritten URLs
HARPE_TOOL_HOST = '10.76.70.229'
HARPE_HOST_USERNAME = 'root'
HARPE_HOST_PASSWD = 'cisco123'

VSPHERES = (('10.225.96.6', 'CISCO\\cs.automation.gen', 'Cisco123$'),)

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
ADMIN_USER                 =  'DUMMY_TO_BE_FILLED'
