# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/beaker_update.py#1 $
# $ DateTime: $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase

class BeakerUpdate(CliKeywordBase):
    """Update Beaker Client via CLI."""

    def get_keyword_names(self):
        return ['beaker_update']

    def beaker_update(self, force=False):
        """
        CLI > beakerupdate command.

        Use this keyword to perform updating of Beaker Client via CLI.

        *Parameters:*
        - `force`: Force update. Boolean. False by default.

        *Example:*
        | Beaker Update |
        | Beaker Update | force=${True} |
        """

        self._cli.beakerupdate(force=force)
