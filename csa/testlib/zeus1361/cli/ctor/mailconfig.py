#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/mailconfig.py#1 $

"""
IAF 2 CLI command: mailconfig
"""

import clictorbase
import socket

from sal.containers.yesnodefault import YES, NO

class mailconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self, email='test@test.qa', mask_pw=NO):
        self._sess.writeln('mailconfig')
        self._query_response(email)
        self._query_response(mask_pw, timeout=10)
        self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    mconfig = mailconfig(cli_sess)
    recip = 'test@' + socket.gethostname()
    mconfig(email=recip, save_pw='Y')

