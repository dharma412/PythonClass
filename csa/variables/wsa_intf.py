# $Id: //prod/main/sarf_centos/variables/wsa_intf.py#3 $
# $DateTime: 2019/06/03 22:56:07 $
# $Author: revlaksh $

import re
import socket
from robot.libraries.BuiltIn import BuiltIn
from network import cs14 as cs14_network
from network import cs21 as cs21_network
from network import cs27 as cs27_network

NETWORKS_MAPPING = {'cs14': cs14_network,'cs21': cs21_network,'cs27': cs27_network}

def get_dut_names(hostname):
    # list of variables that contain hostname of dut
    dut_names = []
    # get robot variables
    robot_vars = BuiltIn().get_variables()

    for key in robot_vars.keys():
        if robot_vars[key] == hostname:
            # skip ${ and } symbols
            dut_names.append(key[2:-1])

    return dut_names

def get_variables(wsa_hostname):
    interface_infos = {}
    # Generate network infos for this client
    this_client = socket.gethostname()
    #this_client_ip = socket.gethostbyname(this_client)

    this_client_ipv4 = socket.getaddrinfo(this_client,
        None, socket.AF_INET)[-1][4][0]
    interface_infos['CLIENT_HOSTNAME'] = this_client
    interface_infos['CLIENT_IP'] = this_client_ipv4
    interface_infos['CLIENT_SUBNET'] = re.sub('.[0-9]*$', '.0/24',
                                                  this_client_ipv4)
    network = wsa_hostname.split('.')[-1]
    if network in ('cs3', 'cs1', 'cs20'):
        last_octet = this_client_ipv4.split('.')[-1]
        last_octet = ((int(last_octet) /32) * 32) + 1
        interface_infos['CLIENT_SUBNET'] = this_client_ipv4.rsplit('.', 1)[0] + '.' + str(last_octet) + "/27"


    if socket.has_ipv6:
        try:
            addr_tuples = socket.getaddrinfo( \
                this_client,None,socket.AF_INET6,0,socket.SOL_TCP)
            this_client_ipv6 = addr_tuples[-1][4][0]
            interface_infos['CLIENT_IPV6'] = this_client_ipv6
            interface_infos['CLIENT_IPV6_SUBNET'] = re.sub(':[0-9A-Fa-f]*$', ':/64',
                                                  this_client_ipv6)
            if network in ('cs1', 'cs3', 'cs14', 'cs20', 'cs21', 'cs27'):
                interface_infos['CLIENT_IPV6_SUBNET'] = re.sub(
                        ':[0-9A-Fa-f]*$',
                        ':/112',
                        this_client_ipv6
                    )
        except socket.gaierror as e:
            print 'WARNING: IPv6 is enabled, but %s not found (%s).' \
                 ' Some tests may fail.' % (this_client, e)

    dut_info = {}
    dut_info.update(generate_ipv4_mgmt_info(wsa_hostname))
    dut_info.update(generate_ipv4_p1_info(wsa_hostname))
    dut_info.update(generate_ipv4_p2_info(wsa_hostname))
    dut_info.update(generate_inst_info(wsa_hostname))
    dut_info.update(generate_ipv6_mgmt_info(wsa_hostname))
    dut_info.update(generate_ipv6_p1_info(wsa_hostname))
    dut_info.update(generate_ipv6_p2_info(wsa_hostname))

    # get ipv4-ipv6 related parameters based on INET_MODEL
    variables = BuiltIn().get_variables()
    if variables["${INET_MODE}"].lower() == 'ipv6':
        interface_infos['IPV_PARAM'] = '-6'
        if dut_info['M1_IPv6_ADDR'] is None:
            print 'WARNING: INET_MODE is set to IPv6,' \
                ' but M1 IPv6 information was not generated.'
        if dut_info['P1_IPv6_ADDR'] is None:
            print 'WARNING: INET_MODE is set to IPv6,' \
                ' but P1 IPv6 information was not generated.'
    else:
        interface_infos['IPV_PARAM'] = '-4'


    for dut_name in get_dut_names(wsa_hostname):
        for key in dut_info.keys():
            int_info_key = dut_name + '_' + key
            interface_infos[int_info_key] = dut_info[key]
            #print('${%s}="%s"' % (int_info_key, dut_info[key]))

        # some additional assigment
        if str(dut_name) == 'DUT':
            interface_infos['CLIENT_GW'] = dut_info['CLIENT_GW']

    return interface_infos

