#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/ping.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class Ping(CliKeywordBase):
    """Ping a network host.
    """

    def get_keyword_names(self):
        return [
            'ping',
        ]

    def ping(self, host, interface=DEFAULT):
        """Performs ping of specified host using the specified interface for
           10 seconds.

        Parameters:
           - `host`: host or IP address of host to ping.
           - `interface`: interface to send ping from.  Either 'Auto', 
                          'Management', 'P1', or 'P2'.  Note that 'P1' or 'P2'
                          is only valid when these interfaces are already
                          configured on appliance.

        Examples:
        | Ping | services.wga |
        | Ping | services.wga | interface=Management |
        | Ping | services.wga | interface=P1 |
        | Ping | services.wga | interface=P2 |
        """
        return self._cli.ping(host=host, interface=interface)
