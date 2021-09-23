#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase

class Passwd(CliKeywordBase):
    """Change your password."""

    def get_keyword_names(self):
        return ['passwd']

    def passwd(self, *args):
        """Change password.

        Parameters:
        - `old_pwd`: Old password, The password must be between 8 and 128 characters long,
           with one uppercase, one special char and one number.
        - `new_pwd`: New password, The password must be between 8 and 128 characters long,
           with one uppercase, one special char and one number.

        Example:
        | Passwd | old_pwd=Cisco123$ | new_pwd=Ironport@123 |

        """

        kwargs = self._convert_to_dict(args)
        kwargs['confirm_new_pwd'] = kwargs['new_pwd']
        self._cli.passwd(**kwargs)
