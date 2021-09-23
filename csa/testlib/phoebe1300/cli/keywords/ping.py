#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/ping.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class Ping(CliKeywordBase):
    """
    Ping a network host.
    CLI command: ping
    """

    def get_keyword_names(self):
        return ['ping']

    def ping(self, host, interface=DEFAULT):
        """
        Performs ping of a network host using the specified interface.

        *Parameters:*
           - `host`: Hostname or IP address to ping.
           - `interface`: Interface to send ping from.

        *Return:*
        String representing percentage of successfully transmitted packets.

        *Examples:*
        | ${res}= | Ping | ${CLIENT} |
        | ${res}= | Ping | ${CLIENT_IP} | interface=Management |
        | ${res}= | Ping | google.com | interface=a001.d1 |
        """
        return self._cli.ping(host=host, interface=interface)
