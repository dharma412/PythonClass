#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/dig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase

class Dig(CliKeywordBase):
    """
    CLI command: dig
    """
    def get_keyword_names(self):
        return [
            'dig_batch_record_lookup',
            'dig_batch_reverse_lookup',
        ]

    def dig_batch_record_lookup(self, *args):
        """
        Runs dig command in batch mode. Lookup record on DNS server.

        *Parameters:*
        - `hostname`: Record that user want to look up. String. Required.
        - `query_type`: Query type can be one from A, PTR, CNAME, MX, SOA,
          NS, TXT. Optional.
        - `source_ip`: The interface to run dig query from. Optional.
        - `dns_ip`: The IP address of DNS server. Optional.
        - `query_over_tcp`: Make query over TCP. Optional.
        - `query_over_udp`: Make query over TCP. Optional.

        *Return:*
        - Output returned by dig command. The output is not parsed. String.

        *Example:*
        | ${res}= | Dig Batch Record Lookup |
        | ... | hostname=google.com |
        | ... | dns_ip=${DNS} |
        | ... | query_type=AAAA |
        | ... | query_over_tcp=yes |
        | Log | ${res} |

        | ${res}= | Dig Batch Record Lookup |
        | ... | hostname=google.com |
        | ... | dns_ip=${DNS} |
        | ... | query_type=MX |
        | Log | ${res} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.dig.dig_batch_lookup_record(**kwargs)

    def dig_batch_reverse_lookup(self, *args):
        """
        Runs dig command in batch mode. Does reverse IP lookup.

        *Parameters:*
        - `reverse_ip`: Reverse lookup IP address. String. Required.
        - `query_type`: Query type can be one from A, PTR, CNAME, MX, SOA,
          NS, TXT. Optional.
        - `dns_ip`: The IP address of DNS server. Optional.
        - `query_over_tcp`: Make query over TCP. Optional.
        - `query_over_udp`: Make query over TCP. Optional.

        *Return:*
        - Output returned by dig command. The output is not parsed. String.

        *Example:*
        | ${res}= | Dig Batch Reverse Lookup |
        | ... | reverse_ip=74.125.224.110 |
        | ... | dns_ip=${DNS} |
        | Log | ${res} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.dig.dig_batch_lookup_reverse(**kwargs)