def generate_ipv4_mgmt_info(wsa_hostname):
    info = {}
    # Generate network infos for Mgmt port of specified WSA
    mgmt_ip = socket.gethostbyname(wsa_hostname)
    mgmt_ip_octets = mgmt_ip.split('.')
    mgmt_gw_octets = mgmt_ip_octets[:-1] + ['1']

    info['M1_IP'] = mgmt_ip
    info['M1_NETMASK'] = '255.255.255.0'
    info['M1_GW'] = '.'.join(mgmt_gw_octets)

    network = wsa_hostname.split('.')[-1]

    if network in ('cs14', 'cs27'):
        info['M1_NETMASK'] = NETWORKS_MAPPING[network]['NETMASK']


    return info

def generate_inst_info(wsa_hostname):
    info = {}
    network = wsa_hostname.split('.')[-1]

    INST_SUFFIX = 'inst'

    inst_hostname = '%s-%s.%s' % (wsa_hostname.split('.')[0],
        INST_SUFFIX , network)
    info['INST'] = inst_hostname

    return info

def generate_ipv4_p1_info(wsa_hostname):
    info = {}
    network = wsa_hostname.split('.')[-1]

    # Generate network infos for P1 of specified WSA
    IBQA_P1_PREFIX = 'd1.'

    P1_SUFFIX = 'p1'

    if network == 'ibqa':
        p1_hostname = IBQA_P1_PREFIX + wsa_hostname
    else:
        p1_hostname = '%s-%s.%s' % (wsa_hostname.split('.')[0],
            P1_SUFFIX , network)

    info['P1'] = p1_hostname


    try:
        p1_ip = socket.gethostbyname(p1_hostname)
        info['P1_IP'] = p1_ip

        # Generate gateway IP for this client and P1 based on inside.wga
        p1_gw_ip_octets = p1_ip.split('.')

        if network in ('ibqa','ibauto'):
            p1_gw_ip_octets = p1_gw_ip_octets[:-1] + ['1']
            info['P1_NETMASK'] = '255.255.255.0'
            info['P1_NETPREFIX'] = '/24'
        elif network in ('cs1', 'cs2', 'cs3', 'cs20'):
            p1_gw_ip_octets[3] = str(int(p1_gw_ip_octets[3]) - 1)
            #p1_gw_ip_octets = p1_gw_ip_octets[:-1] + [str(int(p1_gw_ip_octets[-1]) - 1)]
            info['P1_NETMASK'] = '255.255.255.224'
            info['P1_NETPREFIX'] = '/27'
        elif network in ('cs14', 'cs27', 'cs21'):
            info['P1_NETMASK'] = NETWORKS_MAPPING[network]['DATA_NETMASK']
            info['P1_NETPREFIX'] = '/%s' % NETWORKS_MAPPING[network]['DATA_CIDR']
        else:
            p1_gw_ip_octets[3] = str(int(p1_gw_ip_octets[3]) - 3)
            info['P1_NETMASK'] = '255.255.255.240'
            info['P1_NETPREFIX'] = '/28'

        client_gw_ip_octets = p1_gw_ip_octets[:]
        info['P1_GW'] = '.'.join(p1_gw_ip_octets)
        info['CLIENT_GW'] = '.'.join(client_gw_ip_octets)

        if network in ('cs14', 'cs21', 'cs27'):
            info['P1_GW'] = NETWORKS_MAPPING[network]['DATA1_GW']
            info['CLIENT_GW'] = NETWORKS_MAPPING[network]['DATA1_GW']

    except socket.gaierror as e:
        print 'WARNING: Cannot determine P1 interface information' \
             ' Error while resolving %s (%s)' % (p1_hostname,e)


    return info

