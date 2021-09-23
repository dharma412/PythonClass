#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/nslookup.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class Nslookup(CliKeywordBase):

    """Keywords for nslookup CLI command."""

    def get_keyword_names(self):
        return ['nslookup',
                ]

    def nslookup(self, hostname="localhost", qtype=None):
        """ Get nslookup information.

        *Parameters*\n
        - `hostname`: IP or DNS name of host. Default value is 'localhost'.
        - `qtype`: which information get from DNS server. Available options is:
        A, PTR, CNAME, MX, SOA, NS, TXT.

        *Examples*
        | Nslookup | unian.net | SOA |
        | Nslookup | hostname=google.com | qtype=NS |
        | Nslookup | hostname=195.22.112.23 |
        | Nslookup | 195.22.112.3 | A |
        """
        return self._cli.nslookup(hostname, qtype)

