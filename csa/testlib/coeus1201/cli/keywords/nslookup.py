#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/nslookup.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class Nslookup(CliKeywordBase):

    """Keywords for nslookup CLI command."""

    def get_keyword_names(self):
        return ['nslookup',
                ]

    def nslookup(self, host, query_type=DEFAULT):
        """ Query the nameserver.

        Parameters:
        - `host`:  Hostname or IP address to be resolved.
        - `query_type`: Type of query to perform. String. Possible values are
            'A'     - the host's IP address
            'AAAA'  - the host's IPv6 address
            'CNAME' - the canonical name for an alias
            'MX'    - the mail exchanger
            'NS'    - the name server for the named zone
            'PTR'   - the hostname if the query is an Internet address,
            'SOA'   - the domain's "start-of-authority" information
            'TXT'   - the text information about domain
          This parameter is ignored when hostname is IPv4 or
          IPv6 address and query_type assumed to be 'PTR'.

        Return:
        String with query result.

        Exceptions:
        - MalformedQueryError
          * that exception is raised if DNS query is malformed

        Examples:
        | Nslookup | cisco.com | A |
        | Nslookup | google.com | AAAA |
        | Nslookup | 8.8.8.8 |
        | Nslookup | 4.4.8.8.in-addr.arpa | PTR |
        """
        return self._cli.nslookup(host, query_type)