def generate_ipv4_p2_info(wsa_hostname):
    info = {}
    network = wsa_hostname.split('.')[-1]

    IBQA_P2_PREFIX = 'd2.'
    P2_SUFFIX = 'p2'

    if network == 'ibqa':
        p1_hostname = IBQA_P1_PREFIX + wsa_hostname
    else:
        p2_hostname = '%s-%s.%s' % (wsa_hostname.split('.')[0],
            P2_SUFFIX , network)

    # Generate network infos for P2 of specified WSA
    try:
        p2_ip = socket.gethostbyname(p2_hostname)
        p2_gw_ip_octets = p2_ip.split('.')
        if network in ('ibqa','ibauto'):
            p2_gw_ip_octets = p2_gw_ip_octets[:-1] + ['1']
            info['P2_NETMASK'] = '255.255.255.0'
            info['P2_NETPREFIX'] = '/24'
        elif network in ('cs1', 'cs2', 'cs3', 'cs20'):
            p2_gw_ip_octets[3] = str(int(p2_gw_ip_octets[3]) - 1)
            info['P2_NETMASK'] = '255.255.255.224'
            info['P2_NETPREFIX'] = '/27'
        elif network in ('cs14', 'cs27', 'cs21'):
            info['P2_NETMASK'] = NETWORKS_MAPPING[network]['DATA_NETMASK']
            info['P2_NETPREFIX'] = '/%s' % NETWORKS_MAPPING[network]['DATA_CIDR']
        else:
            p2_gw_ip_octets[3] = str(int(p2_gw_ip_octets[3]) - 3)
            info['P2_NETMASK'] = '255.255.255.240'
            info['P2_NETPREFIX'] = '/28'
        info['P2_GW'] = '.'.join(p2_gw_ip_octets)
        info['P2'] = p2_hostname
        info['P2_IP'] = p2_ip

        if network in ('cs14', 'cs21', 'cs27'):
            info['P2_GW'] = NETWORKS_MAPPING[network]['DATA2_GW']
            info['P2'] = p2_hostname
            info['P2_IP'] = p2_ip

    except socket.gaierror:
        # in case p2 is not set for current wsa, variables will be
        # initialized with None value
        info['P2_NETMASK'] = None
        info['P2_GW'] = None
        info['P2'] = None
        info['P2_IP'] = None

    return info

def generate_ipv6_mgmt_info(wsa_hostname):
    DEFAULT_IPV6_MANAGEMENT_PREFIX = '64'

    info = {}
    network = wsa_hostname.split('.')[-1]
    if network == 'ibauto':
        DEFAULT_IPV6_MANAGEMENT_PREFIX = '76'
    elif network in ('cs1', 'cs3', 'cs20','cs21'):
        DEFAULT_IPV6_MANAGEMENT_PREFIX = '112'
    elif network in ('cs14', 'cs27'):
        DEFAULT_IPV6_MANAGEMENT_PREFIX = NETWORKS_MAPPING[network]['PREFIX']


    try:
        # generate ipv6-related parameters based on ipv6 address of dut
        mgmt_ipv6 = socket.getaddrinfo(wsa_hostname,
            None, socket.AF_INET6)[0][4][0]  #2620:101:2004:4207::123

        array = mgmt_ipv6.split(':')
        array[-1] = '1'
        mgmt_ipv6_gw = ':'.join(array)

        info['M1_IPv6_ADDR'] = mgmt_ipv6
        info['M1_IPv6_PREFIX'] = DEFAULT_IPV6_MANAGEMENT_PREFIX
        info['M1_IPv6_GW'] = mgmt_ipv6_gw

        # backward compatibility - uncomment if needed
        #info['M1_IPv6'] = mgmt_ipv6 + '/' + DEFAULT_IPV6_MANAGEMENT_PREFIX
        #info['M1_GWv6'] = mgmt_ipv6_gw
    except socket.gaierror:
        info['M1_IPv6_ADDR'] = None
        info['M1_IPv6_PREFIX'] = None
        info['M1_IPv6_GW'] = None

    return info

