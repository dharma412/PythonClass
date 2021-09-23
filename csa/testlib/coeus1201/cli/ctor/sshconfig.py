#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/sshconfig.py#2 $

"""
IAF 2 CLI command: sshconfig
"""

import clictorbase as ccb
from sal.deprecated.expect import EXACT
from sal.containers.yesnodefault import YES, NO
REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT

DEBUG = True

import time

class sshconfig(ccb.IafCliConfiguratorBase):

    class SshValueError(ccb.IafCliError): pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {
                ('SSH key does not appear', EXACT) : self.SshValueError,
                ('Value must be an integer', EXACT) : self.SshValueError,
                ('You must enter a value', EXACT) : self.SshValueError,
            }
        )

    def __call__(self):
        self._writeln('sshconfig')
        return self

    def sshd_edit_settings(self, fips_mode=False, pubkey_algorithms=DEFAULT,
                         cipher_algorithms=DEFAULT,
                         mac_methods=DEFAULT,
                         min_server_key_size=DEFAULT,
                         kex_algorithms=DEFAULT,
                         incomplete_ssh_session_timeout=DEFAULT,
                         unsuccessfull_ssh_session_timeout=DEFAULT,
                         ):
        self.level=3
        self._writeln('SSHD')
        self._writeln('SETUP')
        raw = self._read_until('Enter the Incomplete SSH session timeout (in secs) you want to use', timeout=5)
        self._writeln(incomplete_ssh_session_timeout)
        raw = self._read_until('Enter the Minimum Server Key Size you want to use', timeout=5)
        self._writeln(min_server_key_size)
        raw = self._read_until('Enter the Public Key Authentication Algorithms you want to use', timeout=5)
        self._writeln(pubkey_algorithms)
        raw = self._read_until('Enter the KEX Algorithms you want to use', timeout=5)
        self._writeln(kex_algorithms)
        raw = self._read_until('Enter the Cipher Algorithms you want to use', timeout=5)
        self._writeln(cipher_algorithms)
        raw = self._read_until('Enter the Unsuccessful SSH login attempts allowed you want to use', timeout=5)
        self._writeln(unsuccessfull_ssh_session_timeout)
        try:
            raw = self._read_until('Enter the MAC Methods you want to use', timeout=5)
            self._writeln(mac_methods)
        except:
            pass
        self._writeln('')
        self._writeln('')
        self._writeln('')
        return raw

    def user_new(self, user=DEFAULT, ssh_key=REQUIRED):
        self.level=3
        self._writeln('USERKEY')
        self._query_response('USER')
        self._query_response(user)
        self._writeln('NEW')
        self._writeln(ssh_key+'\n')
        self._to_the_top(self.level)

    def new(self, ssh_key=REQUIRED):
        self.level = 1
        self._query_response('USERKEY')
        #time.sleep(1)
        self._query_response('NEW')
        self._expect('Press enter on a blank line', timeout=10)
        self._writeln('%s\n' %ssh_key)
        raw = self._read_until('Choose the operation', timeout=15)
        self._writeln('\n\n\n\n')
        self._to_the_top(self.level)
        return raw


    def delete(self, key_num=REQUIRED):
        self.level = 1
        self._query_response('USERKEY')
        self._query_response('DELETE')
        #self._expect('Enter the number of the key')
        self._query_response('%s' %str(key_num))
        #self._writeln('%s' %str(key_num))
        raw = ""
        index = -1

        try:
            #raw = self._read_until('Choose the operation', timeout=10)
            index = self._query('Choose the operation', 'Value must be an integer', 'Choose the user')
        except:
            raw = self.getbuf()
            self.interrupt()

        if index == 1:
            raise self.SshValueError('Value must be an integer')

        self._writeln('\n\n\n\n')
        self._to_the_top(self.level)
        return raw

    def print_key(self, key_num=REQUIRED):
        self.level = 1
        self._query_response('USERKEY')
        self._query_response('PRINT')
        self._expect('Enter the number of the key', timeout=10)
        self._writeln(str(key_num))
        try:
            raw = self._read_until('Choose the operation', timeout=5)
        except:
            raw = self.getbuf()
            self.interrupt()

        self._writeln('\n\n\n\n')
        self._to_the_top(self.level)
        return raw

    def print_keys(self ):
        self.level = 1
        self._query_response('USERKEY')
        raw = self._read_until('Choose the operation', timeout=10)
        self._writeln('\n\n\n\n')
        self._to_the_top(self.level)
        return raw

    def print_users(self):
        self.level = 1
        self._query_response('USERKEY')
        self._query_response('USER')
        raw = self._read_until('[1]>', timeout=10)
        self._writeln('\n\n\n\n')
        self._to_the_top(self.level)
        return raw

    def user(self, user=DEFAULT):
        self.level = 1
        self._query_response('USERKEY')
        self._query_response('USER')
        self._expect('Choose the user', timeout=10)
        self._query_response(user)
        raw = ""
        index = -1

        try:
            #raw = self._read_until('Choose the operation', timeout=10)
            index = self._query('Choose the operation', 'Choose the user', 'You must enter a value')
        except:
            raw = self.getbuf()
            self.interrupt()

        if index == 2:
            raise self.SshValueError('You must enter a value')

        self._writeln('\n\n\n\n')
        self._to_the_top(self.level)
        return raw

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    sshc = sshconfig(cli_sess)

    # For COEUS product, sshconfig is enabled by default.  Have to disable
    # first.  And then enable.
    sshc().new('ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEAoPWj3H7paui4u6jda9' +
                '/qPY7O8RviJV2RS3KOY/kEDuecaz5b79ceVUGUao/pMw9ZKM6IM4d' +
                'U8CPNJOrzch7Gx8I/jY1tsS65zdDJMr89q=test@test.qa')
    sshc().print_key('1')
    sshc().user()
    sshc().delete('1')
    sshc().sshd_edit_settings()
