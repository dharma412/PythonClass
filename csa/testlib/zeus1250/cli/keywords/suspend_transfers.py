#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/suspend_transfers.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class SuspendTransfers(CliKeywordBase):

    """Keywords for suspendtransfers CLI command."""

    def get_keyword_names(self):
        return ['suspend_transfers',]

    def suspend_transfers(self):
        """ Suspend all data transfers.

        Exceptions:
            - `ConfigError`: in case transfers were not suspended.

        Examples:
        | Suspend Transfers |
        """
        self._cli.suspendtransfers()

