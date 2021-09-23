#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/delete_recipients.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)
from sal.containers.yesnodefault import YES, NO, is_yes

class DeleteRecipients(CliKeywordBase):
    """Delete messages from the queue."""

    def get_keyword_names(self):
        return ['deleterecipients_all',
                'deleterecipients_address',
                'deleterecipients_host']

    def deleterecipients_all(self, confirm='yes'):
        """Delete all messages.

        deleterecipients > all

        Parameters:
            - `confirm`: whether or not delete messages. 'Yes' by default.

        Return:
            Return count of deleted messages.

        Examples:
        | ${count}= | Deleterecipients All |
        """
        confirm = self._process_yes_no(confirm)

        return self._cli.deleterecipients(how='all', sure=confirm)

    def deleterecipients_address(self, address, confirm='yes'):
        """ Delete messages by address.

        deleterecipients > address

        Parameters:
            - `address`: the Envelope From address for the messages you wish to
              delete.
            - `confirm`: whether or not delete messages. 'Yes' by default.

        Return:
            Return count of deleted messages.

        Examples:
        | ${count}= | Deleterecipients Address | address | confirm=No |
        """
        confirm = self._process_yes_no(confirm)

        return self._cli.deleterecipients(how='sender', sender=address, sure=confirm)

    def deleterecipients_host(self, host, confirm='yes'):
        """ Delete messages by host.

        deleterecipients > host

        Parameters:
            - `host`: the hostname for the messages to delete.
            - `confirm`: whether or not delete messages. 'Yes' by default.

        Return:
            Return count of deleted messages.

        Examples:
        | ${count}= | Deleterecipients Host | host |
        """
        confirm = self._process_yes_no(confirm)

        return self._cli.deleterecipients(how='host', host=host, sure=confirm)
