#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/tzupdate.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class Tzupdate(CliKeywordBase):
    """Timezone rules update."""

    def get_keyword_names(self):
        return ['tzupdate', ]

    def tzupdate(self, force=False):
        """Request manual update of Timezone rules.

        tzupdate

        Parameters:
        - `force`: update even if no changes are detected. Either 'True' or 'False'.

        Examples:
        | Tzupdate | force=${True} |
        """

        self._info(self._cli.tzupdate(force))
