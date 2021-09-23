#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/tzupdate.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Tzupdate(CliKeywordBase):
    """Timezone rules update."""

    def get_keyword_names(self):
        return ['tzupdate',]

    def tzupdate(self, force=False):
        """Request manual update of Timezone rules.

        tzupdate

        Parameters:
        - `force`: update even if no changes are detected. Either 'True' or 'False'.

        Examples:
        | Tzupdate | force=${True} |
        """

        self._info(self._cli.tzupdate(force))
