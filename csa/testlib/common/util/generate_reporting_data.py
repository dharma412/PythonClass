#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/generate_reporting_data.py#2 $
# $DateTime: 2019/06/11 06:52:26 $
# $Author: revlaksh $

import time
import re
import os

import sal.time
import subprocess as sub
import socket
from common.util.utilcommon import UtilCommon
from sal.clients import smtp, smtpspam
from common.shell import shell
from SSHLibrary import SSHLibrary
from common.shell import paths

import common.Variables

SEARCH_FROM_START = 'start'
SEARCH_FROM_LAST = 'last'


class GenerateReportingData(UtilCommon):
    """
    Keywords for Generating Data for Email or Web reports
    """

    def get_keyword_names(self):
        return [
            'get_appliance_time',
            'inject_mbox_msgs',
            'inject_raw_msg',
            'make_requests',
            'generate_l4tm_data',
            'wait_for_email_data_download',
            'wait_for_web_data_download',
        ]

    def inject_mbox_msgs(self, listener=None, num_msgs=None, mbox_file=None,
                         rcpt_host_list=None):
        """Injects mbox messages to ESA machine.

        Parameters:
            - `listener`: Interface for SMTP.
            - `num_msgs`: number of messages to inject
            - `mbox_file`: fulll path to mbox file.
            - `rcpt_host_list`: List of hosts (separated by comma) to \
            address mail to.

        Examples:
        | Inject Mbox Msgs |
        | ... | listener=d1.esx-2710-r209s03-esa04.auto |
        | ... | num_msgs=5 |
        | ... | mbox_file=${SARF_HOME}/tests/testdata/antispam/spam.mbox |
        | ... | rcpt_host_list=${SMA} |
        """
        self._info('Sending %s %s messages to %s via %s' % \
                   (num_msgs, mbox_file, rcpt_host_list, listener))

        smtp_spam = smtpspam.SmtpSpam()
        smtp_spam.start(
            inject_host=listener,
            rcpt_host_list=rcpt_host_list,
            num_msgs=num_msgs,
            mbox_filename=mbox_file,
        )
        smtp_spam.wait()

    def inject_raw_msg(self, listener=None, payload=None, rcpt_to=None,
                       mail_from=None, num_msgs=1):
        """Injects raw messages to ESA machine.

        Parameters:
            - `listener`: Interface for SMTP.
            - `payload`: message content
            - `rcpt_to`: email address for To field.
            - `mail_from`: email address for From field.
            - `num_msgs`: number of messages. Default to 1.

        Examples:
        | Inject Raw Msg |
        | ... | listener=d1.esx-2710-r209s03-esa04.auto |
        | ... | payload=Subject: DLP\r\n |
        | ... | rcpt_to=to@ironport.com |
        | ... | mail_from=from@ironport.com |
        | ... | num_msgs=2 |
        """
        for i in xrange(int(num_msgs)):
            smtp.inject(listener, payload, rcpt_to, mail_from)

    def make_requests(self, proxy=None, proxy_type=None, url=None, qty=1, \
                      proxy_user=None, remote_client=None, timeout=60):
        """Makes requests for WSA machine.

        Parameters:
            - `proxy`: Interface for Web proxy with port specified after colon.
            - `proxy_type`: Which proxy type to use. Can be:
            None (default value) or 'http' to use regular proxy
            'socks5' - to use SOCKS proxy (introduced in zeus80)
            'socks5-hostname' - to use SOCKS proxy (introduced in zeus80) with \
            host name
            resolving by proxy.
            - `proxy_user`: String of user and password for authentication of \
            the proxy (with format 'user:password').
            - `url`: URL of a web site (a recepient of requests).
            - `qty`: number of requests for the url.
            - `remote_client`: Remote host from which request should be sent.
            The parameter should be specifed in format: hostname:username:password.
            If it is skipped, data is sent from current machine.

        Examples:
        | Make Requests |
        | ... | proxy=esx-2710-r209s03-wsa02.auto:80 |
        | ... | proxy_user=rtester:raptortester |
        | ... | url=http://services.wga |
        | ... | qty=10 |

        | Make Requests |
        | ... | proxy=esx-2710-r209s03-wsa02.auto:1080 |
        | ... | proxy_type=socks5-hostname |
        | ... | proxy_user=rtester:raptortester |
        | ... | url=http://services.wga |
        | ... | qty=2 |

        """
        if url is None:
            raise ValueError("URL was not specified for Make Request.")

        ssh_session = None
        if remote_client is not None:
            # setup SSH session if requests should be sent from remote host
            client_data = remote_client.split(':')
            if len(client_data) < 3:
                raise ValueError("Remote client should be indicated with " + \
                                 "format: hostname:username:password")
            ssh_session = SSHLibrary()
            ssh_session.open_connection(client_data[0], timeout=60)
            ssh_session.login(client_data[1], client_data[2])
            ssh_session.set_client_configuration(prompt='$')

        proxy_option = '--proxy'
        if proxy_type is not None:
            if proxy_type in ('socks5', 'socks5-hostname'):
                proxy_option = '--' + proxy_type
        _ipv_param = '-4'
        variables = common.Variables.get_variables()
        if variables.has_key("${IPV_PARAM}"):
            _ipv_param = variables["${IPV_PARAM}"]
        if proxy_user is None:
            _cmd_input = 'curl %s -s -D - %s %s --url %s -o /dev/null' % \
                         (_ipv_param, proxy_option, proxy, url)
        else:
            _cmd_input = \
                'curl %s -s -D - %s %s --proxy-user %s --url %s -o /dev/null' \
                % (_ipv_param, proxy_option, proxy, proxy_user, url)

        self._info('Making %s requests to %s' % (qty, url))
        for i in range(int(qty)):
            self._debug("Sending command: %s" % (_cmd_input))
            if ssh_session is None:
                p = sub.Popen(_cmd_input, shell=True, stdout=sub.PIPE,
                              stderr=sub.PIPE)
                output, errors = p.communicate()
                self._debug("Output: %s" % output)
                self._debug("Errors: %s" % errors)
                if errors.find("curl:") >= 0:
                    raise RuntimeError, errors
            else:
                ssh_session.write(_cmd_input)
                out = ssh_session.read_until_prompt()
                self._debug("Out: %s" % out)
                if out.find("curl:") >= 0:
                    raise RuntimeError, out

        if ssh_session is not None:
            ssh_session.close_connection()

    def generate_l4tm_data(self, wsa_dut=None, client=None, destination=None,
                           port=None, action='MONITORED', qty=1):
        """Generates L4TM data for WSA machine by writing data in the database.

        Parameters:
            - `wsa_dut`: Host name of WSA machine.
            - `client`: Client IP or name.
            - `destination`: Web site or IP address.
            - `port`: Port number.
            - `action`: Action of simulated request. Either 'MONITORED' or \
            'BLOCKED'.
            'MONITORED' by default.
            - `qty`: number of simulated requests. 1 by default

        Examples:
        | Generate L4TM Data |
        | ... | wsa_dut=esx-2710-r209s03-wsa02.auto |
        | ... | rate=10 |
        | ... | block_rate=1.0 |
        """
        action = action.upper()
        if action not in ['MONITORED', 'BLOCKED']:
            raise ValueError("action can be only 'MONITORED' or 'BLOCKED'.")
        app_name = 'coeuslogd'
        backdoor_code = (
            "import qlog",
            "qlog_args = ['%s','%s',%s]" % \
            (client, destination, port),
        )

        for i in range(int(qty)):
            backdoor_code += \
                ("qlog.write('WEB.TRAFFIC_MONITOR_%s', *qlog_args)" % action,)

        wsa_shell = shell.get_shell(wsa_dut)
        wsa_shell.backdoor.run(app_name, backdoor_code)
        self._debug("app_name=%s" % (app_name,))
        self._debug("backdoor_code=%s" % (backdoor_code,))

    def generate_l4tm_random_data(self, wsa_dut=None, rate='10', block_rate='0.5',
                                  sample_size='2', timeout=60):
        """Generates L4TM data for WSA machine.

        Parameters:
            - `wsa_dut`: Host name of WSA machine.
            - `rate`: Default to 10.
            - `block_rate`: rate for blocking. 0.0 mean monitoring.
            1.0 means blocking. Default to 0.5.
            - `sample_size`: Size of sample data. Default to 2.
            - `timeout`: timeout for generator. Default to 60 seconds.

        Examples:
        | Generate L4TM Data |
        | ... | wsa_dut=esx-2710-r209s03-wsa02.auto |
        | ... | rate=10 |
        | ... | block_rate=1.0 |
        """
        app_name = 'coeuslogd'
        backdoor_code = (
            'import coro',
            'coro.spawn(coeuslog.coeus_reporting.generate_l4tm_reporting,' \
            'coeuslog.config.coeusReportingRPCServerSockPath, %s, %s, %s)' % \
            (rate, block_rate, sample_size),
        )

        wsa_shell = shell.get_shell(wsa_dut)
        wsa_shell.backdoor.run(app_name, backdoor_code)
        self._info('Delaying for %s seconds' % (timeout,))
        timer = sal.time.CountDownTimer(timeout).start()
        while timer.is_active():
            time.sleep(timeout / 10)

        self._info('Restarting %s' % (app_name,))
        wsa_shell.heimdall.restart(app_name)

    def _get_version_values(self, hostname):
        """Returns dictionary of values, provided by `version` CLI command."""
        ssh_session = SSHLibrary()
        ssh_session.open_connection(hostname, timeout=60)
        ssh_session.login('admin', 'Cisco12$')
        ssh_session.start_command('version')
        out = ssh_session.read_command_output()
        ssh_session.close_connection()
        version_dict = {}
        for line in out.splitlines():
            if len(line) > 0:
                pair = line.split(":", 1)
                if len(pair) > 1:
                    version_dict[pair[0].strip()] = pair[1].strip()
                else:
                    version_dict[pair[0].strip()] = None
        return version_dict

    def get_appliance_time(self, hostname):
        """Get appliance current time.

        Parameters:
            - `hostname`: Host name of an appliance.

        Return:
            String with appliance time in format
            %Y-%m-%d %H:%M:%S (like "2012-04-02 14:13:00")

        Examples:
        | ${start_time}= | Get Appliance Time |
        | ... | c650-01.auto |
        """

        # Getting current time of WSA machine
        start_time = None

        ssh_session = SSHLibrary()
        ssh_session.open_connection(hostname, timeout=60)
        ssh_session.login('admin', 'Cisco12$')
        ssh_session.start_command('status')
        out = ssh_session.read_command_output()
        ssh_session.close_connection()

        match = re.search("([^\ ]+\ [^\ ]+\ \d+\ \d+\:\d+\:\d+\ \d+)", out)
        if match is not None:
            re_groups = match.groups()
            if re_groups is not None:
                start_time = time.strptime(re_groups[0], "%a %b %d %H:%M:%S %Y")
                start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_time)
                self._debug("Appliance time: %s" % start_time)
                return start_time

        return start_time

    def _get_log_line_time(self, log_line):
        """Returns datetime (seconds from epoch) for specified log line."""

        match = re.search("(\w+\s+\d+\s+\d+:\d+:\d+\s+\d+)", log_line)
        self._debug("match: %s" % match)
        if match is None:
            return None

        re_groups = match.groups()
        self._debug("re_groups[0]: %s" % re_groups[0])
        if re_groups[0] is None:
            return None

        _archive_time = time.strptime(re_groups[0], "%b %d %H:%M:%S %Y")
        _archive_time = time.mktime(_archive_time)
        self._debug("_archive_time: %s" % _archive_time)
        return _archive_time

    def _wait_for_pattern_in_log(self, sma_shell, filename, search_patt, \
                                 start_time, timeout):
        """
            Wait for search_patt pattern in a log.
            None is returned if pattern was not found.
            Number of seconds from epoch is returned, if pattern was found.
        """
        _short_interval = 60
        _timer_start = time.time()
        while (time.time() - _timer_start) < timeout:
            result = sma_shell.logreader.search(
                search_patt,
                filename=filename,
                timeout=1,
                skip_hashed=False
            )
            if result.match_qty == 0:
                time.sleep(_short_interval)
                continue

            self._debug("found_lines: %s" % result.found_lines)

            last_line = result.found_lines[-1]
            self._debug("last_line: %s" % last_line)

            archive_time = self._get_log_line_time(last_line)

            self._debug("archive_time: %s" % archive_time)
            self._debug("start_time: %s" % start_time)

            if int(archive_time - start_time) >= 0:
                self._info('Found %s in %s log' % (search_patt, filename))
                return archive_time

            time.sleep(_short_interval)

        return None

    def wait_for_email_data_download(self, sma_dut=None, esa_appliances=None, \
                                     start_time=None, timeout=1800):
        """Wait for downloading data from ESA appliance to SMA.

        Parameters:
            - `sma_dut`: Host name of SMA machine.
            - `esa_appliances`: String of comma-separated list of
              esa_appliances.
            - `start_time`: timestamp to start log parcing.
            It should have format: '2012-03-13 15:08:31'.
            By defaut parsing begins from logging start time.
            - `timeout`: timeout for generator. Default to 1800 seconds.

        Examples:
        | Wait For Email Data Download |
        | ... | c650-01.auto |
        | ... | esx-2710-r209s03-esa04.auto |
        | ${start_time}= | Get Time |
        | Wait For Email Data Download |
        | ... | c650-01.auto |
        | ... | esx-2710-r209s03-esa04.auto |
        | ... | start_time=${start_time} |
        | ... | timeout=3600 |
        """
        timeout = int(timeout)
        if sma_dut is None:
            sma_shell = self._shell
            sma_dut = self.dut
        else:
            sma_shell = shell.get_shell(sma_dut)

        self._debug("SMA DUT: %s" % sma_dut)

        requesting_delta = 0
        if start_time is None:
            start_time = self.get_appliance_time(sma_dut)
            requesting_delta = 360
        self._debug("Start time: %s" % start_time)
        start_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_time_int = time.mktime(start_time) - requesting_delta

        self._info('Waiting for data transfer')
        smad_log = sma_shell.paths.user_logs.smad
        patterns = (
            'TRANSFER: Plugin TRACKINGPLUGIN downloading from (%s|%s)',
            'TRANSFER: Plugin REPORTINGPLUGIN downloading from (%s|%s)'
        )
        for pattern in patterns:
            for esa_hostname in esa_appliances.split(','):
                esa_ip = socket.gethostbyname(esa_hostname.strip())

                search_patt = pattern % (esa_ip, esa_hostname)
                pattern_datetime = self._wait_for_pattern_in_log(sma_shell, \
                                                                 smad_log, search_patt, start_time_int, timeout)

                if pattern_datetime is None:
                    raise RuntimeError, "'%s' was not found in smad logs" % \
                                        (search_patt,)

        self._info('Waiting for archives aggregation')
        reportd_log = sma_shell.paths.user_logs.reportd
        for esa_hostname in esa_appliances.split(','):
            esa_hostname = esa_hostname.strip()
            _version_dict = self._get_version_values(esa_hostname)
            esa_serial = _version_dict['Serial #']
            esa_version = _version_dict['Version']
            version_number = int(esa_version[0:3].replace('.', ''))

            if version_number < 80:
                search_patt = 'Completed aggregating archive.*?%s' % (esa_serial,)
            else:
                search_patt = 'Completed processing all the export files'

            pattern_datetime = self._wait_for_pattern_in_log(sma_shell, \
                                                             reportd_log, search_patt, start_time_int, timeout)

            if pattern_datetime is None:
                raise RuntimeError, 'No %s was found in reportd' % (search_patt,)

    def wait_for_web_data_download(self, sma_dut=None, wsa_appliances=None, \
                                   start_time=None, timeout=1800):
        """Wait for downloading data from WSA appliance to SMA.

        Parameters:
            - `sma_dut`: Host name of SMA machine.
            - `wsa_appliances`: String of comma-separated list of
              wsa_appliances.
            - `start_time`: timestamp to start log parcing.
            It should have format: '2012-03-13 15:08:31'.
            By defaut parsing begins from logging start time.
            - `timeout`: timeout for generator. Default to 1800 seconds.

        Examples:
        | Wait For Web Data Download |
        | ... | c650-01.auto |
        | ... | esx-2710-r209s03-wsa02.auto |
        | ${start_time}= | Get Time |
        | Wait For Web Data Download |
        | ... | c650-01.auto |
        | ... | esx-2710-r209s03-wsa02.auto |
        | ... | start_time=${start_time} |
        | ... | timeout=3600 |
        """
        timeout = int(timeout)
        _keyword_start = time.time()

        if sma_dut is None:
            sma_shell = self._shell
            sma_dut = self.dut
        else:
            sma_shell = shell.get_shell(sma_dut)

        self._debug("SMA DUT: %s" % sma_dut)

        requesting_delta = 0
        if start_time is None:
            start_time = self.get_appliance_time(sma_dut)
            requesting_delta = 360
        self._debug("Start time: %s" % start_time)
        start_time = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_time_int = time.mktime(start_time) - requesting_delta

        self._info('Waiting for data transfer')

        patterns_to_search = []
        coeus_version_dict = {
            '7.5': Coeus75PatternsHolder,
            '7.7': Coeus77PatternsHolder,
            '8.0': Coeus80PatternsHolder,
            '11.5': Coeus115PatternsHolder
        }

        for wsa_hostname in wsa_appliances.split(','):
            wsa_hostname = wsa_hostname.strip()
            wsa_ip = socket.gethostbyname(wsa_hostname.strip())
            _version_dict = self._get_version_values(wsa_hostname)
            wsa_version = _version_dict['Version']
            self._debug("WSA Version: %s" % wsa_version)
            wsa_serial = _version_dict['Serial #']
            self._debug("WSA Serial: %s" % wsa_serial)

            try:
                holder = coeus_version_dict[wsa_version[0:4]]
            except KeyError:
                holder = CoeusPatternsHolder
            patterns_to_search += holder(ip=wsa_ip,
                                         hostname=wsa_hostname,
                                         serial=wsa_serial
                                         ).get_all_patterns()

        pattern_datetime = None
        for (log, search_patt, search_from) in patterns_to_search:
            _time_spent = time.time() - _keyword_start
            if pattern_datetime is not None and search_from == SEARCH_FROM_LAST:
                start_time = pattern_datetime
            else:
                start_time = start_time_int
            self._debug("Searching string '%s' in %s log for %s seconds max" \
                        % (search_patt, log, timeout - _time_spent))
            pattern_datetime = self._wait_for_pattern_in_log(sma_shell, log, \
                                                             search_patt, start_time, timeout - _time_spent)
            if pattern_datetime is None:
                _time_spent = time.time() - _keyword_start
                raise RuntimeError, \
                    "'%s' was not found in %s log after %s seconds." % \
                    (search_patt, log, _time_spent)


