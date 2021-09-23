#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/isedata.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase

class IseData(CliKeywordBase):
    """
    cli -> isedata

    """

    def get_keyword_names(self):
        return [
            'isedata_cache_clear',
            'isedata_cache_show',
            'isedata_sgts',
            'isedata_checkip',
        ]

    def isedata_cache_clear(self):
        """Clear the current ISE ID cache

        Examples:
        | ISE Data Cache Clear |
        """

        return self._cli.isedata().cache_clear()

    def isedata_cache_show(self):
        """Show the ISE ID cache

        Examples:
        | ISE Data Cache Show |
        """

        return self._cli.isedata().cache_show()

    def isedata_sgts(self):
        """Show the ISE SGT table

        Examples:
        | ISE Data SGTS |
        """

        return self._cli.isedata().sgts()

    def isedata_checkip(self, ip_address):
        """Show cache for a given IP Address

        Examples:
        |  ISE Data CheckIP  |  172.191.201.221  |
        """
        return self._cli.isedata().checkip(ip_address)

