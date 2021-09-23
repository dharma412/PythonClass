#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/logconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $


import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
from sal.deprecated.expect import REGEX

from sal.containers.yesnodefault import YES, NO


class logconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ("Log name '\S+' already in use", REGEX): clictorbase.IafCliValueError,
        })

    def __call__(self):
        import handlecluster
        self._writeln('logconfig')
        handlecluster.handle_cluster_questions(self._sess)
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        self._query_response('NEW')
        param_map['log_file'] = ['Choose the log file', DEFAULT, 1]
        param_map['name'] = ['name for the log', REQUIRED]
        param_map['log_level'] = ['Log level:', DEFAULT, 1]
        param_map['bytes_bounce'] = ['bytes of the bounce message', DEFAULT]
        param_map['domain'] = ['domain for which you want', NO_DEFAULT]
        param_map['smtp_sessions'] = ['number of SMTP sessions', DEFAULT]
        param_map['injection_ip'] = ['record injection debug information', \
                                     NO_DEFAULT]
        param_map['inj_sessions'] = ['number of injection sessions', DEFAULT]
        param_map['retrieval'] = ['method to retrieve the logs', DEFAULT, 1]
        param_map['hostname'] = ['Hostname to deliver', NO_DEFAULT]
        param_map['port'] = ['Port to connect to', DEFAULT]
        param_map['username'] = ['Username on the remote', NO_DEFAULT]
        param_map['password'] = ['Passphrase for ', NO_DEFAULT]
        param_map['directory'] = ['Directory on remote host', NO_DEFAULT]
        param_map['filename'] = ['Filename to use', DEFAULT]
        param_map['max_time'] = ['Maximum time to wait', DEFAULT]
        param_map['syslog_proto'] = ['transfer the log data', DEFAULT, 1]
        param_map['facility'] = ['facility do you want', DEFAULT, 1]
        param_map['ssh_proto'] = ['Protocol:', DEFAULT, 1]
        param_map['ssh_host_key'] = ['enable host key checking', DEFAULT]
        param_map['scan_host_SSH_key'] = ['automatically scan the host for ' \
                                          'its SSH key', DEFAULT]
        param_map['max_size_poll'] = ['maximum file size', DEFAULT]
        param_map['max_size_push'] = ['Maximum filesize', DEFAULT]
        param_map['max_files'] = ['maximum number of files', DEFAULT]
        param_map['time_based_rollover'] = ['configure time-based log', DEFAULT]
        param_map['rollover_setting'] = ['Configure log rollover settings', DEFAULT]
        param_map['interval'] = ['Enter an interval', DEFAULT]
        param_map['day'] = ['the day of week to roll over the log', DEFAULT]
        param_map['time'] = ['the time of day to rollover log', DEFAULT]
        param_map['include_pass'] = ['Do you want to include passphrase', DEFAULT]
        param_map['alert'] = ['alert be sent', DEFAULT]
        param_map['should_append_ids'] = ['append system based unique identifiers', DEFAULT]
        param_map['ids_format'] = ['Specify the filename unique identifier format', NO_DEFAULT]
        param_map['rate_limit'] = ['rate limit for logged events', DEFAULT]
        param_map['rate_limit'] = ['enable rate limit for logged events', DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)

    def edit(self, log_to_edit='1', input_dict=None, **kwargs):
        self._query_response('EDIT')
        buf = self._sess.getbuf(clear_buf=False)
        self._query()
        self._select_list_item(log_to_edit, buf)  # no names allowed

        # same param map as for 'new', but with DEFAULT for everything.
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['log_file'] = ['Choose the log file', DEFAULT, 1]
        param_map['name'] = ['name for the log', DEFAULT]
        param_map['rate_limit'] = ['rate limit for logged events', DEFAULT]
        param_map['log_level'] = ['Log level:', DEFAULT, 1]
        param_map['bytes_bounce'] = ['bytes of the bounce message', DEFAULT]
        param_map['domain'] = ['domain for which you want', DEFAULT]
        param_map['smtp_sessions'] = ['number of SMTP sessions', DEFAULT]
        param_map['injection_ip'] = ['record injection debug information', \
                                     DEFAULT]
        param_map['inj_sessions'] = ['number of injection sessions', DEFAULT]
        param_map['retrieval'] = ['method to retrieve the logs', DEFAULT, 1]
        param_map['hostname'] = ['Hostname to deliver', DEFAULT]
        param_map['port'] = ['Port to connect to', DEFAULT]
        param_map['username'] = ['Username on the remote', DEFAULT]
        param_map['password'] = ['Passphrase for ', DEFAULT]
        param_map['directory'] = ['Directory on remote host', DEFAULT]
        param_map['filename'] = ['Filename to use', DEFAULT]
        param_map['max_time'] = ['Maximum time to wait', DEFAULT]
        param_map['syslog_proto'] = ['transfer the log data', DEFAULT, 1]
        param_map['facility'] = ['facility do you want', DEFAULT, 1]
        param_map['ssh_proto'] = ['Protocol:', DEFAULT, 1]
        param_map['ssh_host_key'] = ['enable host key checking', DEFAULT]
        param_map['scan_host_SSH_key'] = ['automatically scan the host for ' \
                                          'its SSH key', DEFAULT]
        param_map['max_size_poll'] = ['maximum file size', DEFAULT]
        param_map['max_size_push'] = ['Maximum filesize', DEFAULT]
        param_map['max_files'] = ['maximum number of files', DEFAULT]
        param_map['time_based_rollover'] = ['configure time-based log', DEFAULT]
        param_map['rollover_setting'] = ['Configure log rollover settings', DEFAULT]
        param_map['interval'] = ['Enter an interval', DEFAULT]
        param_map['day'] = ['the day of week to roll over the log', DEFAULT]
        param_map['time'] = ['the time of day to rollover log', DEFAULT]
        param_map['alert'] = ['alert be sent', DEFAULT]
        param_map['should_append_ids'] = ['append system based unique identifiers', DEFAULT]
        param_map['ids_format'] = ['Specify the filename unique identifier format', NO_DEFAULT]

        param_map.update(input_dict or kwargs)
        result = self._process_input(param_map, do_restart=False)
        self._to_the_top(1)
        return result

    def Print(self):
        self._to_the_top(1)
        raw = self.getbuf()
        START_LABEL = 'Currently configured logs:'
        START_POS = raw.find(START_LABEL) + len(START_LABEL) + 1
        END_LABEL = 'Choose the operation'
        END_POS = raw[START_POS:].find(END_LABEL) + START_POS
        return raw[START_POS:END_POS].strip()

    def delete(self, log_to_delete='1'):
        self._query_response('DELETE')
        self._query_response(log_to_delete)
        self._to_the_top(1)

    def setup(self, frequency='60', log_message_id=YES,
              log_subj_header=YES, log_remote_resp=YES):
        self._query_response('SETUP')
        self._query_response(frequency)
        self._query_response(log_message_id)
        self._query_response(log_subj_header)
        self._query_response(log_remote_resp)
        self._to_the_top(1)

    def logheaders(self, headers=''):
        self._query_response('LOGHEADERS')
        self._query_response(headers)
        self._to_the_top(1)

    def hostkeyconfig(self):
        self._query_response('HOSTKEYCONFIG')
        return logconfigHostkeyconfig(self._get_sess())


