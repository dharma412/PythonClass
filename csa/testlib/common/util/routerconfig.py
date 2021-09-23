#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/routerconfig.py#3 $
# $DateTime: 2019/06/12 01:54:47 $
# $Author: revlaksh $

import socket
import urllib2
import sal.time
import time
import re
import subprocess
import operator
from sal.exceptions import TimeoutError
from common.util.utilcommon import UtilCommon
from common.util.misc import Misc
import common.Variables


# TODO: Move to iaf2/lib if apppropriate
def timed_wrap(func, timeout, *args, **kwargs):
    tmr = sal.time.CountDownTimer(timeout).start()
    e = TimeoutError('func %s timed out after %d seconds' \
                     '' % (func.func_name, timeout))
    while tmr.is_active():
        try:
            return func(*args, **kwargs)
        except Exception, e:
            # Overwrite e if exception is raised, and raise that one.
            time.sleep(2)
    raise e


# Occasional connection refused issues require retries to open URLs
def urlopen_retry(url):
    return timed_wrap(urllib2.urlopen, 20, url)


class IPv4P2RoutingError(Exception):
    """Transparent routing over p2 is not available for IPv4 lab
    """

    def __init__(self):
        self.msg = 'Transparent routing over p2 interface is not available' \
                   ' for IPv4 lab'

    def __str__(self):
        return repr(self.msg)

    # used by Robot Framework to print message to console and log
    def __unicode__(self):
        return unicode(self.__str__())


class PortValueError(Exception):
    """Specified port not in list of available ports
    """

    def __init__(self):
        self.msg = 'Only mgmt, data or data2 as port values are acceptable'

    def __str__(self):
        return repr(self.msg)

    # used by Robot Framework to print message to console and log
    def __unicode__(self):
        return unicode(self.__str__())


