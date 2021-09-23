#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/outbreak_status.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

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
        return ['outbreak_status',]

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