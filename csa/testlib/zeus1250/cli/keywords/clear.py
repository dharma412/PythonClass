#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/clear.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Clear(CliKeywordBase):
    """Clear changes made during current session since last commit."""

    def get_keyword_names(self):
        return ['clear']

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
