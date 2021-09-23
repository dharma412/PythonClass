#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/iseconfig.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import YES, NO


class IseConfig(CliKeywordBase):
    """
    cli -> iseconfig

    """

    def get_keyword_names(self):
        return [
            'iseconfig',
            'iseconfig_enable',
            'iseconfig_disable',
        ]

    # This keyword is to support existing Tests.
    def iseconfig(self,
        enable='Y',
        servers=None,
        ise_data_timeout=None,
        backing_up=None,
        ):
        """Configure ISE for WSA

        Parameters:
        - `enable`: answer to "Do you want to enable ISE?": Y or N
        - `servers`: ISE server names, separated by commas
        - `ise_data_timeout`: timeout for ise data in proxy cache
        - `backing_up`: - interval for backing up statistics in minutes
           (0 means no back up)

        Examples:

        | IseConfig |
        | | enable=Y |
        | | servers=server1.abc,server2.abc |
        | | ise_data_timeout=10 |
        | | backing_up=5 |
        """

        return self._cli.iseconfig().setup(
            enable=enable,
            servers=servers,
            ise_data_timeout=ise_data_timeout,
            backing_up=backing_up,
        )

    def iseconfig_enable(self,
        servers=None,
        ise_data_timeout=None,
        backing_up=None,
        ):
        """Enable ISE on WSA

        Parameters:
        - `servers`: ISE server names, separated by commas
        - `ise_data_timeout`: timeout for ise data in proxy cache
        - `backing_up`: - interval for backing up statistics in minutes
           (0 means no back up)

        Examples:

        | IseConfig Enable |
        | | servers=server1.abc,server2.abc |
        | | ise_data_timeout=10 |
        | | backing_up=5 |
        """
        return self._cli.iseconfig().setup(
            enable='Y',
            servers=servers,
            ise_data_timeout=ise_data_timeout,
            backing_up=backing_up,
        )

    def iseconfig_disable(self):
        """
        Disable ISE on WSA

        Parameters:
        - `enable`: answer to "Do you want to enable ISE?": Y or N

        Examples:
        | IseConfig Disable |
        """
        return self._cli.iseconfig().setup(enable='N')
