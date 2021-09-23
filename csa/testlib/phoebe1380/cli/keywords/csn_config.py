#!/usr/bin/env python
# $Id:  $
# $DateTime:  $
# $Author:  $

from common.cli.clicommon import CliKeywordBase

class CsnConfig(CliKeywordBase):
    """ keywords class to configure CSN """

    def get_keyword_names(self):
        return ['csn_config_enable',
                'csn_config_disable',
               ]

    def csn_config_enable(self):
        """Keyword to enable CSN config

        Parameters: None

        Examples:
        | Csn Config Enable |
        """
        self._cli.csnconfig().enable()

    def csn_config_disable(self):
        """Keyword to disable CSN config

        Parameters: None

        Examples:
        | Csn Config Disable |
        """
        self._cli.csnconfig().disable()

