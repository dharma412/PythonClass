#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/repeng_update.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

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
