#!/usr/bin/env python
"""
CLI command: sshconfig
"""

import clictorbase as ccb
from sal.deprecated.expect import EXACT
from sal.containers.yesnodefault import YES, NO
from sal.containers.yesnodefault import  is_yes, is_no
import re

REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
DEBUG = True

class sslconfig(ccb.IafCliConfiguratorBase):

    class SslValueError(ccb.IafCliError): pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self.protocol_map = {
                                            'sslv3': 'SSLv3.0',
                                            'tls1dot0': 'TLSv1.0',
                                            'tls1dot1': 'TLSv1.1',
                                            'tls1dot2': 'TLSv1.2',
        }

        self.services_dict = {
            'ldaps': 1,
            'updater': 2,
            'proxy': 3,
            'radsec': 4,
            'sicap': 5,
            'webui': 6,
            'all_services': 7,
        }

    def __call__(self):
        self._restart()
        self._writeln('sslconfig')
        raw = self._read_until('>')
        return self

    def fallback(self, enable=REQUIRED):
        self._writeln('FALLBACK')
        raw = self._read_until('>')
        self._info(raw)
        if is_yes(enable):
            match = re.search('enabled', raw)
            if match is not None:
                self._writeln('\n')
            else:
                self._writeln('Y\n')
        if is_no(enable):
            match = re.search('disabled', raw)
            if match is not None:
                self._writeln('\n')
            else:
                self._writeln('Y\n')
        #self._writeln('\n')
        self._to_the_top(1)

    def versions(self, service='proxy', protocol='tls1dot0', enable=REQUIRED):
        service = str(service).lower()
        if service not in self.services_dict.keys():
            raise Exception("Error in Service: Service %s does not exist.\nAvailable services are: %s\nPlease check." %(service, self.services_dict.keys()))

        protocol = str(protocol).lower()
        if protocol not in self.protocol_map.keys():
            raise Exception("Error in Protocol: Protocol %s does not exist.\nAvailable protocols are: %s\nPlease check." %(protocol, self.protocol_map.keys()))

        service_id = self.services_dict[service]
        self._writeln('VERSIONS')

        #Select Service ID
        raw = self._read_until('>')
        self._info(raw)
        self._writeln(service_id)

        #Select Protocol
        raw = self._read_until('>')
        self._info(raw)
        protocol_name = self.protocol_map[protocol]
        match = re.search("\d\. %s" %protocol_name, raw)
        if match is None:
            raise Exception("Error Invalid Protocol: Protocol %s> %s is not available.\nPlease check FIPS status." %(protocol, protocol_name))

        protocol_id = match.group().split(".", 1)[0]
        self._writeln(protocol_id)

        #Enable/Disable Protocol
        raw = self._read_until('>')
        self._info(raw)
        if is_yes(enable):
            match = re.search('Do you want to enable', raw)
            if match is not None:
                self._writeln('Y\n')
            else:
                self._writeln('\n')

        if is_no(enable):
            match = re.search('Do you want to disable', raw)
            if match is not None:
                self._writeln('Y\n')
            else:
                self._writeln('\n')

        #Check status
        raw = self._read_until('>')
        self._info(raw)
        self._to_the_top(1)

    def ciphers(self, service, ciphers_list=REQUIRED):

        services_dict = {
            'proxy': 1,
        }
        service = str(service).lower()
        if service not in services_dict.keys():
            raise Exception("Error in Service: Service %s does not exist.\nAvailable services are: %s\nPlease check." %(service, services_dict.keys()))

        self._writeln('CIPHERS')

        #Select Service
        raw = self._read_until('>')
        match = re.search('\d\. %s' %service.capitalize(), raw)
        if match is not None:
            service_id = match.group().split(".", 1)[0]
            self._writeln(service_id)
        else:
            raise Exception("Error Service Not Available: Service %s does support changing of ciphers." %(service))

        raw = self._read_until('>')
        self._writeln(ciphers_list)
        self._to_the_top(1)

    def compress(self, enable=REQUIRED):

        self._writeln('COMPRESS')

        #Enable/Disable Compression
        raw = self._read_until('>')
        if is_yes(enable):
            match = re.search('enable it', raw)
            if match is not None:
                self._writeln('Y\n')
            else:
                self._writeln('\n')

        if is_no(enable):
            match = re.search('disable it', raw)
            if match is not None:
                self._writeln('Y\n')
            else:
                self._writeln('\n')
        self._to_the_top(1)

    def ecdhe(self, enable=REQUIRED):

        self._writeln('ECDHE')

        #Enable/Disable ECDHE Cipher
        raw = self._read_until('>')
        if is_yes(enable):
            match = re.search('ECDHE cipher status is currently enabled', raw)
            if match is not None:
                self._writeln('\n')
            else:
                self._writeln('Y\n')

        if is_no(enable):
            match = re.search('ECDHE cipher status is currently disabled', raw)
            if match is not None:
                self._writeln('\n')
            else:
                self._writeln('Y\n')
        self._to_the_top(1)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
