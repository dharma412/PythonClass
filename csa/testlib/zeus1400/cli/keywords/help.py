#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/help.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class Help(CliKeywordBase):
    """Shows list of all CLI commands or information about specified."""

    def get_keyword_names(self):
        return ['help']

    def help(self, command=DEFAULT):
        """Help.

        Parameters:
        - `command`: specify CLI command to view help information about it.

        Examples:
        | ${output}= | Help | command=routeconfig |
        | ${output}= | Help | #information about all CLI commands |
        """
        output = self._cli.help(command)
        self._info(output)
        return output
