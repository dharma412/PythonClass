
from common.cli.clicommon import CliKeywordBase


class SmartAccountInfo(CliKeywordBase):
    """
        cli -> smartaccountinfo
    """
    def get_keyword_names(self):
        return ['smart_account_info']

    def smart_account_info(self):
        """
        cli -> smartaccountinfo

        Returns Smart License account info.
        You will see some valid values only when Smart License is enabled.

        *Params*:
        - None

        *Return*:
        - A dictionary containing below keys and their values:
            - Product Instance ID
            - Smart Account Domain
            - Smart Account ID
            - Smart Account Name
            - VLN
            - Virtual Account Domain
            - Virtual Account ID

        *Examples*:
        |  {$smart_account_info}= | Smart Account Info    |
        |  Log Dictionary         | {$smart_account_info} |
        """
        return self._cli.smartaccountinfo()
