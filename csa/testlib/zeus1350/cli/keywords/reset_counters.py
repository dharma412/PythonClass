# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/reset_counters.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $
from common.cli.clicommon import CliKeywordBase


class ResetCounters(CliKeywordBase):
    """
    Reset all of the counters in the system.
    """

    def get_keyword_names(self):
        return ['resetcounters']

    def resetcounters(self):
        """
        Reset all of the counters in SMA.
        Parameters:
            None
        Example:
        | ResetCounters |
        """
        self._cli.resetcounters()
