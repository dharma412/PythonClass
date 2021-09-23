#!/usr/local/bin/python
# $Id: //prod/main/sarf_centos/testlib/sal/net/ipmilib.py#1 $

from __future__ import absolute_import
from __future__ import with_statement

# : Reference Symbols: ipmilib

import os
import re
import subprocess
import sal.net.ping
import sal.irontools
import time

from sal.deprecated import proctools
from sal.deprecated import expect
from sal.exceptions import (ConfigError, TimeoutError)


class IpmiDisabledError(RuntimeError): pass


class SolDisabledError(IpmiDisabledError): pass


class SolOldVersionError(RuntimeError): pass


class SolBusyError(RuntimeError): pass


class IPMIController(object):
    def __init__(self, testobj):
        """ testobj must be an object of a class derived from irontest. Test
        or a hostname string...

        if testobj is a string, we set self.host, else set self.testobj
        """
        self.host = self.testobj = None
        if type(testobj) == type(''):
            self.host = testobj
        else:
            self.testobj = testobj
        check_ipmi()

    def get_ipmi(self):
        host = self.host or self.testobj.cfg.dut.hostname
        where = host.find('.')
        host = host[0:where] + '-ipmi' + host[where:]
        outfile = "%s/ipmi.out" % os.environ['HOME']
        cmd = (('%s -I lan -U admin -P ironport -H %s' \
                ' chassis power status 2>&1')
               % (ipmitool_path, host))
        p = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE)
        sts = os.waitpid(p.pid, 0)
        raw_out = p.stdout.read().strip()
        match = re.search('Chassis Power is (\w*)', raw_out)
        if match:
            line = match.group(1)
        else:
            line = ""
        p.stdout.close()

        return line

    def set_ipmi(self, value, host=None):
        if value != "" and value in ('reset', 'soft', 'off', 'on', 'cycle'):
            host = self.host or self.testobj.cfg.dut.hostname
            where = host.find('.')
            host = host[0:where] + '-ipmi' + host[where:]
            cmd = "%s -I lan -U admin -P ironport " \
                  "-H %s chassis power %s > /dev/null 2>&1" \
                  % (ipmitool_path, host, value)
            p = subprocess.Popen(cmd, shell=True)
            sts = os.waitpid(p.pid, 0)

    def set_boot_device_to_pxe(self):
        host = self.host or self.testobj.cfg.dut.hostname
        where = host.find('.')
        host = host[0:where] + '-ipmi' + host[where:]
        cmd = "%s -I lan -U admin -P ironport " \
              "-H %s chassis bootdev pxe > /dev/null 2>&1" \
              % (ipmitool_path, host)
        p = subprocess.Popen(cmd, shell=True)
        sts = os.waitpid(p.pid, 0)

    def power_cycle(self):
        self.set_ipmi('off')
        print('Shutting down via IPMI, delaying 10 seconds to complete')
        time.sleep(10)
        print("Current IPMI status for DUT: " + self.get_ipmi())
        print('Restarting via IPMI, will wait until SSH connection' +
              ' available to DUT')
        self.set_ipmi('on')
        sal.irontools.wait_for_phoebe(self.host or self.testobj)
        print("Current IPMI status for DUT: " + self.get_ipmi())


def get_ipmi_hostname(hostname):
    """ Crafts IPMI hostname from management hostname """
    where = hostname.find('.')
    hostname = hostname[:where] + '-ipmi' + hostname[where:]
    return hostname


is_ipmi_present_for_host = lambda hostname: \
    sal.net.ping.ping(get_ipmi_hostname(hostname))

ipmitool_path = '/usr/local/bin/ipmitool'


def check_ipmi():
    """ Check if:
    1. IPMITools exist
    2. TODO: SOL is available

    """
    global ipmitool_path
    # validate whether ipmitool is present on IAF machine by default path
    # if not, try to locate
    if not os.path.exists(ipmitool_path):
        cmd = 'which ipmitool'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        ipmitool_path = p.stdout.read().strip()
        if not ipmitool_path:
            raise OSError('No ipmitool available')


