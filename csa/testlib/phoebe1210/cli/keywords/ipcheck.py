#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/ipcheck.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class ipcheck(CliKeywordBase):
    """Display hardware and product configuration details."""

    def get_keyword_names(self):
        return ['ipcheck']

    def ipcheck(self):
        """Display hardware and product configuration details

        *Return:*
        Raw output

        *Examples:*
        | ${info}= | IPCheck |
        | Log | ${info} |
        """
        return self._cli.ipcheck()
