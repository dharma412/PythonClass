#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/sshconfig.py#1 $

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
            ('SSH key does not appear', EXACT) : self.SshValueError,
            })

    def __call__(self):
        self._restart()
        self._writeln('sshconfig')
        return self

    def sshd_edit_settings(self, incomplete_ssh_session_timeout=DEFAULT,
                         min_server_key_size=DEFAULT,
                         pubkey_algorithms=DEFAULT,
                         kex_algorithms=DEFAULT,
                         cipher_algorithms=DEFAULT,
                         unsuccessfull_ssh_session_timeout=DEFAULT,
                         mac_methods=DEFAULT):
        self.level=2
        self._writeln('SSHD')
        output = self._read_until('Setup SSH server configuration settings')
        self._writeln('SETUP')
        self._writeln(incomplete_ssh_session_timeout)
        self._writeln(min_server_key_size)
        self._writeln(pubkey_algorithms)
        self._writeln(kex_algorithms)
        self._writeln(cipher_algorithms)
        self._writeln(unsuccessfull_ssh_session_timeout)
        self._writeln(mac_methods)
        self._to_the_top(self.level)
        return output

    def new(self, ssh_key=REQUIRED):
        self.level=2
        self._writeln('USERKEY')
        self._writeln('NEW')
        self._writeln(ssh_key+'\n')
        self._to_the_top(self.level)

    def delete(self, server=REQUIRED):
        self.level=2
        self._writeln('USERKEY')
        self._query_response('DELETE')
        self._query_response(server)
        self._to_the_top(self.level)

    def print_key(self, key_numbers=REQUIRED):
        self.level=2
        self._writeln('USERKEY')
        self._query_response('PRINT')
        self._query_response(key_numbers)
        self._expect('\n')
        raw = self._read_until('Currently installed')
        self._to_the_top(self.level)
        return raw

    def user(self, user=DEFAULT):
        self.level=2
        self._writeln('USERKEY')
        self._query_response('USER')
        self._query_response(user)
        self._to_the_top(self.level)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    sshc = sshconfig(cli_sess)

    sshc().new('ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEAoPWj3H7paui4u6jda9'+
                '/qPY7O8RviJV2RS3KOY/kEDuecaz5b79ceVUGUao/pMw9ZKM6IM4d'+
                'U8CPNJOrzch7Gx8I/jY1tsS65zdDJMr89q= esafronov@pan.iron')
    sshc().print_key('1')
    sshc().user()
    sshc().delete('1')
