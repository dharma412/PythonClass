#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/techsupport.py#1 $

"""
    techsupport IAF 2 configurator
"""

from sal.containers.yesnodefault import YES
import clictorbase as ccb
from clictorbase import IafCliConfiguratorBase, IafCliError, \
                                REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT

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

    def sshaccess(self, tmp_passwd=REQUIRED, confirm=DEFAULT):
        from sal.containers.yesnodefault import YES
        import time

        self._query_response('SSHACCESS')
        # Temp fix to avoid BAT runs. The keyword needs
        # to be enhanced for the recent change in CLI work flow.
        self._query_response('2')
        self._query_response(tmp_passwd)
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

    def tunnel(self, tmp_passwd='123456', port_num=DEFAULT, delay=20):
        from sal.containers.yesnodefault import YES
        import time
        self._query_response('TUNNEL')
        # Temp fix to avoid BAT runs. The keyword needs
        # to be enhanced for the recent change in CLI work flow.
        self._query_response('2')
        self._query_response(tmp_passwd)
        self._query_response(port_num)
        self._query_response(YES)
        # Delay time increased drastically need further investigation on performance side
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
    print ts().tunnel()
    print ts().status()
    print ts().disable(confirm=YES)
    print ts().status()
