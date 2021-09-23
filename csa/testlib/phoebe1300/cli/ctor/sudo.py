#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/sudo.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
SARF CLI command: sudo
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliError, REQUIRED
from sal.containers.yesnodefault import YES, NO, is_yes

DEBUG = True

from sal.exceptions import ConfigError
from sal.deprecated.expect import EXACT, REGEX


class sudo(clictorbase.IafCliConfiguratorBase):
    class WrongPasswordError(IafCliError):
        pass

    class BadCommandError(IafCliError):
        pass

    def __init__(self, sess):

        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:  # dev box
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('Sorry, try again', EXACT): self.WrongPasswordError,
            ('Bad command', EXACT): self.BadCommandError,
        })

    def __call__(self,
                 cmd=REQUIRED,
                 password=REQUIRED,
                 need_interrupt=NO,
                 interrupt_interval=5):
        import time
        self.clearbuf()
        self._writeln('sudo')
        self._query('>')
        self._writeln(cmd)
        time.sleep(2)
        self._writeln(password)
        first_output_line = ''
        if is_yes(need_interrupt):
            time.sleep(int(interrupt_interval))
            self.interrupt()
        return first_output_line + self._wait_for_prompt()


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    sd = sudo(cli_sess)
    # 'sudo date' not supported on 4.8
    # print sd(cmd='date', password='ironport', need_interrupt=False)
    print sd(cmd='ps', password='1psupp0rt', need_interrupt=False)
    print sd(cmd='top', password='1psupp0rt', need_interrupt=True)
