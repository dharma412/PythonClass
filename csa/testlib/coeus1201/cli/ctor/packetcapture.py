#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/packetcapture.py#2 $

"""
IAF 2 CLI command: packetcapture
"""

import re
from sal.exceptions import ConfigError
import clictorbase as ccb
from sal.containers.yesnodefault import DEFAULT

class packetcapture(ccb.IafCliConfiguratorBase):

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self.packet_capture_status_buffer = ''

    def __call__(self):
        self.clearbuf()
        self._writeln('packetcapture')
        return self

    def _get_status(self):
        if not self.packet_capture_status_buffer:
            self.packet_capture_status_buffer = self.getbuf()
        self._info('_get_status() | Buffer read: %s\n' % self.packet_capture_status_buffer)
        status = re.findall('Status: (.+)', self.packet_capture_status_buffer)
        if not status:
            raise ConfigError, 'packetcapture::_get_status() | Could not obtain the packet capture status.'

        return status[-1]

    def setup(self, input_dict=None, **kwargs):
        self.packet_capture_status_buffer = ''
        param_map = ccb.IafCliParamMap(end_of_command='Choose the operation')
        param_map['max_size'] = ['maximum allowable size', '']
        param_map['stop_limit'] = ['stop the capture when', '']
        param_map['if_name'] = ['interfaces to capture packets from', '']
        param_map['filter'] = ['Enter the filter to be used for the capture', '']
        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')
        return self._process_input(param_map)

    def start(self):
        self.packet_capture_status_buffer = ''
        self._query_response('START')
        self._to_the_top(1)
        self.packet_capture_status_buffer = self.getbuf()
        self._info('start() | Buffer read: %s\n' % self.packet_capture_status_buffer)
        xml_file = re.search('File Name:\s+(\S+\.cap)', self.packet_capture_status_buffer)

        if not xml_file:
            raise ConfigError, 'packetcapture::start() | No capture filename was found in the output.'

        return xml_file.group(1)

    def stop(self):
        self.packet_capture_status_buffer = ''
        self._query_response('STOP')
        self._to_the_top(1)
        status = 'Packet capture stopped'
        self.packet_capture_status_buffer = self.getbuf()
        self._info('stop() | Buffer read: %s\n' % self.packet_capture_status_buffer)

        if status not in self.packet_capture_status_buffer:
            raise ConfigError, 'packetcapture::stop() | Packetcapture was not stopped.'

        return status

    def status(self):
        try:
            self.packet_capture_status_buffer = ''
            self._query_response('STATUS')
            self._to_the_top(1)
            self.packet_capture_status_buffer = self.getbuf()
            self._info('status() | Buffer read: %s\n' % self.packet_capture_status_buffer)
        except:
            self._to_the_top(1)

        return self._get_status()


if __name__=='__main__':

    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    pc = packetcapture(cli_sess)

    pc().setup()

    print 'packetcapture:START', pc().start()
    print 'packetcapture:STATUS', pc().status()
    print 'packetcapture:STOP', pc().stop()

