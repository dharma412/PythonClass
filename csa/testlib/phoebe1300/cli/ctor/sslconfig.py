#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/sslconfig.py#2 $ $DateTime: 2019/09/05 12:07:04 $ $Author: saurgup5 $

"""
SARF CLI command: sslconfig
"""

from sal.containers.yesnodefault import YES, NO, is_no
import clictorbase
import re
from sal.containers.cfgholder import CfgHolder

DEFAULT = clictorbase.DEFAULT
REQUIRED = clictorbase.REQUIRED


class sslconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def inbound(self, input_dict=None, **kwargs):
        param_map = \
            clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['ssl_method'] = ['inbound SMTP ssl method', DEFAULT, True]
        param_map['ssl_cipher'] = ['inbound SMTP ssl cipher', DEFAULT]
        param_map['tls_negotiation'] = ['TLS Renegotiation for inbound SMTP', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('INBOUND')
        return self._process_input(param_map)

    def outbound(self, input_dict=None, **kwargs):
        param_map = \
            clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['ssl_method'] = ['outbound SMTP ssl method', DEFAULT, True]
        param_map['ssl_cipher'] = ['outbound SMTP ssl cipher', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('OUTBOUND')
        return self._process_input(param_map)

    def gui(self, input_dict=None, **kwargs):
        param_map = \
            clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['ssl_method'] = ['GUI HTTPS ssl method', DEFAULT, True]
        param_map['ssl_cipher'] = ['GUI HTTPS ssl cipher', DEFAULT]
        param_map['tls_negotiation'] = ['TLS Renegotiation for GUI HTTPS', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('GUI')
        return self._process_input(param_map)

    def verify(self, cipher=REQUIRED):
        self._query_response('VERIFY')
        self._query_response(cipher)
        res = self._read_until('sslconfig settings:')
        self._to_the_top(self.newlines)
        return res

    def _normalize(self, s):
        return re.sub('[\\W\\d]', '_', s.strip()).lower()

    def get_settings(self, as_dictionary=YES, fips_mode=True):
        raw = self._read_until('Choose the operation')
        self._restart_nosave()  # go to top-level command
        if is_no(as_dictionary):
            return raw
        settings = CfgHolder()
        res = re.findall('(.*):\s+(.*)', raw)
        if res:
            for r in res:
                settings.__setattr__ \
                    (self._normalize(r[0]), r[1].strip())
        else:
            self._warn('Returning raw result')
            return raw
        return settings
