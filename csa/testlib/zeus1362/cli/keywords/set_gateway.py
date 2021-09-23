#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/set_gateway.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class SetGateway(CliKeywordBase):
    """Set the default gateway (router)."""

    def get_keyword_names(self):
        return ['set_gateway']

    def set_gateway(self, ip):
        """Set the default gateway (router).

        Parameters:
        - `ip`: IP address of the gateway.
                The IP address must be 4 numbers separated by a period.
                Each number must be a value from 0 to 255.

        Example:
        | Set Gateway | ip=10.7.10.1 |

        """
        self._cli.setgateway(ip)
