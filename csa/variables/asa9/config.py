# $Id: //prod/main/sarf_centos/variables/asa9/config.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import sys
import os

#Log file location
LOG_FILE = '/tmp/t1.log'
REMOTE_LISTENER_PORT = '4444'

# ASA settings
ASA_TERM_SRVR_IP = '10.126.245.3'
ASA_TERM_SRVR_PORT = '2016'
ASA_IP = '192.168.10.50'
ASA_HOSTNAME = 'HCL-ASA-WEBVPN'
ASA_USERNAME = 'sslwebvpn'
ASA_PASSWORD = 'Cisco!123'
ASA_INTF_LIST = ['OUTSIDE','INSIDE','MGMT']

ASA_OUTSIDE_INTF = 'GigabitEthernet0/1'
ASA_OUTSIDE_IP = '192.168.10.50'
ASA_OUTSIDE_NAME = 'outside'
ASA_OUTSIDE_MASK = '255.255.255.0'
ASA_OUTSIDE_HOST_IP = '192.168.10.200'

ASA_INSIDE_INTF = 'GigabitEthernet0/0'
ASA_INSIDE_IP = '60.60.60.1'
ASA_INSIDE_MASK = '255.255.255.0'
ASA_INSIDE_NAME = 'inside'
ASA_INSIDE_HOST_IP = '60.60.60.30'

ASA_THIRD_INTF = 'GigabitEthernet0/2'
ASA_THIRD_IP = '10.12.24.95'
ASA_THIRD_NAME = 'third'

ASA_MGMT_INTF = 'Management0/0'
ASA_MGMT_IP = '10.126.245.95'
ASA_MGMT_MASK = '255.255.255.128'
ASA_MGMT_NAME = 'management'

# TFTP settings - use nino.cisco.com
TFTP_SERVER_IP = '10.194.201.233'
FTP_SERVER_IP = '10.194.201.233'
DEFAULT_GW = '10.194.225.1'

# Selenium settings
SELENIUM_SPEED = 0.1

# Sikuli setting
SIKULIX_JAR = '/Users/aitang/temp/SikuliX/sikulix.jar'

# Robot root path. See note for required file structure.
# Directory path to contain this config.py: ROBOT_ROOT/variables/asa9/config.py
# ROBOT_ROOT is two levels up from there.
config_holder_dir = os.path.dirname(os.path.abspath(__file__))
ROBOT_ROOT = os.path.join(config_holder_dir, os.path.pardir, os.path.pardir)

# Google Web Toolkit (GWT) settings
GWT_SHOW_CASE_URL = '10.126.245.123/Showcase/'
GWT_MAIL_URL = 'http://172.21.144.30/Mail/'
GWT_DYNAMIC_TABLE = 'http://172.21.144.30/DynaTable/'


# Port forward settings
PORT_FORWARD_LOCAL_PORT = '8083'
INTERNAL_HTTP_SERVER = '21.0.0.2'


# CIFS and FTP settings
FTP_TARGET = 'ftp://anonymous@172.21.144.30/'
FTP_SUB_FOLDER = 'automation'
CIFS_TARGET = 'cifs://cisco:changeme@172.21.144.114/testfolder/'

# OWA 2010
OWA_2010_URL = 'https://172.21.144.21/owa'
OWA_2010_USERNAME = 'ASAWebVPN3\user2d3'
OWA_2010_PASSWORD = 'Foldering_01'
OWA_2010_CONTACT = 'user2d3@asawebvpn3.local'
OWA_SENDER_USERNAME = 'test.chn'
OWA_SENDER_PASSWORD = 'Google123'
OWA_RECEIVE_USERNAME = 'test.blr'
OWA_RECEIVE_PASSWORD = 'Cisco123'
OWA_USERNAME='test chn'
GROUP = 'GROUP@chnwebvpn10.local'
OWA_ADMIN_USERTNAME='Administrator'
OWA_ADMIN_PASSWORD='sslwebvpn!123'
OWA_2010_CONTACT1 = 'testmail@chnwebvpn10.local'
OWA_2010_CONTACT2 = 'testreal@chnwebvpn10.local'
OWA_UNDELIVERABLE_CONTACT = 'none@chnwebvpn10.local'
BROWSER = 'firefox'
