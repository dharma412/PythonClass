#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/ssl_config.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT
from common.cli import cliexceptions

class SslConfig(CliKeywordBase):
    """Configure Ssl ciphers, fallback etc."""

    def get_keyword_names(self):
        return [
            'ssl_config_ciphers',
            'ssl_config_compress',
            'ssl_config_ecdhe',
            'ssl_config_fallback',
            'ssl_config_versions',
        ]

    def ssl_config_fallback(self, enable=DEFAULT):
        """Configure fallback option

        sslconfig > fallback

        Parameters:
        - `enable=Yes/No`

        Example:
        | 
        | Ssl Config Fallback | yes |
        | Ssl Config Fallback | enable=no |        
        """

        self._cli.sslconfig().fallback(enable=enable)

    def ssl_config_versions(self, service, protocol, enable=DEFAULT):
        """Configure Protocols supported by Services
        
        Protocol configuration for a service has to be done one by one.

        sslconfig > versions

        Parameters:
        - `service=sicap | ldaps | updater | proxy | webui | all_services`
        - `protocol=sslv3 | tls1dot0 | tls1dot1 | tls1dot2`
        - `enable=Yes/No`

        Example:
        | 
        | Ssl Config Versions | service=ldaps | protocol=tls1dot0 | enable=Y
        | Ssl Config Versions | service=proxy | protocol=sslv3 | enable=N
        """

        self._cli.sslconfig().versions(service=service, protocol=protocol,enable=enable)

    def ssl_config_compress(self, enable=DEFAULT):
        """Configure Protocol Compression

        sslconfig > compress

        Parameters:
        - `enable=Yes/No`

        Example:
        | 
        | Ssl Config Compress | yes |
        | Ssl Config Compress | enable=no |
        """

        self._cli.sslconfig().compress(enable=enable)

    def ssl_config_ciphers(self, service, ciphers_list):
        """Configure Ciphers

        sslconfig > ciphers

        Parameters:
        - `service=sicap | ldaps | updater | proxy | webui | all_services`
        - `ciphers_list=colon_separated_ciphers`
        
        Example:
        | 
        | Ssl Config Ciphers | proxy |  EECDH:DSS:RSA:!IDEA:!ECDHE-ECDSA-AES256-SHA
        | Ssl Config Ciphers | service=proxy | ciphers_list=!ECDHE-RSA-AES256-SHA:!AES256-SHA:DHE-RSA-AES1 |
        """

        self._cli.sslconfig().ciphers(service=service, ciphers_list=ciphers_list)
    
    def ssl_config_ecdhe(self, enable=DEFAULT):
        """Configure Protocol Compression

        sslconfig > ecdhe

        Parameters:
        - `enable=Yes/No`

        Example:
        | 
        | Ssl Config ECDHE | yes |
        | Ssl Config ECDHE | enable=no |
        """

        self._cli.sslconfig().ecdhe(enable=enable)