from common.cli.clicommon import CliKeywordBase


class Who(CliKeywordBase):
    """
    Returns list of connected users
    """

    def get_keyword_names(self):
        return ['who']

    def who(self):
        """
        Returns the following attributes of the connected users:
        - username
        - role
        - login time
        - idle time
        - remote host
        - what

        *Parameters:*
        None

        *Example:*
        | ${log}=   | Who |
        """

        return str(self._cli.who())
