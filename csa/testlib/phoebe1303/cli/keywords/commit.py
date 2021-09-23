#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase

class Commit(CliKeywordBase):
    """Commit changes."""

    def get_keyword_names(self):
        return ['commit', ]

    def commit(self, comment='SARF configurator', rollback=None):
        """Commit Changes.

        Use this keyword to commit changes that has been made.

        Parameters:
        - `comment`: A string describing the changes you have made. Optional.
        - `rollback`: string decribing if changes has to be rollback. 'Y' or 'N'

        Examples:
        | Commit |

        | Commit | comment=Some changes has been made |

        | Commit | comment=Some changes has been made | rollback=Yes |
        """

        if rollback:
            self._cli.commit(comment,rollback)
        else:
            self._cli.commit(comment)
