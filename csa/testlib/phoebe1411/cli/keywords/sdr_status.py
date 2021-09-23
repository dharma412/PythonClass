# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/sdr_status.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

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
