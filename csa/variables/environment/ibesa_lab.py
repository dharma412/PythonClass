# $Id: //prod/main/sarf_centos/variables/environment/ibesa_lab.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""
==============================================================================
                        IBESA lab Test Environment
==============================================================================
"""
import os
from environment.common import *

INET_MODE = 'ipv4'

DNS = '10.8.152.51'

FTP_SERVER = CLIENT_HOSTNAME

# LDAP auth variables
LDAP_AUTH_SERVER = 'pod0233-client18.ibesa'
LDAP_SERVER_TYPE = 'openldap'
LDAP_AUTH_PORT = '389'
LDAP_BASE_DN = 'dc=qa32,dc=qa'
BASE_DN = 'dc=qa32,dc=qa'
LDAP_BINDDN = 'cn=admin,%s' % (LDAP_BASE_DN,)
LDAP_PASSWORD = 'ironport'

BIND_SERVER = 'vm30bsd0149.ibqa'

RADIUS_SERVER = 'vm30bsd0149.ibqa'

CRES_SERVER = 'res.cisco.com'
CRES_ADMIN = 'rtestuser@ironport.com'
CRES_ADMIN_PASSWORD = 'ironport123'
PXE_SERVER = 'vm30iea0004.ibqa'

MAIL_DELIVERY_SERVER = 'vm30bsd0149.ibqa'
STAGE_SDS = 'v2.beta.sds.cisco.com'
PROD_SDS = 'v2.sds.cisco.com'
STAGE_UPDATER = 'stage-update-manifests.ironport.com'

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
HARPE_TOOL_HOST = '10.76.70.229'
HARPE_HOST_USERNAME = 'root'
HARPE_HOST_PASSWD = 'cisco123'

VSPHERES = (('10.76.68.200', 'vmdev', 'ironport'),)

# SAML Parameters
ADFS_IDP_HOSTNAME = 'vm30win0009.ibqa'
ADFS_IDP_USER_DOMAIN = 'postx.sgg.cisco.com'
ADFS_IDP_USERNAME = 'aminath@postx.sgg.cisco.com'
ADFS_IDP_PASSWORD = 'cisco@123'

WSA_IDP_HOSTNAME = 'vm30wsa0007.ibqa.sgg.cisco.com'
