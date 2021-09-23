#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/sslconfig.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

"""
SARF CLI command: sslconfig
"""

from sal.containers.yesnodefault import YES, NO, is_no
import clictorbase
import re
import string
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
        param_map['ssl_method']  = ['inbound SMTP ssl method', DEFAULT, True]
        param_map['ssl_cipher']  = ['inbound SMTP ssl cipher', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('INBOUND')
        return self._process_input(param_map)

    def outbound(self, input_dict=None, **kwargs):
        param_map = \
        clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['ssl_method']  = ['outbound SMTP ssl method', DEFAULT, True]
        param_map['ssl_cipher']  = ['outbound SMTP ssl cipher', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('OUTBOUND')
        return self._process_input(param_map)

    def gui(self, input_dict=None, **kwargs):
        param_map = \
        clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['versions'] = ['enable/disable SSL/TLS versions', DEFAULT, True]
        param_map['ssl_method'] = ['setting for a specific protocol', DEFAULT, True]
        param_map['confirm'] = ['Enable', DEFAULT, True]
        #param_map['ssl_method']  = ['GUI HTTPS ssl method', DEFAULT, True]
        #param_map['ssl_cipher']  = ['GUI HTTPS ssl cipher', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('VERSIONS')
        return self._process_input(param_map)

    def verify(self, cipher=REQUIRED):
        self._query_response('VERIFY')
        self._query_response(cipher)
        res = self._read_until('sslconfig settings:')
        self._to_the_top(self.newlines)
        return res

    def _normalize(self, s):
        return re.sub('[\\W\\d]', '_', s.strip()).lower()

    def get_settings(self, **kwargs):
        res_dict = {}
        self._query_response('VERSIONS')
        num_entries_str=self._read_until(['[]>'])
        self._writeln()
        num_entries=re.search("(\d)\.\s*All Services",num_entries_str)
        for id in range(1,int(num_entries.groups()[0])):
            self._query_response('VERSIONS')
            self._expect('[]>', timeout=5)
            self._writeln(id)
            res = self._read_until(['To change the setting'])
            self._read_until('>')
            res = res.rsplit(".", 1)
            res = "".join(res)
            result = re.search("Currently enabled protocol\(s\) for (.*) are ([\w\d\.\s\,]+)\n",res)
            list_res = str(result.groups()[1]).translate(None, ' \n\t\r')
            res_dict[result.groups()[0]] = list_res
            self._writeln('1')
            self._read_until('>')
            self._writeln()
        return res_dict

    def set_peer_cert_fqdn(self, input_dict=None, **kwargs):
        self._query_response('PEER_CERT_FQDN')
        if kwargs['enable'] == 'True':
            self._query_response('ENABLE')
        else:
            self._query_response('DISABLE')
        self._to_the_top(self.newlines)

    def peer_cert_fqdn_status(self):
        self._query_response('PEER_CERT_FQDN')
        fqdn_status=self._read_until(['[]>'])
        if 'Disable peer certificate FQDN validation' in fqdn_status:
            return 'Enabled'
        elif 'Enable peer certificate FQDN validation' in fqdn_status:
            return 'Disabled'
        else:
            pass
