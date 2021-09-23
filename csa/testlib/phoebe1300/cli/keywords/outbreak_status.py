#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/outbreak_status.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

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
