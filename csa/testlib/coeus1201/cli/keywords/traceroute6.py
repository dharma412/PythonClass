#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/traceroute6.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions

class Traceroute6(CliKeywordBase):
    """Display the network route to a remote host via IPv6 protocol."""

    def get_keyword_names(self):
        return ['traceroute6',
                ]

    def traceroute6(self, host, interface='Auto'):
        """Display the network route to a remote host.

        Parameters:
        - `host`: host to which you want to trace the route. (must be a hostname
        or an IPv6 address). Mandatory.
        - `interface`: interface do you want to trace from. Available values:
        'Auto', 'Management'.

        Returns: traceroute6 output

        Examples:
        | Traceroute6 | wsa103.wga | interface='Management' |
        | Traceroute6 | wsa103.wga |
        """

        if host is None or not host:
            raise cliexceptions.ConfigError('Please specify host to trace to.')
        output = self._cli.traceroute6(interface, host)
        return output
