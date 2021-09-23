# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/ec_update.py#1 $ $ DateTime: 2014/04/04 23:59:59 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class EcUpdate(CliKeywordBase):
    """Update Enrollment Client via CLI."""

    def get_keyword_names(self):
        return ['ecupdate']

    def ecupdate(self, force=False):
        """
        CLI > ecupdate command.

        Use this keyword to perform updating of Enrillment Client via CLI.

        *Parameters:*
        - `force`: Force update. Boolean. False by default.

        *Example:*
        | Ecupdate |
        | Ecupdate | force |
        """

        self._cli.ecupdate(force=force)
