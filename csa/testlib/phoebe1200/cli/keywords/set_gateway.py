#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/set_gateway.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class SetGateway(CliKeywordBase):
    """Set the default gateway (router)."""

    def get_keyword_names(self):
        return ['set_gateway']

    def set_gateway(self, ip, ip_version=DEFAULT):
        """Set the default gateway (router).

        *Parameters*:
        - `ip_version`: specify gateway for IPv4 or IPv6.
          Either 'ipv4' or 'ipv6'
        - `ip`: IP address of the gateway.
          An IPv4 address must be 4 numbers separated by a period. Each number
          must be a value from 0 to 255. (Example: 192.168.1.1)
          An IPv6 address consists of 8 sets of 16-bit hexadecimal values
          separated by colons. IPv6 addresses allow zero compression in one
          location. (Example: 2001:420:80:1::5)

        *Examples*:
        | Set Gateway | 10.76.68.1 |
        | Set Gateway | 10.76.68.1 | ipv4 |
        | Set Gateway | 2620:101:2004:4201::1 | ipv6 |

        """
        self._cli.setgateway(ip_version, ip)
