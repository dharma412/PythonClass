#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/repeng_update.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class RepengUpdate(CliKeywordBase):
    """Update repeng modules"""

    def get_keyword_names(self):
        return ['repeng_update', ]

    def repeng_update(self, force=False):
        """Update Repeng modules

        *Parameters:*
        - `force`: Whether to apply forced update. ${False} by default

        *Return:*
        - CLI command output as a string

        *Examples:*
        | ${output}= | Repeng Update |
        | Repeng Update | force=${True} |
        """
        return self._cli.repengupdate(force)

