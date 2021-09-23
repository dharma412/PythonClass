# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/ec_status.py#1 $ $ DateTime: 2014/04/04 23:59:59 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class EcUpdate(CliKeywordBase):
    """Get status of Enrollment Client via CLI."""

    def get_keyword_names(self):
        return ['ecstatus']

    def ecstatus(self):
        """
        CLI > ecstatus command.

        Use this keyword to get the status of Enrollment Client via CLI.

        *Parameters:*
        - none

        *Return:*
        - Return the status of enrollment client.

        *Example:*
        | Ecstatus |
        """

        return self._cli.ecstatus()
