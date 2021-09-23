#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/smtp_routes.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class SMTPRoutes(CliKeywordBase):

    """Keywords for smtproutes CLI command."""

    def get_keyword_names(self):
        return ['smtp_routes_new',
                'smtp_routes_edit_add',
                'smtp_routes_edit_remove',
                'smtp_routes_edit_replace',
                'smtp_routes_delete',
                'smtp_routes_print',
                'smtp_routes_import',
                'smtp_routes_export',
                'smtp_routes_clear',
                ]

    def smtp_routes_new(self, domain, destination):
        """Create a new route.

        Parameters:
        - `domain`: domain for which to set up a permanent route.
        - `destination`: destination to route mail to.

        Examples:
        | SMTP Routes New | example.com | /dev/null |
        | SMTP Routes New | example.com | mx1.example.com, mx2.example.com |
        """
        self._cli.smtproutes().new(domain=domain, dest_hosts=destination)

    def smtp_routes_edit_add(self, domain, destination):
        """Add new destination to the route.

        Parameters:
        - `domain`: domain to add destination to.
        - `destination`: destination to add to the route.

        | SMTP Routes Edit Add | example.com | mx3.example.com |
        """
        self._cli.smtproutes().edit(domain).add(destination)

    def smtp_routes_edit_remove(self, domain, destination):
        """Remove an existing destination from the route.

        Parameters:
        - `domain`: domain to delete destination from.
        - `destination`: destination to delete from the route.

        Examples:
        | SMTP Routes Edit Remove | example.com | mx2.example.com |
        """
        self._cli.smtproutes().edit(domain).remove(destination)

    def smtp_routes_edit_replace(self, domain, destination):
        """Set new destination for the route.

        Parameters:
        - `domain`: domain to set up a new destination for.
        - `destination`: destination to route mail to.

        Examples:
        | SMTP Routes Edit Replace | example.com | USEDNS |
        | SMTP Routes Edit Replace | example.com | mx.test.com |
        """
        self._cli.smtproutes().edit(domain).replace(destination)

    def smtp_routes_delete(self, domain):
        """Remove a route.

        Parameters:
        - `domain`: domain to stop routing to.

        Examples:
        | SMTP Routes Delete | example.com |
        """
        self._cli.smtproutes().delete(domain)

    def smtp_routes_print(self):
        """Display all routes.

        Return:
        An output of SMTPROUTES -> PRINT CLI command.

        Examples:
        | ${routes} = | SMTP Routes Print |
        """
        return self._cli.smtproutes().print_all()

    def smtp_routes_import(self, filename):
        """Import new routes from a file.

        Parameters:
        - `filename`: name of the file to import routes from.

        Examples:
        | SMTP Routes Import | routes.dat |
        """
        self._cli.smtproutes().import_routes(filename)

    def smtp_routes_export(self, filename):
        """Export all routes to a file.

        Parameters:
        - `filename`: name of the file to export routes to.

        Examples:
        | SMTP Routes Export | routes.dat |
        """
        self._cli.smtproutes().export(filename)

    def smtp_routes_clear(self):
        """Remove all routes.

        Examples:
        | SMTP Routes Clear |
        """
        self._cli.smtproutes().clear()

