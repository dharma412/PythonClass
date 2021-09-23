#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/sal/net/ifc.py#4 $
# $DateTime: 2019/06/17 01:57:40 $
# $Author: sarukakk $

"""Get a host's IP network interface information.

Information is available for (potentially) 5 network interfaces on a host:
    mg:    cinnamon.qa
    d1: d1.cinnamon.qa
    d2: d2.cinnamon.qa
    d3: d3.cinnamon.qa
    d4: d4.cinnamon.qa
For each of these interfaces the following is available:
    .hostname   ->  d1.cinnamon.qa
    .address    ->  d1.cinnamon.qa
    .subnet_mask->  255.255.0.0
    .jack_name  ->  Data 1

jack_name is only available when MGA model information is passed
to the InterfaceList object.
For non-MGA hosts jack_name is provided but not valid.

LIMITATIONS:
    InterfaceList doesn't work for .mfg hosts.
    Hosts on the .mfg network do not following the naming
    conventions of the other networks so InterfaceList()
    does not work for these hosts.
"""

#: Reference Symbols: ifc

from __future__ import absolute_import

import re
import socket

from sal.containers import cfgholder
import sal.net.sshlib

strict = False  # if True, ensures hostname is fully qualified

mask_hex = {
    0: '0x00000000L', 1: '0x80000000L', 2: '0xC0000000L',
    3: '0xE0000000L', 4: '0xF0000000L', 5: '0xF8000000L',
    6: '0xFC000000L', 7: '0xFE000000L', 8: '0xFF000000L',
    9: '0xFF800000L', 10: '0xFFC00000L', 11: '0xFFE00000L',
    12: '0xFFF00000L', 13: '0xFFF80000L', 14: '0xFFFC0000L',
    15: '0xFFFE0000L', 16: '0xFFFF0000L', 17: '0xFFFF8000L',
    18: '0xFFFFC000L', 19: '0xFFFFE000L', 20: '0xFFFFF000L',
    21: '0xFFFFF800L', 22: '0xFFFFFC00L', 23: '0xFFFFFE00L',
    24: '0xFFFFFF00L', 25: '0xFFFFFF80L', 26: '0xFFFFFFC0L',
    27: '0xFFFFFFE0L', 28: '0xFFFFFFF0L', 29: '0xFFFFFFF8L',
    30: '0xFFFFFFFCL', 31: '0xFFFFFFFEL', 32: '0xFFFFFFFFL'}

TWOINTERFACE = 2
THREEINTERFACE = 3

_mg_hostname_patt = None


