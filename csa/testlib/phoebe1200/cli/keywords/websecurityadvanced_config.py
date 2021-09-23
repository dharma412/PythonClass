#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/websecurityadvanced_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class websecurityadvancedconfig(CliKeywordBase):
    """
    This command is used to configure values used for websecurity config
    cli -> websecurityadvancedconfig
    """

    def get_keyword_names(self):
        return ['websecurityadvanced_config']

    def websecurityadvanced_config(self, *args):
        """
        *Parameters:*
        - `timeout_value`: Enter the new timeout value in milliseconds , Default value = 500
        - `cache_size`: Enter the URL cache size (no. of URLs) , Default value = 500
        - `disable_dns`: Do you want to disable DNS lookups , Default value = N
        - `max_urls`: Enter the maximum number of URLs , Default value = 100
        - `web_hostname`: Enter the Web security service hostname , Default value = sds-external-testing1.ironport.com
        - `threshold_value`: Enter the threshold value for outstanding requests , Default value = 20
        - `verify_servercert`: Do you want to verify server certificate , Default value = N
        - `ttl_value`: Enter the default time-to-live value (seconds) , Default value = 30
        - `rewrite_url_text_href`: Do you want to rewrite both the URL text and the href in the message? Default value = N
        - `additional_headers`: Want to include Additional Headers , Default value = N
        - `headers_name` - Enter the headers (comma seperated), REQUIRED
        - `loglevel_rpc`: Enter the default debug log level for RPC server , Default value = Info
        - `loglevel_sds`: Enter the default debug log level for SDS cache , Default value = Info
        - `loglevel_http`: Enter the default debug log level for HTTP client , Default value = Info

        *Examples:*
        | Websecurityadvancedconfig | timeout_value=300 | cache_size=600 | disable_dns=y | max_urls=12 | web_hostname=ironport.com | threshold_value=10 | verify_servercert=y | ttl_value=20 | additional_headers=yes | headers_name=header1,header2 | loglevel_rpc=Critical | loglevel_sds=Trace | loglevel_http=Trace |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.websecurityadvancedconfig(**kwargs)
