# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/who.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
SARF CLI command: who
"""

from common.cli.clicommon import CliKeywordBase

class Who(CliKeywordBase):
    """
    Returns output of cli/who command
    """

    def get_keyword_names(self):
        return [
            'who',
        ]

    def who(self):
        """
        Returns the output of cli command 'who'

        Parameters:
        None

        Example:
        | Who |
        """

        return str(self._cli.who())
