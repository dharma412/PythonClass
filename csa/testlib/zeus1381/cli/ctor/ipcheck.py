#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
# vim:ts=4:sw=4:expandtab:softtabstop=4:smarttab
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/ipcheck.py#1 $

"""
IAF Command Line Interface (CLI)

command:
    - ipcheck
"""

import clictorbase

class ipcheck(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        return self._wait_for_prompt()

if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = ipcheck(cli_sess)
    # test case
    print cli()
