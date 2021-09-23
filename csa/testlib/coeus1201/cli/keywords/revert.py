#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/revert.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class Revert(CliKeywordBase):
    """Revert AsyncOS."""

    def get_keyword_names(self):
        return [
            'revert',
        ]

    def revert(self, version=DEFAULT, continue_revert=DEFAULT,
                confirm_revert=DEFAULT, wait_for_data=None):
        """Reverting to an Earlier Version of AsyncOS.

        revert

        Parameters:
        - `continue_revert`: should reverting be continued. Either 'Yes' or 'No'.
        - `confirm_revert`: confirm reverting. Either 'Yes' or 'No'.
        Next parameters will be used only if both questions above are answered 'Yes'.
        - `version`: a previous version to use.
        - `wait_for_data`: wait for the reporting data to be synced with the SMA.
            Either 'Yes' or 'No'.


        Examples:
            | Revert |
            | ... | version=7.8 |
            | ... | continue_revert=Yes |
            | ... | confirm_revert=Yes |
        """

        kwargs = {
                  'continue': self._process_yes_no(continue_revert),
                 }

        if kwargs['continue'] == 'Y':
            kwargs['confirm'] = self._process_yes_no(confirm_revert)

            if kwargs['confirm'] == 'Y':
                kwargs['version'] = version

                if wait_for_data is not None:
                    kwargs['wait_for_data'] = wait_for_data

        self._cli.revert(**kwargs)

