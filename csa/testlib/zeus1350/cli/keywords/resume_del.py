#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/resume_del.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class ResumeDel(CliKeywordBase):
    """Keywords for resumedel CLI command."""

    def get_keyword_names(self):
        return ['resumedel', ]

    def resumedel(self):
        """Resume delivery.

        Exceptions:
        - `ConfigError`: in case delivery can not be resumed.

        Examples:
        | Resume Del |
        """
        self._cli.resumedel()
