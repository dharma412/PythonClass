#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/sshconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
IAF 2 CLI command: sshconfig
"""

import clictorbase as ccb
from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import EXACT
from sal.exceptions import TimeoutError

REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT
DEBUG = True


class sshconfig(ccb.IafCliConfiguratorBase):
    class SshValueError(ccb.IafCliError): pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('SSH key does not appear', EXACT): self.SshValueError,
        })

    def __call__(self):
        self._restart()
        self._writeln('sshconfig')
        return self

    def sshd_edit_settings(self, fips_mode=False, pubkey_algorithms=DEFAULT,
                           cipher_algorithms=DEFAULT,
                           mac_methods=DEFAULT,
                           min_server_key_size=DEFAULT,
                           kex_algorithms=DEFAULT, ):
        self.level = 2
        self._writeln('SSHD')
        self._writeln('SETUP')
        self._writeln(pubkey_algorithms)
        self._writeln(cipher_algorithms)
        if not fips_mode:
            self._writeln(mac_methods)
        self._writeln(min_server_key_size)
        self._writeln(kex_algorithms)
        self._to_the_top(self.level)

    def new(self, ssh_key=REQUIRED):
        self.level = 2
        self._writeln('USERKEY')
        self._writeln('NEW')
        self._writeln(ssh_key + '\n')
        self._to_the_top(self.level)

    def delete(self, ssh_key=REQUIRED):
        self.level = 2
        self._writeln('USERKEY')
        self._query_response('DELETE')
        self._query_response(ssh_key)
        self._to_the_top(self.level)

    def print_key(self, key_numbers=REQUIRED):
        self.level = 2
        self._writeln('USERKEY')
        self._query_response('PRINT')
        self._query_response(key_numbers)
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw.strip("\r\n")

    def user_new(self, user=DEFAULT, ssh_key=REQUIRED):
        self.level = 3
        self._writeln('USERKEY')
        self._query_response('USER')
        self._query_response(user)
        self._writeln('NEW')
        self._writeln(ssh_key + '\n')
        self._to_the_top(self.level)

    def user_delete(self, user=DEFAULT, ssh_key=REQUIRED):
        self.level = 3
        self._writeln('USERKEY')
        self._query_response('USER')
        self._query_response(user)
        self._writeln('DELETE')
        self._writeln(ssh_key)
        self._to_the_top(self.level)

    def user_print(self, user=DEFAULT, key_number=REQUIRED):
        self.level = 3
        self._writeln('USERKEY')
        self._query_response('USER')
        self._query_response(user)
        self._query_response('PRINT')
        self._query_response(key_number)
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw.strip("\r\n")
