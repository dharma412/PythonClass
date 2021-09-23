#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/sdr_advanced_config.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class SdrAdvancedConfig(CliKeywordBase):
    """
    This command is used to configure values used for sender domain reputation advanced config
    cli -> sdradvancedconfig
    """

    def get_keyword_names(self):
        return ['sdr_advanced_config',
                'sdr_advanced_config_batch']

    def sdr_advanced_config(self, *args):
        """
        *Parameters:*
        - `sdr_lookup_timeout_value`: Enter SDR lookup timeout in seconds. Default: 5
        - `sdr_service_hostname`: Enter the Domain Reputation service hostname. Default: v2.beta.sds.cisco.com
        - `sdr_verify_server_certificate`: Do you want to verify server certificate. Default: Yes
        - `sdr_rpc_log_level`: Enter the default debug log level for RPC server. Default: Info
        - `sdr_http_client_log_level`: Enter the default debug log level for HTTP Client. Default: Info
        - `sdr_match_exceptions_envelope_from_domain`: Do you want exception list matches based on envelope-from domain only. Default: Yes
        *Examples:*
        | Sdr Advanced Config                                   |
        | ... | sdr_lookup_timeout_value=10                     |
        | ... | sdr_service_hostname=example.com                |
        | ... | sdr_verify_server_certificate=No                |
        | ... | sdr_rpc_log_level=Debug                         |
        | ... | sdr_http_client_log_level=Warn                  |
        | ... | sdr_match_exceptions_envelope_from_domain=No    |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sdradvancedconfig(**kwargs)

    def sdr_advanced_config_batch(self, *args):
        """
        Keyword to run sdrconfig command in batch mode.

        :params:
            timeout: timeout value
            host: service hostname
            verify_peer: verify server certificate
            debug_rpc_server: rpc server log debug level
            debug_http_client: http client log debug level
        :return:
            None
        :examples:
            | Sdr Advanced Config Batch                 |
            | ... | timeout=10                          |
            | ... | host=v2.sds.cisco.com               |
            | ... | verify_peer=1                       |
            | ... | debug_rpc_server=Info               |
            | ... | debug_http_client=Info              |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sdradvancedconfig.batch(**kwargs)
