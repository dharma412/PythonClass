# $Id: //prod/main/sarf_centos/variables/environment/ibauto_lab.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""
==============================================================================
                        IBAuto lab Test Environment
==============================================================================
Robot variable file for .ibauto lab.
This file depents on two environment variables:
    WSA - should contain hostname of the WSA appliance under test
    SLICE_SERVER - should contain hostname of the FreeBSD server reserved for
    the slice (this variable is used in 'default' module)
"""

import socket, os
from environment.common import *

INET_MODE = 'ipv4'
IPV_PARAM = '-4'

DNS = '10.225.96.31'

REGION = 'America'
COUNTRY = 'United States'
TIME_ZONE = 'Los_Angeles'

SLICE_SERVER = os.environ.get("SLICE_SERVER")

IIS_SERVER = 'ad1.ibauto'
IIS_SERVER_UNIX_FORMAT = 'ad2.ibauto'

# Tools Server - that's a box to run such tools as icaptestd.py
# It should be different from DUT, Client, and HTTP_SERVER
TOOLS = 'tools.ibauto'

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
UPSTRM_PROX1 = "sarf-squid.ibauto"

# SSW
SSW_MODE = 'M1' # M1 is an alias for Management Interface
                # P1 - another option for Data Interface

# Active Directory Server 1
AD1_SERVER = 'ad1.ibauto'
AD1_DOMAIN = 'AD01.IBAUTO'
AD1_NET_DOMAIN = 'AD01'
AD1_USER = 'user1'
AD1_USER_PW = 'pass1'
AD1_BASE_DN = 'cn=Users,dc=ad01,dc=ibauto'
AD1_BIND_BASE_DN = 'cn=user1,cn=Users,dc=ad01,dc=ibauto'
AD1_BIND_BASE_PW = 'pass1'
AD1_JOIN_USER = 'administrator'
AD1_JOIN_PW = 'Cisco1234$'
AD_JOIN_USER = 'administrator'
AD_JOIN_USER_PASSWORD = 'Cisco1234$'
AD1_SECRET = 'ironport'

# Active Directory Server 2
AD2_SERVER = 'ad2.ibauto'
AD2_DOMAIN = 'AD202.IBAUTO'
AD2_NET_DOMAIN = 'AD02'
AD2_USER = 'user1'
AD2_USER_PW = 'pass1'
AD2_BASE_DN = 'cn=Users,dc=ad02,dc=ibauto'
AD2_BIND_BASE_DN = 'cn=user1,cn=Users,dc=ad02,dc=ibauto'
AD2_BIND_BASE_PW = 'pass1'
AD2_JOIN_USER = 'administrator'
AD2_JOIN_PW = 'Cisco1234$'

#Windows 2008 Active Directory server
WIN2K8_AD_SERVER = 'ad01.ibauto'
WIN2K8_AD_DOMAIN = 'AD01.IBAUTO'
WIN2K8_AD_JOIN_USER = 'administrator'
WIN2K8_AD_JOIN_PW = 'Cisco1234$'

# NTLM auth variables
NTLM_AUTH_SERVER = AD1_SERVER
AD_DOMAIN = AD1_DOMAIN
AD_NET_DOMAIN = AD1_NET_DOMAIN
AD_SERVER1 = AD1_SERVER

# LDAP auth variables
# Until an open ldap server is setup, using AD server for LDAP.
LDAP_AUTH_SERVER = 'ad1.ibauto'
LDAP_AUTH_PORT = '389'
LDAP_BASE_DN = 'dc=ad01,dc=ibauto'
USER_NAME_ATTR = 'uid'
USER_FILTER_QUERY     =  'objectclass'
LDAP_ADMIN_DN = 'cn=administrator,cn=Users,dc=ad01,dc=ibauto'
LDAP_ADMIN_PASS = 'Cisco1234$'

LDAP_USER = 'ldapuser'
LDAP_USER_PASSWORD = 'ironport'

LDAP_BIND_BASE_DN = LDAP_ADMIN_DN
LDAP_BIND_BASE_PW = LDAP_ADMIN_PASS

#RADIUS auth variables
RADIUS_SERVER = 'radius-server.ibauto'
RADIUS_PORT = '1812'
RADIUS_SECRET = 'cisco123'
RADIUS_USER = 'user1'
RADIUS_USER_PASSWORD = 'user1pass'


# ex DLP server conf variable
EX_DLP_SERVER = SLICE_SERVER
EX_DLP_SERVER_PORT = '1344'
EX_DLP_RECONNECTIONS = '2'
EX_DLP_SERVICE_URL = 'icap://%s:%s/reqmod' % (EX_DLP_SERVER, EX_DLP_SERVER_PORT,)


#symantec
SY_DLP_SERVER = 'symantecdlp.auto.sgg.cisco.com'
SY_DLP_SERVER_PORT = '4000'
SY_DLP_RECONNECTIONS = '2'
SY_DLP_SERVICE_URL = 'icap://%s:%s/reqmod' % (SY_DLP_SERVER, SY_DLP_SERVER_PORT)

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
SNMP_ENABLED      = 'yes'           # Specify whether to enable or disable snmp: 'yes' or 'no'
SNMP_IP_INTERFACE = 'Management'    # Specify an interface for SNMP requests: 'Management', 'P1', 'P2'
SNMP_V3PHRASE     = 'ironport'      # Specify SNMPv3 passphrase which must be at least 8 chars
SNMP_PORT         = '161'           # Specify port that SNMP daemon listens on
SNMP_V2ENABLED    = 'yes'           # Specify whether to service SNMP v1/v2 requests: 'yes' or 'no'
SNMP_V2PHRASE     = 'ironport'      # specify v1/v2 community string
SNMP_V2NETWORK    = '10.92.147.0/24'# Specify networks that v1/v2 requests are allowed
SNMP_TRAP_TARGET  = '10.92.145.222' # Specify trap target ip
SNMP_TRAP_PHRASE  = 'ironport'      # Specify trap community string
SNMP_TRAP_CONFIG_PATH = '/usr/local/etc/snmp/snmptrapd.conf' ## Specify trap configuration file path
SNMP_CHANGE_TRAP_STATUS  = 'no'     # Specify whether to change current settings for enterprise trap status: 'yes' or 'no'
SNMP_LOCATION     = 'San Bruno, CA USA'   # Specify location string
SNMP_CONTACT      = 'admin@system.com'    # Specify contact string
SNMP_MIBS         = '+ASYNCOS-MAIL-MIB'   # Included MIB module
SNMP_VERSION      = '3'                   # SNMP version - 3 or 2c
SNMP_SECNAME_v1   = 'v1get'               # Security name - corresponds to -u option in snmpwalk ver. 1
SNMP_SECNAME_v2   = 'v2get'               # Security name - corresponds to -u option in snmpwalk ver. 2
SNMP_SECNAME      = 'v3get'               # Security name - corresponds to -u option in snmpwalk ver. 3
SNMP_AUTH_PROTOCOL = 'MD5'                # Snmp authentication protocol - SHA | MD5
SNMP_V3_SECLEVEL   = 'authNoPriv'         # SNMP version 3 security level - coresponds to -l option
SNMP_NET_MIB_DIR   = '/usr/local/share/snmp/mibs'   # Net snmp standard mib directory
SNMP_IRONPORT_MIB_DIR = '/home/www/mibs/main'       # Ironport standard mib directory

# Feature Key update server
FEATURE_KEY_UPDATES_SERVER  = 'qa10.qa.sgg.cisco.com'
FEATURE_KEY_BASE_PATH       = '/home/upgrades/fkey/data'

THIRD_PARTY_TOOLS_UPDATE_SERVER = 'updater1.ibauto.devit.ciscolabs.com:443'
UPDATE_SERVER = 'updater1.ibauto.devit.ciscolabs.com'
UPDATE_SERVER_01  = 'updater1.ibauto.devit.ciscolabs.com'

NTLM_REALM_01   =       'NtlmRealm01'
NTLM_REALM_02   =       'NtlmRealm02'
NTLM_REALM_03   =       'NtlmRealm03'
NTLM_REALM_04   =       'NtlmRealm04'
NTLM_REALM_05   =       'NtlmRealm05'
NTLM_REALM_06   =       'NtlmRealm06'
NTLM_REALM_07   =       'NtlmRealm07'
NTLM_REALM_08   =       'NtlmRealm08'
NTLM_REALM_09   =       'NtlmRealm09'
NTLM_REALM_10   =       'NtlmRealm10'


NTLM_AUTH_SERVER_01 =   'ntlm-server01.ibauto'
NTLM_AUTH_SERVER_02 =   'ntlm-server02.ibauto'
NTLM_AUTH_SERVER_03 =   'ntlm-server03.ibauto'
NTLM_AUTH_SERVER_04 =   'ntlm-server04.ibauto'
NTLM_AUTH_SERVER_05 =   'ntlm-server05.ibauto'
NTLM_AUTH_SERVER_06 =   'ntlm-server06.ibauto'
NTLM_AUTH_SERVER_07 =   'ntlm-server07.ibauto'
NTLM_AUTH_SERVER_08 =   'ntlm-server08.ibauto'
NTLM_AUTH_SERVER_09 =   'ntlm-server09.ibauto'
NTLM_AUTH_SERVER_10 =   'ntlm-server10.ibauto'

AD_DOMAIN_01        =   'FOREST01.IBAUTO'
AD_DOMAIN_02        =   'FOREST02.IBAUTO'
AD_DOMAIN_03        =   'FOREST03.IBAUTO'
AD_DOMAIN_04        =   'FOREST04.IBAUTO'
AD_DOMAIN_05        =   'FOREST05.IBAUTO'
AD_DOMAIN_06        =   'FOREST06.IBAUTO'
AD_DOMAIN_07        =   'FOREST07.IBAUTO'
AD_DOMAIN_08        =   'FOREST08.IBAUTO'
AD_DOMAIN_09        =   'FOREST09.IBAUTO'
AD_DOMAIN_10        =   'FOREST10.IBAUTO'

NTLM_USER_01        =   'u01f01'
NTLM_USER_02        =   'u01f02'
NTLM_USER_03        =   'u01f03'
NTLM_USER_04        =   'u01f04'
NTLM_USER_05        =   'u01f05'
NTLM_USER_06        =   'u01f06'
NTLM_USER_07        =   'u01f07'
NTLM_USER_08        =   'u01f08'
NTLM_USER_09        =   'u01f09'
NTLM_USER_10        =   'u01f10'

NTLM_USER_PASS_01   =   'p01f01$'
NTLM_USER_PASS_02   =   'p01f02$'
NTLM_USER_PASS_03   =   'p01f03$'
NTLM_USER_PASS_04   =   'p01f04$'
NTLM_USER_PASS_05   =   'p01f05$'
NTLM_USER_PASS_06   =   'p01f06$'
NTLM_USER_PASS_07   =   'p01f07$'
NTLM_USER_PASS_08   =   'p01f08$'
NTLM_USER_PASS_09   =   'p01f09$'
NTLM_USER_PASS_10   =   'p01f10$'

NTLM_GROUP_01       =   'g01f01'
NTLM_GROUP_02       =   'g01f02'
NTLM_GROUP_03       =   'g01f03'
NTLM_GROUP_04       =   'g01f04'
NTLM_GROUP_05       =   'g01f05'
NTLM_GROUP_06       =   'g01f06'
NTLM_GROUP_07       =   'g01f07'
NTLM_GROUP_08       =   'g01f08'
NTLM_GROUP_09       =   'g01f09'
NTLM_GROUP_10       =   'g01f10'

AD_JOIN_USER_01     =   'administrator'
AD_JOIN_USER_PASS_01 =  'Cisco1234$'
AD_JOIN_USER_PASS_WRONG =  'ironport'

DNS_IP_01           =   '10.8.67.165'
DNS_IP_02           =   '10.8.67.166'
DNS_IP_03           =   '10.8.67.167'
DNS_IP_04           =   '10.8.67.168'
DNS_IP_05           =   '10.8.67.169'
DNS_IP_06           =   '10.8.67.170'
DNS_IP_07           =   '10.8.67.171'
DNS_IP_08           =   '10.8.67.172'
DNS_IP_09           =   '10.8.67.173'
DNS_IP_10           =   '10.8.67.174'

#EXTERNAL LDAP
# Until an open ldap server is setup, using AD server for LDAP.
EX_BASE_DN            =  'dc=ad01,dc=ibauto'
EX_USER_AUTH_QUERY    =  '(&(objectClass=person)(cn={u}))'
EX_USER_AUTH_ATTR     =  'cn'
EX_USER_AUTH_BASE_DN  =  EX_BASE_DN
EX_GROUP_QUERY        =  '(&(cn=externaluserGroup)(memberUid={u}))'
EX_GROUP_USER_ATTR    =  'memberUid'
EX_GROUP_NAME_ATTR    =  'cn'
EX_GROUP_DIRECTORY    =  'externaluserGroup'
EX_LDAP_USER          =  LDAP_USER
EX_LDAP_USER_PWD      =  LDAP_USER_PASSWORD

#FEEDS_SERVERS
FEED_SERVER        =     'ad1.ibauto'
NGINX_SERVER       =     'nginxserver.ibauto'
LIGHTTPD_SERVER    =     'lighttpdserver.ibauto'

#WCCP ROUTER IP. This IP Adrress belongs to IBAUTO Lab
WCCP_ROUTER_IP_M1          =    '10.8.63.101'
WCCP_ROUTER_IP_P1          =    '10.8.64.101'

#x509 OCSP Responder
X509_OCSP_RESPONDER        =  TOOLS
OCSP_SERVER                =  TOOLS

WBNP_SERVER = 'wbnp01.ibauto.devit.ciscolabs.com'