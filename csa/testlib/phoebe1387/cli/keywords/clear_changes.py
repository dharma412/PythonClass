#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/clear_changes.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase
import traceback

class ClearChanges(CliKeywordBase):
    """
    cli -> clearchanges

    Provides keyword to clear changes made during this session since last commit
    """

    def get_keyword_names(self):
        return ['clear_changes',
               ]

    def clear_changes(self, confirm='yes'):
        """
        Clear changes made during this session since last commit

        *Parameters*:
        - `confirm`: confirm clearing changes made during this session.
          Either 'yes' or 'no'

        *Returns*:
          - `True` if changes made since last commit were cleared
          - `False` if no changes were made since last commit

        *Examples*:
        | ${Status}= | Clear Changes | confirm=yes |
        """
        try:
            return self._cli.\
              clearchanges(confirm_clear=self._process_yes_no(confirm))
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e

