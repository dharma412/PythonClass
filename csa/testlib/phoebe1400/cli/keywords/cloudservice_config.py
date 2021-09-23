from common.cli.clicommon import CliKeywordBase

class CloudserviceConfig(CliKeywordBase):

    def get_keyword_names(self):
        return ['cloudservice_config',
                'cloudservice_config_enable',
                'cloudservice_config_register',
                'cloudservice_config_deregister',
                'cloudservice_config_setfqdn',
                'cloudservice_config_status',
                'cloudservice_config_disable',
                'cloudservice_config_fetch_certificate',
                'cloudservice_config_csn_enable',
                'cloudservice_config_csn_disable',
                'cloudservice_config_secureX_enable',
                'cloudservice_config_secureX_disable',
               ]

    def cloudservice_config_enable(self, cloud_server):
        """Keyword to enable and set Secure Cloud Servers

        *Parameters*
        - `cloud_server` : Option for Secure Cloud Servers.
            | Key | Value |
            | 1 | AMERICAS (api-sse.cisco.com) |
            | 2 | EUROPE (api.eu.sse.itd.cisco.com) |

        Examples:
        | Cloudservice Config Enable| AMERICAS |
        """
        return self._cli.cloudserviceconfig().enable(cloud_server)

    def cloudservice_config_status(self):
        """Keyword to get Cloud Service Config Status

        *Parameters*
        will return the status of the cloud service config status
        |REGISTERED|INPROGRESS|DISABLED

        Examples:
        |${status}= | Cloudservice Config Status |
        """
        return self._cli.cloudserviceconfig().status()

    def cloudservice_config_disable(self):
        """Keyword to disable Secure Cloud Servers
        Examples:
        | Cloudservice Config Disable |
        """
        return self._cli.cloudserviceconfig().disable()

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
    
    def cloudservice_config_fetch_certificate(self, overwrite='YES'):
        """Keyword to download the Cisco Talos certificate and key

        *Parameters*
        - None

        Examples:
        | ${output}= | Cloudservice Config Fetch Certificate 
        | ${output}= | Cloudservice Config Fetch Certificate | overwrite=No
        """
        return self._cli.cloudserviceconfig().fetch_certificate(overwrite)

    def cloudservice_config_csn_enable(self):
        """Keyword to Cloudservice CSN enable

        *Parameters*
        - None

        Examples:
        | Cloudservice Config Csn Enable |
        """
        return self._cli.cloudserviceconfig().csnconfig_enable()

    def cloudservice_config_csn_disable(self):
        """Keyword to Cloudservice CSN disable

        *Parameters*
        - None

        Examples:
        | Cloudservice Config Csn Disable |
        """
        return self._cli.cloudserviceconfig().csnconfig_disable()

    def cloudservice_config_secureX_enable(self):
        """Keyword to Cloudservice SecureX enable

        *Parameters*
        - None

        Examples:
        | Cloudservice Config SecureX Enable |
        """
        return self._cli.cloudserviceconfig().securex_enable()

    def cloudservice_config_secureX_disable(self):
        """Keyword to Cloudservice SecureX Disable

        *Parameters*
        - None

        Examples:
        | Cloudservice Config SecureX Disable |
        """
        return self._cli.cloudserviceconfig().securex_disable()
