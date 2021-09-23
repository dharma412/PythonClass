#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/mail_config.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase, DEFAULT


class MailConfig(CliKeywordBase):
    """Mails the current XML configuration to the given email address.
       You may specify more than one address.
    """

    def get_keyword_names(self):
        return ['mail_config']

    def mail_config(self, email, passwd_option=DEFAULT):
        """Mail config

        Parameters:
        - `email`: email(s) to send the configuration file to.
                   String of comma separated values to represent
                   more than one emails
        - `passwd_option`: Takes one of these
                           - Mask
                           - Encrypt
                           - Plain

        Example:
        | Mail Config | test@test.qa | passwd_option=Mask |

        """
        pass_opt_dict = {}
        pass_opt_dict['mask'] = 1
        pass_opt_dict['encrypt'] = 2
        pass_opt_dict['plain'] = 3
        if passwd_option.lower() not in pass_opt_dict:
            raise ValueError("%s option is not available" % passwd_option)
        self._cli.mailconfig(email, pass_opt_dict[passwd_option.lower()])
