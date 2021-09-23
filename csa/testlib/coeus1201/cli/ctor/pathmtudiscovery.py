#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/pathmtudiscovery.py#1 $

"""
    pathmtudiscovery
"""

import clictorbase
from sal.containers.yesnodefault import YES, NO

class pathmtudiscovery(clictorbase.IafCliConfiguratorBase):

    def __call__(self, answer=clictorbase.DEFAULT):
        self._writeln('pathmtudiscovery')
        self._query_response(answer)
        self._wait_for_prompt()

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    pmd = pathmtudiscovery(cli_sess)
    pmd()
    pmd(answer=YES)
    pmd(answer=NO)
