#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/ipcheck.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
