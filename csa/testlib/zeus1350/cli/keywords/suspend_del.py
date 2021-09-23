#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/suspend_del.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class SuspendDel(CliKeywordBase):
    """Keywords for suspenddel CLI command."""

    def get_keyword_names(self):
        return ['suspend_del', ]

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
