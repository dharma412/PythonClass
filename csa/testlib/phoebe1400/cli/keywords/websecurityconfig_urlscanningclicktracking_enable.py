# $Id:
# $DateTime:
# $Author:

from common.cli.clicommon import CliKeywordBase

class websecurityconfig_urlscanningclicktracking_enable(CliKeywordBase):
    """
    Batch Command to enable clicktracking for url scanning purpose
    cli -> websecurityconfig urlscanning clicktracking enable
    """
    def get_keyword_names(self):
        return ['websecurityconfig_urlscanningclicktracking_enable']

    def websecurityconfig_urlscanningclicktracking_enable(self):
        """
        *Example:*
        | ${status} | Websecurityconfig Urlscanningclicktracking Enable |
        | Log | ${status} |
        """
        return (self._cli.websecurityconfigurlscanningclicktrackingenable())