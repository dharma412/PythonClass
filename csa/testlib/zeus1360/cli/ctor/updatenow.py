#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/updatenow.py#1 $

"""
    IAF 2 CLI ctor - updatenow
"""

import clictorbase

class updatenow(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._sess.writeln('updatenow')
        self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    un = updatenow(cli_sess)
    un()