class logconfigHostkeyconfig(clictorbase.IafCliConfiguratorBase):

    def new(self, hostname, ssh_key):
        self._query_response('new')
        self._query_response(hostname)
        self._writeln(ssh_key.rstrip('\r\n') + '\n\n')
        self._to_the_top(1)

    def edit(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        self._query_response('edit')
        # Works only with numbers.
        param_map['key_num'] = ['Enter the number of the key', REQUIRED]
        param_map['hostnames'] = ['Enter the hostnames', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)

    def delete(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        self._query_response('delete')
        # Works only with numbers.
        param_map['key_num'] = ['Enter the number of the key', REQUIRED]
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)

    def scan(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        self._query_response('scan')
        self.clearbuf()
        param_map['hostname'] = ['Please enter the host', REQUIRED]
        param_map['ssh_proto'] = ['Choose the ssh protocol', DEFAULT, 1]
        param_map['add_keys'] = ['Add the preceding host', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)
        raw = self.getbuf()
        if raw.find('Choose the operation') >= 0:
            return raw[:raw.find('Choose the operation')]
        else:
            return raw

    def host(self):
        import re
        self._query_response('host')
        resp = self._read_until('Choose the operation')
        patt = re.compile('^.+Host\skeys\sfor', re.DOTALL)
        resp = re.sub(patt, 'Host keys for', resp)
        self._to_the_top(2)
        return resp

    def Print(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        self._query_response('print')
        self.clearbuf()
        param_map['key_num'] = ['Enter the number of the key you wish to print',
                                REQUIRED]
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)
        raw = self.getbuf()
        if raw.find('Choose the operation') >= 0:
            return raw[:raw.find('Choose the operation')]
        else:
            return raw

    def fingerprint(self):
        import re
        self._query_response('fingerprint')
        resp = self._read_until('Choose the operation')
        patt = re.compile('^.+Host\skeys\sfor', re.DOTALL)
        resp = re.sub(patt, 'Host keys for', resp)
        self._to_the_top(2)
        return resp

    def user(self):
        import re
        self._query_response('user')
        resp = self._read_until('Choose the operation')
        patt = re.compile('^.+Host\skeys\sfor', re.DOTALL)
        resp = re.sub(patt, 'Host keys for', resp)
        self._to_the_top(2)
        return resp
