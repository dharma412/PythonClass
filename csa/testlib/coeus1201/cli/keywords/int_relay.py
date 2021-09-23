#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/int_relay.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class IntRelay(CliKeywordBase):
    """Update the internal SMTP relay hosts.
    """

    def get_keyword_names(self):
        return [
            'int_relay_new',
            'int_relay_edit',
            'int_relay_delete',
            'int_relay_routing_table',
            'int_relay_auth',
        ]

    def int_relay_new(self, host):
        """Add new SMTP relay entry.

        intrelay > new

        Parameters:
        - `host`: the hostname or IP of the SMTP relay. It may be suffixed with
        a colon to indicate a port to use other than 25, such as
        'smtp.example.com:547'.

        Examples:
        | Int Relay New | foo.com |
        | Int Relay New | foobar.com:26 |
        """

        self._cli.intrelay().new(host)

    def int_relay_edit(self,
                       old_host,
                       new_host=DEFAULT):
        """ Modify SMTP relay entry.

        intrelay > edit

        Parameters:
        - `old_host`: host entry to edit.
        - `new_host`: hostname of IP which will be used to replace the old one.

        Examples:
        | Int Relay Edit | foo.com | new_host=bar.com |
        """

        self._cli.intrelay().edit(old_host, new_host)

    def int_relay_delete(self, host):
        """Remove SMTP relay entry.

        intrelay > delete

        Parameters:
        - `host`: host entry to delete.

        Examples:
        | Int Relay Delete | bar.com |
        | Int Relay Delete | foobar.com:26 |
        """

        self._cli.intrelay().delete(host)

    def int_relay_auth(self, use_auth=DEFAULT, user=DEFAULT, password=DEFAULT):
        """Configure SMTP authentication.

        intrelay > auth

        Parameters:
        - `use_auth`: Use SMTP authentication or not. Acceptable values
        are 'yes' or 'no'. Default 'no'.
        - `user`: SMTP authentication username.
        - `password`: SMTP authentication password.

        Examples:
        | Int Relay Auth |
        | Int Relay Auth | use_auth=yes | user=foo | password=bar |
        """

        use_auth = self._process_yes_no(use_auth)
        self._cli.intrelay().auth(use_auth, user, password)

    def int_relay_routing_table(self, table=DEFAULT):
        """Specify which routing table will be used.

        intrelay > routing table

        Parameters:
        - `table`: routing table to use. Available tables: 'Data', 'Management'.
        Default is 'Management'.

        Examples:
        | Int Relay Routing Table |
        | Int Relay Routing Table | table=Data |
        | Int Relay Routing Table | table=Management |
        """

        self._cli.intrelay().routing_table(table)
