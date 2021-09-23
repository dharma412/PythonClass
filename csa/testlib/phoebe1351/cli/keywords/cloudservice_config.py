#!/usr/bin/env python
# $Id:  $
# $DateTime:  $
# $Author:  $

from common.cli.clicommon import CliKeywordBase

class CloudserviceConfig(CliKeywordBase):

    def get_keyword_names(self):
        return ['cloudservice_config',
                'cloudservice_config_register',
                'cloudservice_config_deregister',
                'cloudservice_config_setfqdn',
               ]

    def cloudservice_config(self, settrs):
        """Keyword to set Threat response server

        *Parameters*
        - `settrs` : Option for Threat response server.
            | Key | Value |
            | 1 | AMERICAS (api-sse.cisco.com) |
            | 2 | EUROPE (api.eu.sse.itd.cisco.com) |

        Examples:
        | Cloudservice Config| settrs=AMERICAS |
        """
        return self._cli.cloudserviceconfig().settrs(settrs)

    def cloudservice_config_register(self, token_id):
        """Keyword to set Threat response server

        Examples:
        | Cloudservice Config Register| token_id=a389f98df0e77c5411148e96e239e05d |
        """
        return self._cli.cloudserviceconfig().register(token_id)

    def cloudservice_config_deregister(self):
        """Keyword to set Threat response server

        Examples:
        | Cloudservice Config Deregister|
        """
        return self._cli.cloudserviceconfig().deregister()

    def cloudservice_config_setfqdn(self, label, fqdn):
        """Keyword to set label to threat response server

        Examples:
        | Cloudservice Config setfqdn| label=AMERICAS | fqdn =stage-api-sse.cisco.com |
        """
        return self._cli.cloudserviceconfig().setfqdn(label, fqdn)

