#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/delivernow.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $


from common.cli.clicommon import CliKeywordBase


class DeliverNow(CliKeywordBase):

    """Keywords for delivernow CLI command"""

    def get_keyword_names(self):
        return ['deliver_now_all',
                'deliver_now_to_domain']

    def deliver_now_all(self):
        """Reschedule all messages for immediate delivery.

        Examples:
        | Deliver Now All |
        """
        self._cli.delivernow()

    def deliver_now_to_domain(self, domain):
        """Reschedule messages for immediate delivery for specific domain.

        Parameters:
        - `domain`: domain to schedule immediate delivery for.

        Examples:
        | Deliver Now To Domain | mail.qa |
        """
        self._cli.delivernow('host', domain)

