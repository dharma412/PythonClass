#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/external_dlp_config.py#1 $

from common.cli.clicommon import CliKeywordBase
from common.cli import cliexceptions

class ExternalDlpConfig(CliKeywordBase):
    """Set options related to ICAP DLP scanning on the proxy."""

    def get_keyword_names(self):
        return [
            'external_dlp_config',
        ]

    def external_dlp_config(self, size=''):
        """Set options related to ICAP DLP scanning on the proxy.

        externaldlpconfig

        Parameters:
        - `size`: Minimum request body size (bytes) for External DLP over ICAP
        scanning. Number from 1 to 65 536.

        Examples:

        | External DLP Config |

        | External DLP Config | size=2048 |
        """

        if size and not size.isdigit():
            raise cliexceptions.ConfigError(
                'Size value must be a number from 1 to 65,536.')

        self._cli.externaldlpconfig(size)
