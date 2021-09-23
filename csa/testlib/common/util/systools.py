#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/common/util/systools.py#2 $
# $DateTime: 2019/06/11 06:52:26 $
# $Author: revlaksh $

# python imports
import functools
import os.path
import re

# sarf imports
import sal.time
import sal.net.socket
from sal.net.ipmilib import is_ipmi_present_for_host, IpmiDisabledError
from sal import irontools
import sal.net.ping
from sal.containers.yesnodefault import YES
import socket
import time
from sal.exceptions import ConfigError, TimeoutError
from common.util.utilcommon import UtilCommon
from common.shell import shell
from common.cli.clicommon import CliKeywordBase
from common.util.misc import Misc

# variables
from credentials import DUT_ADMIN, DUT_ADMIN_PASSWORD
import network

from common.util.platform_services import VMWareServices, IPMIServices


class NetinstallNoBuild(Exception): pass


class RebootError(Exception): pass


class UpgradeError(Exception): pass


class NoAccessToDutError(Exception): pass


class NoAdvancedPlatformServices(Exception): pass


class SysTools(UtilCommon):
    """
        Some useful System Tools to aid automated QA working.

        The machine to be used (rebooted, upgraded, ...) is the one which
        hostname specified during initialisation of UtilsLibrary or saved in
        ${DUT} variable.
    """

    # list of methods to be exposed as RF keywords
    def get_keyword_names(self):
        return [
            'wait_until_dut_reboots',
            'wait_until_dut_is_accessible',
            'reboot_and_wait',
            'upgrade_and_wait',
            'shutdown_cycle',
            'kill_proc',
            'shift_time',
            'restore_network_settings',
            'install_qa_backdoor',
            'restore_machine',
            'get_dut_build',
            'sync_time',
            'reset_cycle',
            'set_boot_device_to_pxe',
            'restore_root_access',
            '_is_dut_a_virtual_model',
        ]

    def _get_cli(self, transport='ssh'):
        if hasattr(self, '_rfs') and self._rfs:
            admin_password = DUT_ADMIN_PASSWORD
        else:
            admin_password = Misc(None, None).get_admin_password(self.dut)

        get_dynamic_cli = lambda lib_path, transport: __import__(lib_path + '.cli.cli',
                                                                 globals(), locals(), ['get_cli'], -1). \
            get_cli(self.dut, DUT_ADMIN, admin_password, transport=transport)
        cli = get_dynamic_cli(self.dut_version, transport)
        current_lib_path = self._get_lib_path(cli)
        if self.dut_version != current_lib_path:
            # DUT version is changed due to netinstall/upgrade/revert
            self.dut_version = current_lib_path
            return get_dynamic_cli(self.dut_version, transport)
        else:
            return cli

    def _get_psc(self):
        if not hasattr(self, '__platform_services_controller'):
            if is_ipmi_present_for_host(self.dut):
                self.__platform_services_controller = IPMIServices(self.dut)
            else:
                try:
                    self.__platform_services_controller = VMWareServices(self.dut)
                except Exception as e:
                    raise NoAdvancedPlatformServices('The %s box has no advanced hardware ' \
                                                     'platform services available: no IPMI neither VSphere.\n' \
                                                     'Please choose an IPMI-enabled hardware box or a virtual box in' \
                                                     'order to use this keyword ' % (self.dut,))
        return self.__platform_services_controller

    def _setup_network(self, cli):
        dut_ip = socket.gethostbyname(self.dut)
        network_settings = network.get_variables()
        mgmt_settings = {'DNS': network_settings['DNS'],
                         'IP': dut_ip,
                         'GW': re.sub(r'\d+$', '1', dut_ip),
                         'NETMASK': network_settings['NETMASK']}
        cli.interfaceconfig().edit(if_name='Management',
                                   address=mgmt_settings['IP'],
                                   netmask=mgmt_settings['NETMASK'],
                                   hostname=self.dut,
                                   SSH='Y')
        cli.setgateway(ip=mgmt_settings['GW'])
        cli.dnsconfig().setup(use_own='Internet')
        cli.dnsconfig().setup(use_own='Use own',
                              ip_addr=mgmt_settings['DNS'])
        cli.sethostname(self.dut)
        cli.commit('defaults set via IPMI')
        self._info('Network is set up')

    def _wait_for_ports(self, ports, timeout=600):
        ports = self._convert_to_tuple(ports)
        for host_port in ports:
            # extract interface if it is specified
            if host_port.find(':') != -1:
                host, port = host_port.rsplit(':', 2)
            else:
                host = self.dut
                port = host_port
            self._info("Wait for port %s:%s" % (host, port))
            sal.net.socket.wait_for_port(host, int(port), timeout=timeout)

    def _wait_for_cli(self, timeout=240):
        '''
            If there are 10 ssh login failures within 240 seconds from a given IP, ssh will be blocked from the same IP.
            This code handles the error.
            Manual fix:
                /data/bin/heimdall_svc -r ipblockd; /etc/rc.d/syslogd restart;
        '''
        start = time.time()
        SLEEP_INTERVAL = 30
        while (time.time() - start) < int(timeout):
            try:
                self._info('Trying to get cli...')
                admin_password = Misc(None, None).get_admin_password(self.dut)
                cli = shell.get_shell(self.dut, 'admin', admin_password)
            except:
                import traceback
                self._debug(traceback.print_exc())
                self._info('Failed to get cli. Sleeping %s seconds' % SLEEP_INTERVAL)
                time.sleep(SLEEP_INTERVAL)
            else:
                self._info('Cli ready check passed')
                cli.close()
                break
        else:
            self._warn('Cli was not ready in %s seconds' % timeout)

    def wait_until_dut_reboots(self, timeout=480, wait_for_ports=None):
        """ Wait until DUT machine reboots and ssh comes up.

        Parameters:
            - `timeout`: time to wait for reboot (default 360 sec)
            - `wait_for_ports`: string of comma separated pairs
              [interface:]port. If interface is skip then Management interface
              is used.

        Examples:
        | Wait until DUT Reboots |
        | Wait until DUT Reboots | timeout=300 |
        | Wait until DUT Reboots | wait_for_ports=22, ${DUT_P1}:3128 |
        """
        # value can be string when came from RobotFramwork
        timeout = int(timeout)

        # Give DUT some time for shutdown
        time.sleep(5)

        try:
            start = time.time()
            self._info('Wait for dut to come up...')
            sal.net.ping.wait_for_reboot(self.dut, timeout=timeout)
            self._info('Dut is online.')

            self._info('Wait for ssh to come up...')
            sal.net.socket.wait_for_port(self.dut, 22, timeout=timeout)

            self._info('Wait for cli to be ready...')
            self._wait_for_cli(timeout=timeout)

            self._info('Resetting the DUT shell...')
            self.start_shell_session()

            if wait_for_ports is not None:
                self._wait_for_ports(wait_for_ports, timeout)

            # DUT may lose root access after upgrade in RfS mode
            # So, let's restore it
            # self.restore_root_access()

            elapsed = time.time() - start
            self._info('Rebooting completed successfully in %ss.' % str(elapsed))
            # Misc(self.dut, self.dut_version).wait_until_ready(timeout)
        except (sal.net.ping.PingError, TimeoutError), e:
            self._info('After rebooting [%s] was not reached in [%s] sec!' % \
                       (self.dut, timeout))
            raise RebootError, e

    def wait_until_dut_is_accessible(self, timeout=480, wait_for_ports=None):
        """ Wait until DUT machine is accessible.

        Parameters:
            - `timeout`: time to wait for reboot (default 360 sec)
            - `wait_for_ports`: string of comma separated pairs
              [interface:]port. If interface is skip then Management interface
              is used.

        Examples:
        | Wait until DUT Is Accessible |
        | Wait until DUT Is Accessible | timeout=300 |
        | Wait until DUT Is Accessible | wait_for_ports=22, ${DUT_P1}:3128 |
        """
        # value can be string when came from RobotFramwork
        timeout = int(timeout)
        try:
            start = time.time()

            self._info('Wait for ssh to come up...')
            sal.net.socket.wait_for_port(self.dut, 22, timeout=timeout)

            self._info('Wait for cli to be ready...')
            self._wait_for_cli(timeout=timeout)

            self._info('Resetting the DUT shell...')
            self.start_shell_session()

            if wait_for_ports is not None:
                self._wait_for_ports(wait_for_ports, timeout)

            elapsed = time.time() - start
            self._info('DUT accessed successfully in %ss.' % str(elapsed))
            Misc(self.dut, self.dut_version).wait_until_ready(timeout)
        except (sal.net.ping.PingError, TimeoutError), e:
            self._info('DUT [%s] could not be reached in [%s] sec!' % \
                       (self.dut, timeout))
            raise NoAccessToDutError, e

    def reboot_and_wait(self, wait_for_ports=None):
        """ Reboot a DUT machine and wait for ssh to come up.

        Parameters:
            - `wait_for_ports`: string of comma separated pairs
              [interface:]port. If interface is skip then Management interface
              is used.

        Examples:
        | Reboot and Wait |
        | Reboot and Wait | wait_for_ports=8080, ${DUT_P1}:3128 |
        """
        self._info('Rebooting %s.' % (self.dut))
        self._get_cli().reboot()
        self.wait_until_dut_reboots(timeout=360, wait_for_ports=wait_for_ports)

    def upgrade_and_wait(self, build, timeout=360, wait_for_ports=None, downloadonly='n'):
        """ Upgrade to a given version and wait for ssh to some up after reboot.

        Parameters:
            - `build`: build to upgrade to.
            Should be in format N.X.Y-ZZZ (i.e., 4.7.0-142)
            - `timeout`: time to wait for reboot (default 360 sec)
            - `wait_for_ports`: string of comma separated pairs
              [interface:]port. If interface is skip then Management interface
              is used.

        Examples:
        | Upgrade and Wait | 7.5.0-270 |
        | Upgrade and Wait | 7.5.0-270 | timeout=600 |
        | Upgrade and Wait | 7.5.0-270 | wait_for_ports=8080, ${DUT_P1}:3128 |
        """
        # Upgrade to the given build.
        self._get_cli().upgrade().downloadinstall(build)

        try:
            self.wait_until_dut_reboots(timeout, wait_for_ports)
        except RebootError, e:
            raise UpgradeError, e

    def shutdown_cycle(self, seconds=0, poweroff_timeout=90, wait_for_ports=None):
        """Shutdowns and then starts the DUT using IPMI or VSphere.

        Parameters:
            - `seconds`: timeout before shutdown starts
            - `poweroff_timeout`: timeout to wait for power off (default 90s)

        Examples:
        | Shutdown Cycle |
        | Shutdown Cycle | seconds=10 | poweroff_timeout=100 |
        """
        self._info('Shutting down the DUT...')
        self._get_cli().shutdown(int(seconds))
        self._get_psc().power_on(600, int(poweroff_timeout))

        self.wait_until_dut_reboots(timeout=360, wait_for_ports=wait_for_ports)

    def reset_cycle(self, wait_for_ports=None):
        """Resets DUT using IPMI or VSphere.

        Examples:
        | Reset Cycle |
        """
        self._get_psc().reset(15)

        self.wait_until_dut_reboots(timeout=360, wait_for_ports=wait_for_ports)

    def set_boot_device_to_pxe(self):
        """Sets boot device of DUT to pxe using IPMI.

        Examples:
        | Set Boot Device to PXE |
        """
        self._get_psc().set_pxe_boot_device()

    def kill_proc(self, name, sig_name='KILL'):
        """ Kill specified by name processes on a DUT.

        Parameters:
            - `name`: part of or full name of process to send signal to.
            Processes will be searched using command:

            'ps axww | grep `name` | grep -v grep'

            - `sig_name`: signal to be send to the precess. KILL is used by
              default.

        Return:
                List of processes being killed

        Examples:
        | Kill Proc | updaterd |
        | ${hup_proc} = | Kill Proc | webroot | sig_name=HUP |
        """
        self._info('Killing %s...' % name)
        send_cmd = self._shell.send_cmd
        cmd_ps = 'ps axww | grep %s | grep -v grep' % name
        cmd_ps_out = send_cmd(cmd_ps)
        if not cmd_ps_out:
            return []  # No process to kill.
        res = []
        for line in cmd_ps_out.splitlines():
            pid = line.split()[0]
            out_kill = send_cmd('kill -s %s %s' % (sig_name, pid))
            if not out_kill:
                self._info('PID:%s killed.' % (pid,))
                res.append(pid)
            else:
                self._info('PID:%s: no such process.' % (pid,))
        return res

    def _restore_box_network_via_ipmi(self, timeout=300):
        SLEEP_INTERVAL = 10

        internal_exception = ''
        tmr = sal.time.CountDownTimer(timeout).start()
        while tmr.is_active():
            # get access to the IPMI SOL
            try:
                ipmi_cli = self._get_cli(transport='ipmi')
                try:
                    self._setup_network(cli=ipmi_cli)
                    break
                finally:
                    ipmi_cli.close()
                    del ipmi_cli
            except Exception as e:
                internal_exception = e
            time.sleep(SLEEP_INTERVAL)
        else:
            raise TimeoutError('Failed to setup management interface via IMPI SOL'
                               ' within the %d minutes interval.\nInternal exception:' \
                               ' %s' % (timeout / 60, internal_exception,))

    def restore_network_settings(self, RfS=True):
        """Restore following network settings using IPMI SOL
        if necessary (and if IPMI SOL is present on host)
        - IP and Netmask of the Management interface
        - Default Gateway
        - DNS server

        Parameters:
            - `RfS`: specifies whether DUT is after netinstall in Release for
              Shipping mode. Either True or False and True is used by default.

              If DUT is netinstalled in Release for Shipping mode then wait
              until it is rebooted and eventually turned off after that turn on
              it using IPMI or VSphere and restore network settings.

        Examples:
        | Netinstall | build_id_regex=coeus-7-5-0-270 | preconfigure=Shipping |
        | Restore Network Settings | RfS=${True} |
        """
        # if machine is netinstalled in Release for Shipping mode
        # then wait until it is rebooted and then eventually turned off
        # after that turn on it
        if RfS:
            self._rfs = True
            self._info('Wait for RfS installed')
            sal.net.ping.wait_until_not_reachable(self.dut, 600)
            self._get_psc().power_on(300, 1500)

        # Virtual machines should properly get IP over DHCP,
        # so this is needed ONLY for hardware appliances
        # with IPMI 2.0 controllers (no luck without IPMI)
        if not sal.net.socket.check_port(self.dut, 22):
            self._info('self._restore_box_network_via_ipmi')
            try:
                self._restore_box_network_via_ipmi(300)
            except TimeoutError as e:
                ## Catch exception if IPMI is not enabled for DUT or
                ## IPMI interface is down
                self._info('====================================================')
                self._info('==  ERROR: Could NOT reach DUT\'s IPMI interface  ==')
                self._info('====================================================')
                raise e;
            except:
                raise

        self._info('Wait for ssh to come up...')
        sal.net.socket.wait_for_port(self.dut, 22, 300)

        self._info('Resetting the DUT shell...')
        self.restore_root_access()
        self.start_shell_session()

    def install_qa_backdoor(self, qa_backdoor_loc=None):
        """
        Install QA backdoor utility on DUT. This operation is required after
        netinstalling the DUT in Release for Shipping mode to restore access to
        QA backdoor: http://dut_hostname:8123

        Parameters:
            - `qa_backdoor_loc`: location on the DUT where qabackdoor.sh file
              will be copied. When None the default location is used:
              `/data/etc/rc.d/qabackdoor.sh`

        Examples:
        | Install QA Backdoor |
        | Install QA Bachdoor | qa_backdoor_loc=/data/etc/qabackdoor.sh |
        """
        qa_backdoor_loc = qa_backdoor_loc or \
                          '/data/etc/rc.d/qabackdoor.sh'
        hostname = self.dut
        # get the backdoor script from the location

        self.restore_root_access()
        # copy the script to the box
        sal.net.sshlib.scp(dst='%s@%s:%s' % (
            irontools.get_ruser(),
            hostname,
            qa_backdoor_loc,
        ),
                           src=os.path.join(self._get_testdata_dir(),
                                            'qabackdoor.sh'),
                           )

        # start the qabackdoor
        ssh = sal.net.sshlib.get_ssh(host=hostname, user=irontools.get_ruser())
        try:
            command = 'sh %s start' % qa_backdoor_loc
            ssh.writeln(command)
            ssh.wait_for_prompt(10)
            sal.net.socket.wait_for_port(self.dut, 8123, 120)
            self._info('QA backdoor is successfully installed on %s ' \
                       'and running' % (self.dut,))
        finally:
            ssh.close()

    def restore_root_access(self):
        """Restore rtestuser account (For example,
        after netinstall in RfS mode)
        """
        CliKeywordBase(self.dut, self.dut_version).start_cli_session_if_not_open()
        try:
            ssh = sal.net.sshlib.get_ssh(host=self.dut, user=irontools.get_ruser())
            try:
                ssh.writeln('uname')
            finally:
                ssh.close()
        except Exception as e:
            self._info('Root access is denied on %s\n%s\nRestoring...' % \
                       (self.dut, str(e)))
            cli = self._get_cli()
            status = cli.techsupport().status()
            if status.find('currently disabled') == -1:
                # sometimes it is necessary to reenable this
                # to get root access (?bug)
                cli.techsupport().disable(confirm=YES)
            cli.techsupport().sshaccess(tmp_pwd='Cisco123456789', confirm=YES,
                                        password_option='user_input')

    def restore_machine(self):
        """Restore DUT machine after different emergencies:
        - Turn it on if it is turned off (only if the machine has IMPI interface)
        - Restore network connectivity if machine was installed into
          Release for Shipping mode (only if the machine has IMPI interface)
        - Install QA backdoor if it not installed
        - Restart cli and shell sessions

        After using this keyword your DUT machine will be ready for running
        SARF test scripts.

        Example:
        | Restore Machine |
        """
        self._info('Checking for network connectivity on port 22')
        if not sal.net.socket.check_port(self.dut, 22):
            self._info('Checking whether %s is powered on' % \
                       (self.dut,))
            self._get_psc().power_on(300, 20)

            self._info("%s machine is not available via SSH. " \
                       "Restoring network connectivity" % self.dut)
            self.restore_network_settings(RfS=False)
        else:
            self._info('Checking for network connectivity on port 22')
            sal.net.socket.wait_for_port(self.dut, 22, 300)

        self._info('Checking for root access')
        self.restore_root_access()

        self._info('Checking for QA backdoor presence')
        if not sal.net.socket.check_port(self.dut, 8123):
            self._info("QA backdoor is not available on %s machine. " \
                       "Installing QA backdoor" % self.dut)
            self.install_qa_backdoor()

        self._info('Starting shell and cli sessions')
        self.start_shell_session()
        CliKeywordBase(self.dut, self.dut_version).start_cli_session()

    def _parse_version_command_output(self, output):
        """Parses the version cli command output
        and caches all parsed vars into object variables:
        dut_version, dut_model and dut_serial.
        Returns dictionary whose keys are var names without
        'dut_' prefix and corresponding parsed values
        """
        PATTERNS = {'version': r'Version: *([\d\.\-]+)',
                    'model': r'Model: *([\w]+)',
                    'serial': r'Serial #: *([\w\-]+)'}
        results = {}
        # First trying old format of version
        if not isinstance(output, basestring):
            for attr_name in PATTERNS.iterkeys():
                if hasattr(output, attr_name):
                    results[attr_name] = getattr(output, attr_name)
        # If old format fails parsing from new format
        if not results:
            for attr_name, pattern in PATTERNS.iteritems():
                match = re.search(pattern, output)
                if match:
                    results[attr_name] = match.group(1)
        if len(results) == len(PATTERNS):
            # Cache all parsed params into current object
            # since the DUT model and serial are constant
            # within the whole test
            for attr_name, value in results.iteritems():
                if not hasattr(self, 'dut_%s' % (attr_name,)):
                    setattr(self, 'dut_%s' % (attr_name,), value)
            return results
        else:
            raise AssertionError('Failed to parse %s from version command ' \
                                 'output:\n%s' % (pattern, output))

    def get_dut_build(self):
        """
        Return full build number that is installed on the DUT.

        Examples:
        | ${build} = | Get DUT Build |
        """
        dut_build_version = None
        try:
            versionoutput = self._get_cli().version()
            dut_build_version = self._parse_version_command_output(versionoutput)['version']
            if dut_build_version is None:
                raise Exception("get_dut_build() | Exception: Failed to read"
                                " the version from the DUT")
        except Exception as e:
            self._info(
                "get_dut_build() | Exception: Failed to read the version from the DUT | return [dut_build_version]: %s" % str(
                    dut_build_version))
        return dut_build_version

    def _get_dut_model(self):
        """
        Returns Model type of the DUT
        """
        if not hasattr(self, 'dut_model'):
            self.get_dut_build()
        return self.dut_model

    def _get_dut_serial(self):
        """
        Returns Serial # of the DUT
        """
        if not hasattr(self, 'dut_serial'):
            self.get_dut_build()
        return self.dut_serial

    def _get_lib_path(self, cli=None):
        """Returns appliance automation libs prefix
        for the current appliance version in format
        <greek_appliance_name><major_version_number>
        """
        GREEK_DUT_NAMES_MAP = {'S': 'coeus',
                               'C': 'phoebe', 'X': 'phoebe',
                               'M': 'zeus'}
        if cli is None:
            cli = self._get_cli()
        versionoutput = cli.version()
        build = self._parse_version_command_output(versionoutput)['version']
        greek_dut_name = GREEK_DUT_NAMES_MAP[self._get_dut_model()[0]]
        label = greek_dut_name + build.replace('.', '').replace('-', '')[:5]
        libs = os.listdir(os.path.join(os.environ['SARF_HOME'], 'testlib'))
        if label in libs:
            return label
        elif label[:-1] in libs:
            return label[:-1]
        elif label[:-2] in libs:
            return label[:-2]
        elif label[:-3] in libs:
            return label[:-3]
        else:
            raise RuntimeError, 'Library not available for %s' % (label)

    def _is_dut_a_virtual_model(self):
        """
        Returns True if a virtual Model(i.e if S000V,S100V,S300V,S600V) else False
        """
        OLD_VIRTUAL_MODELS = ('C801', 'C802', 'C804', 'C808', 'S10',)
        model = self._get_dut_model()
        is_virtual = (model in OLD_VIRTUAL_MODELS) or (model[-1] == 'V')
        self._info('Is %s (%s) a virtual model: %s' % \
                   (self.dut, model, is_virtual))
        return is_virtual

    # symlink: publishes method and saves backward compatibility
    is_virtual_model = _is_dut_a_virtual_model

    def sync_time(self, maxoffset=600):
        """
        Checks the DUT's time compared to the local machine.
        If it's off by more than max offset, set the DUT to the
        test runner's system time

        Examples:
        | Sync Time |
        """
        cli = self._get_cli()
        dut_status = cli.status()
        dut_time_str = dut_status.get_system('status_as_of')
        format = '%a %b %d %H:%M:%S %Y %Z'
        dut_time = time.mktime(time.strptime(dut_time_str, format))
        mytime = time.time()
        time_diff = abs(mytime - dut_time)
        if time_diff <= maxoffset:
            self._info \
                ("System time matches RF test-runner to %d seconds" % time_diff)
            return False
        # assumes test runner's host is correct local time
        self._info \
            ("Setting the system time to current time (off by %d sec)." % time_diff)
        cli.settime(timeval=time.localtime())
        cli.commit()
        return True

    def shift_time(self, seconds=None):
        """Shift time on DUT

        Parameters:
            - `seconds`: number of shifting seconds

        Examples:
        | Shift Time | 3600 |
        | Shift Time | -3600 |
        """
        self._info('Fetching current time from DUT...')
        cli = self._get_cli()
        time_str = cli.settime()

        self._info('Shifting time on %s seconds...' % seconds)
        tmr = sal.time.MutableTime()
        tmr = tmr.get_mutable(time_str)
        tmr.add_seconds(int(seconds))
        time_str = cli.settime(tmr.strftime('%m/%d/%Y %H:%M:%S'))
