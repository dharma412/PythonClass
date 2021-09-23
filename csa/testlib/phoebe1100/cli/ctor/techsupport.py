#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/techsupport.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
    techsupport IAF 2 configurator
"""
from sal.containers.yesnodefault import YES
from sal.deprecated.expect import EXACT
import clictorbase as ccb
from clictorbase import IafCliConfiguratorBase, IafCliError, \
    REQUIRED, DEFAULT


class techsupport(ccb.IafCliConfiguratorBase):
    class NoStateError(ccb.IafCliError):
        pass

    class FailedToEnableError(ccb.IafCliError):
        pass

    class FailedToDisableError(ccb.IafCliError):
        pass

    newlines = 1

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('Unable to retrieve current state', EXACT): self.NoStateError,
            ('Failed to enable service access', EXACT):
                self.FailedToEnableError,
            ('Failed to disable service access', EXACT):
                self.FailedToDisableError,
        })

    def __call__(self):
        self._writeln('techsupport')
        return self

    def tunnel(self, temp_pwd=DEFAULT, port_number=REQUIRED, confirm=DEFAULT, password_option=DEFAULT):
        self._query_response('TUNNEL')
        if password_option == 'random_generated':
            self._query_response('1')
            self._query_response(port_number)
            self._query_response(confirm)
        elif password_option == 'user_input':
            self._query_response('2')
            self._query_response(temp_pwd)
            self._query_response(port_number)
            self._query_response(confirm)
        lines = self._read_until('Choose the operation you want to perform')
        lines = lines.partition('string:')[2]
        lines = lines.partition('to your Cisco')[0]
        self._to_the_top(self.newlines)
        return lines

    def sshaccess(self, temp_pwd=DEFAULT, confirm=DEFAULT, password_option=DEFAULT):
        self._query_response('SSHACCESS')
        if password_option == 'random_generated':
            self._query_response('1')
            self._query_response(confirm)
        elif password_option == 'user_input':
            self._query_response('2')
            self._query_response(temp_pwd)
            self._query_response(confirm)
        lines = self._read_until('Choose the operation you want to perform')
        lines = lines.partition('string:')[2]
        lines = lines.partition('to your Cisco')[0]
        self._to_the_top(self.newlines)
        return lines

    def disable(self, confirm=DEFAULT):
        self._query_response('DISABLE')
        self._query_response(confirm)
        self._to_the_top(self.newlines)

    def status(self):
        self._query_response('STATUS')
        lines = self._read_until('Choose the operation you want to perform')
        self._to_the_top(self.newlines)
        return lines


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    ts = techsupport(cli_sess)
    pdb.set_trace()
    ts().tunnel(temp_pwd='123456', port_number=25, confirm=YES)
    print ts().status()
    ts().disable(confirm=YES)
    ts().sshaccess(temp_pwd='123456', confirm=YES)
    print ts().status()
    ts().disable(confirm=YES)
