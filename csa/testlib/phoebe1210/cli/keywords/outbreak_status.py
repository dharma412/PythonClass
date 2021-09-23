#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/outbreak_status.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
SARF CLI command: outbreakstatus
"""

from common.cli.clicommon import CliKeywordBase


class OutbreakStatus(CliKeywordBase):
    """
    Get the Outbreak Filters status.

    CLI command: outbreakstatus
    """

    def get_keyword_names(self):
        return ['outbreak_status', ]

    def outbreak_status(self):
        """Get Outbreak Filters status.

        CLI command: outbreakstatus

        *Parameters:*
        None

        *Return:*
        Raw output.

        *Examples:*
        | ${status}=  | Outbreak Status |
        | Log  ${status} |
        """
        return self._cli.outbreakstatus()
