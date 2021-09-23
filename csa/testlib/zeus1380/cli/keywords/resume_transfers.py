#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/resume_transfers.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class ResumeTransfers(CliKeywordBase):

    """Keywords for resumetransfers CLI command."""

    def get_keyword_names(self):
        return ['resume_transfers',]

    def resume_transfers(self):
        """Resume transfers.

        Exceptions:
        - `ConfigError`: in case transfers were not resumed.

        Examples:
        | Resume Transfers |
        """
        self._cli.resumetransfers()

