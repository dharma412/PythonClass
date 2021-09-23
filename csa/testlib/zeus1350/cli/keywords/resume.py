#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/resume.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class Resume(CliKeywordBase):
    """Keywords for resume CLI command."""

    def get_keyword_names(self):
        return ['resume', ]

    def resume(self):
        """Resume receiving and delivery.

        Exceptions:
        - `ConfigError`: in case receiving and delivery can not be resumed.

        Examples:
        | Resume |
        """
        self._cli.resume()
