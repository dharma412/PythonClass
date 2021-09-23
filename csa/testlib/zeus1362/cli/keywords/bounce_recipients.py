#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/bounce_recipients.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)
from sal.containers.yesnodefault import YES, NO, is_yes

class BounceRecipients(CliKeywordBase):
    """Bounce messages from the queue."""

    def get_keyword_names(self):
        return ['bouncerecipients_all',
                'bouncerecipients_address',
                'bouncerecipients_host']

    def bouncerecipients_all(self, confirm='yes', check_status='no'):
        """Bounce all messages.

        bouncerecipients > all

        Parameters:
            - `confirm`: whether or not bounce messages. 'Yes' by default.
            - `check_status`: whether or not check how deliveries are currently
              suspended. 'No' by default.

        Return:
            Return count of bounced messages.

        Examples:
        | ${log}= | Bouncerecipients All |
        """
        confirm = self._process_yes_no(confirm)
        check_status = self._process_yes_no(check_status)

        return self._cli.bouncerecipients(how='all', sure=confirm,
                                    check_status=check_status)

    def bouncerecipients_address(self, address, confirm='yes',
                                            check_status='no'):
        """ Bounce messages by address.

        bouncerecipients > address

        Parameters:
            - `address`: the Envelope From address for the messages you wish to
              bounce.
            - `confirm`: whether or not bounce messages. 'Yes' by default.
            - `check_status`: whether or not check how deliveries are currently
              suspended. 'No' by default.

        Return:
            Return number of bounced messages.

        Examples:
        | ${log}= | Bouncerecipients Address | address | confirm=No |
        """
        confirm = self._process_yes_no(confirm)
        check_status = self._process_yes_no(check_status)

        return self._cli.bouncerecipients(how='sender', address=address, sure=confirm,
                                    check_status=check_status)

    def bouncerecipients_host(self, host, confirm='yes', check_status='no'):
        """ Bounce messages by host.

        bouncerecipients > host

        Parameters:
            - `host`: the hostname for the messages to bounce.
            - `confirm`: whether or not bounce messages. 'Yes' by default.
            - `check_status`: whether or not check how deliveries are currently
              suspended. 'No' by default.

        Return:
            Return count of bounced messages.

        Examples:
        | ${log}= | Bouncerecipients Host | host |
        """
        confirm = self._process_yes_no(confirm)
        check_status = self._process_yes_no(check_status)

        return self._cli.bouncerecipients(how='host', hostname=host, sure=confirm,
                                    check_status=check_status)
