#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/quit.py#1 $

from common.cli.clicommon import CliKeywordBase

class Quit(CliKeywordBase):
    """Exit the CLI."""

    def get_keyword_names(self):
        return [
            'quit',
        ]

    def quit(self, confirm='yes'):
        """Quit CLI

        Parameter:
        - `confirm`: Confirm 'Yes' or 'No' to quit when pending
                     CLI changes have not been committed.

        Example:
        | Quit | confirm=yes |

        """
        self._cli.quit(self._process_yes_no(confirm))
