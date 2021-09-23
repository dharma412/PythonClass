# $Id:
# $DateTime:
# $Author:

from common.cli.clicommon import CliKeywordBase


class outbreakconfigclicktracking_enable(CliKeywordBase):
    """
    Batch Command to enable clicktracking for outbreakconfig
    cli -> outbreakconfig clicktracking enable
    """

    def get_keyword_names(self):
        return ['outbreakconfigclicktracking_enable']

    def outbreakconfigclicktracking_enable(self):
        """
        *Example:*
        | ${status} | Outbreakconfigclicktracking Enable |
        | Log | ${status} |
        """
        return (self._cli.outbreakconfigclicktrackingenable())
