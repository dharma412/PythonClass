#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/ldap_flush.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class LDAPFlush(CliKeywordBase):
    """Keywords for ldapflush CLI command."""

    def get_keyword_names(self):
        return ['ldap_flush', ]

    def ldap_flush(self, confirm=DEFAULT):
        """Flush any cached LDAP results.

        Parameters:
        - `confirm`: confirm LDAP cache flush.

        Examples:
        | LDAP Flush |
        | LDAP Flush | yes |
        """
        self._cli.ldapflush(self._process_yes_no(confirm))
