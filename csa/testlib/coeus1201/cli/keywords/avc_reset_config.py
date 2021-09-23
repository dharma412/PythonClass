#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/avc_reset_config.py#1 $

from common.cli.clicommon import CliKeywordBase

class AvcResetConfig(CliKeywordBase):

    """Reset AVC configuration."""

    def get_keyword_names(self):
        return [
            'avc_reset_config',
        ]

    def avc_reset_config(self):

        """AVC configuration reset.

        Examples:
        | AVC Reset Config |
        """
        self._cli.avcresetconfig()

