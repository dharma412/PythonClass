#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/sbstatus.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

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
