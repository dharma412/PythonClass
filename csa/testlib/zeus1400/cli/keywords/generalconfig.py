from common.cli.clicommon import CliKeywordBase

class generalconfig(CliKeywordBase):

    def get_keyword_names(self):
        return [
                'generalconfig_securex_status',
                'generalconfig_enable_securex',
                'generalconfig_disable_securex',
               ]

    def generalconfig_securex_status(self):
        """Keyword to get Securex Status

        *Parameters*
        will return the status of the securex status as
        |ENABLED|DISABLED

        Examples:
        |${status}= | GeneralConfig Securex Status |
        """
        return self._cli.generalconfig().get_securex_status()


    def generalconfig_disable_securex(self):
        """Keyword to disable Securex
        Examples:
        | Generalconfig Disable Securex |
        """
        return self._cli.generalconfig().disable_securex()


    def generalconfig_enable_securex(self):
        """Keyword to enable securex

        Examples:
        | Generalconfig Enable Securex|
        """
        return self._cli.generalconfig().enable_securex()

