# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/whoami.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Whoami(CliKeywordBase):
    """
    Returns information about current user
    """
    def get_keyword_names(self):
        return ['whoami' ]

    def whoami(self):
        """
        Returns the following attributes of the current user:
        - user name
        - full name
        - list of groups

        *Parameters:*
        None

        *Example:*
        | ${log}=   | Whoami |
        """

        return str(self._cli.whoami())