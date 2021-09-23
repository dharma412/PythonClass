#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/unsubscribe.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class Unsubscribe(CliKeywordBase):
    """Update the Global Unsubscribe list"""

    def get_keyword_names(self):
        return ['unsubscribe_new',
                'unsubscribe_delete',
                'unsubscribe_enable',
                'unsubscribe_disable',
                'unsubscribe_print',
                'unsubscribe_clear',
                'unsubscribe_import',
                'unsubscribe_export',
                'unsubscribe_drop',
                'unsubscribe_bounce',
               ]

    def unsubscribe_new(self, entry_name):
        """Create a new entry

        Parameters:
        - `entry_name`: entry to add

        Examples:
        | Unsubscribe New | @example.com |
        | Unsubscribe New | @.example1.com |
        | Unsubscribe New | example@ |
        """
        self._cli.unsubscribe().new(entry_name)

    def unsubscribe_delete(self, entry_name):
        """Remove an entry from Global Unsubscribe list.

        Parameters:
        - `entry_name`: entry to remove from list.

        Examples:
        | Unsubscribe Delete | @example.com |
        """
        self._cli.unsubscribe().delete(entry_name)

    def unsubscribe_enable(self):
        """Enable the Global Unsubscribe feature

        Examples:
        | Unsubscribe Enable |
        """
        self._cli.unsubscribe().setup('Yes')

    def unsubscribe_disable(self):
        """Disable the Global Unsubscribe feature.

        Examples:
        | Unsubscribe Disable |
        """
        self._cli.unsubscribe().setup('No')

    def unsubscribe_print(self):
        """Display all entries from Global Unsubscribe list.

        Return:
        An output of UNSUBSCRIBE -> PRINT CLI command.

        Examples:
        | ${uns} = | Unsubscribe Print |
        """
        return self._cli.unsubscribe().Print()

    def unsubscribe_clear(self):
        """Remove all entries from Global Unsubscribe list

        Examples:
        | Unsubscribe Clear |
        """
        self._cli.unsubscribe().clear()

    def unsubscribe_import(self, file_name):
        """Import entries from a file.

        Parameters:
        - `filename`: name of the file for import.

        Examples:
        | Unsubscribe Import | uns.dat |
        """
        self._cli.unsubscribe().Import(file_name)

    def unsubscribe_export(self, file_name):
        """Export all entries to a file.

        Parameters:
        - `filename`: name of the file for export

        Examples:
        | Unsubscribe Export | uns.dat |
        """
        self._cli.unsubscribe().export(file_name)

    def unsubscribe_drop(self):
        """Drop matching messages

        Examples:
        | Unsubscribe Drop |
        """
        self._cli.unsubscribe().setup('Yes', 'Drop')

    def unsubscribe_bounce(self):
        """Bounce matching messages

        Examples:
        | Unsubscribe Bounce |
        """
        self._cli.unsubscribe().setup('Yes', 'Bounce')