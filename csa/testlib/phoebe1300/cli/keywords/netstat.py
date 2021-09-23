#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/netstat.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class Netstat(CliKeywordBase):
    """Keywords for netstat CLI command."""

    def get_keyword_names(self):
        return ['netstat',
                ]

    def netstat(self, interface, info_type=DEFAULT, ip_version=DEFAULT, \
                address_as_number=DEFAULT, avoid_truncating=DEFAULT,
                bytes=DEFAULT, dropped=DEFAULT,
                num_sec=DEFAULT, timeout=30,
                ):
        """ Get netstat information.

        *Parameters*\n
        Selector: Is a string or regular expression.
                  1. If selector is a string, the first input list option
                  that contains selector will be chosen.
                  2. If selector is a regular expression, then the first input
                  list option that matches selector will be chosen.\n
        - `interface`: Name of interface on device. Selector.
        - `info_type`: What kind of information you want to get.
        - `ip_version` : ip_version . ipv4 or ipv6
        - `address_as_number`: show ip or DNS name. If NO (which is default)
        then show ip address.
        - `avoid_truncating`: Yes or No. If No (which is default), than output
          contain full adresses and vice versa.
        - `bytes`: Yes or No. If No (which is default), than output doesn't
          contain information about amount of packest and vice versa.
        - `dropped`: Yes or No. If No (which is default), than information about
          dropped packet won't be showed in output.
        - `num_sec`: number of seconds between renewing information. Default is
          10.
        - `timeout`: how long take output. Default is 30 seconds.

        *Examples*

        | Netstat | Data 2 | info_type=sockets | address_as_number=YES |
        | ... | avoid_truncating=YES |
        | Netstat | Data 1 | info_type=interfaces | bytes=YES | dropped=YES |
        | Netstat | Management | info_type=traffic | num_sec=10 | dropped=NO |
        | Netstat | Management | info_type=queues | address_as_number=YES |
        | ... | avoid_truncating=NO |
        """
        return self._cli.netstat(info_type, ip_version, address_as_number,
                                 avoid_truncating, interface, bytes, dropped, num_sec, int(timeout))
