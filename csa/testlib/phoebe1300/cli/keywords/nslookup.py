#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/nslookup.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
SARF CLI command: nslookup
"""

from common.cli.clicommon import CliKeywordBase


class Nslookup(CliKeywordBase):
    """
    Query the nameserver.
    CLI command: nslookup
    """

    def get_keyword_names(self):
        return ['nslookup']

    def nslookup(self, *args):
        """CLI command: nslookup

        *Parameters:*
        - `hostname`: The host or IP address to resolve.
        - `qtype`: Query type: _A_, _AAAA_, _PTR_, _CNAME_, _MX_, _SOA_, _NS_, _TXT_
        | 1 | A | the host's IP address |
        | 2 | AAAA | the host's IPv6 address |
        | 3 | CNAME | the canonical name for an alias |
        | 4 | MX | the mail exchanger |
        | 5 | NS | the name server for the named zone |
        | 6 | PTR | the hostname if the query is an Internet address,
        otherwise the pointer to other information |
       | 7 | SOA | the domain's "start-of-authority" information |
       | 8 | TXT | the text information |

        *Return:*
        Raw output

        *Examples:*
        | Nslookup | hostname=google.com |
        | Nslookup | hostname=google.com | qtype=mx |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.nslookup(**kwargs)
