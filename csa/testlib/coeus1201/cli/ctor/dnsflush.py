#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/dnsflush.py#1 $

"""
    IAF 2 CLI ctor - dnsflush
"""

import clictorbase
from sal.containers.yesnodefault import YES, NO

class dnsflush(clictorbase.IafCliConfiguratorBase):
    global YES, NO

    def __call__(self, sure=YES):
        self._writeln('dnsflush')
        self._query_response(sure)
        self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    df = dnsflush(cli_sess)
    df(sure=NO)
    df(sure=YES)