class RouterConfig(UtilCommon):
    """
    Control IronPort IT router pages.
    """

    def __init__(self, *args, **kwargs):
        UtilCommon.__init__(self, *args, **kwargs)

        self.extern_host = 'outside.wga'
        self.intern_host = 'inside.wga'

        self.setslots_url = 'http://%s/setslots.php' % self.intern_host
        self.setl4_url = 'http://%s/setl4.php' % self.intern_host
        self.tapenable_url = 'http://%s/tapenable.php' % self.extern_host

        self.machines = {}
        self.slot = None
        self.domain = '.wga'
        if not self._is_ipv6_lab():
            self._populate_machines()
            self.slot = self.machines.get(self.dut)
            if not self.slot:
                self._warn("Machine %s is not found on http://inside.wga. " \
                           "It would not be possible to set machine into " \
                           "transparent routing" % (self.dut,))
        else:
            self.slot = self._get_ipv6_slice()

        self.client_slot = socket.gethostname()[4:7]

    def get_keyword_names(self):
        return [
            'set_slot',
            'unset_slot',
            'set_l4',
            'enable_tap',
            'disable_tap',
            'set_transparent_routing',
            'unset_transparent_routing',
        ]

    # IPv6 Lab specific methods
    def _is_ipv6_lab(self):
        return True

    def _get_ipv6_slice(self):
        variables = common.Variables.get_variables()
        NETWORK_ID = variables["${LAB_ID}"]
        if self._is_ipv6_lab():
            if re.match("^\D{3}\d{3}\D", self.dut) or re.match("^\D{3}\d{4}\-\D{3}(\d{3})", self.dut):
                if NETWORK_ID == 'IBAUTO':
                    slice = self.dut[11:14]
                else:
                    slice = self.dut[3:6]
                self._debug('In _get_ipv6_slice got slice="%s"' % (slice,))
                return slice
            else:
                return None
        else:
            return None

    def _get_ipv6_port(self, port):
        port_map = {'data': 'p1', 'mgmt': 'm1', 'data2': 'p2'}
        return port_map[port]

    def _control_redirection(self, port, onoff):
        variables = common.Variables.get_variables()
        control_redirection_command = "$SARF_HOME/tools/controlredirection.sh"
        USER = 'testuser'
        PWD = 'ironport'

        # Get IP of interface that will be set/unset as the next hop ip address
        ipv4_next_hop = variables["${WSA_" + self._get_ipv6_port(port).upper() + "_IP}"]

        # Get IPV6 of interface that will be set/unset as the next hop ip address
        ipv6_next_hop = variables["${WSA_" + self._get_ipv6_port(port).upper() + "_IPv6_ADDR}"]

        if variables.has_key("${TRANSPARENT_ROUTING_SERVER}"):
            HOST = variables["${TRANSPARENT_ROUTING_SERVER}"]
        else:
            if re.search("\.(.*)", self.dut).group(1) == "cs3" or re.search("\.(.*)", self.dut).group(1) == "cs20":
                if self.dut.find(".cs3") > -1:
                    HOST = 'tools.cs3'
                elif self.dut.find(".cs20") > -1:
                    HOST = 'tools.cs20'

                control_redirection_command = "/usr/local/bin/controlredirection.sh"
                m = re.match('0*(.{2,})', self.slot)
                cmd = "%s %s %s %s " % \
                      (
                          control_redirection_command,
                          m.group(1),
                          self._get_ipv6_port(port),
                          onoff
                      )
                Misc(None, None).run_on_host(
                    HOST,
                    USER,
                    PWD,
                    cmd)
                return ''
            elif re.search("\.(.*)", self.dut).group(1) == "cs1":
                HOST = 'tools.cs1'
                control_redirection_command = "/usr/local/bin/controlredirection.sh"
                m = re.match('0*(.{2,})', self.slot)
                cmd = "%s %s %s %s " % \
                      (
                          control_redirection_command,
                          m.group(1),
                          self._get_ipv6_port(port),
                          onoff
                      )
                Misc(None, None).run_on_host(
                    HOST,
                    USER,
                    PWD,
                    cmd)
                return ''
            elif self.dut.find(".cs14") > -1:
                if variables.has_key("${TOOLS}"):
                    HOST = variables["${TOOLS}"]
                else:
                    HOST = "tools.cs14"
                control_redirection_command = "/usr/local/bin/controlredirection.sh"
                cmd = "%s %s %s %s %s " % \
                      (
                          control_redirection_command,
                          self.client_slot,
                          self.dut[4:7],
                          self._get_ipv6_port(port),
                          onoff
                      )
                Misc(None, None).run_on_host(
                    HOST,
                    USER,
                    PWD,
                    cmd)
                return ''
            elif self.dut.find(".cs27") > -1:
                if variables.has_key("${TOOLS}"):
                    HOST = variables["${TOOLS}"]
                else:
                    HOST = "tools.cs27"
                control_redirection_command = "/usr/local/bin/controlredirection.sh"
                cmd = "%s %s %s %s %s " % \
                      (
                          control_redirection_command,
                          self.client_slot,
                          self.dut[4:7],
                          self._get_ipv6_port(port),
                          onoff
                      )
                Misc(None, None).run_on_host(
                    HOST,
                    USER,
                    PWD,
                    cmd)
                return ''
            elif self.dut.find(".auto") > -1:
                HOST = 'management.auto'
            elif self.dut.find(".ibauto") > -1:
                HOST = 'tools.ibauto'
            else:
                # HOST = 'vm10bsd0243.wga' old tool server
                HOST = 'tools.wga'

        # removed leading 0s from slot; otherwise slot is treated is octal
        m = re.match('0*(.{2,})', self.slot)
        cmd = "%s %s %s %s %s %s " % \
              (
                  control_redirection_command,
                  m.group(1),
                  self._get_ipv6_port(port),
                  onoff,
                  ipv4_next_hop,
                  ipv6_next_hop
              )
        Misc(None, None).run_on_host(
            HOST,
            USER,
            PWD,
            cmd)
        return ''

    # IPv4 Lab specific methods
    def _populate_machines(self):
        mach_txt = urlopen_retry('http://%s/machines.txt' \
                                 '' % self.intern_host).read()
        for mach_line in mach_txt.splitlines():
            if not mach_line.startswith('#') and mach_line.strip():
                slot, mach, wiring = mach_line.split(',')
                # ignore wiring for now, it may be used to verify
                # machine setup in the future.
                self.machines['%s%s' % (mach, self.domain)] = int(slot)

    def set_slot(self, client_hostname=None, server_hostname=None):
        """ Add client to the WSA using "Setslots Control Panel".

        Parameters:
            - `client_hostname`: host name if the client to be added. If None
              then current client on which SARF is run will be added.
            - `server_hostname`: hostname of DUT for which setting is changed.
              If not specified then DUT specified during initialization of
              UtilsLibrary will be used.

        Parameters:
        | Set Slot |
        | Set Slot | client_hostname=vm10bsd0113.wga | server_hostname=wsa74.wga |
        """
        client_hostname = client_hostname or socket.gethostname()
        slot = self.slot or self.machines.get(server_hostname)
        assert slot, "No server hostname passed to set_slot or UtilsLibrary"

        urlopen_retry('%s?client=%s&slot=%d' \
                      '' % (self.setslots_url, client_hostname, slot)).read()

    def unset_slot(self, client_hostname=None):
        """ Remove client from the WSA using "Setslots Control Panel".

        Parameters:
            - `client_hostname`: host name if the client to be removed. If None
              then current client on which SARF is run will be removed.

        Parameters:
        | Unset Slot |
        | Unset Slot | client_hostname=vm10bsd0113.wga |
        """
        client_hostname = client_hostname or socket.gethostname()
        ip = socket.gethostbyname(client_hostname)
        path = '?remove=1&client=%s%%2F32' % ip  # eg. ip/32
        urlopen_retry(self.setslots_url + path).read()

    def set_l4(self, mode, server_hostname=None):
        """ Set L4 Switch Emulation Mode using "L4 Switch Emulation Control
        Panel".

        Parameters:
            - `mode`: L4 switch emulation mode either data, mgmt, spoof or none
            - `server_hostname`: hostname of DUT for which setting is changed.
            If not specified then DUT specified during initialization of
            UtilsLibrary will be used.

        Examples:
        | Set L4 | data |
        | Set L4 | none | server_hostname=wsa74.wga |
        """
        slot = self.slot or self.machines.get(server_hostname)
        assert slot, "No server hostname passed to set_l4 or UtilsLibrary"
        assert mode in ('data', 'mgmt', 'spoof', 'none'), \
            "Invalid mode for set_l4: %r" % mode
        url = self.setl4_url + '?slot=%d&mode=%s' % (slot, mode)
        urlopen_retry(url).read()

    def enable_tap(self, server_hostname=None):
        """ Enable Tap for DUT using "Data Tap Control Panel".

        Parameters:
            - `server_hostname`: hostname of DUT for which Tap will be enabled.
            If not specified then DUT specified during initialization of
            UtilsLibrary will be used.

        Examples:
        | Enable Tap |
        | Enable Tap | server_hostname=wsa74.wga |
        """
        slot = self.slot or self.machines.get(server_hostname)
        assert slot, "No server hostname passed to enable_tap or UtilsLibrary"
        urlopen_retry('%s?tap=%d&changewga=Enable+Tap' \
                      '' % (self.tapenable_url, slot)).read()

    def disable_tap(self, server_hostname=None):
        """ Disable Tap for DUT using "Data Tap Control Panel".

        Parameters:
            - `server_hostname`: hostname of DUT for which Tap will be disabled.
            If not specified then DUT specified during initialization of
            UtilsLibrary will be used.

        Examples:
        | Disable Tap |
        | Disable Tap | server_hostname=wsa74.wga |
        """
        slot = self.slot or self.machines.get(server_hostname)
        assert slot, "No server hostname passed to disable_tap or UtilsLibrary"
        urlopen_retry('%s?bridge=%d&changewga=Disable+Tap' \
                      '' % (self.tapenable_url, slot)).read()

    def set_transparent_routing(self, port=None):
        """ Configure your client and router for transparent routing.

        Configure the network router (usually inside.wga) to route port 80/443
        traffic from this client through the WSA.

        Host name of the router is specified in $SARF_HOME/variables/network.py

        Parameters:
          - `port`: The port of the WSA to forward traffic through.
            Possible values:
            `mgmt` - for transparent routing over management interface(M1);
            `data` - for transparent routing over data interface(P1);
            `data2` - for transparent routing over data interface(P2);
            Default: 'mgmt'.

        Examples:
        | Set Transparent Routing |
        | Set Transparent Routing | port=data |
        """
        if port is not None:
            port = str(port.lower().strip())
        else:
            port = 'mgmt'

        self._info("Set client redirection on %s port in IPv6 lab" % (port,))
        if self._is_ipv6_lab():
            ports = {'mgmt': 'off', 'data': 'off', 'data2': 'off'}
            if port not in ports.keys():
                raise PortValueError
            # IPv6 Lab
            ports[port] = 'on'
            output = ''
            for port, state in sorted(ports.iteritems(),
                                      key=operator.itemgetter(1)):
                # first go items with off value, so transparent redirection
                # turns off for corresponding ports and finally it turns on
                # for port with on value
                output += '\nSetting redirection to %s for port %s\n' % \
                          (state, port)
                output += self._control_redirection(port, state)
            self._debug(output)

        else:
            # IPv4 Lab
            if port == 'data2':
                raise IPv4P2RoutingError()

            client = socket.gethostname()
            self._info("Set client redirection and set l4 routing port to " \
                       + port)
            self.set_slot(client)
            self.set_l4(port)

    def unset_transparent_routing(self):
        """ Configure your client and router to disable transparent routing.

        Examples:
        | Unset Transparent Routing |
        """
        if self._is_ipv6_lab():
            # IPv6 Lab
            self._info("Unset client redirection in IPv6 lab.")
            ports = {'mgmt': 'off', 'data': 'off', 'data2': 'off'}
            output = ''
            for port, state in ports.iteritems():
                output += '\nSetting redirection to %s for port %s\n' % \
                          (state, port)
                output += self._control_redirection(port, state)
            self._debug(output)

        else:
            # IPv4 Lab
            client = socket.gethostname()
            self._info("Unset client redirection and set l4 routing port to " \
                       "\'none\'")
            self.unset_slot(client)
            self.set_l4('none')
