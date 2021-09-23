#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/check_proxy_restart.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class CheckProxyRestart(CliKeywordBase):

    """Keywords for checkproxyrestart CLI command."""

    def get_keyword_names(self):
        return ['check_proxy_restart',]

    def check_proxy_restart(self, cm_version):
        """Check whether publishing a configuration master will trigger a proxy
        restart on any hosts.

        Parameters:
        - `cm_version`: configuration master version to check. One of 6.3, 7.1,
           or 7.5.

        Return:
        An output of the command.

        Examples:
        | ${output} = | Check Proxy Restart  6.3 |
        | ${output} = | Check Proxy Restart  7.5 |
        """
        return self._cli.checkproxyrestart(cm_version)

