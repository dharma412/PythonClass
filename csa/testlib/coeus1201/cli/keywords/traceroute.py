#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/traceroute.py#1 $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions

class Traceroute(CliKeywordBase):
    """Display the network route to a remote host."""

    def get_keyword_names(self):
        return ['traceroute',
                ]

    def traceroute(self, host, interface='Auto'):
        """Display the network route to a remote host.

        Parameters:
        - `host`: host to which you want to trace the route. (must be a hostname
        or an IP). Mandatory.
        - `interface`: interface do you want to trace from. Available values:
        'Auto', 'Management'.

        Examples:
        | Traceroute | wsa103.wga | interface='Management' |

        | Traceroute | wsa103.wga |
        """

        if host is None or not host:
            raise cliexceptions.ConfigError('Please specify host to trace to.')
        output = self._cli.traceroute(interface, host)
        return output
