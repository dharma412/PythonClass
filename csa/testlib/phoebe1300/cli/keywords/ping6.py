#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/ping6.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class Ping6(CliKeywordBase):
    """
    Ping a network host.
    CLI command: ping6
    """

    def get_keyword_names(self):
        return ['ping6']

    def ping6(self, host, interface=DEFAULT):
        """
        Performs ping6 of a network host using the specified interface.

        *Parameters:*
           - `host`: Hostname or IP address to ping.
           - `interface`: Interface to send ping from.

        *Return:*
        String representing percentage of successfully transmitted packets.

        *Examples:*
        | ${res}= | Ping6 | 2620:101:2004:4201::bb |
        | ${res}= | Ping6 | ${CLIENT_IPV6} | interface=Management |
        | ${res}= | Ping6 | google.com | interface=a001.d1 |
        """
        return self._cli.ping6(host=host, interface=interface)
