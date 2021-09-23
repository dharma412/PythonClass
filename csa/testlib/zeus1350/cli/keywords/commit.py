#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/commit.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
from common.util.misc import Misc


class Commit(CliKeywordBase):
    """Commit changes."""

    def get_keyword_names(self):
        return ['commit', ]

    def commit(self, comment='SARF configurator'):
        """Commit Changes.

        Use this keyword to commit changes that has been made.

        Parameters:
        - `comment`: A string describing the changes you have made. Optional.

        Examples:
        | Commit |

        | Commit | comment=Some changes has been made |
        """

        self._cli.commit(comment)
        Misc(self.dut, self.dut_version).wait_until_ready()
