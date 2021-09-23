# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/sdr_status.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class SdrStatus(CliKeywordBase):
    """Get status of Sender Domain Repuataion engine via CLI."""

    def get_keyword_names(self):
        return ['sdrstatus']

    def sdrstatus(self):
        """
        CLI > sdrstatus command.

        Use this keyword to get the status of Sender Domain Repuataion engine via CLI.

        *Parameters:*
        - none

        *Return:*
        - Return the status of Sender Domain Repuataion engine.

        *Example:*
        | ${sdr_status}= | Sdrstatus     |
        | Log            | ${sdr_status} |
        """

        return self._cli.sdrstatus()
