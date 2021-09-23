#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/resume.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class Resume(CliKeywordBase):

    """Keywords for resume CLI command."""

    def get_keyword_names(self):
        return ['resume',]

    def resume(self):
        """Resume receiving and delivery.

        Exceptions:
        - `ConfigError`: in case receiving and delivery can not be resumed.

        Examples:
        | Resume |
        """
        self._cli.resume()

