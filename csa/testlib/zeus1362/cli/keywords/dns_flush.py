#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/dns_flush.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class DnsFlush(CliKeywordBase):

    def get_keyword_names(self):
        return ['dnsflush']

    def dnsflush(self, sure='Yes'):
        """CLI Command: dnsflush.

        `sure`: answer to confirmation question. Either Yes, No or Default.
            Yes is used by default.
            Default value is chosen via hitting <Enter>.

        Examples:
        | dnsflush |
        | dnsflush | sure=No |
        """
        self._cli.dnsflush(self._process_yes_no(sure))
