#!/usr/bin/env python

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
        | ${output}= | Help | command=listenerconfig |
        | ${output}= | Help | #information about all CLI commands |
        """
        output = self._cli.help(command)
        self._info(output)
        return output
