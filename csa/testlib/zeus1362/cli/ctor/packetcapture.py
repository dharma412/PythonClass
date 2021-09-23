#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/packetcapture.py#1 $
# $DateTime: 2020/06/10 22:29:20 $
# $Author: sarukakk $

"""
IAF 2 CLI command: packetcapture
"""

import re
from sal.deprecated.expect import REGEX, EXACT
from sal.exceptions import ConfigError
import clictorbase as ccb
from clictorbase import DEFAULT


class packetcapture(ccb.IafCliConfiguratorBase):
    _new_lines = 1
    msg = "Choose the operation you want to perform:"

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self.status_attr_map = {}
        self.status_attr_map['status'] = 'Status:'
        self.status_attr_map['file_name'] = 'File Name:'
        self.status_attr_map['file_size'] = 'File Size:'
        self.status_attr_map['duration'] = 'Duration:'
        self.status_attr_map['limit'] = 'Limit:'
        self.status_attr_map['interface'] = 'Interface\(s\):'
        self.status_attr_map['filter'] = 'Filter:'

    def __call__(self):
        self.clearbuf()
        self._writeln('packetcapture')
        self._expect([(self.msg, EXACT)])
        return self

    def _get_status(self, buf):
        self._debug('In _get_status')
        self._debug(buf)
        status = {}
        for key in self.status_attr_map.keys():
            status[key] = ''

        for key, val in self.status_attr_map.items():
            text = re.findall(val+'\s+(.+)', buf)
            if text:
                status[key] = text[-1].strip()
        self._debug('_get_status result')
        self._debug(status)
        return status

    def setup(self, input_dict=None, **kwargs):
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['max_size'] = ['maximum allowable size', DEFAULT]
        param_map['stop_limit'] = ['stop the capture when', DEFAULT]
        param_map['if_name'] = ['interfaces to capture packets from', DEFAULT]
        param_map['filter'] = ['with the existing filter', DEFAULT]
        param_map['client_port'] = ['Enter port(s)', DEFAULT]
        param_map['client_ip'] = ['Enter Client IP(s)', DEFAULT]
        param_map['server_ip'] = ['Enter Server IP(s)', DEFAULT]
        param_map['custom_filter'] = ['custom filter', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)

    def start(self):
        self._query_response('START')
        self._expect([(self.msg, EXACT)])
        buf = self.getbuf()
        start = buf.find('[]> START')
        buf = buf[start:]
        status = self._get_status(buf)
        status['status'] = buf.split('\n')[2].strip()
        self._to_the_top(self._new_lines)
        return status

    def stop(self):
        self._query_response('STOP')
        self._expect([(self.msg, EXACT)])
        buf = self.getbuf()
        start = buf.find('[]> STOP')
        buf = buf[start:]
        status = self._get_status(buf)
        status['status'] = buf.split('\n')[2].strip()
        self._to_the_top(self._new_lines)
        return status

    def status(self):
        buf = self.getbuf()
        status = self._get_status(buf)
        if status['status'] != 'No capture running':
            self.clearbuf()
            self._query_response('STATUS')
            self._expect([(self.msg, EXACT)])
            buf = self.getbuf()
            start = buf.find('[]> STATUS')
            buf = buf[start:]
            status = self._get_status(buf)

        self._to_the_top(self._new_lines)
        return status

if __name__=='__main__':

    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    pc = packetcapture(cli_sess)

    pc().setup(filter='PREDEFINED')
    pc().setup(filter='CUSTOM')
    pc().setup(filter='CLEAR')

    print 'packetcapture:START', pc().start()
    print 'packetcapture:STATUS', pc().status()
    print 'packetcapture:STOP', pc().stop()

