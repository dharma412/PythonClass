#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/who.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
SARF CLI command: who
"""

import clictorbase

class who(clictorbase.IafCliConfiguratorBase):
    """
    Returns the List who is logged in
    """
    def __call__(self):
        self.clearbuf
        result = ''
        self._writeln("who")

        # Removing input (first 2 lines) and final prompt (last line)
        lines = self._wait_for_prompt().split("\n")
        for number in range(2,len(lines) - 1):
            result += lines[number]

        return result
