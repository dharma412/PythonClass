#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/sbstatus.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
IAF Command Line Interface (CLI)

command:
    - sbstatus
"""

import clictorbase


class sbstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        return self._wait_for_prompt()
