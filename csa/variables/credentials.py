# $Id: //prod/main/sarf_centos/variables/credentials.py#1 $
"""Test environment users credentials variables.
"""

HTTP_USER = "testuser"
HTTP_PASSWORD = "ironport"
TESTUSER = 'testuser'
TESTUSER_PASSWORD = 'ironport'
AD_USER = 'iafuser' # It's used for LDAP and NTLM authentication
AD_USER_PASSWORD = 'ironport'
IAFUSER = 'iafuser' # It's used for LDAP and NTLM authentication
IAFUSER_PASSWORD = 'ironport'
IAFUSER2 = 'iafuser2' # It's used for LDAP and NTLM authentication
IAFUSER2_PASSWORD = 'ironport'
DUT_ADMIN = 'admin'
DUT_ADMIN_PASSWORD = 'ironport'
DUT_ADMIN_SSW_PASSWORD = 'Cisco12$'
DUT_ADMIN_TMP_PASSWORD = 'Cisco21$'
DUT_ENABLEDIAG = 'enablediag'
DUT_ENABLEDIAG_PASSWORD = 'ironport'
RTESTER = 'rtester'
RTESTER_PASSWORD = 'ironport'
RTESTUSER = 'rtestuser'
RTESTUSER_PASSWORD = 'ironport'
FTPUSER = 'ftpuser'
FTPUSER_PASSWORD = 'ironport'
LDAP_USER = 'rtester'
LDAP_USER_PASSWORD = 'raptortester'
NTLM_USER = 'rtester'
NTLM_USER_PASSWORD = 'ironport'
AD_JOIN_USER = 'admin'
AD_JOIN_USER_PASSWORD = 'cisco123'
NOVELL_CL_USER = 'admin'
NOVELL_CL_USER_PW = 'ironport'
EDIR_USER = 'user01'
EDIR_USER_PW = 'ironport'
SERVICE_USER = 'service'
SERIAL_USER = 'serialnumber'

#Users and groups in connection with Bugzilla bug 56061
BUG_USER='bug56061_user1'
BUG_GROUP='bug56061_grp1'
BUG_USER_PASSWORD='ironport'

#AVC credentials
SF_LOGIN = 'avc.ak.gtalk1@gmail.com'
SF_PASS = 'ironport123'
NTLM_USER = 'buguser'
NTLM_USER_1 = 'buguser1'
NTLM_USER_PW = 'ironport'

# User used in SMA/WSA automation
LDAP_SMA_USER = 'smatestuser'
LDAP_SMA_USER_PASS = 'password123'
LDAP_SMA_USER_GROUP = 'smatestusergroup'

# User used in x509 OCSP REsponder tests
X509_OCSP_RESPONDER_USER      =  TESTUSER
X509_OCSP_RESPONDER_PASSWORD  =  TESTUSER_PASSWORD

#APJC Server Securex API Credentials
APJC_USER = 'Krithika Selva'
APJC_CLIENT_ID = 'client-94325fbf-986f-4f0d-ae1d-c1696d1825f0'
APJC_CLIENT_SECRET = '-OxbU1BOJ1qLfsmavkp1eKrr4Z9ZPbdeDPHZoBFby7_2YgxOZWMxyA'

#EU Server Securex API Credentials
EU_USER = 'Krithika Selva'
EU_CLIENT_ID = 'client-f6af7ee4-3cea-4b31-9146-06e927eebca1'
EU_CLIENT_SECRET = 'x6D6jBmxsKd3GmO6hU2J0HGlddW0bIWsrZX0TIf92y2huZ14seBvXA'

#NAM Server Securex API Credentials
NAM_USER = 'Krithika Selva'
NAM_CLIENT_ID = 'client-8cd77da0-04b8-422d-8eb0-bfdefdda8dd8'
NAM_CLIENT_SECRET = '7iHCNNjO1-qxBmjI4uWpoap02gl-Es8SRkhwYYk3_VBx3z31QmVnPw'

#NO Permission API Credentials
NOPER_CLIENT_ID = 'client-6a4feccc-e590-4079-9a7e-508e687bc534'
NOPER_CLIENT_SECRET = 'yV3QgXksQ8uxboLpk3J5mit2nIShkgNptF6zdcIjh3NjBwb89UQzCw' 
