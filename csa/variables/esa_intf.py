# $Id: //prod/main/sarf_centos/variables/esa_intf.py#5 $
# $DateTime: 2019/09/25 07:09:06 $
# $Author: saurgup5 $

import re
import warnings

import common.socketwrapper as socket
from credentials import RTESTUSER, RTESTUSER_PASSWORD
from robot.libraries.BuiltIn import BuiltIn
from sal.exceptions import BadEnvironment, HostDown
from SSHLibrary import SSHLibrary


IPV4 = 'ipv4'
IPV6 = 'ipv6'
interface_infos = {}


from network import wga as wga_network, ibesa as ibesa_network, \
      ibqa as ibqa_network, qa as qa_network, sma as sma_network, \
      perf1 as perf1_network, perf2 as perf2_network, perf3 as perf3_network, \
      cs2 as cs2_network, cs14 as cs14_network,cs27 as cs27_network, aws as aws_network, cs21 as cs21_network, \
      cs19 as cs19_network , cs33 as cs33_network

NETWORKS_MAPPING = {'aws':aws_network,
                    'wga': wga_network,
                   'ibqa': ibqa_network,
                   'ibeng': ibqa_network,
                   'ibesa': ibesa_network,
                   'cs2': cs2_network,
                   'cs14': cs14_network,
                   'cs19': cs19_network,
                   'cs21': cs21_network,
                   'cs27': cs27_network,
                   'cs33': cs33_network,
                   'qa': qa_network,
                   'sma': sma_network,
                   'perf1': perf1_network,
                   'perf2': perf2_network,
                   'perf3': perf3_network,}


def get_network_mask(network):
    if network in NETWORKS_MAPPING:
        dut_netmask = NETWORKS_MAPPING[network]['NETMASK']
        dut_data_netmask = NETWORKS_MAPPING[network]['DATA_NETMASK']
    else:
        warnings.warn('Network .%s is not present in standard networks '\
                      'list. Using default values for netmasks.' % (network,))
        dut_netmask ='255.255.255.0'
        dut_data_netmask = '255.255.255.0'
    return (dut_netmask, dut_data_netmask)

def get_prefixlen(network):
    if network in NETWORKS_MAPPING:
        dut_prefix = NETWORKS_MAPPING[network]['PREFIX']
        dut_data_prefix = NETWORKS_MAPPING[network]['DATA_PREFIX']
    else:
        warnings.warn('Network .%s is not present in standard networks '\
                      'list. Using default values for prefixes.' % (network,))
        dut_prefix = '64'
        dut_data_prefix = '64'
    return (dut_prefix, dut_data_prefix)

def get_relay_hosts(inet_mode=IPV4, prefix_length=64):
    relay_hosts = '172.0.0.0/8,10.0.0.0/8'
    if inet_mode == IPV6:
        this_client = socket.getfqdn()
        ip_address = socket.gethostbyname(this_client, IPV6)
        d1_ip_address = socket.gethostbyname('d1.' + this_client, IPV6)
        d2_ip_address = socket.gethostbyname('d2.' + this_client, IPV6)
        networks = ':'.join(ip_address.split(':')[0:prefix_length/16]) + '::/%s'\
                   %(prefix_length,) + ','
        networks = networks + ':'.join(d1_ip_address.split(':'\
                   )[0:prefix_length/16]) + '::/%s' %(prefix_length) + ','
        networks = networks + ':'.join(d2_ip_address.split(':'\
               )[0:prefix_length/16]) + '::/%s' %(prefix_length)
        relay_hosts = relay_hosts + ',' + networks
    return relay_hosts

def get_cidr(network):
    if network in NETWORKS_MAPPING:
        dut_cidr = NETWORKS_MAPPING[network]['CIDR']
        dut_data_cidr = NETWORKS_MAPPING[network]['DATA_CIDR']
    else:
        warnings.warn('Network .%s is not present in standard networks '\
                      'list. Using default values for CIDR.' % (network,))
        dut_cidr ='24'
        dut_data_cidr = '19'
    return (dut_cidr, dut_data_cidr)

def get_dns(network):
    if network in NETWORKS_MAPPING:
        dns = NETWORKS_MAPPING[network]['DNS']
    else:
        warnings.warn('Network .%s is not present in standard networks '\
                      'list. Using default values for DNS.' % (network,))
        dns ='192.198.0.1'
    return dns

def get_http_proxy():
    try:
        return BuiltIn().get_variables()['${HTTP_PROXY}']
    except:
        return None

def get_https_proxy():
    try:
        return BuiltIn().get_variables()['${HTTPS_PROXY}']
    except:
        return None

def get_gateway(ip_address, inet_mode=IPV4):
    if inet_mode == IPV6:
        ip_list = ip_address.split(':')
        gw_list = ip_list[:-1] + ['1']
        return ':'.join(gw_list)
    else:
        ip_list = ip_address.split('.')
        gw_list = ip_list[:-1] + ['1']
        return '.'.join(gw_list)

