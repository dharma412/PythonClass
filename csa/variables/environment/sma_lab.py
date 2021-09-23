# $Id $
# $DateTime $
# $Author $
"""
==============================================================================
                        SMA lab Test Environment
==============================================================================
"""
from wga_lab import *
from environment.common import *

# LDAP auth variables
LDAP_AUTH_SERVER = 'esx-r209s01-bsd04.sma'
LDAP_SERVER_TYPE = 'openldap'
LDAP_AUTH_PORT = '389'
LDAP_BASE_DN = 'dc=bsd04,dc=sma'
LDAP_BINDDN = 'cn=admin,%s' % (LDAP_BASE_DN,)
LDAP_PASSWORD = 'ironport'

BIND_SERVER = 'esx-r209s01-bsd04.sma'

RADIUS_SERVER = 'esx-r209s01-bsd04.sma'
