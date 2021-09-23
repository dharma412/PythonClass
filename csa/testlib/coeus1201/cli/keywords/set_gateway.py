#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/set_gateway.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class SetGateway(CliKeywordBase):
    """Set the default gateway (router)."""

    def get_keyword_names(self):
        return ['set_gateway']

    def set_gateway(self, interface=DEFAULT, ip=DEFAULT, protocol=DEFAULT):
        """Set the default gateway (router).

        Parameters:
        - `interface`: Interface, 'Data' or 'Management'. Mandatory.
        - `ip`: IP address of the gateway.
            The IP address must be a valid IPv4 or a IPv6 address.
            IPV4 must be 4 numbers separated by a period.  Each number must be a
            value from 0 to 255. (Ex: 192.168.1.1).
            A Valid IPv6 address is represented by 8 groups of 16-bit
            hexadecimal values separated by colons (:). (Ex: 2001:420:80:1::5)
        - `protocol`: choose ip protocol. Either 'IPv4' or 'IPv6'.
                If None - use default protocol (currently IPv4)

        Example:
        | Set Gateway | interface=Management | ip=10.7.10.1 |
        | Set Gateway | interface=Management | protocol=IPv4 | interface=Data |
        | Set Gateway | interface=Management | protocol=IPv6 | ip=fc01::1 |
        | Set Gateway | interface=Data | protocol=IPv6 | ip=fc02::1 |

        """
        self._cli.setgateway(interface, ip, protocol)
