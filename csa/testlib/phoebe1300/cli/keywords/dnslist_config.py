#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/dnslist_config.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class DnsListConfig(CliKeywordBase):
    """
    dnslistconfig setup [--timeout=<int>] [--negative_ttl=<int>]

    Configure the query settings for a DNS-based list service. For the
    'setup' command, the following options are valid:

    timeout - Maximum number of seconds to wait for an DNS response.
    negative_ttl - The number of seconds to cache a "not found" DNS
                   response.
    """

    def get_keyword_names(self):
        return ['dnslistconfig_setup']

    def dnslistconfig_setup(self, *args):
        """
        dnslistconfig -> setup

        *Parameters:*
        - `ttl`: The number of seconds to cache a "not found" DNS
                   response. Default is 1800s
        - `timeout` : Maximum number of seconds to wait for an DNS response.
                      Default is 3s

        *Examples:*
        | dnslistconfig setup | ttl=10 | timeout=30 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.dnslistconfig().setup(**kwargs)
