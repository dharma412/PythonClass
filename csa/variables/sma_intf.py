# $Id: //prod/main/sarf_centos/variables/sma_intf.py#2 $
# $DateTime: 2019/05/29 01:29:05 $
# $Author: sarukakk $

import re
import socket
from robot.libraries.BuiltIn import BuiltIn

interface_infos = {}

def get_network_mask(network):
    if network == 'sma':
        dut_netmask = '255.255.254.0'
        dut_data1_netmask = '255.255.248.0'
        dut_data2_netmask = '255.255.248.0'
    elif network == 'wga':
        dut_netmask ='255.255.255.0'
        dut_data1_netmask = '255.255.0.0'
        dut_data2_netmask = '255.255.0.0'
    elif network == 'auto':
        dut_netmask = '255.255.254.0'
        dut_data1_netmask = '255.255.252.0'
        dut_data2_netmask = '255.255.252.0'
    elif network == 'eng' or network == 'qa':
        dut_netmask ='255.255.255.0'
        dut_data1_netmask = '255.255.224.0'
        dut_data2_netmask = '255.255.224.0'
    else:
        dut_netmask ='255.255.255.0'
        dut_data1_netmask = '255.255.255.0'
        dut_data2_netmask = '255.255.255.0'

    return (dut_netmask, dut_data1_netmask, dut_data2_netmask)

def get_dns(network):
    if network in ['sma', 'wga', 'auto']:
        dns = '172.29.176.4'
    elif network in ['eng', 'qa']:
        dns = '10.92.144.4'
    elif network == 'ibqa':
        dns = '10.104.229.4'
    else:
        dns ='192.198.0.1'

    return dns

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

def get_variables(sma_hostname):

    # get ipv4-ipv6 related parameters based on IP_PROTOCOL
    robot_vars = BuiltIn().get_variables()
    if robot_vars["${INET_MODE}"].lower() == 'ipv6':
        interface_infos['IPV_PARAM'] = '-6'
    # Generate network infos for this client
    this_client = socket.gethostname()
    interface_infos['CLIENT'] = this_client
    this_client_ip = socket.gethostbyname(this_client)
    interface_infos['CLIENT_IP'] = this_client_ip
    if socket.has_ipv6:
        try:
            addr_tuples = socket.getaddrinfo( \
                this_client,None,socket.AF_INET6,0,socket.SOL_TCP)
            interface_infos['CLIENT_IPV6'] = addr_tuples[-1][4][0]
        except socket.gaierror as e:
            print 'WARNING: IPv6 is enabled, but %s not found (%s).' \
                  ' Some tests may fail.' % (this_client, e)
    network = this_client.split('.')[-1]

    for dut_name in get_dut_names(sma_hostname):

        # Generate network mask for different labs
        lab = sma_hostname.split('.')[-1]
        (interface_infos['%s_NETMASK' % (dut_name,)],
        interface_infos['%s_DATA1_NETMASK' % (dut_name,)],
        interface_infos['%s_DATA2_NETMASK' % (dut_name,)]) = get_network_mask(lab)

        # Generate dns for different labs
        interface_infos['%s_DNS' % (dut_name,)] = get_dns(lab)

        # Generate network infos for Mgmt port of specified SMA
        interface_infos[dut_name] = sma_hostname
        mgmt_ip = socket.gethostbyname(sma_hostname)
        interface_infos['%s_IP' % (dut_name,)] = mgmt_ip
        mgmt_ip_octets = mgmt_ip.split('.')
        mgmt_gw_octets = mgmt_ip_octets[:-1] + ['1']
        interface_infos['%s_GW' % (dut_name,)] = '.'.join(mgmt_gw_octets)

        try:
            # Generate network infos for Data1 interface of specified SMA
            sma_d1_hostname = 'd1.%s' % (sma_hostname,)
            interface_infos['%s_DATA1' % (dut_name,)] = sma_d1_hostname
            d1_ip = socket.gethostbyname(sma_d1_hostname)
            interface_infos['%s_DATA1_IP' % (dut_name,)] = d1_ip
            d1_ip_octets = d1_ip.split('.')
            d1_gw_octets = d1_ip_octets[:-1] + ['1']
            interface_infos['%s_DATA1_GW' % (dut_name,)] = '.'.join(d1_gw_octets)
        except socket.gaierror:
            # in case Data1 is not set for current SMA, variables will be
            # initialized with None value
            interface_infos['%s_DATA1' % (dut_name,)] = None
            interface_infos['%s_DATA1_IP' % (dut_name,)] = None
            interface_infos['%s_DATA1_GW' % (dut_name,)] = None

        try:
            # Generate network infos for Data2 interface of specified SMA
            sma_d2_hostname = 'd2.%s' % (sma_hostname,)
            interface_infos['%s_DATA2' % (dut_name,)] = sma_d2_hostname
            d2_ip = socket.gethostbyname(sma_d2_hostname)
            interface_infos['%s_DATA2_IP' % (dut_name,)] = d2_ip
            d2_ip_octets = d2_ip.split('.')
            d2_gw_octets = d2_ip_octets[:-1] + ['1']
            interface_infos['%s_DATA2_GW' % (dut_name,)] ='.'.join(d2_gw_octets)
        except socket.gaierror:
            # in case Data2 is not set for current SMA, variables will be
            # initialized with None value
            interface_infos['%s_DATA2' % (dut_name,)] = None
            interface_infos['%s_DATA2_IP' % (dut_name,)]  = None
            interface_infos['%s_DATA2_GW' % (dut_name,)] = None

    return interface_infos