def generate_ipv6_p1_info(wsa_hostname):
    DEFAULT_IPV6_DATA_PREFIX = '68'
    P1_IPV6_SUFFIX = 'p1'

    info = {}
    network = wsa_hostname.split('.')[-1]
    if network == 'ibauto':
        DEFAULT_IPV6_DATA_PREFIX = '76'
    elif network in ('cs1', 'cs3', 'cs20','cs21'):
        DEFAULT_IPV6_DATA_PREFIX = '112'
    elif network in ('cs14', 'cs27'):
        DEFAULT_IPV6_DATA_PREFIX = NETWORKS_MAPPING[network]['DATA_PREFIX']

    p1_ipv6_hostname = '%s-%s.%s' % (wsa_hostname.split('.')[0],
            P1_IPV6_SUFFIX , network)

    try:
        p1_ipv6 = socket.getaddrinfo(p1_ipv6_hostname,
            None, socket.AF_INET6)[0][4][0]

        array = p1_ipv6.split(':')
        array[-1] = '1'
        p1_ipv6_gw = ':'.join(array)

        info['P1_IPv6_ADDR'] = p1_ipv6
        info['P1_IPv6_PREFIX'] = DEFAULT_IPV6_DATA_PREFIX
        info['P1_IPv6_GW'] = p1_ipv6_gw

        # backward compatibility - uncomment if needed
        #info['M1_IPv6'] = mgmt_ipv6 + '/' + DEFAULT_IPV6_DATA_PREFIX
        #info['P1_GWv6'] = p1_ipv6_gw
    except socket.gaierror:
        info['P1_IPv6_ADDR'] = None
        info['P1_IPv6_PREFIX'] = None
        info['P1_IPv6_GW'] = None

    return info

def generate_ipv6_p2_info(wsa_hostname):
    DEFAULT_IPV6_DATA_PREFIX = '68'
    P2_IPV6_SUFFIX = 'p2'

    info = {}
    network = wsa_hostname.split('.')[-1]
    if network == 'ibauto':
        DEFAULT_IPV6_DATA_PREFIX = '76'
    elif network in ('cs1', 'cs3', 'cs20','cs21'):
        DEFAULT_IPV6_DATA_PREFIX = '112'
    elif network in ('cs14', 'cs27'):
        DEFAULT_IPV6_DATA_PREFIX = NETWORKS_MAPPING[network]['DATA_PREFIX']

    p2_ipv6_hostname = '%s-%s.%s' % (wsa_hostname.split('.')[0],
            P2_IPV6_SUFFIX , network)

    try:
        p2_ipv6 = socket.getaddrinfo(p2_ipv6_hostname,
            None, socket.AF_INET6)[0][4][0]

        array = p2_ipv6.split(':')
        array[-1] = '1'
        p2_ipv6_gw = ':'.join(array)

        info['P2_IPv6_ADDR'] = p2_ipv6
        info['P2_IPv6_PREFIX'] = DEFAULT_IPV6_DATA_PREFIX
        info['P2_IPv6_GW'] = p2_ipv6_gw

        # backward compatibility - uncomment if needed
        #info['M1_IPv6'] = mgmt_ipv6 + '/' + DEFAULT_IPV6_DATA_PREFIX
        #info['P2_GWv6'] = p2_ipv6_gw
    except socket.gaierror:
        info['P2_IPv6_ADDR'] = None
        info['P2_IPv6_PREFIX'] = None
        info['P2_IPv6_GW'] = None

    return info
