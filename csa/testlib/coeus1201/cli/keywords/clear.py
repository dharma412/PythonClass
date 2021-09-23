#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/clear.py#1 $

from common.cli.clicommon import CliKeywordBase


class Clear(CliKeywordBase):

    """Clear changes made during current session since last commit."""

    def get_keyword_names(self):
        return [
            'clear',
        ]

    def clear(self, confirm='Yes'):

        """Clear.

        Parameters:
        - `confirm`: string with answer to confirmation question.
                    Either Yes or No. Yes is used by default.

        Examples:
        | clear | # Yes is used by default |
        | clear | confirm=No |
        """

        self._cli.clear(self._process_yes_no(confirm))

