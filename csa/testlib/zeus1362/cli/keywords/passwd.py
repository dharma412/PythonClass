#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/passwd.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Passwd(CliKeywordBase):
    """Change your password.
       Not available as a batch command.
       Guest users do not need to run the 'commit' command."""

    def get_keyword_names(self):
        return ['passwd']

    def passwd(self, old_pwd=None, new_pwd=None, abbrev=True):
        """Change password.

        Parameters:
        - `old_pwd`: Old password.
        - `new_pwd`: New password.
        - `abbrev` : which of commands will be used(both command are identical):
        | *abbrev* | *command* |
        | True   | passwd  |
        | False  | password |

        Example:
        | Passwd | old_pwd=ironport | new_pwd=123456 |

        """
        self._cli.passwd(old_pwd, new_pwd, abbrev)
