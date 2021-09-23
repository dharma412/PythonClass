#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/dns_flush.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class DnsFlush(CliKeywordBase):

    def get_keyword_names(self):
        return ['dnsflush']

    def dnsflush(self, sure='Yes'):
        """CLI Command: dnsflush.

        *Parameters:*

        `sure`: answer to confirmation question. Either Yes, No or Default.
            Yes is used by default.
            Default value is chosen via hitting <Enter>.

        *Examples:*
        | dnsflush |
        | dnsflush | sure=No |
        """
        self._cli.dnsflush(self._process_yes_no(sure))
