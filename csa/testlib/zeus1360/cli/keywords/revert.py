#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/revert.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class Revert(CliKeywordBase):
    """Revert AsyncOS."""

    def get_keyword_names(self):
        return ['revert',]

    def revert(self, version=DEFAULT, continue_revert=DEFAULT, confirm_revert=DEFAULT ):
        """Reverting to an Earlier Version of AsyncOS.

        revert

        Parameters:
        - `version`: a previous version to use.
        - `continue_revert`: should reverting be continued. Either 'Yes' or 'No'.
        - `confirm_revert`: confirm reverting. Either 'Yes' or 'No'.

        Examples:
            | Revert |
            | ... | version=7.8 |
            | ... | continue_revert=Yes |
            | ... | confirm_revert=Yes |
        """
        kwargs = {
                  'version': version,
                  'continue': self._process_yes_no(continue_revert),
                 }

        if continue_revert.strip().lower() == 'yes':
            kwargs['confirm'] = self._process_yes_no(confirm_revert)

        self._cli.revert(**kwargs)
