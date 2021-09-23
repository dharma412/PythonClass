#!/usr/bin/env python
# $Id: isadminclirestricted.py,v 1.0
# $DateTime: 2017/03/15
# $Author: okurochk

from common.cli.clicommon import CliKeywordBase


class IsAdminCliRestricted(CliKeywordBase):
    """
    Checks if standard set of CLI commands is restricted.
    """

    def get_keyword_names(self):
        return ['is_admin_cli_restricted']

    def is_admin_cli_restricted(self):
        """
         Checks if standard set of CLI commands is either available or restricted.
         Returns True or False.
         Returns None if command returned unexpected output.
         *Parameters:*
         None

         *Example:*
         | ${is_restricted}=  |Is Admin Cli Restricted |
         | Run Keyword if  | ${is_restricted} |
         """

        return str(self._cli.isadminclirestricted())
