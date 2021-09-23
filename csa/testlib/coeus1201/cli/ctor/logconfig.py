#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/logconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
IAF 2 CLI command: logconfig
"""

import re
import traceback

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT

TIMEOUT=10

class logconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('logconfig')
        return self

    def auditlogconfig(self, backups, loadable):
        self.clearbuf()
        try:
            self._query_response('auditlogconfig', timeout=TIMEOUT)
            self._query_response(backups, timeout=TIMEOUT)
            self._query_response(loadable, timeout=TIMEOUT)
            self._to_the_top(1, timeout=TIMEOUT)
            return self.getbuf()
        except:
            self.interrupt()
            traceback.print_exc()
            raise

    def new(self, input_dict=None, **kwargs):
        self._query_response('new')

        param_map = clictorbase.IafCliParamMap( \
            end_of_command='Choose the operation')
        param_map['log_file']      = ['Choose the log file', DEFAULT, 1]
        param_map['name']          = ['name for the log', REQUIRED]
        param_map['log_level']     = ['Log level:', DEFAULT, 1]
        param_map['port']          = ['Port to connect', DEFAULT]
        param_map['retrieval']     = ['method to retrieve the logs', DEFAULT, 1]
        param_map['hostname']      = ['Hostname to deliver', NO_DEFAULT]
        param_map['username']      = ['Username on the remote', NO_DEFAULT]
        param_map['password']      = ['Passphrase for ', NO_DEFAULT]
        param_map['directory']     = ['Directory on remote host', NO_DEFAULT]
        param_map['filename']      = ['Filename to use', DEFAULT]
        param_map['configure_rollover'] = \
            ['time-based log files rollover', DEFAULT]
        param_map['settings']      = ['log rollover settings', DEFAULT, 1]
        param_map['interval']      = ['Enter a number of seconds', DEFAULT]
        param_map['day_of_week']   = ['the day of week to roll over', REQUIRED]
        param_map['time_of_day']   = ['the time of day to rollover', REQUIRED]
        param_map['max_size_poll'] = ['maximum file size', DEFAULT]
        param_map['max_files']     = ['maximum number of files', DEFAULT]
        param_map['max_size_push'] = ['Maximum filesize', DEFAULT]
        param_map['ssh_proto']     = ['Protocol:', DEFAULT, 1]
        param_map['key_checking']  = ['enable host key checking', DEFAULT]
        param_map['ssh_scan'] = \
            ['for its SSH key, or enter it manually', DEFAULT]
        param_map['host_key']    = \
            ['Enter the public SSH host key', REQUIRED]
        param_map['alert_when_rollover_files_removed']    = \
            ['Should an alert be sent when files are removed', DEFAULT]
        param_map['compress']      = ['want to compress logs', DEFAULT]

        # parameters for 4. Access Logs
        param_map['log_style'] = \
            ['Choose the log style for this subscription:', DEFAULT]
        param_map['http_codes'] = \
            ['Enter the HTTP Error Status codes', DEFAULT]

        # parameters for Syslog Push
        param_map['transfer_protocol'] = \
            ['Which protocol do you want to use to transfer the log data?',
            DEFAULT]
        param_map['msg_size'] = \
            ['Maximum message size for syslog push:',
            NO_DEFAULT]
        param_map['facility'] = \
            ['Which facility do you want the log data to be sent as?', DEFAULT]
        param_map['syslog_disk_buffer'] = \
            ['Enable syslog disk buffer', DEFAULT]
        # parameters for 35. Request Debug Logs
        param_map['modules'] = \
            ['Choose modules where enhanced request logging is to be performed',
            DEFAULT]
        param_map['requests'] = \
            ['Please enter the number of requests for which to perform enhanced logging',
            DEFAULT]
        param_map['criteria'] = \
            ['Choose the request criteria for logging:', DEFAULT]
        param_map['ip'] = ['Specify source IP address', REQUIRED]
        param_map['domain'] = ['Specify target domain', DEFAULT]

        # parameters for 48. W3C Logs
        param_map['format_string'] = ['Enter the format string:', DEFAULT]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def edit(self, log_to_edit='1', input_dict=None, **kwargs):
        self._query_response('EDIT')
        buf = self._sess.getbuf(clear_buf=False)
        self._query()
        self._select_list_item(log_to_edit, buf)# no names allowed

        # same param map as for 'new', but with DEFAULT for everything.
        param_map = clictorbase.IafCliParamMap( \
            end_of_command='Choose the operation')
        param_map['log_file']      = ['Choose the log file', DEFAULT, 1]
        param_map['name']          = ['name for the log', DEFAULT]
        param_map['log_level']     = ['Log level:', DEFAULT, 1]
        param_map['retrieval']     = ['method to retrieve the logs', DEFAULT, 1]
        param_map['hostname']      = ['Hostname to deliver', NO_DEFAULT]
        param_map['username']      = ['Username on the remote', NO_DEFAULT]
        param_map['password']      = ['Passphrase for ', NO_DEFAULT]
        param_map['directory']     = ['Directory on remote host', NO_DEFAULT]
        param_map['filename']      = ['Filename to use', DEFAULT]
        param_map['configure_rollover'] = \
            ['time-based log files rollover', DEFAULT]
        param_map['settings']      = ['log rollover settings', DEFAULT, 1]
        param_map['interval']      = ['Enter a number of seconds', DEFAULT]
        param_map['day_of_week']   = ['the day of week to roll over', DEFAULT]
        param_map['time_of_day']   = ['the time of day to rollover', DEFAULT]
        param_map['max_size_poll'] = ['maximum file size', DEFAULT]
        param_map['max_files']     = ['maximum number of files', DEFAULT]
        param_map['max_size_push'] = ['Maximum filesize', DEFAULT]
        param_map['ssh_proto']     = ['Protocol:', DEFAULT, 1]
        param_map['key_checking']  = ['enable host key checking', DEFAULT]
        param_map['ssh_scan'] = \
            ['for its SSH key, or enter it manually', DEFAULT]
        param_map['host_key']    = \
            ['Enter the public SSH host key', DEFAULT]
        param_map['alert_when_rollover_files_removed']    = \
            ['Should an alert be sent when files are removed', DEFAULT]
        param_map['compress']      = ['want to compress logs', DEFAULT]

        # parameters for 4. Access Logs
        param_map['log_style'] = \
            ['Choose the log style for this subscription:', DEFAULT]
        param_map['http_codes'] = \
            ['Enter the HTTP Error Status codes', DEFAULT]

        # parameters for Syslog Push
        param_map['transfer_protocol'] = \
            ['Which protocol do you want to use to transfer the log data?',
            DEFAULT]
        param_map['msg_size'] = \
            ['Maximum message size for syslog push:',
            DEFAULT]
        param_map['facility'] = \
            ['Which facility do you want the log data to be sent as?', DEFAULT]
        param_map['syslog_disk_buffer'] = \
            ['Enable syslog disk buffer', DEFAULT]

        # parameters for 35. Request Debug Logs
        param_map['modules'] = \
            ['Choose modules where enhanced request logging is to be performed',
            DEFAULT]
        param_map['requests'] = \
            ['Please enter the number of requests for which to perform enhanced logging',
            DEFAULT]
        param_map['criteria'] = \
            ['Choose the request criteria for logging:', DEFAULT]
        param_map['ip'] = ['Specify source IP address', DEFAULT]
        param_map['domain'] = ['Specify target domain', DEFAULT]

        # parameters for 48. W3C Logs
        param_map['format_string'] = ['Enter the format string:', DEFAULT]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def delete(self, log_to_delete='1'):
        self._query_response('DELETE')
        buf = self._sess.getbuf(clear_buf=False)
        self._query()
        self._select_list_item(log_to_delete, buf)# no names allowed
        self._to_the_top(1)

    def hostkeyconfig(self):
        self._query_response('hostkeyconfig')
        return logconfigHostkeyconfig(self._get_sess())

class logconfigHostkeyconfig(clictorbase.IafCliConfiguratorBase):
    def new(self, hostname, ssh_key):
        self._query_response('new')
        self._query_response(hostname)
        self._writeln(ssh_key)
        self._writeln("\n")
        resp = self._read_until('Choose the operation')
        self._to_the_top(2)
        return resp

    def edit(self, key_num, hosts):
        self._query_response('edit')
        self._query_response(key_num)
        self._query_response(hosts)
        self._to_the_top(2)

    def delete(self, key_num):
        self._query_response('delete')
        self._query_response(key_num)
        self._to_the_top(2)

    def scan(self, hostnames, protocol_num, add_preceding_host):
        self._query_response('scan')
        self._query_response(hostnames)
        self._query_response(protocol_num)
        self._query_response(add_preceding_host)
        resp = self._read_until('Choose the operation')
        self._to_the_top(2)
        return resp
    def _print(self, key_num):
        self._query_response('print')
        self._query_response(key_num)
        resp = self._read_until('Choose the operation')
        self._to_the_top(2)
        return resp

    def host(self):
        self._query_response('host')
        resp = self._read_until('Choose the operation')
        patt = re.compile('^.+Host\skeys\sfor', re.DOTALL)
        resp = re.sub(patt, 'Host keys for', resp)
        self._to_the_top(2)
        return resp

    def fingerprint(self):
        self._query_response('fingerprint')
        resp = self._read_until('Choose the operation')
        patt = re.compile('^.+Host\skeys\sfor', re.DOTALL)
        resp = re.sub(patt, 'Host keys for', resp)
        self._to_the_top(2)
        return resp

    def user(self):
        self._query_response('user')
        resp = self._read_until('Choose the operation')
        patt = re.compile('^.+Host\skeys\sfor', re.DOTALL)
        resp = re.sub(patt, 'Host keys for', resp)
        self._to_the_top(2)
        return resp
