#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/resume.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

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

