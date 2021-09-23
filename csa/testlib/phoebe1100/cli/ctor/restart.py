#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
# vim:ts=4:sw=4:expandtab:softtabstop=4:smarttab
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/restart.py#1 $

"""
IAF Command Line Interface (CLI)

Usually files here are used one per CLI command. However,
this restart.py module is here to give easy access to the
test modules to exit out of any command.

"""

__version__ = "Revision: $"
# $Source: /cvsroot/iaf2/libipt/phoebe55/cli/ctor/restart.py,v $
__revision = '$Revision: #1 $'
import clictorbase


class restart(clictorbase.IafCliConfiguratorBase):
    def __call__(self, save_changes=False):
        if save_changes:
            self._restart()
        else:
            self._restart_nosave()


if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    cli = restart(clictorbase.get_sess())
    # test case
    print cli()
