#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/keywords/passwd.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Passwd(CliKeywordBase):
    """Change your password.
       Not available as a batch command.
       Guest users do not need to run the 'commit' command."""

    def get_keyword_names(self):
        return ['passwd']

    def passwd(self, old_pwd=None, new_pwd=None, abbrev=True, sys_gen_passwd=None):
        """Change password.

        Parameters:
        - `old_pwd`: Old password.
        - `new_pwd`: New password.
        - `abbrev` : which of commands will be used(both command are identical):
        | *abbrev* | *command* |
        | True   | passwd  |
        | False  | password |
        - `sys_gen_passwd` : yes or No

        Example:
        | Passwd | old_pwd=ironport | new_pwd=123456 |
        | ${sys_psw}= | Passwd | old_pwd=ironport | sys_gen_passwd=yes |

        """
        return self._cli.passwd(old_pwd, new_pwd, abbrev, sys_gen_passwd)
