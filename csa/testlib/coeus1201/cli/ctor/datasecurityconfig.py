#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/datasecurityconfig.py#1 $

"""
    datasecurityconfig
"""

import clictorbase

class datasecurityconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self, size=clictorbase.DEFAULT):
        self._writeln('datasecurityconfig')
        self._query_response(size)
        self._wait_for_prompt()

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ds = datasecurityconfig(cli_sess)
    ds()
    ds(size=1200)
