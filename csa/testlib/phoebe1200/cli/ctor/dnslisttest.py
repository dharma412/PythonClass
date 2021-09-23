#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/dnslisttest.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $
"""
IAF2 CLI command dnslisttest
"""

import re
from sal.containers import cfgholder
from sal.containers.yesnodefault import YES, NO
import clictorbase

DEFAULT = clictorbase.DEFAULT
REQUIRED = clictorbase.REQUIRED


class dnslisttest(clictorbase.IafCliConfiguratorBase):

    def __call__(self, server=REQUIRED, ip=DEFAULT):
        self._writeln(self.__class__.__name__)
        self._query_response(server)
        self._query_response(ip)
        return self._parse_result(self._read_until())

    def _parse_result(self, raw):
        reg = re.search('Querying: (?P<query_str>.*?)Result: (?P<result>.*)',
                        raw, re.DOTALL)
        if reg:
            return cfgholder.CfgHolder(
                {'query_str': reg.group('query_str').strip(),
                 'result': reg.group('result').strip(),
                 })
        return raw


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    dt = dnslisttest(cli_sess)
    out = dt(server='tinydns.qa')
    print out.result
