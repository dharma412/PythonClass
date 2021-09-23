#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/grep.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class Grep(CliKeywordBase):

    """Keywords for grep CLI command."""

    def get_keyword_names(self):
        return ['grep_logs',
                ]

    def grep_logs(self, log_name, regex=DEFAULT, insensitive=DEFAULT):
        """ Get information from log files on device.

        *Parameters*
        - `log_name`: name of the log file in 'grep' command promt.
        - `regex`: an extended grep expression. String.
        - `insensitive`: ingnore or not case sensitivities. Yes or No. Default Yes

        *Return*
        All strings from log file with satisfied provided regular expression.

        *Examples*
        | Grep Logs | authentication | regex=failed | authentication |
        | Grep Logs | gui_logs | regex=SN: | insensitive=No |
        | Grep Logs | backup_logs |
        """
        return self._cli.grep(log_name, regex, insensitive)

