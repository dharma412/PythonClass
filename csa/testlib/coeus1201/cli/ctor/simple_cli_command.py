#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/simple_cli_command.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
    Execute a cli command and return its output.
    Optionally interrupt if break_timeout is specified
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase
import time

DEBUG = True


class simple_cli_command(clictorbase.IafCliConfiguratorBase):

    def __call__(self, command, break_timeout=None):
        self._writeln(command)
        if break_timeout:
            time.sleep(float(break_timeout))
            self._sess.interrupt()
        return self._wait_for_prompt()
