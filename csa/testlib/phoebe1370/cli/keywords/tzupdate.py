#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/tzupdate.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

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
