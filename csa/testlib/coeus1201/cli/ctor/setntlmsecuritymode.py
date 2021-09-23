#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/setntlmsecuritymode.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
    IAF 2 CLI ctor - setntlmsecuritymode
"""

import clictorbase
from sal.containers.yesnodefault import YES, NO

DEBUG = True

class setntlmsecuritymode(clictorbase.IafCliConfiguratorBase):
    """setntlmsecuritymode
        -  Configures the security mode used while joining to
           the Active Directory server.
    """

    def __call__(self, mode=''):
        self._writeln('setntlmsecuritymode')
        self._query_response('1')
        self._query_select_list_item(mode)
        self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    setntlm = setntlmsecuritymode(cli_sess)
    setntlm(mode='1')
    setntlm(mode='2')
