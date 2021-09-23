# $Id: //prod/main/sarf_centos/variables/environment/cs3_lab.py#2 $
# $DateTime: 2019/06/12 01:54:47 $
# $Author: revlaksh $

"""
==============================================================================
 CS3 PCloud lab Test Environment
==============================================================================
Robot variable file for .cs3 lab.
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

REGION = 'America'
COUNTRY = 'United States'
TIME_ZONE = 'Los_Angeles'

SLICE_SERVER = os.environ.get("SLICE_SERVER")
COADVISOR_SERVER = 'coadvisor-server01.cs3'

IIS_SERVER = 'ad1.cs3'
IIS_SERVER_UNIX_FORMAT = 'ad2.cs3'

# Tools Server - that's a box to run such tools as icaptestd.py
# It should be different from DUT, Client, and HTTP_SERVER
TOOLS = 'tools.cs3'

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
UPSTRM_PROX1 = "squid-server01.cs3"

# SSW
SSW_MODE = 'M1'         # M1 is an alias for Management Interface
# P1 - another option for Data Interface

# Active Directory Server 1
AD1_SERVER = 'ad1.cs3'
AD1_DOMAIN = 'AD01.CS3'
AD1_NET_DOMAIN = 'AD01'
AD1_USER = 'user1'
AD1_USER_PW = 'pass1'
AD1_BASE_DN = 'cn=Users,dc=ad1,dc=cs3'
AD1_BIND_BASE_DN = 'cn=user1,cn=Users,dc=ad1,dc=cs3'
AD1_BIND_BASE_PW = 'pass1'
AD1_JOIN_USER = 'administrator'
AD1_JOIN_PW = 'Cisco1234$'
AD_JOIN_USER = 'administrator'
AD_JOIN_USER_PASSWORD = 'Cisco1234$'
AD1_SECRET = 'ironport'

# Active Directory Server 2
AD2_SERVER = 'ad2.cs3'
AD2_DOMAIN = 'AD02.CS3'
AD2_NET_DOMAIN = 'AD02'
AD2_USER = 'user1'
AD2_USER_PW = 'pass1'
AD2_BASE_DN = 'cn=Users,dc=ad2,dc=cs3'
AD2_BIND_BASE_DN = 'cn=user1,cn=Users,dc=ad2,dc=cs3'
AD2_BIND_BASE_PW = 'pass1'
AD2_JOIN_USER = 'administrator'
AD2_JOIN_PW = 'Cisco1234$'


# Active Directory Server 3
AD3_SERVER = 'ad3.cs3'
AD3_DOMAIN = 'AD03.CS3'
AD3_NET_DOMAIN = 'AD03'
AD3_USER = 'administrator'
AD3_USER_PW = 'Cisco1234$'
AD3_BASE_DN = 'cn=Users,dc=ad3,dc=cs3'
AD3_BIND_BASE_DN = 'cn=user1,cn=Users,dc=ad3,dc=cs3'
AD3_BIND_BASE_PW = 'pass1'
AD3_JOIN_USER = 'administrator'
AD3_JOIN_PW = 'Cisco1234$'

#Windows 2008 Active Directory server
WIN2K8_AD_SERVER = 'ad1.cs3'
WIN2K8_AD_DOMAIN = 'AD01.CS3'
WIN2K8_AD_JOIN_USER = 'administrator'
WIN2K8_AD_JOIN_PW = 'Cisco1234$'

# NTLM auth variables
NTLM_AUTH_SERVER = AD1_SERVER
AD_DOMAIN = AD1_DOMAIN
AD_NET_DOMAIN = AD1_NET_DOMAIN
AD_SERVER1 = AD1_SERVER

# LDAP auth variables
# Until an open ldap server is setup, using AD server for LDAP.
LDAP_AUTH_SERVER = 'ad1.cs3'
LDAP_AUTH_PORT = '389'
LDAP_BASE_DN = 'dc=AD01,dc=CS3'
USER_NAME_ATTR = 'uid'
USER_FILTER_QUERY = 'objectclass'
LDAP_ADMIN_DN = 'cn=administrator,cn=Users,dc=AD01,dc=CS3'
LDAP_ADMIN_PASS = 'Cisco1234$'
LDAP_USER = 'ldapuser'
LDAP_USER_PASSWORD = 'ironport'
LDAP_BIND_BASE_DN = LDAP_ADMIN_DN
LDAP_BIND_BASE_PW = LDAP_ADMIN_PASS


# Active Directory 2
LDAP_AUTH_SERVER_AD2 = 'ad2.cs3'
LDAP_AUTH_PORT_AD2 = '389'
LDAP_BASE_DN_AD2 = 'dc=AD02,dc=CS3'
USER_NAME_ATTR_AD2 = 'cn'
USER_FILTER_QUERY_AD2 = 'None'
LDAP_ADMIN_DN_AD2 = 'cn=administrator,cn=Users,dc=AD02,dc=CS3'
LDAP_ADMIN_PASS_AD2 = 'Cisco1234$'
LDAP_USER_AD2 = 'ldapuser'
LDAP_USER_PASSWORD_AD2 = 'ironport'
LDAP_BIND_BASE_DN_AD2 = LDAP_ADMIN_DN_AD2
LDAP_BIND_BASE_PW_AD2 = LDAP_ADMIN_PASS_AD2


# Active Directory 3
LDAP_AUTH_SERVER_AD3 = 'ad3.cs3'
LDAP_AUTH_PORT_AD3 = '389'
LDAP_BASE_DN_AD3 = 'dc=AD03,dc=CS3'
USER_NAME_ATTR_AD3 = 'cn'
USER_FILTER_QUERY_AD3 = 'None'
LDAP_ADMIN_DN_AD3 = 'cn=administrator,cn=Users,dc=AD03,dc=CS3'
LDAP_ADMIN_PASS_AD3 = 'Cisco1234$'
LDAP_USER_AD3 = 'ldapuser'
LDAP_USER_PASSWORD_AD3 = 'ironport'
LDAP_BIND_BASE_DN_AD3 = LDAP_ADMIN_DN_AD3
LDAP_BIND_BASE_PW_AD3 = LDAP_ADMIN_PASS_AD3

# RADIUS auth variables
RADIUS_SERVER = 'radius-server01.cs3'
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
DUT_HTTP_PROXY_PORT_LIST = '3128'
#DUT_HTTP_PROXY_PORT_LIST = '3128,9128,9130'
MULTIPROXY_SUPPORTED_DUT_MODEL_LIST = 'S600V'

DIR_WITH_FILES_FOR_UPLOAD = '/home/testuser/files_for_upload'

# cpt snmp variables
SNMP_ENABLED = 'yes'   # Specify whether to enable or disable snmp: 'yes' or 'no'
SNMP_IP_INTERFACE = 'Management'    # Specify an interface for SNMP requests: 'Management', 'P1', 'P2'
SNMP_V3PHRASE = 'ironport'    # Specify SNMPv3 passphrase which must be at least 8 chars
SNMP_PORT = '161'    # Specify port that SNMP daemon listens on
SNMP_V2ENABLED = 'yes'    # Specify whether to service SNMP v1/v2 requests: 'yes' or 'no'
SNMP_V2PHRASE = 'ironport'  # specify v1/v2 community string
SNMP_V2NETWORK = '10.92.147.0/24'    # Specify networks that v1/v2 requests are allowed
SNMP_TRAP_TARGET = '10.92.145.222'    # Specify trap target ip
SNMP_TRAP_PHRASE = 'ironport'  # Specify trap community string
SNMP_TRAP_CONFIG_PATH = '/usr/local/etc/snmp/snmptrapd.conf'    # Specify trap configuration file path
SNMP_CHANGE_TRAP_STATUS = 'no'    # Specify whether to change current settings for enterprise trap status: 'yes' or 'no'
SNMP_LOCATION = 'San Bruno, CA USA'   # Specify location string
SNMP_CONTACT = 'admin@system.com'    # Specify contact string
SNMP_MIBS = '+ASYNCOS-MAIL-MIB'   # Included MIB module
SNMP_VERSION = '3'   # SNMP version - 3 or 2c
SNMP_SECNAME_v1 = 'v1get'   # Security name - corresponds to -u option in snmpwalk ver. 1
SNMP_SECNAME_v2 = 'v2get'   # Security name - corresponds to -u option in snmpwalk ver. 2
SNMP_SECNAME = 'v3get'   # Security name - corresponds to -u option in snmpwalk ver. 3
SNMP_AUTH_PROTOCOL = 'MD5'    # Snmp authentication protocol - SHA | MD5
SNMP_V3_SECLEVEL = 'authNoPriv'    # SNMP version 3 security level - coresponds to -l option
SNMP_NET_MIB_DIR = '/usr/local/share/snmp/mibs'   # Net snmp standard mib directory
SNMP_IRONPORT_MIB_DIR = '/home/www/mibs/main'   # Ironport standard mib directory

# Feature Key update server
FEATURE_KEY_UPDATES_SERVER = 'qa10.qa.sgg.cisco.com'
FEATURE_KEY_BASE_PATH = '/home/upgrades/fkey/data'

THIRD_PARTY_TOOLS_UPDATE_SERVER = 'updater01.cs3.devit.ciscolabs.com:443'
UPDATE_SERVER = 'updater01.cs3.devit.ciscolabs.com'
UPDATE_SERVER_01 = 'updater01.cs3.devit.ciscolabs.com'

UPDATE_SERVER_NEW = 'stage-stg-updates.ironport.com'
OPS_UPDATE_SERVER_FOR_VIRTUAL  = 'ops-updates-cc-vip.vega.ironport.com'
# Updgrade server
UPDATE_SERVER_UPGRADE  = 'updater03.wga.sgg.cisco.com'


NTLM_REALM_01 = 'NtlmRealm01'
NTLM_REALM_02 = 'NtlmRealm02'
NTLM_REALM_03 = 'NtlmRealm03'
NTLM_REALM_04 = 'NtlmRealm04'
NTLM_REALM_05 = 'NtlmRealm05'
NTLM_REALM_06 = 'NtlmRealm06'
NTLM_REALM_07 = 'NtlmRealm07'
NTLM_REALM_08 = 'NtlmRealm08'
NTLM_REALM_09 = 'NtlmRealm09'
NTLM_REALM_10 = 'NtlmRealm10'


NTLM_AUTH_SERVER_01 = 'ntlm-server01.cs3'
NTLM_AUTH_SERVER_02 = 'ntlm-server02.cs3'
NTLM_AUTH_SERVER_03 = 'ntlm-server03.cs3'
NTLM_AUTH_SERVER_04 = 'ntlm-server04.cs3'
NTLM_AUTH_SERVER_05 = 'ntlm-server05.cs3'
NTLM_AUTH_SERVER_06 = 'ntlm-server06.cs3'
NTLM_AUTH_SERVER_07 = 'ntlm-server07.cs3'
NTLM_AUTH_SERVER_08 = 'ntlm-server08.cs3'
NTLM_AUTH_SERVER_09 = 'ntlm-server09.cs3'
NTLM_AUTH_SERVER_10 = 'ntlm-server10.cs3'

AD_DOMAIN_01 = 'FOREST01.cs3'
AD_DOMAIN_02 = 'FOREST02.cs3'
AD_DOMAIN_03 = 'FOREST03.cs3'
AD_DOMAIN_04 = 'FOREST04.cs3'
AD_DOMAIN_05 = 'FOREST05.cs3'
AD_DOMAIN_06 = 'FOREST06.cs3'
AD_DOMAIN_07 = 'FOREST07.cs3'
AD_DOMAIN_08 = 'FOREST08.cs3'
AD_DOMAIN_09 = 'FOREST09.cs3'
AD_DOMAIN_10 = 'FOREST10.cs3'

NTLM_USER_01 = 'u01f01'
NTLM_USER_02 = 'u01f02'
NTLM_USER_03 = 'u01f03'
NTLM_USER_04 = 'u01f04'
NTLM_USER_05 = 'u01f05'
NTLM_USER_06 = 'u01f06'
NTLM_USER_07 = 'u01f07'
NTLM_USER_08 = 'u01f08'
NTLM_USER_09 = 'u01f09'
NTLM_USER_10 = 'u01f10'

NTLM_USER_PASS_01 = 'p01f01$'
NTLM_USER_PASS_02 = 'p01f02$'
NTLM_USER_PASS_03 = 'p01f03$'
NTLM_USER_PASS_04 = 'p01f04$'
NTLM_USER_PASS_05 = 'p01f05$'
NTLM_USER_PASS_06 = 'p01f06$'
NTLM_USER_PASS_07 = 'p01f07$'
NTLM_USER_PASS_08 = 'p01f08$'
NTLM_USER_PASS_09 = 'p01f09$'
NTLM_USER_PASS_10 = 'p01f10$'

NTLM_GROUP_01 = 'g01f01'
NTLM_GROUP_02 = 'g01f02'
NTLM_GROUP_03 = 'g01f03'
NTLM_GROUP_04 = 'g01f04'
NTLM_GROUP_05 = 'g01f05'
NTLM_GROUP_06 = 'g01f06'
NTLM_GROUP_07 = 'g01f07'
NTLM_GROUP_08 = 'g01f08'
NTLM_GROUP_09 = 'g01f09'
NTLM_GROUP_10 = 'g01f10'

AD_JOIN_USER_01 = 'administrator'
AD_JOIN_USER_PASS_01 = 'Cisco1234$'
AD_JOIN_USER_PASS_WRONG = 'ironport'

DNS_IP_01 = '10.10.201.12'
DNS_IP_02 = '10.10.201.13'
DNS_IP_03 = '10.10.201.14'
DNS_IP_04 = '10.10.201.15'
DNS_IP_05 = '10.10.201.16'
DNS_IP_06 = '10.10.201.17'
DNS_IP_07 = '10.10.201.18'
DNS_IP_08 = '10.10.201.19'
DNS_IP_09 = '10.10.201.20'
DNS_IP_10 = '10.10.201.21'

#EXTERNAL LDAP
#Until an open ldap server is setup, using AD server for LDAP.
EX_LDAP_SERVER = 'ldap-server01.cs3'
EX_BASE_DN = 'dc=AD01,dc=CS3'
EX_USER_AUTH_QUERY = '(&(objectClass=person)(cn={u}))'
EX_USER_AUTH_ATTR = 'cn'
EX_USER_AUTH_BASE_DN = EX_BASE_DN
EX_GROUP_QUERY = '(&(cn=externaluserGroup)(memberUid={u}))'
EX_GROUP_USER_ATTR = 'memberUid'
EX_GROUP_NAME_ATTR = 'cn'
EX_GROUP_DIRECTORY = 'externaluserGroup'
EX_LDAP_USER = LDAP_USER
EX_LDAP_USER_PWD = LDAP_USER_PASSWORD

#Until an open ldap server is setup, using AD2 server for LDAP.
EX_LDAP_SERVER_AD2 = 'ldap-server02.s3'
EX_BASE_DN_AD2 = 'dc=AD02,dc=CS3'
EX_USER_AUTH_QUERY_AD2 = '(&(objectClass=person)(cn={u}))'
EX_USER_AUTH_ATTR_AD2 = 'cn'
EX_USER_AUTH_BASE_DN_AD2 = EX_BASE_DN
EX_GROUP_QUERY_AD2 = '(&(cn=externaluserGroup)(memberUid={u}))'
EX_GROUP_USER_ATTR_AD2 = 'memberUid'
EX_GROUP_NAME_ATTR_AD2 = 'cn'
EX_GROUP_DIRECTORY_AD2 = 'externaluserGroup'
EX_LDAP_USER_AD2 = LDAP_USER
EX_LDAP_USER_PWD_AD2 = LDAP_USER_PASSWORD


#Until an open ldap server is setup, using AD3 server for LDAP.
EX_LDAP_SERVER_AD3 = 'ldap-server03.cs3'
EX_BASE_DN_AD3 = 'dc=AD03,dc=CS3'
EX_USER_AUTH_QUERY_AD3 = '(&(objectClass=person)(cn={u}))'
EX_USER_AUTH_ATTR_AD3 = 'cn'
EX_USER_AUTH_BASE_DN_AD3 = EX_BASE_DN
EX_GROUP_QUERY_AD3 = '(&(cn=externaluserGroup)(memberUid={u}))'
EX_GROUP_USER_ATTR_AD3 = 'memberUid'
EX_GROUP_NAME_ATTR_AD3 = 'cn'
EX_GROUP_DIRECTORY_AD3 = 'externaluserGroup'
EX_LDAP_USER_AD3 = LDAP_USER
EX_LDAP_USER_PWD_AD3 = LDAP_USER_PASSWORD

# FEEDS_SERVERS
FEED_SERVER = 'ad1.cs3'
NGINX_SERVER = 'nginx-server01.cs3'
LIGHTTPD_SERVER = 'lighttpd-server01.cs3'

# WCCP ROUTER IP. This IP Adrress belongs to cs3 Lab
WCCP_ROUTER_IP_M1 = 'SET:WCCP_ROUTER_IP_M1'
WCCP_ROUTER_IP_P1 = 'SET:WCCP_ROUTER_IP_P1'

# x509 OCSP Responder
X509_OCSP_RESPONDER = TOOLS
OCSP_SERVER = TOOLS

WBNP_SERVER = 'wbnp-server01.cs3.devit.ciscolabs.com'

#Jenkins info
JENKINS_SERVER = 'jenkins.cs3'
JENKINS_PORT = '8080'
JENKINS_USER = 'testuser'
JENKINS_USER_PWD = 'Ironport456$'


# SNMP server details for snmp ipv6 test cases
SNMP_SERVER_HOST = 'snmp-server01.cs3'
SNMP_SERVER_IPV4 = '10.10.201.24'
SNMP_SERVER_IPV6 = '2001:420:5440:2005:f10:0:a:18'
SNMP_SERVER_USER = 'cisco'
SNMP_SERVER_PWD = 'cisco'

#Kerberos HA Vrrp variables
VRRP_HA_IP       =  '10.10.192.220'
KERBEROS_HA_USER       =  'administrator'
KERBEROS_HA_PWD       =  'Cisco1234$'

# Samba HA Vrrp Variables
VRRP_HA_IP_SAMBA       =  '10.10.192.200'

#Client with tshark
CLIENT_HOSTNAME_tshark   =  'wsa088-client01.cs3'

# AnyconnectVPN variables
ANYCONNECT_CLIENT_IP = '10.10.201.38'
ANYCONNECT_LOGIN_USER = 'cisco'
ANYCONNECT_LOGIN_PWD = 'cisco'
ASA_PORT = '11999'
HTTP_SERVER_SUCCESS_MSG = 'It works'
ANYCONNECT_IP_POOL = '12.119.10.10-30'
ASA_IN_IP = '192.168.0.2'
ASA_OUT_IP= '192.168.1.1'
CLIENT_ROUTE_IP = '12.119.0.0'
SUBNET_MASK_16 = '16'
SUBNET_MASK_24 = '24'
HTTP_SERVER_SUBNET = '192.168.2.0'
HTTP_SERVER_IP = '192.168.2.2'
ANYCONNECT_P1_IP = '192.168.1.2'
ANYCONNECT_P2_IP = '192.168.2.1'

# CDA Variables
CDA_IP                     =  '10.10.201.42'
CDA_URL                    =  'https://10.10.201.42/cda/index.html'
CDA_USER                   =  'admin'
CDA_PASSWORD               =  'Ironp0rt'
KERBROSE_CLIENT_IP         =  '10.10.201.39'
ADMIN_USER                 =  'Administrator'
KERBROSE_CLIENT_PASSWORD   =  'cisco'
KERBROSE_CLIENT_USER       =  'cisco'

# CS3 lab VCenter is u32c01p15-vc.cisco.com
VSPHERES = (('u32c01p15-vc.cisco.com', 'CISCO\\cs.automation.gen', 'Cisco234@'),)

#proxy url
CISCO_STAGE_URL = 'http://stage.secure-web.sco.cisco.com'
