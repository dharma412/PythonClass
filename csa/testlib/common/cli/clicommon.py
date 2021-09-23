#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/cli/clicommon.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.logging import Logger
from common.arguments import ArgumentParser
import sys

from common.util.misc import Misc

from sal.containers.yesnodefault import YES, NO

DEFAULT = ''


class CliKeywordBase(Logger, ArgumentParser):
    # class level dictionary
    # all CLI test libraries will work with single dictionary instance
    __shared_state = {}

    def __init__(self, dut, dut_version):
        # dut info attributes
        self.dut = dut
        self.dut_version = dut_version

        if not CliKeywordBase.__shared_state.has_key(self.dut):
            self.start_cli_session()

    # RF Hybrid API for Test Libraries
    def get_keyword_names(self):
        return [
            'start_cli_session',
            'start_cli_session_if_not_open',
            'close_cli_session',
            'restart_cli_session',
            'reset_expired_passphrase_from_cli',
            'reset_passphrase_on_expiry_reminder_from_cli',
            'interrupt_cli',
            'write_to_cli',
            'read_from_cli',
        ]

    def interrupt_cli(self):
        self._cli.get_sess().interrupt()
        return

    def write_to_cli(self, command_string):
        self._cli.get_sess().writeln(command_string)
        return

    def read_from_cli(self):
        return self._cli.get_sess().getbuf()

    # keywords
    def start_cli_session(self, user='admin', password=None):
        self._info('Username:' + str(user))
        self._info('Password:' + str(password))
        if user == 'admin' and password is None:
            password = self.get_admin_password()
        try:
            self._cli = self._get_ironcli(user, password)
            return True
        except:
            self._info('CLI session could not be started ' + str(sys.exc_info()))
            self._cli = _NoCliSession()
            return False

    def reset_passphrase_on_expiry_reminder_from_cli(self, user='admin', password=None, reset='True'):
        """This keyword is used to reset password from CLI
            when the password expiry banner is seen while logging into dut

        Parameters: None
        Usage: Reset Passphrase On Expiry Reminder From Cli
        """
        try:
            if user == 'admin' and password is None:
                password = self.get_admin_password()
            lib_path = self.dut_version
            cli_module = __import__(lib_path + '.cli.cli', globals(), locals(),
                                    ['get_cli'], -1)
            if reset == 'True':
                ironcli = cli_module.get_cli(self.dut, user, password, reset_password=True)
            elif reset == 'False':
                ironcli = cli_module.get_cli(self.dut, user, password, reset_password=False)
            self._cli = ironcli
        except:
            self._info('CLI session could not be started ' + str(sys.exc_info()))
            self._cli = _NoCliSession()

    def reset_expired_passphrase_from_cli(self, user='admin', password=None):
        """This keyword is used to reset expired password from CLI

        Parameters: None
        Usage: Reset Expired Passphrase From Cli
        """
        try:
            if user == 'admin' and password is None:
                password = self.get_admin_password()
            lib_path = self.dut_version
            cli_module = __import__(lib_path + '.cli.cli', globals(), locals(),
                                    ['get_cli'], -1)
            ironcli = cli_module.get_cli(self.dut, user, password, reset_password=True)
            self._cli = ironcli
        except:
            self._info('CLI session could not be started ' + str(sys.exc_info()))
            self._cli = _NoCliSession()

    def start_cli_session_if_not_open(self, user='admin', password=None):
        self._info('Username:' + str(user))
        self._info('Password:' + str(password))
        if user == 'admin' and password is None:
            password = self.get_admin_password()
        # check whether _cli is open
        if self._is_cli_session_open():
            self._info('CLI session is still open')
        else:
            self._info('CLI session was closed. Trying to restart it...')
            try:
                self._cli = self._get_ironcli(user, password)
                self._info('CLI session was successfully restarted')
            except:
                self._info('CLI session could not be started ' + str(sys.exc_info()))
                self._cli = _NoCliSession()
                raise

    def close_cli_session(self):
        try:
            self._cli.close()
        except:
            self._info("CLI session could not be closed " + str(sys.exc_info()))
            self._cli = _NoCliSession()

    def restart_cli_session(self):
        self.close_cli_session()
        self.start_cli_session()

    # helper methods
    def _is_cli_session_open(self):
        if isinstance(self._cli, _NoCliSession):
            # cli session could not be opened when start_cli_session was
            # called
            self._debug('self._cli is instance of _NoCliSession class.')
            return False
        else:
            try:
                self._cli.version()
                # cli session is open
                return True
            except:
                # exception occurs when accesing to cli session
                self._debug('Exception occurs when running version command.')
                return False

    # custom processing for _cli atrribute
    def __getattr__(self, name):
        if name == '_cli':
            return CliKeywordBase.__shared_state[self.dut]['ironcli']
        else:
            raise AttributeError("'%s' instance has no attribute '%s'" % \
                                 (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if name == '_cli':
            CliKeywordBase.__shared_state[self.dut] = {'ironcli': value}
        else:
            self.__dict__[name] = value

    def _get_ironcli(self, user='admin', password=None):
        if user == 'admin' and password is None:
            password = self.get_admin_password()
        lib_path = self.dut_version
        cli_module = __import__(lib_path + '.cli.cli', globals(), locals(),
                                ['get_cli'], -1)
        ironcli = cli_module.get_cli(self.dut, user, password)
        return ironcli

    # arguments processing methods
    def _process_yes_no(self, yes_no):
        choose = yes_no.lower()[:1]
        if choose == 'y' or choose == 'n':
            return choose.upper()
        elif choose == 'd' or choose == '':
            return ''
        else:
            raise ValueError("Incorrect value %s. Expected either Yes, No or "
                             "Default" % (choose,))

    def _convert_to_dict(self, args):
        kwargs = {}
        for arg in args:
            pos = arg.find('=')
            if pos >= 0:
                kwargs[str(arg[:pos])] = str(arg[pos + 1:])
            else:
                raise ValueError('Only named argumnets are accepted')
        return kwargs

    def _set_yes_no_object(self, value):
        if self._process_yes_no(value) == 'Y':
            return YES
        elif self._process_yes_no(value) == 'N':
            return NO

    def get_admin_password(self):
        return Misc(None, None).get_admin_password(self.dut)


class _NoCliSession(object):
    def __getattr__(self, name):
        raise RuntimeError('No CLI session is open')

    def __nonzero__(self):
        return False
