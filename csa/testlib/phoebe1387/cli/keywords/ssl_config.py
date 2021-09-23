#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase

class SslConfig(CliKeywordBase):
    """
    CLI command: sslconfig
    """
    def get_keyword_names(self):
        return ['ssl_config_inbound',
                'ssl_config_outbound',
                'ssl_config_verify',
                'ssl_config_gui',
                'ssl_config_get_settings',
                'ssl_config_other_client_tlsv10',
                'ssl_config_peer_cert_fqdn',
                'ssl_config_peer_cert_x509']

    def ssl_config_inbound(self, *args):
        """Edit Inbound SMTP ssl settings.

        CLI command: sslconfig > inbound

        *Parameters:*
        - `ssl_method`: The inbound SMTP ssl method.
        | 1 | SSL v2 |
        | 2 | SSL v3 |
        | 3 | TLS v1 |
        | 4 | SSL v2 and v3 |
        | 5 | SSL v3 and TLS v1 |
        | 6 | SSL v2, v3 and TLS v1 |
        - `ssl_cipher`: The inbound SMTP ssl cipher.
        - `tls_negotiation`: Enable/Disable TLS Renegotiation for inbound SMTP

        *Return:*
        None

        *Examples:*
        | SSL Config Inbound |
        | ... | ssl_method=SSL v2 |
        | ... | ssl_cipher=ADH-RC4-MD5 |
        | ... | tls_negotiation=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sslconfig().inbound(**kwargs)

    def ssl_config_outbound(self, *args):
        """Edit Outbound SMTP ssl settings.

        CLI command: sslconfig > outbound

        *Parameters:*
        - `ssl_method`: The outbound SMTP ssl method.
        | 1 | SSL v2 |
        | 2 | SSL v3 |
        | 3 | TLS v1 |
        | 4 | SSL v2 and v3 |
        | 5 | SSL v3 and TLS v1 |
        | 6 | SSL v2, v3 and TLS v1 |
        - `ssl_cipher`: The outbound SMTP ssl cipher.

        *Return:*
        None

        *Examples:*
        | SSL Config Outbound |
        | ... | ssl_method=2 |
        | ... | ssl_cipher=DHE-RSA-CAMELLIA256-SHA |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sslconfig().outbound(**kwargs)

    def ssl_config_gui(self, *args):
        """Edit GUI HTTPS ssl settings.

        CLI command: sslconfig > gui

        *Parameters:*
        - `ssl_method`: GUI HTTPS ssl method.
        | 1 | SSL v2 |
        | 2 | SSL v3 |
        | 3 | TLS v1 |
        | 4 | SSL v2 and v3 |
        | 5 | SSL v3 and TLS v1 |
        | 6 | SSL v2, v3 and TLS v1 |
        - `ssl_cipher`: GUI HTTPS ssl cipher.
        - `tls_negotiation`: Enable/Disable TLS Renegotiation for GUI HTTPS

        *Return:*
        None

        *Examples:*
        | SSL Config Gui |
        | ... | ssl_method=TLS v1 |
        | ... | ssl_cipher=AES256-SHA |
        | ... | tls_negotiation=0 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sslconfig().gui(**kwargs)

    def ssl_config_verify(self, *args):
        """Verify and show ssl cipher list.

        CLI command: sslconfig > verify

        *Parameters:*
        - `cipher`: The ssl cipher to verify.

        *Return:*
        Raw output.

        *Examples:*
        | ${ciphers} | SSL Config Verify |
        | ... | cipher=SHA |
        | Log | ${ciphers} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.sslconfig().verify(**kwargs)

    def ssl_config_get_settings(self, *args):
        """Return ssl settings.

        CLI command: sslconfig

        *Parameters:*
        - `as_dictionary`: Return the result formatted as dictionary(CfgHolder). YES or NO.
        - `fips_mode`: Return the result in case if DUT is in FIPS mode. True or False
        Keys: _outbound_smtp_ciphers_, _outbound_smtp_method_, _inbound_smtp_ciphers_, _inbound_smtp_method_, _gui_https_method_, _gui_https_ciphers_.

        *Return:*
        Dictionary(CfgHolder).
        The dictionary may look like:
        {'outbound_smtp_ciphers': 'RC4-SHA:RC4-MD5:ALL',
         'outbound_smtp_method': 'sslv3tlsv1',
         'inbound_smtp_ciphers': 'RC4-SHA:RC4-MD5:ALL',
         'inbound_smtp_method': 'sslv3tlsv1',
         'gui_https_method': 'sslv3tlsv1',
         'gui_https_ciphers': 'RC4-SHA:RC4-MD5:ALL'}

        *Examples:*
        | ${raw}= | SSL Config Get Settings | as_dictionary=no |
        | ${raw_fips}= | SSL Config Get Settings | as_dictionary=no | fips_mode=${True} |
        | ${dict}= | SSL Config Get Settings |
        | Log | ${raw} |
        | Log | ${raw_fips} |
        | Log Dictionary | ${dict} |
        # cfgholder allows accessing keys with '.' dot syntax:
        | Should Be Equal | ${dict.inbound_smtp_ciphers} | ADH-RC4-MD5 |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.sslconfig().get_settings(**kwargs)

    def ssl_config_other_client_tlsv10(self, *args):
        """Edit OTHER_CLIENT_TLSV10 ssl settings.

        CLI command: sslconfig > other_client_tlsv10

        *Parameters:*
        - `enable`: Pass ${True} to enable other_client_tlsv10
                    Pass ${False} to disable other_client_tlsv10

        *Return:*
        None

        *Examples:*
        | SSL Config Other Client Tls | enable=${True}  |
        | SSL Config Other Client Tls | enable=${False} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sslconfig().other_client_tls(**kwargs)

    def ssl_config_peer_cert_fqdn(self, *args):
        """Edit PEER_CERT_FQDN ssl settings.

        CLI command: sslconfig > peer_cert_fqdn

        *Parameters:*
        - `enable`: Pass ${True} to enable other_client_tlsv10
                    Pass ${False} to disable other_client_tlsv10

        *Return:*
        None

        *Examples:*
        | SSL Config Peer Cert Fqdn | enable=${True}  |
        | SSL Config Peer Cert Fqdn | enable=${False} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sslconfig().peer_cert_fqdn(**kwargs)
    
    def ssl_config_peer_cert_x509(self, *args):
        """Edit PEER_CERT_X509 ssl settings.

        CLI command: sslconfig > peer_cert_x509

        *Parameters:*
        - `enable`: Pass ${True} to enable other_client_tlsv10
                    Pass ${False} to disable other_client_tlsv10

        *Return:*
        None

        *Examples:*
        | SSL Config Peer Cert X509 | enable=${True}  |
        | SSL Config Peer Cert X509 | enable=${False} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sslconfig().peer_cert_x509(**kwargs)
