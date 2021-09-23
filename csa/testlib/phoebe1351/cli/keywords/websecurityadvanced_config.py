#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/websecurityadvanced_config.py#2 $
# $DateTime: 2020/01/16 23:03:15 $
# $Author: saurgup5 $

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
        - `max_urls`: Enter the maximum number of URLs , Default value = 100
        - `max_urls_attachment`: Enter the maximum number of URLs , Default value = 25
        - `rewrite_url_text_href`: Do you want to rewrite both the URL text and the href in the message
        - `additional_headers`: Want to include Additional Headers , Default value = N
        - `headers_name` - Enter the headers (comma seperated), REQUIRED

        *Examples:*
        | Websecurityadvancedconfig             |
        | ... | timeout_value=300               |
        | ... | max_urls=12                     |
        | ... | max_urls_attachment=25          |
        | ... | rewrite_url_text_href=Y         |
        | ... | additional_headers=yes          |
        | ... | headers_name=header1,header2    |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.websecurityadvancedconfig(**kwargs)
