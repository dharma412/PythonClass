#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/netinstall.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from __future__ import absolute_import
import sys

from common.util.utilcommon import UtilCommon
from common.util.systools import SysTools
from sal.net import ping
from sal.net.services import netinstallpage, qabdbase

import sal.net.socket
from sal.containers import cfgholder
from sal.exceptions import ConfigError
from common.cli.clicommon import CliKeywordBase


class BadBuildIDError(ConfigError):
    def __init__(self, build_id):
        self.build_id = build_id

    def __str__(self):
        return 'Build ID: "%s" did not match any real builds' % self.build_id

    # RobotFramework use this method instead of __str__()
    def __unicode__(self):
        return unicode(self.__str__())


# for debugging
do_netinstall = True


class Netinstall(UtilCommon):
    """
        This Test Library requires specifying at least the DUTs hostname and
        build_id to netinstall a DUT.

        A regular expression search is performed on the list of build_ids.
        When `build_id_regex` matches multiple build_ids:
         if there is at least one build in format aaaa-X-X-XXX:
             take the latest within such builds
         else:
             take the latest build in the whole list

        The hostname will be parsed to determine the network it's
        located on and the netinstall.cgi script for that network will be used.
        The network is used only as an optimization to search the
        build IDs on a particular network instead of search all networks.
        If the network is unknown all networks are searched.

        The netinstall command is issued via the qabackdoor web UI.

        After the netinstall, the script will block until port 22 is open.
        If the ssh port(22) opens 0 is returned. Otherwise and
        exception is raised.
    """

    def __init__(self, *args, **kwargs):
        # call parent's constructor
        UtilCommon.__init__(self, *args, **kwargs)

        self.systools = SysTools(*args, **kwargs)

    def get_keyword_names(self):
        return [
            'redo_netinstall',
            'netinstall',
            'configure_netinstall_page'
        ]

    def configure_netinstall_page(self, hostname=None, build_id_regex=None,
                                  model=None, preconfigure='testing'):
        """Configure Netinstall Page

        Configure netinstall page with customized parameters.Keyword setup
        desired values on `Netinstall / Edit` page

        Parameters:
            - `hostname`: host name of the machine to be netinstalled. If None
              then hostname specified during initialisation of UtilsLibrary or
              hostname saved in ${DUT} variable will be used
            - `build_id_regex`: a regular expression to be used in search that
              is performed on the list of build_ids.
              if there is at least one build in format aaaa-X-X-XXX:
             take the latest within such builds
              else take the latest build that matches build_id_regex
            - `model`: new value of DUT model that will be selected before
              netinstall. If None then value is left unchanged.
            - `preconfigure`: value to be selected from preconfigure drop-down
              list. Possible values: Testing, Release, Harness and Shipping (for
              Release for Shipping).

        Examples:
        | Configure Netinstall Page | ${DUT} | build_id_regex=coeus-7.5.0-270 |
        """
        hostname = hostname or self.dut
        pi = netinstallpage.PhoebeInstall()

        # get build_id
        network = hostname.split('.')[-1]
        if network not in netinstallpage.cfg.datalisturl.keys():
            # Netinstall web page on all networks is searched (is slow!)
            self._info('Warning: Unknown network(%s)' % network)
            network = None
        build_id = self._get_build_id(build_id_regex, pi, network)

        # If we passed a build_id_regex, and no build was found
        # give a nice error message.
        if build_id_regex and not build_id:
            self._info('Error: Build ID: "%s" did not match any real ' \
                       'builds' % build_id_regex)
            raise BadBuildIDError, (build_id_regex,)
            return -1

        if not build_id:
            self._info('Error: No build_id selected')
            return -1

        self._info("Configuring Netinstall page  %s:%s" % (hostname, build_id))

        # Configure netinstall page
        pi.change(hostname, build_id, str(model).upper(), preconfigure)
        return 0, build_id

    def redo_netinstall(self, hostname=None, wait_for_reboot=True,
                        wait_for_ports=None):
        """ Redo Netinstall

        Perform netinstall using same version, build, preconfigure as DUT has
        now. Keyword is just following `redo netinstall` link on QA backdoor.

        Parameters:
            - `hostname`: host name of the machine to be netinstalled. If None
              then hostname specified during initialisation of UtilsLibrary or
              hostname saved in ${DUT} variable will be used
            - `wait_for_reboot`: whether wait until the machine is rebooted and
              starts listening port 22. True is used by default.
            - `wait_for_ports`: string of comma separated pairs
              [interface:]port. If interface is skip then Management interface
              is used.

        Examples:
        | Redo Netinstall |
        | Redo Netinstall | ${DUT} |
        | Redo Netinstall | wsaXX.wga | wait_for_reboot=${False} |
        | Redo Netinstall | ${DUT} | wait_for_ports=8080, ${DUT_P1}:3128 |
        """
        # use hostname given during initialisation of UtilsLibrary
        hostname = hostname or self.dut

        self._info("Redo Netinstallation %s" % (hostname))

        # netinstall
        self._netinstall(hostname=hostname, wait_for_reboot=wait_for_reboot,
                         wait_for_ports=wait_for_ports)

    def netinstall(self, hostname=None, build_id_regex=None, model=None,
                   wait_for_reboot=True, exact_select=False, preconfigure='testing',
                   wait_for_ports=None):
        """ Netinstall

        Perform netinstall with customized parameters. Keyword setup desired
        values on `Netinstall / Edit` page then follow `redo netinstall` link on
        QA backdoor.

        Parameters:
            - `hostname`: host name of the machine to be netinstalled. If None
              then hostname specified during initialisation of UtilsLibrary or
              hostname saved in ${DUT} variable will be used
            - `build_id_regex`: a regular expression to be used in search that
              is performed on the list of build_ids.  When `build_id_regex`
              matches multiple build_ids the last build_id in the build_id list
              is used.
            - `model`: new value of DUT model that will be selected before
              netinstall. If None then value is left unchanged.
            - `wait_for_reboot`: whether wait until the machine is rebooted and
              starts listening port 22. True is used by default.
              This parameter does not take effect when `preconfigure` is
              'shipping' such as IP address of the machine will be changed to
              default one 192.168.42.42.
            - `exact_select`: if True then exception is raised in case more then
              one build is matched `build_id_regex`. By default - False.
            - `preconfigure`: value to be selected from preconfigure drop-down
              list. Possible values: Testing, Release, Harness and Shipping (for
              Release for Shipping).
            - `wait_for_ports`: string of comma separated pairs
              [interface:]port. If interface is skip then Management interface
              is used.

        Examples:
        | Netinstall | build_id_regex=coeus-7.5.0-270 | |
        | Netinstall | ${DUT} | build_id_regex=coeus-7.5.0-270 |
        | Netinstall | ${DUT} | build_id_regex=coeus-7-5-0-270 |
        | ... | exact_select=${True} | preconfigure=Shipping |
        | ... | wait_for_reboot=${False} | |
        | Netinstall | ${DUT} | build_id_regex=coeus-7-5-0-270 |
        | ... | wait_for_ports=8080, ${DUT_P1}:3128 |
        """

        # use hostname given during initialisation of UtilsLibrary
        hostname = hostname or self.dut

        preconfigure = preconfigure.lower().strip()
        assert preconfigure in ('testing', 'release', 'shipping',
                                'harness')
        # do not wait when machine in installed into Release for Shipping mode
        if preconfigure == 'shipping':
            wait_for_reboot = False

        # configure netinstall page
        status, build_id = self.configure_netinstall_page(hostname=hostname,
                                                          build_id_regex=build_id_regex,
                                                          model=model, preconfigure=preconfigure)

        # netinstall
        self._netinstall(hostname=hostname, wait_for_reboot=wait_for_reboot,
                         wait_for_ports=wait_for_ports)

        # wait until host becomes unreachable when release for shipping
        # mode is selected
        if preconfigure == 'shipping':
            ping.wait_until_not_reachable(hostname, timeout=1200)

        # also returns build_id, for use when a build_id_regex is passed in
        return 0, build_id

    def _get_build_id(self, build_id_regex=None, pi=None, network=None,
                      exact_select=False):
        if build_id_regex is None:
            raise ValueError, 'Can not select build to netinstall! ' \
                              'build_id_regex is None'
        bl = pi.get_build_list(build_id_regex, network)
        if not bl:
            self._print_available_builds(pi, network, '.*')
            raise ValueError, 'There are not any builds matching %s' \
                              % build_id_regex
        if exact_select and len(bl) > 1:
            self._print_available_builds(pi, network, build_id_regex)
            raise ValueError, 'There are multiple builds matching %s' \
                              % build_id_regex
        found_standard = False
        duplicate = False
        for build in bl:
            if build.count('-') == 4:
                build_name = build
                if not found_standard:
                    found_standard = True
                else:
                    if found_standard:
                        duplicate = True
        if not found_standard:
            self._warn('Did not find matching standard builds')
            build_name = bl[-1]
        if duplicate:
            self._warn('Found multiple matching standard builds')
        self._info('Installing build:' + build_name)
        return build_name

    def _print_available_builds(self, pi, network, pattern):
        all_builds = pi.get_build_list(pattern, network)
        self._info('Available builds:')
        for build in all_builds:
            self._info(build)

    def _netinstall(self, hostname=None, wait_for_reboot=True,
                    wait_for_ports=None):
        if do_netinstall:
            qabdbase.get_qabackdoor(hostname).redo_netinstall()
        else:
            self._info('Skipping netinstall step')
        # wait for ssh port to open
        if wait_for_reboot:
            self._info('Waiting for %s to reboot...' % hostname)
            ping.wait_for_reboot(hostname, timeout=1800)
            self._info('Rebooted. Waiting for port 22 to open')
            sal.net.socket.wait_for_port(hostname, 22, timeout=2300)
            self._info('Port 22 is open')

        # wait for additional ports
        if wait_for_ports is not None:
            self._info('Waiting for ports %s to open' % wait_for_ports)
            self.systools._wait_for_ports(wait_for_ports, timeout=900)
            self._info('Ports %s are now open!' % wait_for_ports)
