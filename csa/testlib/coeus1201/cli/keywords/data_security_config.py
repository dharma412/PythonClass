#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/data_security_config.py#1 $

from common.cli.clicommon import CliKeywordBase

class DataSecurityConfig(CliKeywordBase):
    """Set options related to Cisco IronPort data security policies."""

    def get_keyword_names(self):
        return ['data_security_config']

    def data_security_config(self, size=None):
        """Data security configuration.

        Parameters:
        - `size`: Minimum request body size (bytes) for
            data security scanning. Mandatory parameter.

        Examples:
        | Data Security Config | size=1200 |
        """
        if not size:
            raise ValueError('Size must be set.')

        if not size.isdigit():
            raise ValueError('Value must be an integer from 1 to 65,536.')

        self._cli.datasecurityconfig(int(size))