#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/passwd.py#1 $

from common.cli.clicommon import CliKeywordBase

class Passwd(CliKeywordBase):
    """Change your password.
       Not available as a batch command.
       Guest users do not need to run the 'commit' command."""

    def get_keyword_names(self):
        return [
            'passwd',
        ]

    def passwd(self, old_pwd=None, new_pwd=None):
        """Change password.

        Parameters:
        - `old_pwd`: Old password, The password must be between 6 and 128 characters long
        - `new_pwd`: New password, The password must be between 6 and 128 characters long

        Example:
        | Passwd | old_pwd=ironport | new_pwd=123456 |

        """
        self._cli.passwd(old_pwd, new_pwd)
