#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/sbstatus.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

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
