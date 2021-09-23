# $Id:
# $DateTime:
# $Author:

from common.cli.clicommon import CliKeywordBase


class websecurityconfig_urlscanningclicktracking_disable(CliKeywordBase):
    """
    Batch Command to disable clicktracking for url scanning purpose
    cli -> websecurityconfig urlscanning clicktracking disable
    """

    def get_keyword_names(self):
        return ['websecurityconfig_urlscanningclicktracking_disable']

    def websecurityconfig_urlscanningclicktracking_disable(self):
        """
        *Example:*
        | ${status} | Websecurityconfig Urlscanningclicktracking Disable |
        | Log | ${status} |
        """
        return (self._cli.websecurityconfigurlscanningclicktrackingdisable())