def get_num_data_intf(hostname):
    try:
        ssh_session = SSHLibrary()
        host_ip = socket.gethostbyname(hostname,IPV4)
        try:
            ssh_session.open_connection(host_ip, timeout=60)
            ssh_session.login(RTESTUSER, RTESTUSER_PASSWORD)
            out = ssh_session.execute_command('ifconfig -l')
        finally:
            ssh_session.close_connection()
        all_iface_cnt = len(out.split())
        data_iface_cnt = all_iface_cnt - 2
        ## This workaround is need till lab team fixes
        ## #140939 Need to resolve Data 3 interface for C670 models
        if data_iface_cnt >= 3:
            return 2
        # return num of interfaces without loopback and management
        return data_iface_cnt
    except Exception as e:
        raise HostDown(
            'Can\'t connect to the CLI of %s due to error:\n%s'\
            % (hostname, e))

def get_dut_names(hostname, robot_vars):
    # list of variables that contain hostname of dut
    dut_names = []
    for key in robot_vars.keys():
        if robot_vars[key] == hostname:
            # skip ${ and } symbols
            dut_names.append(key[2:-1])
    return dut_names

def get_variables(esa_hostname):
    # get robot variables
    robot_vars = BuiltIn().get_variables()
    inet_mode = robot_vars['${INET_MODE}'].lower()
    num_of_data_intf = get_num_data_intf(esa_hostname)
    if inet_mode != 'ipv4' and inet_mode != 'ipv6':
        raise BadEnvironment, 'Incorrect value [%s] ' %(inet_mode) + \
            'specified for variable INET_MODE. Should either be ipv4 or ipv6'

    for dut_name in get_dut_names(esa_hostname, robot_vars):
        this_client = socket.gethostname()
        interface_infos['CLIENT'] = this_client
        this_client_ip = socket.gethostbyname(this_client,IPV4)
        interface_infos['CLIENT_IP'] = this_client_ip
        if socket.has_ipv6:
            try:
                interface_infos['CLIENT_IPV6'] =\
                    socket.gethostbyname(this_client,IPV6)
            except socket.gaierror as e:
                print 'WARNING: IPv6 is enabled, but %s not found (%s).'\
                  ' Some tests may fail.' % (this_client, e)
        lab = esa_hostname.split('.')[-1]
        interface_infos['NETWORK'] = lab
        interface_infos['%s_DNS' % (dut_name,)] = get_dns(lab)
        (interface_infos['%s_NETMASK' % (dut_name,)], data_netmask) = \
                                                        get_network_mask(lab)
        (interface_infos['%s_CIDR' % (dut_name,)], data_cidr) = get_cidr(lab)
        interface_infos[dut_name] = esa_hostname
        ip_addr = socket.gethostbyname(esa_hostname, IPV4)
        interface_infos['%s_IP' %(dut_name,)] = ip_addr
        interface_infos['%s_GW' %(dut_name,)] = get_gateway(ip_addr, IPV4)
        interface_infos['%s_PROXY' % (dut_name,)] = get_http_proxy()
        interface_infos['%s_HTTPS_PROXY' % (dut_name,)] = get_https_proxy()
        interface_infos['%s_RELAY_HOSTS' %(dut_name,)] = get_relay_hosts(inet_mode)

        for index in xrange(1,num_of_data_intf + 1):
            interface_infos['%s_DATA%s_NETMASK' %(dut_name, index)] = \
                                                                  data_netmask
            interface_infos['%s_DATA%s_CIDR' %(dut_name, index)] = \
                                                                  data_cidr
            data_hostname = 'a001.d%s.%s' %(index, esa_hostname)
            interface_infos['%s_DATA%s' %(dut_name, index)] = data_hostname
            ip_addr = socket.gethostbyname(data_hostname, IPV4)
            interface_infos['%s_DATA%s_IP' %(dut_name, index)] = ip_addr
            interface_infos['%s_DATA%s_GW' %(dut_name, index)] = \
                                                      get_gateway(ip_addr, IPV4)

        if inet_mode == 'ipv6':
            interface_infos['CLIENT_IPv6'] = \
                                          socket.gethostbyname(this_client,IPV6)
            interface_infos['%s_IPv6_PREFIX' % (dut_name,)], data_prefix = \
                                        get_prefixlen(interface_infos['NETWORK'])
            ip_addr = socket.gethostbyname(esa_hostname, IPV6)
            interface_infos['%s_IPv6' %(dut_name,)] = ip_addr
            interface_infos['%s_IPv6_GW' %(dut_name,)] = \
                                                     get_gateway(ip_addr, IPV6)
            for index in xrange(1,num_of_data_intf + 1):
                interface_infos['%s_DATA%s_IPv6_PREFIX' %(dut_name, index)] = \
                                                                    data_prefix
                data_hostname = 'a001.d%s.%s' %(index, esa_hostname)
                ip_addr = socket.gethostbyname(data_hostname, IPV6)
                interface_infos['%s_DATA%s_IPv6' %(dut_name, index)] = ip_addr
                interface_infos['%s_DATA%s_IPv6_GW' %(dut_name, index)] = \
                                                     get_gateway(ip_addr, IPV6)
    return interface_infos
