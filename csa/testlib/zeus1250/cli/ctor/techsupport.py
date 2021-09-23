#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/techsupport.py#3 $

"""
    techsupport IAF 2 configurator
"""
from sal.containers.yesnodefault import YES
from sal.deprecated.expect import EXACT
import clictorbase as ccb
from clictorbase import IafCliConfiguratorBase, IafCliError, \
    REQUIRED, DEFAULT

DEBUG = True

class techsupport(ccb.IafCliConfiguratorBase):


    class NoStateError(ccb.IafCliError): pass
    class FailedToEnableError(ccb.IafCliError): pass
    class FailedToDisableError(ccb.IafCliError): pass


    newlines = 1

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
             ('Unable to retrieve current state', EXACT) : self.NoStateError,
             ('Failed to enable service access', EXACT) :
                                                    self.FailedToEnableError,
             ('Failed to disable service access', EXACT) :
                                                    self.FailedToDisableError,
             })
        self.do_tunnel = False

    def __call__(self, param=''):
        if param:
            self.do_tunnel = True
        self._writeln('techsupport ' + param)
        return self

    def sshaccess(self, temp_pwd=REQUIRED, confirm=DEFAULT):
        from sal.containers.yesnodefault import YES
        import time

        self._query_response('SSHACCESS')
        self._query_response('2')
        self._query_response(temp_pwd)
        self._query_response(confirm)
        # XXX old comment form ironport.py:
        # it takes about 15 secs for ssh tunnel to connect
        if (confirm == YES) and self.do_tunnel:
            time.sleep(15)
        self._to_the_top(self.newlines)

    def disable(self, confirm=DEFAULT):
        self._query_response('DISABLE')
        self._query_response(confirm)
        self._to_the_top(self.newlines)

    def status(self):
        self._query_response('STATUS')
        lines = self._read_until('Choose the operation you want to perform')
        self._to_the_top(self.newlines)
        return lines

    def tunnel(self, temp_pwd=REQUIRED, port='', confirm=DEFAULT, delay=5):
        import time
        self._query_response('TUNNEL')
        self._query_response('2')
        self._query_response(temp_pwd)
        self._query_response(port)
        self._query_response(confirm)
        time.sleep(delay)
        self._sess.interrupt()


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    ts = techsupport(cli_sess)
    print ts().sshaccess(temp_pwd='1234356', confirm=YES)
    print ts().disable(confirm=YES)
    print ts().tunnel(temp_pwd='1234356', confirm=YES)
    print ts().disable(confirm=YES)
    print ts().status()
