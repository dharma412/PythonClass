#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/ldapflush.py#1 $

"""
IAF 2 CLI command: ldapflush
"""

import clictorbase
from sal.containers.yesnodefault import YES, NO


class ldapflush(clictorbase.IafCliConfiguratorBase):
    def __call__(self, flush=YES):
        self._sess.writeln('ldapflush')
        self._query_response(flush)
        self._wait_for_prompt()


if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    flusher = ldapflush(cli_sess)
    flusher(flush=NO)
    flusher(flush=YES)
