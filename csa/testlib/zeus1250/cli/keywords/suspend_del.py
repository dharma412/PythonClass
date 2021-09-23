#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/suspend_del.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

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

