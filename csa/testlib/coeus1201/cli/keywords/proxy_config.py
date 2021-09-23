#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/proxy_config.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class ProxyConfig(CliKeywordBase):

    """Configure the proxy. """

    def get_keyword_names(self):
        return [
            'proxy_config_setup',
        ]

    def proxy_config_setup(self, enable=DEFAULT):
        """Configure the proxy mode.

        Parameters:
        - `enable`: enabling or disabling Web Proxy.
            Either 'Yes' or 'No'.

        Examples:
        | Proxy Config Setup | enable=yes |
        | Proxy Config Setup | enable=no |
        """
        self._cli.proxyconfig().setup(self._process_yes_no(enable))