class IpmiSolExpect(expect.Expect):
    """ Implements a IPMI SOL transport
    :IVariables:
        - `_dummy_prompt`: The regexp which matches all expected prompts
    """

    _dummy_prompt = expect.RegexUserMatch(r'\S+>|\S+:\S+ \d+\]')

    def login(self, user, password):
        # Use cases:
        # 1. normal login prompt
        # 2. previous CLI session ("ironport.example.com>" or "c650s11.sma>")
        # 3. previous rshell session ("c650s11:rybilevych 1]")
        # 4. CLI in some interim state
        # Behavior:
        # - perform login steps in #1
        # - Logout and then login in #2 and #3
        # - restart to main prompt, logout, and login
        try:
            self.expect(['login:', self._dummy_prompt], timeout=10)
        except TimeoutError:
            self._restart_nosave()
            self.expect(['login:', self._dummy_prompt], timeout=10)

        if self.expectindex == 0:
            # Username is asked
            self.writeln(user)
            self.expect(['ssword:'], timeout=60)
            if self.expectindex == 0:
                self.writeln(password)

        else:
            # already logged in as different user. Relogin
            self._logout(force=True)
            time.sleep(2)
            self.login(user, password)

    def _restart_nosave(self, waittime=2):
        """_restart(): Return to the top-level prompt without caring
        if there are any:
            "-- Changes not recorded" or other errors from the CLI.
        """
        for dummy in range(10):
            try:
                self.expect([self._dummy_prompt], timeout=waittime)
                return
            except TimeoutError:
                self.interrupt()
        else:
            raise ConfigError, 'restart failed'

    def _logout(self, force=False):
        """ Logs out
        Assumes that main prompt is already reached
        """
        self.writeln('quit')
        if force:
            self.expect(['Are you sure you wish to exit?', 'AsyncOS '], timeout=60)
            if self.expectindex == 0:
                self.writeln('y')

    def close(self):
        """ Overrides base.
        attempts to gently close the connection.
        """
        self._restart_nosave()
        self._logout(force=True)
        self.writeln('')
        self.writeln('~.')
        expect.Expect.close(self)


def get_ipmi_sol_safe(host, user=None, password=None, prompt=None, cmd='',
                      logfile=None, extraoptions='', devmode=False, force_prompt=None):
    """Returns an IpmiSolExpect object."""

    pm = proctools.get_procmanager()

    command = '%s -I lanplus -H %s -U admin -P ironport sol activate' % (ipmitool_path, get_ipmi_hostname(host))

    sessproc = pm.spawnpty(command, logfile=logfile)
    sess = IpmiSolExpect(sessproc)

    sess.expect(['SOL Session operational.',
                 'SOL payload already active on another session',
                 'No response activating SOL payload',
                 'Unable to establish LAN session',
                 'Unable to establish IPMI v2 / RMCP+ session',
                 ])

    if sess.expectindex == 0:
        # SOL Session operational.
        sess.writeln('')
    elif sess.expectindex == 1:
        # some another process using this channel
        raise SolBusyError('SOL payload already active on another session')
    elif sess.expectindex == 2:
        raise SolDisabledError
    elif sess.expectindex == 3:
        raise IpmiDisabledError
    elif sess.expectindex == 4:
        raise SolOldVersionError('%s must support IPMI v2' % host)

    # Great! We have working terminal. Try to login and configure expect object.

    sess.login(user, password)

    return sess


def get_ipmi_sol_unsafe(host, user=None, password=None, prompt=None, cmd='',
                        logfile=None, extraoptions='', devmode=False, force_prompt=None):
    """ Returns an IpmiSolExpect object.

    Forces session if it is already spawned by others.
    """
    try:
        return get_ipmi_sol_safe(host, user, password, prompt, cmd, logfile, extraoptions, devmode, force_prompt)
    except SolBusyError:
        # deactivate previous session
        os.system(('%s -I lanplus -U admin -P ironport -H %s' \
                   ' sol deactivate') % (ipmitool_path, get_ipmi_hostname(host)))

        return get_ipmi_sol_safe(host, user, password, prompt, cmd, logfile, extraoptions, devmode, force_prompt)


if __name__ == '__main__':
    host = 'c670q02.qa'
    user = 'admin'
    password = 'ironport'
    lib_path = 'phoebe76'

    if is_ipmi_present_for_host(host):
        cli_module = __import__(lib_path + '.cli.cli', globals(), locals(),
                                ['get_cli'], -1)
        cli = cli_module.get_cli(host, user, password, transport='ipmi')
        try:
            mgmt_settings = {'IP': '10.92.145.170',
                             'NETMASK': '255.255.255.0',
                             'DNS': '10.92.144.4',
                             'GW': '10.92.145.1'}
            cli.interfaceconfig().edit(if_name='Management',
                                       address=mgmt_settings['IP'],
                                       netmask=mgmt_settings['NETMASK'],
                                       hostname=host,
                                       SSH='Y')
            cli.sethostname(host)
            cli.setgateway(ip=mgmt_settings['GW'])
            cli.dnsconfig().setup(use_own='Internet')
            cli.dnsconfig().setup(use_own='Use own',
                                  ip_addr=mgmt_settings['DNS'])
            cli.commit()
        finally:
            cli.close()
