# $Id:
# $DateTime:
# $Author:

from common.cli.clicommon import CliKeywordBase

class outbreakconfigclicktracking_disable(CliKeywordBase):
    """
    Batch Command to disable clicktracking for outbreakconfig
    cli -> outbreakconfig clicktracking disable
    """
    def get_keyword_names(self):
        return ['outbreakconfigclicktracking_disable']

    def outbreakconfigclicktracking_disable(self):
        """
        *Example:*
        | ${status} | Outbreakconfigclicktracking Disable |
        | Log | ${status} |
        """
        return (self._cli.outbreakconfigclicktrackingdisable())