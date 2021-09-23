#!/usr/bin/env python
# $Id:  $
# $DateTime:  $
# $Author:  $

from common.cli.clicommon import CliKeywordBase

class ThreatresponseConfig(CliKeywordBase):
    """ keywords class to configure Threatresponse """

    def get_keyword_names(self):
        return ['threatresponse_config_enable',
                'threatresponse_config_disable',
               ]

    def threatresponse_config_enable(self,):
        """Keyword to enable Threat response config (CTR )

        Parameters: None

        Examples:
        | Threatresponse Config Enable |
        """

        self._cli.threatresponseconfig().enable()

    def threatresponse_config_disable(self,):
        """Keyword to disable Threat response config (CTR )

        Parameters: None

        Examples:
        | Threatresponse Config Disable |
        """

        self._cli.threatresponseconfig().disable()

