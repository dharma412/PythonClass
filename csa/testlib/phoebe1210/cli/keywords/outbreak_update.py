#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/outbreak_update.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
SARF CLI command: outbreakupdate
"""

from common.cli.clicommon import CliKeywordBase


class OutbreakUpdate(CliKeywordBase):
    """
    Request an immediate update of CASE rules and engine core.

    CLI command: outbreakupdate
    """

    def get_keyword_names(self):
        return ['outbreak_update', ]

    def outbreak_update(self, *args):
        """Request an immediate update of CASE rules and engine core.

        CLI command: outbreakupdate

        *Parameters:*
        - `force`: Force updates. YES or NO.

        *Return:*
        True(Boolean) if requested successfully.
        Else raise an exception.

        *Examples:*
        | Outbreak Update | force=yes |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.outbreakupdate(**kwargs)
