#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/reset_counters.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

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
