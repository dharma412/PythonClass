#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/quit.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

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
