#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/suspend.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class Suspend(CliKeywordBase):

    """Keywords for suspend CLI command."""

    def get_keyword_names(self):
        return ['suspend',]

    def suspend(self, delay=None):
        """Suspend receiving and delivery.

        Parameters:
        - `delay`: maximum number of seconds to wait for connections to close
           before doing a forceful disconnect.

        Examples:
        | Suspend |
        | Suspend | 10 |
        """
        self._cli.suspend(delay)

