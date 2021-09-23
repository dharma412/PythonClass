#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/stripheaders.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
SARF CLI command: stripheaders
"""


import clictorbase
from clictorbase import REQUIRED, IafCliError, IafCliConfiguratorBase,\
    IafCliCtorNotImplementedError

from sal.deprecated.expect import EXACT
DEBUG = True

class stripheaders(clictorbase.IafCliConfiguratorBase):
    """
    CLI command: stripheaders
    """
    class MinHeadersError(IafCliError): pass
    class MaxHeadersError(IafCliError): pass

    newlines = 1

    def __init__(self, sess):

        # use the correct scoping for IafCliConfiguratorBase
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
             ('You must configure at least', EXACT) : self.MinHeadersError,
             ('You can configure only up to', EXACT) : self.MaxHeadersError,
             })

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, headers=REQUIRED):
        self._query_response('SETUP')
        self._query_response(headers)
        self._to_the_top(self.newlines)

    def clusterset(self):

        raise IafCliCtorNotImplementedError

    def clustershow(self):

        raise IafCliCtorNotImplementedError

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    sh = stripheaders(cli_sess)
    sh().setup(headers='from')
    sh().setup(headers='delete')

