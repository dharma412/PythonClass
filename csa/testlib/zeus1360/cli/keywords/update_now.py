#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/update_now.py#1 $

from common.cli.clicommon import CliKeywordBase

class UpdateNow(CliKeywordBase):
    """Update all the components via CLI."""

    def get_keyword_names(self):
        return [
            'update_now',
        ]

    def update_now(self):
        """Update Now.

        Use this keyword to perform updating of all the components via CLI.

        Example:
        | Update Now |
        """

        self._cli.updatenow()
