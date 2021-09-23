#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/diagnostic.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
IAF 2 CLI command: diagnostic
"""

import clictorbase as ccb
from sal.deprecated.expect import EXACT
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO, DEFAULT

class diagnostic(ccb.IafCliConfiguratorBase):

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self.clearbuf()
        self._writeln('diagnostic')
        return self

    def net(self):
        self._query_response('NET')
        return netDiagnostic(self._get_sess())

    def proxy(self):
        self._query_response('PROXY')
        return proxyDiagnostic(self._get_sess())

    def reporting(self):
        self._query_response('REPORTING')
        return reportingDiagnostic(self._get_sess())

class netDiagnostic(ccb.IafCliConfiguratorBase):
    newlines = 2

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {('Capture already running', EXACT): ConfigError,
             ('Capture Not Running', EXACT): ConfigError})

    def start(self):
        self._query_response('START')
        self._to_the_top(self.newlines)

    def stop(self):
        self._query_response('STOP')
        self._to_the_top(self.newlines)

    def status(self):
        self._query_response('STATUS')
        self._to_the_top(self.newlines)

    def filter(self, filter=''):
        self._query_response('FILTER')
        self._writeln(filter)
        self._to_the_top(self.newlines)

    def interface(self, if_name=''):
        self._query_response('INTERFACE')
        self._writeln(if_name)
        self._to_the_top(self.newlines)

    def clear(self, confirm=YES):
        self._query_response('CLEAR')
        while self._query(self._sub_prompt, 'Do you want to remove '):
            self._writeln(confirm)
        self._to_the_top(self.newlines)

class proxyDiagnostic(ccb.IafCliConfiguratorBase):
    newlines = 2

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {('Proxy is already offline', EXACT): ConfigError,
             ('Proxy is already resumed', EXACT): ConfigError})

    def snap(self, timeout=120):
        self._query_response('SNAP')
        self._to_the_top(self.newlines, timeout)

    def offline(self, timeout=120):
        self._query_response('OFFLINE')
        self._to_the_top(self.newlines, timeout)

    def resume(self, timeout=120):
        self._query_response('RESUME')
        self._to_the_top(self.newlines, timeout)

    def cache(self, timeout=120):
        self._query_response('CACHE')
        self._to_the_top(self.newlines, timeout)

class reportingDiagnostic(ccb.IafCliConfiguratorBase):
    newlines = 2

    def deletedb(self, confirm=YES, timeout=120):
        self._query_response('DELETEDB')
        self._query("This command will delete all reporting data")
        self._writeln(confirm)
        self._to_the_top(self.newlines, timeout)

    def disable(self, timeout=120):
        self._query_response('DISABLE')
        self._to_the_top(self.newlines, timeout)

    def enable(self, timeout=120):
        self._query_response('ENABLE')
        self._to_the_top(self.newlines, timeout)


if __name__ == '__main__':

    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    dg = diagnostic(cli_sess)

    dg().proxy().offline()
    dg().proxy().resume()
    dg().proxy().cache()

    dg().reporting().deletedb(YES)
    dg().reporting().disable()
    dg().reporting().enable()

    dg().net().start()
    dg().net().status()
    dg().net().stop()
    dg().net().clear(YES)

