# $Id: //prod/main/sarf_centos/variables/environment/auto_lab.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""
==============================================================================
                        Auto lab Test Environment
==============================================================================
Robot variable file for .auto lab.
This file depents on two environment variables:
    WSA - should contain hostname of the WSA appliance under test
    SLICE_SERVER - should contain hostname of the FreeBSD server reserved for
    the slice (this variable is used in 'default' module)
"""

import socket, os
from environment.common import *

INET_MODE = 'ipv4'
IPV_PARAM = '-4'

DNS = '172.29.176.4'

REGION = 'America'
COUNTRY = 'United States'
TIME_ZONE = 'Los_Angeles'

SLICE_SERVER = os.environ.get("SLICE_SERVER") or "server001.auto"

IIS_SERVER = 'ad1.auto'
IIS_SERVER_UNIX_FORMAT = 'ad2.auto'

# HTTP Server
HTTP_SERVER = SLICE_SERVER

# Tools Server - that's a box to run such tools as icaptestd.py
# It should be different from DUT, Client, and HTTP_SERVER
TOOLS = 'tools.auto'

# Server for setting and unsetting transparent routing
TRANSPARENT_ROUTING_SERVER = 'management.auto' # does not work from tools.auto

# server with special test files (badware, files by types etc)
SERVICE_SERVER = TOOLS

# HTTPS server that had expired certificate
# locate under /usr/local/etc/apache22/ssl/expired.crt
EXPIRED_HTTPS = "tools.auto"

# HTTPS server that had certificate with no CN defined
# locate under /usr/local/etc/apache22/ssl/nocn.crt
NOCN_HTTPS = "tools.auto"

# HTTPS server that had certificate with NULL character in CN
# locate under /usr/local/etc/apache22/ssl/nullincn.crt
NULLINCN_HTTPS = "tools.auto"

# Upstream proxy
UPSTRM_PROX1 = "sarf-squid1.auto"

# SSW
SSW_MODE = 'M1' # M1 is an alias for Management Interface
                # P1 - another option for Data Interface

# Active Directory Server 1
AD1_SERVER = 'ad1.auto'
AD1_DOMAIN = 'AD1.AUTO'
AD1_NET_DOMAIN = 'AD1'
AD1_USER = 'user1'
AD1_USER_PW = 'pass1'
AD1_BASE_DN = 'cn=Users,dc=ad1,dc=auto'
AD1_BIND_BASE_DN = 'cn=user1,cn=Users,dc=ad1,dc=auto'
AD1_BIND_BASE_PW = 'pass1'
AD1_JOIN_USER = 'admin'
AD1_JOIN_PW = 'cisco123'
AD1_SECRET = 'ironport'

# Active Directory Server 2
AD2_SERVER = 'ad2.auto'
AD2_DOMAIN = 'AD2.AUTO'
AD2_NET_DOMAIN = 'AD2'
AD2_USER = 'user1'
AD2_USER_PW = 'pass1'
AD2_BASE_DN = 'cn=Users,dc=ad2,dc=auto'
AD2_BIND_BASE_DN = 'cn=user1,cn=Users,dc=ad2,dc=auto'
AD2_BIND_BASE_PW = 'pass1'
AD2_JOIN_USER = 'admin'
AD2_JOIN_PW = 'cisco123'

#Windows 2008 Active Directory server
WIN2K8_AD_SERVER = 'ad1.auto'
WIN2K8_AD_DOMAIN = 'AD1.AUTO'
WIN2K8_AD_JOIN_USER = 'admin'
WIN2K8_AD_JOIN_PW = 'cisco123'

# NTLM auth variables
NTLM_AUTH_SERVER = AD1_SERVER
AD_DOMAIN = AD1_DOMAIN
AD_NET_DOMAIN = AD1_NET_DOMAIN
AD_SERVER1 = AD1_SERVER

# LDAP auth variables
LDAP_AUTH_SERVER = 'ldap1.auto'
LDAP_AUTH_PORT = '389'
LDAP_BASE_DN = 'ou=Automation,dc=ldap1,dc=auto'
USER_NAME_ATTR = 'uid'
USER_FILTER_QUERY     =  'objectclass'
LDAP_ADMIN_DN = 'cn=administrator,ou=Automation,dc=ldap1,dc=auto'
LDAP_ADMIN_PASS = 'ironport'

LDAP_BIND_BASE_DN = LDAP_ADMIN_DN
LDAP_BIND_BASE_PW = LDAP_ADMIN_PASS

#RADIUS auth variables
RADIUS_SERVER = 'ntlm-server14.auto'
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
FTP_UPSTREAM_DUT_PROXY = 'wsa020.auto'

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

# ssh tunnel variables
SSH_TUNNEL_HOST = 'tunnels-int.cisco.com'

# Novell variables
NOVELL_SERVER        = 'vm10win0173.wga'
NOVELL_CLIENT        = 'vm10win0174.wga'
NOVELL_BASE_DN       = 'o=wga'
NOVELL_BIND_BASE_DN  = 'cn=admin,o=wga'
NOVELL_BIND_BASE_PW  = 'ironport'

# ASA variables
ASA_SERVER           = 'asa5520-01.wga'
ASA_PORT             = '11999'
ASA_PASSWORD         = 'ironport'


# Syslog server
SYSLOG_SERVER = TOOLS

# Feature Key update server
FEATURE_KEY_UPDATES_SERVER  = 'qa10.qa'
FEATURE_KEY_BASE_PATH       = '/home/upgrades/fkey/data'

THIRD_PARTY_TOOLS_UPDATE_SERVER = 'updater1.auto.sgg.cisco.com:443'
UPDATE_SERVER = 'updater1.auto.sgg.cisco.com'
UPDATE_SERVER_01 = 'updater1.auto.sgg.cisco.com'

#CRES Server settings
CRES_SERVER = 'esx16-cres3q01.qa.sbr.ironport.com'
CRES_ADMIN = 'rtestuser@ironport.com'
CRES_ADMIN_PASSWORD = 'ironport'
CRES_ADMIN_PASSWORD = 'ironport'
PXE_SERVER = 'vm10iea0058.qa.sbr.ironport.com'

# All VSphere servers. Override this constant in lab files in order to look for
# virtual machines located only in the particular lab
VSPHERES = (('10.92.144.58', 'vmdev', 'ironport'),
            ('10.92.144.58', 'sarf', 'rtestuser'),
            ('10.92.144.105', 'administrator', 'ironport'))
NTLM_AUTH_SERVER_01 = 'ntlm-server03.auto'
AD_DOMAIN_01 = 'FOREST03.AUTO'
DNS_IP_01 = '10.7.32.45'
TUI_AGENT = 'ntlm-server15.auto'
AD_JOIN_USER_PASS_01 = 'ironport123$'

#winbindd_watchdog_enhancements credentials
AD2 = 'ad1.auto'
IAF_AD2 = 'iaf-ad2.auto'
AD2_DOMAIN = 'AD1.AUTO'
AD2_PASS = 'cisco123'

WBNP_SERVER = 'wbnp01.auto.sgg.cisco.com'

#Added HTTP server for the HTTP put content issue faced
HTTP_SERVER_NEW = TOOLS

#Multiforest servers

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

NTLM_AUTH_SERVER_01 =   'ntlm-server07.auto'
NTLM_AUTH_SERVER_02 =   'ntlm-server10.auto'
NTLM_AUTH_SERVER_03 =   'ntlm-server03.auto'
NTLM_AUTH_SERVER_04 =   'ntlm-server04.auto'
NTLM_AUTH_SERVER_05 =   'ntlm-server05.auto'
NTLM_AUTH_SERVER_06 =   'ntlm-server06.auto'
NTLM_AUTH_SERVER_07 =   'ntlm-server02.auto'
NTLM_AUTH_SERVER_08 =   'ntlm-server08.auto'
NTLM_AUTH_SERVER_09 =  'ntlm-server09.auto'
NTLM_AUTH_SERVER_10 =   'ntlm-server01.auto'

AD_DOMAIN_01        =   'FOREST07.auto'
AD_DOMAIN_02        =   'FOREST10.auto'
AD_DOMAIN_03        =   'FOREST03.auto'
AD_DOMAIN_04        =   'FOREST04.auto'
AD_DOMAIN_05        =   'FOREST05.auto'
AD_DOMAIN_06        =   'FOREST06.auto'
AD_DOMAIN_07        =   'FOREST02.auto'
AD_DOMAIN_08        =   'FOREST08.auto'
AD_DOMAIN_09        =   'FOREST09.auto'
AD_DOMAIN_10        =   'FOREST01.auto'
AD_DOMAIN_08_CUTTED =   'FOREST008'

DNS_IP_01           =   '10.7.32.49'
DNS_IP_02           =   '10.7.32.52'
DNS_IP_03           =   '10.7.32.45'
DNS_IP_04           =   '10.7.32.46'
DNS_IP_05           =   '10.7.32.47'
DNS_IP_06           =   '10.7.32.48'
DNS_IP_07           =   '10.7.32.44'
DNS_IP_08           =   '10.7.32.50'
DNS_IP_09           =   '10.7.32.51'
DNS_IP_10           =   '10.7.32.43'

NTLM_USER_01        =   'u01f07'
NTLM_USER_02        =   'u01f010'
NTLM_USER_03        =   'u01f03'
NTLM_USER_04        =   'u01f04'
NTLM_USER_05        =   'u01f05'
NTLM_USER_06        =   'u01f06'
NTLM_USER_07        =   'u01f02'
NTLM_USER_08        =   'u01f08'
NTLM_USER_09        =   'u01f09'
NTLM_USER_10        =   'u01f01'

NTLM_USER_PASS_01   =   'p01f07$'
NTLM_USER_PASS_02   =   'p01f010$'
NTLM_USER_PASS_03   =   'p01f03$'
NTLM_USER_PASS_04   =   'p01f04$'
NTLM_USER_PASS_05   =   'p01f05$'
NTLM_USER_PASS_06   =   'p01f06$'
NTLM_USER_PASS_07   =   'p01f02$'
NTLM_USER_PASS_08   =   'p01f08$'
NTLM_USER_PASS_09   =   'p01f09$'
NTLM_USER_PASS_10   =   'p01f01$'

NTLM_GROUP_01       =   'g01f07'
NTLM_GROUP_02       =   'g01f010'
NTLM_GROUP_03       =   'g01f03'
NTLM_GROUP_04       =   'g01f04'
NTLM_GROUP_05       =   'g01f05'
NTLM_GROUP_06       =   'g01f06'
NTLM_GROUP_07       =   'g01f02'
NTLM_GROUP_08       =   'Domain Users'
NTLM_GROUP_09       =   'g01f09'
NTLM_GROUP_10       =   'g01f01'

AD_JOIN_USER_01     =   'administrator'
AD_JOIN_USER_PASS_01 =  'Cisco1234$'
AD_JOIN_USER_PASS_WRONG =  'ironport'

#ISE
ISE_SERVER_1     =   'vm10ise0001.auto'
ISE_RADIUS_SECRET    =   'Cisco123'

#EXTERNAL LDAP
EX_BASE_DN            =  'dc=ldap1,dc=auto'
EX_USER_AUTH_QUERY    =  '(&(objectClass=person)(objectClass=shadowAccount)(uid={u}))'
EX_USER_AUTH_ATTR     =  'cn'
EX_USER_AUTH_BASE_DN  =  EX_BASE_DN
EX_GROUP_QUERY        =  '(&(cn=admin_group)(memberUid={u}))'
EX_GROUP_USER_ATTR    =  'memberUid'
EX_GROUP_NAME_ATTR    =  'objectClass'
EX_GROUP_DIRECTORY    =  'posixGroup'
EX_LDAP_USER          =  'rtester'
EX_LDAP_USER_PWD      =  'raptortester'

#FEEDS_SERVERS
FEED_SERVER        =     'ad1.auto.sgg.cisco.com'
NGINX_SERVER       =     'nginxserver.auto.sgg.cisco.com'
LIGHTTPD_SERVER    =     'lighttpdserver.auto.sgg.cisco.com'

#x509 OCSP Responder
X509_OCSP_RESPONDER        =  TOOLS
OCSP_SERVER                =  TOOLS
