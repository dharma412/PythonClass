from common.cli.clicommon import CliKeywordBase


class Whoami(CliKeywordBase):
    """
    Displays your login ID and the groups you are a member of.
    """

    def get_keyword_names(self):
        return ['whoami']

    def whoami(self):
        """
        Returns the following attributes of the connected user:
        - username
        - Fullname
        - Groups

        *Parameters:*
        None

        *Example:*
        | ${log}=   | Whoami |
        """

        return str(self._cli.whoami())
