#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/dns_status.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class DnsStatus(CliKeywordBase):
    """ Keyword for dnsstatus CLI command.
    """

    def get_keyword_names(self):
        return ['dnsstatus']

    def dnsstatus(self):
        """Display DNS statistics.

        Return:
            DNS statistics.

        Examples:
        | ${status}= | dnsstatus |
        """
        return self._cli.dnsstatus()