class _InterfaceInfo:
    """Given a hostname and optional mga model type,
        determine the ip address, subnet mask and jack name"""
    # originally in etc/iaf/subnets.cfg
    subnets = cfgholder.LockingCfgHolder()

    subnets.aws.d1 = 24
    subnets.aws.d2 = 24
    subnets.aws.mg = 24

    subnets.perf2.d1 = 16
    subnets.perf2.d2 = 16
    subnets.perf2.mg = 24

    subnets.perf.d1 = 16
    subnets.perf.d2 = 16
    subnets.perf.mg = 24

    subnets.ibqa.d1 = 19
    subnets.ibqa.d2 = 19
    subnets.ibqa.mg = 24

    subnets.ibesa.d1 = 24
    subnets.ibesa.d2 = 24
    subnets.ibesa.mg = 24

    subnets.cs1.d1 = 27
    subnets.cs1.d2 = 27
    subnets.cs1.mg = 24

    subnets.cs2.d1 = 19
    subnets.cs2.d2 = 19
    subnets.cs2.mg = 24

    subnets.cs3.d1 = 27
    subnets.cs3.d2 = 27
    subnets.cs3.mg = 24

    subnets.cs14.d1 = 19
    subnets.cs14.d2 = 19
    subnets.cs14.mg = 24

    subnets.cs19.d1 = 19
    subnets.cs19.d2 = 19
    subnets.cs19.mg = 24

    subnets.cs27.d1 = 19
    subnets.cs27.d2 = 19
    subnets.cs27.mg = 24

    subnets.cs33.d1 = 19
    subnets.cs33.d2 = 19
    subnets.cs33.mg = 24

    subnets.cs20.d1 = 27
    subnets.cs20.d2 = 27
    subnets.cs20.mg = 24

    subnets.ibauto.d1 = 19
    subnets.ibauto.d2 = 19
    subnets.ibauto.mg = 24

    subnets.ibeng.d1 = 16
    subnets.ibeng.d2 = 16
    subnets.ibeng.mg = 24

    subnets.ibwsa.data = 28
    subnets.ibwsa.mg = 24
    # netmask for data port of non-WSA machines
    subnets.ibwsa.d1 = 16

    # value specifies the CIDR block prefix (ranges from 0 to 32 inclusive)
    subnets.auto.d1 = 22
    subnets.auto.d2 = 22
    subnets.auto.mg = 23

    subnets.qa.d1 = 19
    subnets.qa.d2 = 19
    subnets.qa.mg = 24

    subnets.cpt.d1 = 22
    subnets.cpt.d2 = 22
    subnets.cpt.mg = 24

    subnets.qb.d1 = 19
    subnets.qb.d2 = 19
    subnets.qb.mg = 24

    subnets.qap.d1 = 16
    subnets.qap.d2 = 16
    subnets.qap.mg = 24

    subnets.rep.d1 = 16
    subnets.rep.d2 = 16
    subnets.rep.mg = 24

    # NOTE: only 172.[16|21|22].h.[1,17,33,49,65,81,97,113] are configured
    subnets.eng.d1 = 19
    subnets.eng.d2 = 19
    subnets.eng.mg = 24

    subnets.sma.d1 = 21
    subnets.sma.d2 = 21
    subnets.sma.mg = 23

    subnets.dev.d1 = 24
    subnets.dev.d2 = 24
    subnets.dev.mg = 24

    subnets.mlab1.d1 = 16
    subnets.mlab1.d2 = 16
    subnets.mlab1.mg = 24
    subnets.mlab1.d3 = 16
    subnets.mlab1.d4 = 16

    # NOTE: only a000 to a09 are configured in the cmlab
    subnets.cmlab.d1 = 24
    subnets.cmlab.d2 = 24
    subnets.cmlab.mg = 24

    subnets.train.d1 = 16
    subnets.train.d2 = 16
    subnets.train.mg = 24

    subnets.run.d1 = 24
    subnets.run.d2 = 24
    subnets.run.mg = 23

    subnets.wga.data = 28
    subnets.wga.mg = 24
    # netmask for data port of non-WSA machines
    subnets.wga.d1 = 16

    subnets.somaqa.d1 = 16
    subnets.somaqa.d2 = 16
    subnets.somaqa.mg = 24

    # NOTE: .mfg does not follow naming convention
    # subnets.mfg.

    # Add corporate subnet(10.1.1.X)?
    # subnets.corp.mg = 18 # haven't verified correctness!

    # No need to allow dynamic creation of new subnets
    subnets.lock()

    def __init__(self, hostname, model=''):
        """model is from iaf/etc/models.cfg"""
        global strict
        if strict:  # ensure hostname is fully qualified
            self.hostname = socket.getfqdn(hostname)  # can be slow
        else:
            self.hostname = hostname

        self.address = socket.gethostbyname(self.hostname)
        self.subnet_mask = self._calc_subnet_mask(self.hostname)
        self.network = get_network(self.hostname)
        # this gives nick names for public and private listeners. If
        # a002.d1.c600-05.auto is the hostname, then it returns a002.d1
        self.nick = '.'.join(self.hostname.split('.')[:-2])

        self.eth_name = self._get_mga_eth_name(self.hostname)
        self.model = model
        # Don't need jack_name, eth_name and model for device from
        # .wga network.
        if self.network not in ('wga', 'ibwsa'):
            self.jack_name = self._get_mga_jack_name(self.hostname, model)

    def __str__(self):
        return self.hostname

    def _calc_subnet_mask(self, hostname):
        """Determine dotted quad subnet mask associated with hostname"""
        network_name = get_network(hostname)
        subnet_name = self._get_subnet(hostname)
        assert subnet_name, "Unable to determine hostname's subnet"
        return self._cidr2quad(self.subnets[network_name][subnet_name])

    def _get_subnet(self, hostname):
        parts = hostname.split('.')
        if parts[1] in ('wga', 'ibwsa') and 'data' in parts[0].split('-'):
            return 'data'
        for subnet_name in ('d1', 'd2', 'd3', 'd4'):
            if subnet_name in parts:
                return subnet_name
        else:
            return 'mg'

    def _cidr2quad(self, cidr_block_prefix):
        """Convert CIDR prefix to dotted quad subnet mask
            Eg. 24 -> '255.255.255.0'"""
        global mask_hex
        intval = eval(mask_hex[int(cidr_block_prefix)])
        s = '%c%c%c%c' % (((intval >> 24) & 0x000000ff), ((intval & 0x00ff0000) >> 16),
                          ((intval & 0x0000ff00) >> 8), (intval & 0x000000ff))
        return socket.inet_ntoa(s)

    def _get_mga_jack_name(self, hostname, model):
        # Map MGA hostname+MGA model to jack name.
        #
        # jack name can be: Data 1, Data 2, Data 3, Data 4, Management
        #
        # For MGA Models: d1->Data 1, d2-> Data 2, d3->Data 3
        #               d4->Data 4, mg->Management
        #
        # The exception is the c10 and c100.
        #   c10 or c100 on cmlab:
        #       d1->Data 1, d2->Data 2
        #   c10 or c100 on every other network (qa qb eng mlab1 train run):
        #       mg->Data 1, d1->Data 2

        # NOTE: may be better if jack info is in a config file instead

        if model.lower() in ('c10', 'c100', 'c150', 'c160', 'b10'):
            subnet_name = self._get_subnet(hostname)
            if hostname.lower().find('.cmlab') >= 0:
                if subnet_name == 'd1':
                    return 'Data 1'
                elif subnet_name == 'd2':
                    return 'Data 2'
            else:  # c10 or c100 is on (qa qb eng mlab1 train run)
                if subnet_name == 'mg':  # Management
                    return 'Data 1'
                elif subnet_name == 'd1':
                    return 'Data 2'
        else:
            subnet_name = self._get_subnet(hostname)
            if subnet_name[0] == 'd':  # Data interface
                return 'Data ' + subnet_name[-1]
            elif subnet_name == 'mg':  # Management
                return 'Management'

        # should not reach this line of code
        raise RuntimeError, "Unable to determine hostname's jackname"

    def _get_ifconfig_data(self, hostname):
        """Read ifconfig output using ssh

        NOTE! The interface must have the IP address of the 'hostname' arg
        in order for the correct eth_name to be returned by this method.
        If you run this method before the MGA is configured an 'unknown'
        eth_name will be returned.

        #em0: flags=8843 mtu 1500
        #    options=b
        #    inet 172.21.56.1 netmask 0xffff0000 broadcast 172.21.255.255
        #    ether 00:11:43:36:80:ae
        #    media: Ethernet autoselect (100baseTX )
        #    status: active
        #lo0: flags=8049 mtu 16384
        #    inet 127.0.0.1 netmask 0xff000000
        """

        # Get ethernet card name (eg. em0, em1, etc) for given interface
        if hostname.find('.mlab') == -1:
            mgt_hostname = _construct_mg_hostname(hostname)
        else:
            mgt_hostname = '.'.join(hostname.split('.')[-3:])

        ifconfig_txt = ''
        cmd = 'ifconfig -a'
        ifconfig_txt = sal.net.sshlib.ssh_command(mgt_hostname, command=cmd,
                                                  user='rtestuser',
                                                  password='ironport',
                                                  devmode=False)
        return ifconfig_txt

    def _get_mga_eth_name(self, hostname):
        """ Read ifconfig_txt and get the ethernet interface name """

        ifconfig_txt = self._get_ifconfig_data(hostname)
        target_addr = socket.gethostbyname(hostname)

        eth2ip = {}
        lines = ifconfig_txt.split('\n')
        eth_name = ''
        for line in lines:
            m = re.search('^(\w+\d+): ', line)
            if m:
                eth_name = m.group(1)
                eth2ip[eth_name] = []
                continue

            m = re.search('inet (\d+\.\d+\.\d+\.\d+)', line)
            if m:
                ifconfig_ip_addr = m.group(1)
                if target_addr == ifconfig_ip_addr:
                    return eth_name
        return 'unknown'

    def _get_all_interfaces(self, hostname):
        """This function returns the number of hardware interfaces on the
           dut. A dictionary with the the ethernet interface name and the
           correponding Ips is returned.
        """
        ifconfig_txt = self._get_ifconfig_data(hostname)
        eth2ip = {}
        lines = ifconfig_txt.split('\n')
        eth_name = ''
        for line in lines:
            m = re.search('^(\w+\d+): ', line)
            if m and m.group(1) <> 'lo0':
                eth_name = m.group(1)
                eth2ip[eth_name] = ''
                continue

            m = re.search('inet (\d+\.\d+\.\d+\.\d+)', line)
            if m:
                eth2ip[eth_name] = m.group(1)

        return eth2ip

    def _get_num_interfaces(self):
        """ Returns the num of interfaces that the DUT has """
        num_interfaces = self._get_all_interfaces(self.hostname).__len__()
        return num_interfaces

    def _get_data_gw_ip(self):
        """ Returns the IP address of the gateway associate with data
            port of the WSA.  According to inside.wga:

                data_gw_ip = data_port_ip with (4th octet - 1)

            Note: This method applies to WSA product only."""

        if not re.search('-data.', self.hostname):
            raise ValueError, "Data gateway is only available for Data port " \
                              "of WSA product."
        ip_octets = self.address.split('.')
        ip_octets[3] = str(int(ip_octets[3]) - 1)
        return '.'.join(ip_octets)

    def _get_client_gw_ip(self):
        """ Returns the IP address of the gateway associate with client
            side in WSA network.  Need to specify this when configure
            proxy over Data port of WSA.  According to inside.wga:

                client_gw_ip = data_port_ip with (4th octet + 12)

            Note: This method applies to WSA product only."""

        if not re.search('-data.', self.hostname):
            raise ValueError, "Client gateway is only available for Data " \
                              "port of WSA product."
        ip_octets = self.address.split('.')
        ip_octets[3] = str(int(ip_octets[3]) + 12)
        return '.'.join(ip_octets)