class CoeusPatternsHolder(object):
    def __init__(self, ip, hostname, serial):
        self._ip = ip
        self._hostname = hostname
        self._serial = serial
        self.logs = paths.get_paths().user_logs

    def get_transfer_patterns(self):
        patterns_to_search = []
        search_patt = \
            'TRANSFER: Plugin WEBREPORTINGPLUGIN downloading from (%s|%s) .*webrec.*' \
            % (self._ip, self._hostname)
        patterns_to_search.append((self.logs.smad, search_patt, SEARCH_FROM_START))
        search_patt = \
            'TRANSFER: Plugin REPORTINGPLUGIN downloading from (%s|%s) .*rpx.*' % \
            (self._ip, self._hostname)
        patterns_to_search.append((self.logs.smad, search_patt, SEARCH_FROM_START))
        return patterns_to_search

    def get_merging_patterns(self):
        patterns_to_search = []
        search_patt = 'Merged partition.*%s' % (self._serial,)
        patterns_to_search.append((self.logs.haystackd, search_patt, \
                                   SEARCH_FROM_START))
        return patterns_to_search

    def get_processing_patterns(self):
        patterns_to_search = []
        search_patt = "Completed unpacking imported archive.*%s" % (self._serial,)
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_START))
        search_patt = \
            'Completed aggregating export files .* WEB_SYSTEM_CAPACITY'
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_LAST))
        search_patt = 'Completed processing all the export files'
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_LAST))
        return patterns_to_search

    def get_all_patterns(self):
        patterns_to_search = []
        patterns_to_search += self.get_transfer_patterns()
        patterns_to_search += self.get_merging_patterns()
        patterns_to_search += self.get_processing_patterns()
        return patterns_to_search


