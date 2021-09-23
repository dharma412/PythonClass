#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/reset_injctl.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class Resetinjctl(CliKeywordBase):
    """
       Provides keyword to reset the internal injection counters
    """

    def get_keyword_names(self):
        return ['reset_injctl']

    def reset_injctl(self):
        """
        Reset the internal injection counters (hidden command) to zero
        for throttling and such.

        *Parameters*:
            None

        *Example*:
        | Reset Injctl |
        """
        self._cli.resetinjctl()
