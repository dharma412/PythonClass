# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/whoami.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

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