#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/websecurity_config.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class websecurityconfig(CliKeywordBase):
    """
    cli -> websecurityconfig
    This command is used to enable/disable url filtering and correspondingly assign urllist to the url whitelist
    """

    def get_keyword_names(self):
        return ['websecurity_config']

    def websecurity_config(self, *args):
        """
        *Parameters:*
        - `url_enable`: Enable URL Filtering or not , Default value = N
        - `url_disable`: Disable URL Filtering or not , Default value = Y
        - `enable_url_clicktracking`: Enable URL Click Tracking or not , Default value = N
        - `disable_url_clicktracking`: Disable URL Click Tracking or not , Default value = N
        - `urllist_add`: Want to add URL list or not , Default value = N
        - `clientcert_set`: Want to set client certificate or not , Default value = N
        - `urllist_number`: Enter the number of URL list to export , REQUIRED
           Example:
             1. urllist_1
             2. urllist_2
             Enter the number of URL list to export
        - `certificate_number`: Choose the certificate , REQUIRED
           Example:
             1. certificate_1
             2. certificate_2
             Choose the certificate

        *Examples:*
        | Websecurity Config | url_enable=YES | urllist_add=YES | urllist_number=1 | enable_url_clicktracking=YES |
        | Websecurity Config | url_disable=NO | clientcert_set=YES | certificate_number=1 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.websecurityconfig(**kwargs)
