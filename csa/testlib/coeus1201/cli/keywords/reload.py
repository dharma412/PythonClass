# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/reload.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
SARF CLI command: reload
"""

from common.cli.clicommon import CliKeywordBase

class Reload(CliKeywordBase):
    """
    Returns output of cli/reload command
    """

    def get_keyword_names(self):
        return [
            'reload',
        ]

    def reload(self, action='y'):
        """
        Returns the output of cli command 'reload'

        Parameters:
        None

        Example:
        | Reload action=y|
        """

        return str(self._cli.reload(action))
