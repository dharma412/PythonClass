#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/update_now.py#1 $

from common.cli.clicommon import CliKeywordBase


class UpdateNow(CliKeywordBase):
    """Update all the components via CLI."""

    def get_keyword_names(self):
        return ['update_now', ]

    def update_now(self, force=False):
        """
        CLI > updatenow command.

        Use this keyword to perform updating of all the components via CLI.

        *Parameters:*
        - `force`: Force update. Boolean. False by default.

        *Example:*
        | Update Now |
        """

        self._cli.updatenow(force=force)
