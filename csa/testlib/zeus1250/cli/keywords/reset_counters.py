# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/reset_counters.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $
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
