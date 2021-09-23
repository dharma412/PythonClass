# $Id: //prod/main/sarf_centos/variables/network.py#8 $
# $DateTime: 2019/09/30 12:04:06 $
# $Author: saurgup5 $

import socket

aws = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '10.10.1.5',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.255.0',
    'CIDR'            : '24',
    'DATA_CIDR'       : '24',
    'PREFIX'          : '64',
    'DATA_PREFIX'     : '64',
    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'esa-automation-triage-team@cisco.com',
    'DELIVER_REPORTS' : 'esa-automation-triage-team@cisco.com',
}

ibwsa = {
    'GUI_USER'  : 'admin',
    'GUI_PW'    : 'ironport',
    'DNS'       : '',
    'REGION'    : '',
    'COUNTRY'   : '',
    'TIME_ZONE'  : '',
}

wga = {
# this info went to $SARF_HOME/variables/environment/ files
}

ibqa = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '10.104.229.4',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.224.0',
    'CIDR'            : '24',
    'DATA_CIDR'       : '19',
    'PREFIX'          : '64',
    'DATA_PREFIX'     : '64',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.ibqa',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.ibqa',
}

ibesa = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '10.8.152.51',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.255.0',
    'CIDR'            : '24',
    'DATA_CIDR'       : '24',
    'PREFIX'          : '76',
    'DATA_PREFIX'     : '76',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.ibesa',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.ibesa',
}

cs1 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '192.168.0.252',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.255.224',
    'CIDR'            : '24',
    'DATA_CIDR'       : '27',
    'PREFIX'          : '112',
    'DATA_PREFIX'     : '112',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.cs1',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.cs1',
}

cs2 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '192.168.0.252',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.224.0',
    'CIDR'            : '24',
    'DATA_CIDR'       : '19',
    'PREFIX'          : '112',
    'DATA_PREFIX'     : '112',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.cs2',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.cs2',
}

cs3 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '192.168.0.252',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.255.224',
    'CIDR'            : '24',
    'DATA_CIDR'       : '27',
    'PREFIX'          : '112',
    'DATA_PREFIX'     : '112',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.cs3',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.cs3',
}

cs14 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '192.168.0.252',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.224.0',
    'DATA1_GW'        : '10.11.0.1',
    'DATA2_GW'        : '10.12.0.1',
    'CLIENT_GW'       : '10.10.4.1',
    'CIDR'            : '24',
    'DATA_CIDR'       : '19',
    'PREFIX'          : '112',
    'DATA_PREFIX'     : '112',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Los_Angeles',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.cs14',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.cs14',
}

cs19 = {
    'GUI_USER': 'admin',
    'GUI_PW': 'ironport',
    'DNS': '192.168.0.252',
    'NETMASK': '255.255.255.0',
    'DATA_NETMASK': '255.255.224.0',
    'CIDR': '24',
    'DATA_CIDR': '19',
    'PREFIX': '112',
    'DATA_PREFIX': '112',

    'REGION': 'America',
    'COUNTRY': 'United States',
    'TIME_ZONE': 'Pacific (Los_Angeles)',
    'ADMIN_PW': 'ironport',
    'NTP': 'time.ironport.com',
    'EMAIL_ALERTS': 'esa-automation-triage-team@cisco.com',
    'DELIVER_REPORTS': 'esa-automation-triage-team@cisco.com',
}

cs20 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '192.168.0.252',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.255.224',
    'CIDR'            : '24',
    'DATA_CIDR'       : '27',
    'PREFIX'          : '112',
    'DATA_PREFIX'     : '112',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.cs20',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.cs20',
}

cs21 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '192.168.0.252',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.224.0',
    'DATA1_GW'        : '10.3.0.1',
    'DATA2_GW'        : '10.4.0.1',
    'CLIENT_GW'       : '10.10.4.1',
    'CIDR'            : '24',
    'DATA_CIDR'       : '19',
    'PREFIX'          : '112',
    'DATA_PREFIX'     : '112',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.cs21',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.cs21',
}

cs27 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '192.168.0.252',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.224.0',
    'DATA1_GW'        : '10.11.0.1',
    'DATA2_GW'        : '10.12.0.1',
    'CLIENT_GW'       : '10.10.4.1',
    'CIDR'            : '24',
    'DATA_CIDR'       : '19',
    'PREFIX'          : '112',
    'DATA_PREFIX'     : '112',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Los_Angeles',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.cs27',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.cs27',
}

cs33 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '192.168.0.252',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.224.0',
    'DATA1_GW'        : '10.11.0.1',
    'DATA2_GW'        : '10.12.0.1',
    'CLIENT_GW'       : '10.10.4.1',
    'CIDR'            : '24',
    'DATA_CIDR'       : '19',
    'PREFIX'          : '112',
    'DATA_PREFIX'     : '112',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Los_Angeles',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@dummy.mail.cs33',
    'DELIVER_REPORTS' : 'testuser@dummy.mail.cs33',
}


qa = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '10.92.144.4',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.224.0',
    'CIDR'            : '24',
    'DATA_CIDR'       : '19',
    'PREFIX'          : '64',
    'DATA_PREFIX'     : '64',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific Time (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@mail.qa',
    'DELIVER_REPORTS' : 'testuser@mail.qa',
}

sma = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '10.92.151.132',
    'NETMASK'         : '255.255.254.0',
    'DATA_NETMASK'    : '255.255.248.0',
    'CIDR'            : '24',
    'DATA_CIDR'       : '19',
    'PREFIX'          : '64',
    'DATA_PREFIX'     : '64',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific Time (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@cisco.com',
    'DELIVER_REPORTS' : 'testuser@cisco.com',
}

perf1 = {
    'GUI_USER'        : 'admin',
    'GUI_PW'          : 'ironport',
    'DNS'             : '10.92.151.132',
    'NETMASK'         : '255.255.255.0',
    'DATA_NETMASK'    : '255.255.192.0',
    'CIDR'            : '24',
    'DATA_CIDR'       : '16',
    'PREFIX'          : '64',
    'DATA_PREFIX'     : '64',

    'REGION'          : 'America',
    'COUNTRY'         : 'United States',
    'TIME_ZONE'       : 'Pacific Time (Los_Angeles)',
    'ADMIN_PW'        : 'ironport',
    'NTP'             : 'time.ironport.com',
    'EMAIL_ALERTS'    : 'testuser@cisco.com',
    'DELIVER_REPORTS' : 'testuser@cisco.com',
}
perf3 = perf2 = perf1

def get_variables():
    this_client = socket.gethostname()
    network = this_client.split('.')[-1]
    if network == 'aws':
        return aws
    elif network == 'ibwsa':
        return ibwsa
    elif network == 'wga':
        return wga
    elif network in ('ibqa', 'ibeng'):
        return ibqa
    elif network == 'ibesa':
        return ibesa
    elif network == 'cs1':
        return cs1
    elif network == 'cs2':
        return cs2
    elif network == 'cs3':
        return cs3
    elif network == 'cs14':
        return cs14
    elif network == 'cs19':
        return cs19
    elif network == 'cs20':
        return cs20
    elif network == 'cs21':
        return cs21
    elif network == 'cs27':
        return cs27
    elif network == 'cs33':
        return cs33
    elif network in ('qa', 'eng'):
        return qa
    elif network == 'sma':
        return sma
    elif network.startswith('perf'):
        return perf1
    else:
        return wga
