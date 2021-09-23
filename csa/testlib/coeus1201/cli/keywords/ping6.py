#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/ping6.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class Ping6(CliKeywordBase):
    """Ping a network host via IPv6 protocol.
    """

    def get_keyword_names(self):
        return [
            'ping6',
        ]

    def ping6(self, host, interface=DEFAULT):
        """Performs ping of specified host using the specified interface for
           10 seconds.

        Parameters:
           - `host`: host or IP address of host to ping.
           - `interface`: interface to send ping from.  Either 'Auto',
                          'Management', 'P1', or 'P2'.
                          Note that 'P1' or 'P2' is only valid when these
                          interfaces are already configured on appliance.

        Returns: percentage of successful pings (interger value from 0 to 100)

        Examples:
        | Ping6 | services.wga |
        | Ping6 | services.wga | interface=Management |
        | Ping6 | services.wga | interface=P1 |
        | Ping6 | services.wga | interface=P2 |
        """
        return self._cli.ping6(host=host, interface=interface)
