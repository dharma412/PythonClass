#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/quotaquery.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class QuotaQuery(CliKeywordBase):
    """Configure local users that are allowed to use the system.
    """

    def get_keyword_names(self):
        return [
            'quota_reset',
            'quota_resetall',
            'quota_search',
        ]

    def quota_reset(self, search_str):
        """Reset quota for specific entry in proxy quota cache.

           quotaquery -> reset

        Parameters:
           - `search_str`: username/IP address.

        Examples:
        | Quota Reset | foo |
        """
        output = self._cli.quotaquery().reset(search_str=search_str)
        self._info(output)
        return output

    def quota_resetall(self):
        """Reset quota for all entry in proxy quota cache.

           quotaquery -> resetall

        Examples:
        | Quota Resetall |
        """
        output = self._cli.quotaquery().resetall()
        self._info(output)
        return output

    def quota_search(self, search_str):
        """Search a list of space separated users in quota cache.

           quotaquery -> search

        Parameters:
           - `search_str`: username/IP address.

        Examples:
        | Quota Search | foo |
        | Quota Search | foo1 foo2 10.0.0.1 |
        """
        output = self._cli.quotaquery().search(search_str=search_str)
        self._info(output)
        return output