class Coeus75PatternsHolder(CoeusPatternsHolder):

    def get_processing_patterns(self):
        patterns_to_search = []
        search_patt = "Completed unpacking imported archive.*%s" % \
                      (self._serial,)
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_START))
        search_patt = \
            'Completed aggregating export files .* WEB_USER_DETAIL'
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_LAST))
        search_patt = 'Completed processing all the export files'
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_LAST))
        return patterns_to_search


class Coeus77PatternsHolder(CoeusPatternsHolder):

    def get_transfer_patterns(self):
        patterns_to_search = []
        search_patt = \
            'TRANSFER: Plugin WEBREPORTINGPLUGIN downloading from (%s|%s)' \
            % (self._ip, self._hostname)
        patterns_to_search.append((self.logs.smad, search_patt, \
                                   SEARCH_FROM_START))
        search_patt = \
            'TRANSFER: Plugin REPORTINGPLUGIN downloading from (%s|%s) .*rpx.*' \
            % (self._ip, self._hostname)
        patterns_to_search.append((self.logs.smad, search_patt, \
                                   SEARCH_FROM_START))
        return patterns_to_search

    def get_processing_patterns(self):
        patterns_to_search = []
        search_patt = "Completed unpacking imported archive.*%s" % (self._serial,)
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_START))
        search_patt = \
            'Completed aggregating export files .* WEB_SYSTEM_CAPACITY'
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_LAST))
        search_patt = 'Completed processing all the export files'
        patterns_to_search.append((self.logs.reportd, search_patt, \
                                   SEARCH_FROM_LAST))
        return patterns_to_search


class Coeus80PatternsHolder(Coeus77PatternsHolder): pass


class Coeus115PatternsHolder(Coeus75PatternsHolder): pass
