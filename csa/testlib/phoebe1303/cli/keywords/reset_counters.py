#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/reset_counters.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class ResetCounters(CliKeywordBase):
    """
       Provides keyword to reset counters in the system
    """

    def get_keyword_names(self):
        return ['reset_counters']

    def reset_counters(self):
        """
        Reset all of the counters in the system.

        *Parameters*:
            None

        *Example*:
        | Reset Counters |
        """
        self._cli.resetcounters()
