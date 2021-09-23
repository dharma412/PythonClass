#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/redirect_recipients.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase
from sal.containers.yesnodefault import is_yes

class RedirectRecipients(CliKeywordBase):

    """Keywords for redirectrecipients CLI command."""

    def get_keyword_names(self):
        return ['redirect_recipients']

    def redirect_recipients(self, hostname, confirm='yes'):
        """Redirect recipients.

        Parameters:
        - `hostname`: Host or IP address to send all messages to.
        - `confirm`: Whether or not to redirect all mail in the queue to
          'hostname'. 'Yes' by default.

        Examples:
        | Redirect Recipients | test13.com | confirm=No |
        | Redirect Recipients | 1.2.3.4 |
        """

        input_dict = {
                'hostname': hostname,
                'confirm': self._process_yes_no(confirm),
                }

        self._cli.redirectrecipients(input_dict)
