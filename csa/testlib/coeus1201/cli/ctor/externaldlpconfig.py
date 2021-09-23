#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/externaldlpconfig.py#1 $

"""
    externaldlpconfig
"""

import clictorbase

class externaldlpconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self, size=clictorbase.DEFAULT):
        self._writeln('externaldlpconfig')
        self._query_response(size)
        self._wait_for_prompt()

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    edc = externaldlpconfig(cli_sess)
    edc()
    edc(size=1200)
