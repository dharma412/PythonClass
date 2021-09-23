# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/sdr_update.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class SdrUpdate(CliKeywordBase):
    """Update Sender Domain Reputation engine via CLI."""

    def get_keyword_names(self):
        return ['sdrupdate']

    def sdrupdate(self, force=False):
        """
        CLI > sdrupdate command.

        Use this keyword to perform updating of Sender Domain Reputation engine via CLI.

        *Parameters:*
        - `force`: Force update. Boolean. False by default.

        *Example:*
        | Sdrupdate |
        | Sdrupdate | force |
        """

        self._cli.ecupdate(force=force)
