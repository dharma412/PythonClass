#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
# vim:ts=4:sw=4:expandtab:softtabstop=4:smarttab
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/domainredirect.py#1 $

"""
IAF Command Line Interface (CLI)

command:
    - domainredirect
"""

__version__ = "$Revision: #1 $"
# $Source: /cvsroot/iaf2/libipt/phoebe55/cli/ctor/domainredirect.py,v $

__revision = '$Revision: #1 $'

import clictorbase


class domainredirect(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        self._wait_for_prompt()
        return False


if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    cli = domainredirect(clictorbase.get_sess())
    # test case
    print cli()
