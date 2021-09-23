#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1361/cli/keywords/tcpservices.py#1
# $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class tcpservices(CliKeywordBase):
    """
    cli -> wipedata
    """
    def get_keyword_names(self):
        return [
                'tcp_services',
                ]

    def tcp_services(self):
        return self._cli.tcpservices()

