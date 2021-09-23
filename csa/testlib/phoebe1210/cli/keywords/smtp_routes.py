#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/smtp_routes.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class SmtpRoutes(CliKeywordBase):
    """
    CLI command: smtproutes
    """

    def get_keyword_names(self):
        return ['smtp_routes_new',
                'smtp_routes_delete',
                'smtp_routes_print',
                'smtp_routes_export',
                'smtp_routes_import',
                'smtp_routes_clear',
                'smtp_routes_edit_add',
                'smtp_routes_edit_replace',
                'smtp_routes_edit_remove', ]

    def smtp_routes_new(self, *args):
        """Create a new route.

        CLI command: smtproutes > new

        *Parameters:*
        - `domain`: The domain for which to set up a permanent route.
        Partial hostnames such as ".example.com" are allowed.
        Use "ALL" for the default route.
        - `dest_hosts`: The destination hosts, separated by commas, that mail for `domain` should be delivered to.
        Enter _USEDNS_ by itself to use normal DNS resolution for this route.
        Enter _/dev/null_ by itself if you wish to discard the mail.
        Enclose in square brackets to force resolution via address (A) records, ignoring any MX records.
        - `smtp_profiling`: Associate an SMTP authentication profile with this route. YES or NO.
        - `smtp_profile`: The SMTP authentication profile to use.

        *Return:*
        None

        *Examples:*
        | Smtp Routes New |
        | ... | domain=${qa} |
        | ... | dest_hosts=${CLIENT} |
        | ... | smtp_profiling=yes |
        | ... | smtp_profile=${out} |

        | Smtp Routes New |
        | ... | domain=${ru} |
        | ... | dest_hosts=/dev/null |

        | Smtp Routes New |
        | ... | domain=${cisco} |
        | ... | dest_hosts=${CLIENT}:777/pri\=10, ${CLIENT_IP}:888/pri\=100 |

        | Smtp Routes New |
        | ... | domain=${gmail} |
        | ... | dest_hosts=USEDNS |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtproutes().new(**kwargs)

    def smtp_routes_delete(self, *args):
        """Remove a route.

        CLI command: smtproutes > delete

        *Parameters:*
        - `domain`: The hostname you want to stop routing.

        *Return:*
        None

        *Examples:*
        | Smtp Routes Delete |
        | ... | domain=${ru} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtproutes().delete(**kwargs)

    # def smtp_routes_print(self, *args):
    def smtp_routes_print(self):
        """Display all routes.

        CLI command: smtproutes > print

        *Parameters:*
        None

        *Return:*
        Raw output.

        *Examples:*
        | ${routes} | Smtp Routes Print |
        | Log | ${routes} |
        """
        # kwargs = self._convert_to_dict(args)
        # return self._cli.smtproutes().print_all(**kwargs)
        return self._cli.smtproutes().print_all()

    def smtp_routes_export(self, *args):
        """Export all routes to a file.

        CLI command: smtproutes > export

        *Parameters:*
        - `filename`: A name for the exported file.

        *Return:*
        None

        *Examples:*
        | Smtp Routes Export |
        | ... | filename=${routes_file} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtproutes().export_routes(**kwargs)

    def smtp_routes_import(self, *args):
        """Import new routes from a file.

        CLI command: smtproutes > import

        *Parameters:*
        - `filename`: The name of the file on machine to import from.

        *Return:*
        None

        *Examples:*
        | Smtp Routes Import |
        | ... | filename=${routes_file} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtproutes().import_routes(**kwargs)

    def smtp_routes_clear(self):
        """Remove all routes.

        CLI command: smtproutes > clear

        *Parameters:*
        None

        *Return:*
        None

        *Examples:*
        | Smtp Routes Clear |
        """
        self._cli.smtproutes().clear()

    def smtp_routes_edit_add(self, *args):
        """Edit SMTP Route. Add new destination hosts.

        CLI command: smtproutes > edit > SOME_DOMAIN > ADD

        *Parameters:*
        - `domain`: The hostname to edit.
        - `new_domain`: The new domain for which you want to set up a permanent route.
        - `dest_hosts`: The destination hosts, separated by commas, that mail for `domain` should be delivered to.
        Enter _USEDNS_ by itself to use normal DNS resolution for this route.
        Enter _/dev/null_ by itself if you wish to discard the mail.
        Enclose in square brackets to force resolution via address (A) records, ignoring any MX records.
        - `smtp_profiling`: Associate an SMTP authentication profile with this route. YES or NO.
        - `smtp_profile`: The SMTP authentication profile to use.

        *Return:*
        None

        *Examples:*
        | Smtp Routes Edit Add |
        | ... | domain=${qa} |
        | ... | dest_hosts=mail.${NETWORK} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtproutes(). \
            edit(kwargs.pop('domain'), kwargs.pop('new_domain', None)). \
            add(**kwargs)

    def smtp_routes_edit_replace(self, *args):
        """Edit SMTP Route. Specify a new destination or set of destinations.

        CLI command: smtproutes > edit > SOME_DOMAIN > REPLACE

        *Parameters:*
        - `domain`: The hostname to edit.
        - `new_domain`: The new domain for which you want to set up a permanent route.
        - `dest_hosts`: The destination hosts, separated by commas, that mail for `domain` should be delivered to.
        Enter _USEDNS_ by itself to use normal DNS resolution for this route.
        Enter _/dev/null_ by itself if you wish to discard the mail.
        Enclose in square brackets to force resolution via address (A) records, ignoring any MX records.
        - `smtp_profiling`: Associate an SMTP authentication profile with this route. YES or NO.
        - `smtp_profile`: The SMTP authentication profile to use.

        *Return:*
        None

        *Examples:*
        | Smtp Routes Edit Replace |
        | ... | domain=${qa} |
        | ... | new_domain=${ua} |
        | ... | smtp_profiling=no |
        | ... | dest_hosts=boo.mail.${NETWORK} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtproutes(). \
            edit(kwargs.pop('domain'), kwargs.pop('new_domain', None)). \
            replace(**kwargs)

    def smtp_routes_edit_remove(self, *args):
        """Edit SMTP Route. Remove an existing destination.

        CLI command: smtproutes > edit > SOME_DOMAIN > REMOVE

        *Parameters:*
        - `domain`: The hostname to edit.
        - `new_domain`: The new domain for which you want to set up a permanent route.
        - `dest_hosts`: The destination to remove.

        *Return:*
        None

        *Examples:*
        | Smtp Routes Edit Remove |
        | ... | domain=${cisco} |
        | ... | dest_hosts=${CLIENT} |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.smtproutes(). \
            edit(kwargs.pop('domain'), kwargs.pop('new_domain', None)). \
            remove(**kwargs)
