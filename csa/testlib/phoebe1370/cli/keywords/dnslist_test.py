#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/dnslist_test.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase
import traceback

class DnsListTest(CliKeywordBase):
    """
    dnslisttest <query server> <test IP address>

    Test a DNS lookup for a DNS-based list service.

    """

    def get_keyword_names(self):
        return ['dnslist_test',
               ]

    def dnslist_test(self, *args):
        """
        dnslisttest

        *Parameters:*
        - `server`: Enter the query server name
        - `ip` : Enter the test IP address to query for

        *Returns*:
          Dictionary with following component as keys:
          - `query_str`
          - `result`

        *Examples*:
        | ${Status}= | dnslist_test | server=tinydns.qa | ip=1.1.1.1 |
        """
        kwargs = self._convert_to_dict(args)
        try:
            return dict(self._cli.dnslisttest(**kwargs))
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e
