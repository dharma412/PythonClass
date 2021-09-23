#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/proxyconfig.py#1 $

"""
    IAF 2 CLI ctor - proxyconfig
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
                IafCliError, IafUnknownOptionError, REQUIRED, DEFAULT
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class proxyconfig(clictorbase.IafCliConfiguratorBase):
    """proxyconfig
        - configure the proxy
    """
    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('proxyconfig')
        self._expect(['Proxy cannot be configured because', 'Choose the operation'])
        if self._expectindex == 0:
            raise clictorbase.IafCliError('The Web Proxy can not be configured because '\
                                   'neither Data or Management interface is configured.')
        return self

    def setup(self, state=''):
        self.newline=0
        self._query_response('SETUP')
        self._query_response(state)
        self._to_the_top(self.newline)

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    pc = proxyconfig(cli_sess)

    pc().setup()
    pc().setup(state='y')
    pc().setup(state='n')