def _construct_mg_hostname(hostname):
    """ Finds the hostname of the management interface using any other hostname
    of given box

    ESA:
        a001.d1.mike.qa --> mike.qa
        d1.c600-06.auto --> c600-06.auto
    SMA:
        m1000s01.sma --> m1000s01.sma
    WSA:
        wsa61-data.wga --> wsa61.wga
        wsa75.wga.sbr.ironport.com --> wsa75.wga.sbr.ironport.com

    """
    # pattern matches the following groups:
    # group(1): hostname without network
    # group(2): "-data" value if present; None othervise
    # group(3): subnet name (wsa, sma, auto, eng, run, ...)
    # group(4): full domain suffix if given (sbr.ironport.com)
    global _mg_hostname_patt
    if not _mg_hostname_patt:
        _mg_hostname_patt = re.compile(r'([-\w]+?)(-data)?\.(%s)(.*)' %
                                       '|'.join(_InterfaceInfo.subnets.keys()))

    res = _mg_hostname_patt.search(hostname)
    assert res, 'mgmt hostname cant be retrieved from given data: %s' % hostname

    mg_hostname = '%s.%s%s' % (res.group(1), res.group(3), res.group(4))

    # simple verification whether hostname exists. If not, socket.gaierror is thrown
    socket.gethostbyname(mg_hostname)

    return mg_hostname


