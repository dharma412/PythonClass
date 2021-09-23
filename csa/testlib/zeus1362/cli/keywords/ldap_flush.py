#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/ldap_flush.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class LDAPFlush(CliKeywordBase):

    """Keywords for ldapflush CLI command."""

    def get_keyword_names(self):
        return ['ldap_flush',]

    def ldap_flush(self, confirm=DEFAULT):
        """Flush any cached LDAP results.

        Parameters:
        - `confirm`: confirm LDAP cache flush.

        Examples:
        | LDAP Flush |
        | LDAP Flush | yes |
        """
        self._cli.ldapflush(self._process_yes_no(confirm))

