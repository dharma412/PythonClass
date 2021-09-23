#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/mail_config.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class MailConfig(CliKeywordBase):
    """Mails the current XML configuration to the given email address.
       You may specify more than one address.
    """

    def get_keyword_names(self):
        return [
            'mail_config',
        ]

    def mail_config(self, email, mask_passwd=DEFAULT):
        """Mail config

        Parameters:
        - `email`: email(s) to send the configuration file to.
                   String of comma separated values to represent
                   more than one emails
        - `mask_passwd`: To mask password. Must be YES or NO

        Example:
        | Mail Config | test@test.qa | mask_passwd=NO |

        """
        mask_passwd = str(mask_passwd).lower()
        if mask_passwd in ('yes', 'y'):
            mask_passwd = 1
        else:
            mask_passwd = 2
        self._cli.mailconfig(email, mask_passwd)
