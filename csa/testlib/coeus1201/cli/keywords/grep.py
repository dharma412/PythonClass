#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/grep.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class Grep(CliKeywordBase):

    """Keywords for grep CLI command."""

    def get_keyword_names(self):
        return [
            'grep_logs',
        ]

    def grep_logs(self, log_name, regex=DEFAULT, insensitive=DEFAULT, non_matching=DEFAULT):
        """ Get information from log files on device.

        Parameters:
        - `log_name`: name of the log file in 'grep' command promt.
        - `regex`: an extended grep expression. String.
        - `insensitive`: ingnore or not case sensitivities. Yes or No. Default Yes.
        - `non_matching`: select non-matching lines. Yes or No. Default No.

        Return:
        All strings from log file with satisfied provided regular expression.

        Exceptions:
        - NotFoundError
          * that exception is raised if no lines are matched
        - TailError
          * that exception is raised on tail error
        - GrepError
          * that exception is raised on grep error

        Examples:
        | Grep Logs | authlogs | regex=failed |
        | Grep Logs | gui_logs | regex=SN: | insensitive=No |
        | Grep Logs | gui_logs | regex=user:admin | non_matching=Yes |
        | Grep Logs | ftpd_logs |
        """
        return self._cli.grep(log_name, regex, insensitive, non_matching)
