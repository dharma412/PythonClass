#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/netstat.py#1 $

from common.cli.clicommon import CliKeywordBase

class Netstat(CliKeywordBase):
    """Display information about networks and connections."""

    def get_keyword_names(self):
        return ['netstat']

    def netstat(self, info='all'):
        """Netstat.

        Parameters:
        - `info`: string with info type to specify custom data to print.
                Proper values are: 'all', 'tcp', 'udp', 'ip', 'icmp', 'igmp'
                'routing', 'connections'. Default value is 'all'.

        Examples:
        | netstat | #to show all information |
        | netstat | info=tcp |
        | netstat | info=icmp |
        | netstat | info=routing | #to show routing table information |
        | ${command_output}= | netstat | info=tcp | #to put command output to a variable |
        """
        output = self._cli.netstat(info)
        self._info(output)
        return output