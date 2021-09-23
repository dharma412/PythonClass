#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/tzupdate.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

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
