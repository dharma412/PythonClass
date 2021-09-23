from common.cli.clicommon import CliKeywordBase

class Proxystat(CliKeywordBase):
    """
    Returns output of cli/proxystat
    """
    def get_keyword_names(self):
        return [
            'proxystat',
        ]

    def proxystat(self):
        """
        Returns the output of cli command 'proxystat'

        Parameters:
        None

        Example:
        | ${log}=   | Proxystat |
        """
        return str(self._cli.proxystat())
