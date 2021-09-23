# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/sdr_status.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

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
