#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/dns_status.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

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
