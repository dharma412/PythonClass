#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/smtp_relay.py#1 $

from common.cli.clicommon import CliKeywordBase

class SmtpRelay(CliKeywordBase):
    """Update the internal SMTP relay hosts.
    """

    def get_keyword_names(self):
        return [
            'smtp_relay_new',
            'smtp_relay_edit',
            'smtp_relay_delete',
            'smtp_relay_routing_table',
            'smtp_relay_auth',
        ]

    def smtp_relay_new(self, host):
        """Add new SMTP relay entry.

        smtprelay > new

        Parameters:
        - `host`: the hostname or IP of the SMTP relay. It may be suffixed with
        a colon to indicate a port to use other than 25, such as
        'smtp.example.com:547'.

        Examples:
        | SMTP Relay New | foo.com |
        | SMTP Relay New | foobar.com:26 |
        """

        self._cli.smtprelay().new(host)

    def smtp_relay_edit(self,
                       old_host,
                       new_host=''):
        """Edit SMTP relay entry.

        smtprelay > edit

        Parameters:
        - `old_host`: host entry to edit.
        - `new_host`: hostname of IP which will be used to replace the old one.

        Examples:
        | SMTP Relay Edit | foo.com | new_host=bar.com |
        """

        self._cli.smtprelay().edit(old_host, new_host)

    def smtp_relay_delete(self, host):
        """Delete SMTP relay entry.

        smtprelay > delete

        Parameters:
        - `host`: host entry to delete.

        Examples:
        | SMTP Relay Delete | bar.com |
        | SMTP Relay Delete | foobar.com:26 |
        """

        self._cli.smtprelay().delete(host)

    def smtp_relay_auth(self, use_auth='', user='', password=''):
        """Set SMTP relay auth parameters.

        smtprelay > auth

        Parameters:
        - `use_auth`: Use SMTP authentication or not. Acceptable values
        are 'yes' or 'no'.
        - `user`: SMTP authentication username.
        - `password`: SMTP authentication password.

        Examples:
        | SMTP Relay Auth |
        | SMTP Relay Auth | use_auth=yes | user=foo | password=bar |
        """

        use_auth = self._process_yes_no(use_auth)
        self._cli.smtprelay().auth(use_auth, user, password)

    def smtp_relay_routing_table(self, table=''):
        """Specify which routing table will be used.

        smtprelay > routing table

        Parameters:
        - `table`: routing table to use. Available tables: 'Data', 'Management'.

        Examples:
        | SMTP Relay Routing Table |
        | SMTP Relay Routing Table | table=Data |
        | SMTP Relay Routing Table | table=Management |
        """

        self._cli.smtprelay().routingtable(table)
