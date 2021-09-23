# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/beaker_status.py#1 $
# DateTime: $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase

class BeakerStatus(CliKeywordBase):
    """Get status of Beaker Client via CLI."""

    def get_keyword_names(self):
        return ['beaker_status']

    def beaker_status(self):
        """
        CLI > beaker_status command.

        Use this keyword to get the status of Beaker Client via CLI.

        *Parameters:*
        - none

        *Return:*
        - Return the status of Beaker Client.

        *Example:*
        | ${beaker_status} |  Beaker Status |
        """

        return self._cli.beakerstatus()
