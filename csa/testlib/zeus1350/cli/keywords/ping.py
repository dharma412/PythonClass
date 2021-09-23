#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/ping.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class Ping(CliKeywordBase):
    """Ping a network host.
    """

    def get_keyword_names(self):
        return ['ping']

    def ping(self, host, interface=DEFAULT):
        """Performs ping of specified host using the specified interface for
           10 seconds.

        Parameters:
           - `host`: host or IP address of host to ping.
           - `interface`: interface to send ping from.  Either 'Auto',
                          'Management', 'P1', or 'P2'.  Note that 'P1' or 'P2'
                          is only valid when these interfaces are already
                          configured on appliance.

        Return:


        Examples:
        | ${out}= | Ping | services.wga |
        | ${out}= | Ping | services.wga | interface=Management |
        | ${out}= | Ping | services.wga | interface=P1 |
        | ${out}= | Ping | services.wga | interface=P2 |
        """
        out = self._cli.ping(host=host, interface=interface)
        self._info(out)
        return out
