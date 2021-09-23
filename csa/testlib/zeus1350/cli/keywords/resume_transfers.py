#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/resume_transfers.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class ResumeTransfers(CliKeywordBase):
    """Keywords for resumetransfers CLI command."""

    def get_keyword_names(self):
        return ['resume_transfers', ]

    def resume_transfers(self):
        """Resume transfers.

        Exceptions:
        - `ConfigError`: in case transfers were not resumed.

        Examples:
        | Resume Transfers |
        """
        self._cli.resumetransfers()
