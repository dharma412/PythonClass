#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/rangerequestdownload.py#1 $

"""
    rangerequestdownload
"""

import clictorbase
from sal.containers.yesnodefault import YES, NO

class rangerequestdownload(clictorbase.IafCliConfiguratorBase):

    def __call__(self, answer=clictorbase.DEFAULT):
        self._writeln('rangerequestdownload')
        self._query_response(answer)
        self._wait_for_prompt()

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    rrd = rangerequestdownload(cli_sess)
    rrd()
    rrd(answer=YES)
    rrd(answer=NO)
