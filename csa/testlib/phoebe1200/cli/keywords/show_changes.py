#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/show_changes.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class ShowChanges(CliKeywordBase):
    """Shows changes made during current session."""

    def get_keyword_names(self):
        return ['show_changes']

    def show_changes(self):
        """Show Changes.

        Examples:
        | Show Changes |
        | ${command_output}= | Show Changes |
        """
        output = self._cli.showchanges()
        self._info(output)
        return output
