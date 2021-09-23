#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/quit.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Quit(CliKeywordBase):
    """Exit the CLI."""

    def get_keyword_names(self):
        return ['quit']

    def quit(self, confirm='yes'):
        """Quit CLI

        Parameter:
        - `confirm`: Confirm 'Yes' or 'No' to quit when pending
                     CLI changes have not been committed.

        Example:
        | Quit | confirm=yes |

        """
        self._cli.quit(self._process_yes_no(confirm))
