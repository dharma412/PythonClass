#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/ipcheck.py#3 $

from common.cli.clicommon import CliKeywordBase

class IpCheck(CliKeywordBase):
    """Display hardware and product configuration details."""

    def get_keyword_names(self):
        return ['ipcheck', ]

    def ipcheck(self):
        """Ipcheck

        Use this keyword to display hardware and product configuration details.

        Example:
        | Ipcheck |
        """

        output = self._cli.ipcheck()
        return output
