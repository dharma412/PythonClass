# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/reset_counters.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $
from common.cli.clicommon import CliKeywordBase
class ResetCounters(CliKeywordBase):
    """
    Reset all of the counters in the system.
    """
    def get_keyword_names(self):
        return ['resetcounters' ]
    def resetcounters(self):
        """
        Reset all of the counters in SMA.
        Parameters:
            None
        Example:
        | ResetCounters |
        """
        self._cli.resetcounters()
