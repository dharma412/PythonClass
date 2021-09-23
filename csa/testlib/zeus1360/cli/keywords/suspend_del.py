#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/suspend_del.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class SuspendDel(CliKeywordBase):

    """Keywords for suspenddel CLI command."""

    def get_keyword_names(self):
        return ['suspend_del',]

    def suspend_del(self, delay=None):
        """Suspend delivery.

        Parameters:
        - `delay`: maximum number of seconds to wait for connections to close
           before doing a forceful disconnect.

        Examples:
        | Suspend Del |
        | Suspend Del | 10 |
        """
        self._cli.suspenddel(delay)

