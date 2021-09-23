#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/rollovernow.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class RollOverNow(CliKeywordBase):

    """Roll over a log file."""

    def get_keyword_names(self):
        return ['roll_over_now']

    def roll_over_now(self, logname='All Logs'):
        """Roll over a log file.

        Parameters:
        - `logname`: name of the log subscription to roll over.  Defaulted
           to 'All Logs' to roll over all log files.

        Examples:
        | Roll Over Now |
        | Roll Over Now | logname=cli_logs |
        | Roll Over Now | logname=smad_logs |
        """
        self._cli.rollovernow(logname)


