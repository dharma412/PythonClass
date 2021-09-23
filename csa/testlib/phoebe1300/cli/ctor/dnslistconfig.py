#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/dnslistconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
IAF 2 CLI command: dnslistconfig
"""

import clictorbase
from clictorbase import DEFAULT, IafCliConfiguratorBase

DEBUG = True


class dnslistconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('dnslistconfig')
        return self

    def setup(self, ttl=DEFAULT, timeout=DEFAULT):
        self.newlines = 1
        self._query_response('SETUP')
        self._query_response(ttl)
        self._query_response(timeout)
        self._to_the_top(self.newlines)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    dnslc = dnslistconfig(cli_sess)

    dnslc().setup(ttl='60', timeout='20')
