#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/logconfig.py#2 $
# $DateTime: 2020/06/23 23:14:35 $
# $Author: mrmohank $

"""
CLI command: logconfig
"""

import re

import clictorbase

from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import REGEX


class logconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ("Log name '\S+' already in use", REGEX): clictorbase.IafCliValueError,
        })

    def __call__(self):
        self._writeln('logconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        self._query_response('NEW')
        param_map['log_file']      = ['Choose the log file', DEFAULT, 1]
        param_map['name']          = ['name for the log', REQUIRED]
        param_map['log_level']     = ['Log level:', DEFAULT, 1]
        param_map['bytes_bounce']  = ['bytes of the bounce message', DEFAULT]
        param_map['domain']        = ['domain for which you want', NO_DEFAULT]
        param_map['smtp_sessions'] = ['number of SMTP sessions', DEFAULT]
        param_map['injection_ip']  = ['record injection debug information', \
                                        NO_DEFAULT]
        param_map['inj_sessions']  = ['number of injection sessions', DEFAULT]
        param_map['retrieval']     = ['method to retrieve the logs', DEFAULT, 1]
        param_map['hostname']      = ['Hostname to deliver', NO_DEFAULT]
        param_map['port']          = ['Port to connect to', DEFAULT]
        param_map['username']      = ['Username on the remote', NO_DEFAULT]
        param_map['password']      = ['Password for ', NO_DEFAULT]
        param_map['directory']     = ['Directory on remote host', NO_DEFAULT]
        param_map['filename']      = ['Filename to use', DEFAULT]
        param_map['max_time']      = ['Maximum time to wait', DEFAULT]
        param_map['syslog_proto']  = ['transfer the log data', DEFAULT, 1]
        param_map['facility']      = ['facility do you want', DEFAULT, 1]
        param_map['ssh_host_key']  = ['enable host key checking', DEFAULT]
        param_map['scan_host_ssh_key'] = ['automatically scan the host for '\
                                          'its SSH key', DEFAULT]
        param_map['max_size'] = [re.compile('[Mm]aximum file\s?size'), DEFAULT]
        param_map['max_files']     = ['maximum number of files', DEFAULT]
        param_map['time_based_rollover'] = ['configure time-based log', DEFAULT]
        param_map['rollover_setting'] = ['Configure log rollover settings',DEFAULT]
        param_map['interval'] = ['Enter a number of seconds, minutes', DEFAULT]
        param_map['day'] = ['the day of week to roll over the log', DEFAULT]
        param_map['time'] = ['the time of day to rollover log', DEFAULT]

        param_map['rate_limit'] = ['enable rate limit for logged events', DEFAULT]
        param_map['time_range'] = ['Time range in seconds', DEFAULT]
        param_map['number_of_events'] = ['Maximum number of events to be logged', DEFAULT]
        param_map['include_pwd']   = ['include passwords', DEFAULT]
        param_map['append_unique_id'] = ['append system based unique identifiers', DEFAULT]
        param_map['unique_id'] = ['Specify the filename unique identifier format', NO_DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def edit(self, log_to_edit='1', input_dict=None, **kwargs):
        self._query_response('EDIT')
        buf = self._sess.getbuf(clear_buf = False)
        self._query()
        self._select_list_item(log_to_edit, buf)# no names allowed

        # same param map as for 'new', but with DEFAULT for everything.
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['log_file']      = ['Choose the log file', DEFAULT, 1]
        param_map['name']          = ['name for the log', DEFAULT]
        param_map['log_level']     = ['Log level:', DEFAULT, 1]
        param_map['rate_limit'] =    ['enable rate limit for logged events', DEFAULT]
        param_map['time_range'] =    ['Time range in seconds', DEFAULT]
        param_map['number_of_events'] =    ['Maximum number of events to be logged', DEFAULT]
        param_map['bytes_bounce']  = ['bytes of the bounce message', DEFAULT]
        param_map['domain']        = ['domain for which you want', DEFAULT]
        param_map['smtp_sessions'] = ['number of SMTP sessions', DEFAULT]
        param_map['injection_ip']  = ['record injection debug information', \
            DEFAULT]
        param_map['inj_sessions']  = ['number of injection sessions', DEFAULT]
        param_map['retrieval']     = ['method to retrieve the logs', DEFAULT, 1]
        param_map['hostname']      = ['Hostname to deliver', DEFAULT]
        param_map['port']          = ['Port to connect to', DEFAULT]
        param_map['username']      = ['Username on the remote', DEFAULT]
        param_map['password']      = ['Password for ', DEFAULT]
        param_map['directory']     = ['Directory on remote host', DEFAULT]
        param_map['filename']      = ['Filename to use', DEFAULT]
        param_map['max_time']      = ['Maximum time to wait', DEFAULT]
        param_map['syslog_proto']  = ['transfer the log data', DEFAULT, 1]
        param_map['facility']      = ['facility do you want', DEFAULT, 1]
        param_map['ssh_host_key']  = ['enable host key checking', DEFAULT]
        param_map['scan_host_ssh_key'] = ['automatically scan the host for ' \
            'its SSH key',DEFAULT]
        param_map['max_size'] = [re.compile('[Mm]aximum file\s?size'), DEFAULT]
        param_map['max_files']     = ['maximum number of files', DEFAULT]
        param_map['time_based_rollover'] = ['configure time-based log', DEFAULT]
        param_map['rollover_setting'] = ['Configure log rollover settings',DEFAULT]
        param_map['interval'] = ['Enter a number of seconds, minutes', DEFAULT]
        param_map['day'] = ['the day of week to roll over the log', DEFAULT]
        param_map['time'] = ['the time of day to rollover log', DEFAULT]
        param_map['include_pwd']   = ['include passwords', DEFAULT]
        param_map['append_unique_id'] = ['append system based unique identifiers', DEFAULT]
        param_map['unique_id'] = ['Specify the filename unique identifier format', NO_DEFAULT]

        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def delete(self, log_to_delete='1'):
        self._query_response('DELETE')
        buf = self._sess.getbuf(clear_buf = False)
        self._query()
        self._select_list_item(log_to_delete, buf)# no names allowed
        self._to_the_top(1)

    def setup(self, frequency='60', log_message_id=YES,
                    log_subj_header=YES, log_remote_resp=YES):
        self._query_response('SETUP')
        self._query_response(frequency)
        self._query_response(log_message_id)
        self._query_response(log_subj_header)
        self._query_response(log_remote_resp)
        self._to_the_top(1)

    def logheaders(self, headers = ''):
        self._query_response('LOGHEADERS')
        self._query_response(headers)
        self._to_the_top(1)

    def hostkeyconfig(self):
        self._query_response('HOSTKEYCONFIG')
        return logconfigHostkeyconfig(self._get_sess())

class logconfigHostkeyconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def _get_key(self):
        resp = self._read_until('Choose the operation')
        patt = re.compile('^.+Host\skeys\sfor', re.DOTALL)
        resp = re.sub(patt, 'Host keys for', resp)
        self._to_the_top(self.newlines)
        return resp

    def new(self, hostname, ssh_key):
        self._query_response('new')
        self._query_response(hostname)
        self._writeln(ssh_key + '\r\n\r\n')
        self._to_the_top(self.newlines)

    def edit(self, key_num, hosts):
        self._query_response('edit')
        self._query_response(key_num)
        self._query_response(hosts)
        self._to_the_top(self.newlines)

    def delete(self, key_num):
        self._query_response('delete')
        self._query_response(key_num)
        self._to_the_top(self.newlines)

    def scan(self, input_dict = None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        self._query_response('scan')
        param_map['hostname']  = ['Please enter the host', REQUIRED]
        param_map['ssh_proto'] = ['Choose the ssh protocol', DEFAULT, 1]
        param_map['add_keys']  = ['Add the preceding host', DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def print_key(self, key_num):
        self._query_response('print')
        self._query_response(key_num)
        return self._get_key()

    def host(self):
        self._query_response('host')
        return self._get_key()

    def fingerprint(self):
        self._query_response('fingerprint')
        return self._get_key()

    def user(self):
        self._query_response('user')
        return self._get_key()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    lc = logconfig(cli_sess)

    cmd = {'name' :'blah','log_file':'Bounce Logs','retrieval':'3', \
           'hostname':'automation.ironport.com','username':'dang', \
           'directory':'/tmp/scp_push.qa','filename':'blah','ssh_proto':'1'}
    cmd['ssh_host_key'] = 'YES'

    lc().new(cmd)

    cmd = {'name': 'blah1','bytes_bounce':'1000','filename':'blah',\
           'max_time':'1000', 'max_size_push':'5242880', 'ssh_host_key': 'NO'}

    lc().edit(log_to_edit = 'blah', input_dict = cmd)

