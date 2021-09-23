#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
# vim:ts=4:sw=4:expandtab:softtabstop=4:smarttab
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/who.py#1 $

"""
IAF Command Line Interface (CLI)

command:
    - who
"""

import clictorbase


class who(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        raw = ''
        tries = 1
        # look for prompt up to five times
        # if we can't find who info the first time
        while raw.lower().find('username') == -1 and tries <= 5:
            raw += self._sess.read_until()
            tries += 1

        return raw


if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess object is present in namespace, we're using
    # the dev unit test harness, don't get a new one
    # also set valid gateway address to eng env if present, qa if not
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = who(cli_sess)
    # test case
    print cli()