def get_network(hostname='localhost'):
    """Parse hostname and return qa, eng, cmlab, train, run, mfg, mlab1, .wga"""
    if hostname == 'localhost':
        hostname = socket.gethostname()
    parts = hostname.split('.')
    network_name = parts[-1]  # .qa, .eng, .cmlab, .train, .run, .wga
    if parts[-2] == 'mlab1':  # mlab1.qa is a special case
        network_name = 'mlab1'
    return network_name


class InterfaceList:
    """Acces IP interface information for a DUT."""

    def __init__(self, hostname='', model=''):
        self.hostname = hostname or socket.gethostname()
        self.model = model.lower()
        self.network = get_network(self.hostname)
        self.num_interfaces = _InterfaceInfo(self.hostname, self.model)._get_num_interfaces()

    def d1(self, prefix=''):
        """d1 (usually Data 1) Interface"""
        if prefix: prefix += '.'
        if self.network in ('wga', 'ibwsa') and self.model.startswith('s'):
            # for WSA, hostname for data port is typically 'wsaXX-data.wga'
            hostname = (self.hostname.split('.'))[0] + '-data.' + self.network
            return _InterfaceInfo(hostname, self.model)
        else:
            return _InterfaceInfo(prefix + 'd1.' + self.hostname, self.model)

    def d2(self, prefix=''):
        """d2 (usually Data 2) Interface"""
        if prefix: prefix += '.'
        return _InterfaceInfo(prefix + 'd2.' + self.hostname, self.model)

    def d3(self, prefix=''):
        """d3 (usually Data 3) Interface"""
        if prefix: prefix += '.'
        return _InterfaceInfo(prefix + 'd3.' + self.hostname, self.model)

    def d4(self, prefix=''):
        """d4 (usually Data 4) Interface"""
        if prefix: prefix += '.'
        return _InterfaceInfo(prefix + 'd4.' + self.hostname, self.model)

    def mg(self):
        """mg (management) Interface"""
        return _InterfaceInfo(self.hostname, self.model)

    def public(self):
        """Return interface that has the default public smtp mga listener.
        This is only valid for netinstallable MGAs"""
        # if the MGA is a c10 or c100, the public listener is on d1
        if self.num_interfaces < THREEINTERFACE:
            return self.d1()
        else:
            return self.d2()

    def private(self):
        """Return interface that has the default private smtp mga listener.
        This is only valid for netinstallable MGAs. If model is blocker, create a private listener on same interface"""
        ## If dut is a 2 appliance box i.e. b10, c10 etc, create a private listener
        ## on the d1 interface itself

        if self.num_interfaces < THREEINTERFACE:
            return self.d1('a002')
        else:
            return self.d1()

    """ Dev box interfaces - main_smtp and main_qmqp.
        These run on the "management" interface - the only one a
        dev unit has. """

    main_smtp = mg
    main_qmqp = mg


class TestClientInfo:
    """Provides network information of the client.  In WSA land, the client would
       be the test machine where all IAF test suite gets initiated.

       TODO:  This class currently does not provide network infos for other interfaces
              that are available on test machine in .mga or .auto land.  Will update
              as needed"""

    def __init__(self):
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)

    def get_this_client_hostname(self):
        """Return the hostname of the client."""
        return self.hostname

    def get_this_client_ip(self):
        """Return the IP address of the client."""
        return self.ip
