#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/dns_flush.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

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
