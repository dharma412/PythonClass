#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/ldaptest.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)


class LDAPTest(CliKeywordBase):
    """
    cli -> ldaptest

    Perform a single LDAP query test based on the parameters given.
    """

    def get_keyword_names(self):
        return ['ldap_test']

    def ldap_test(self, query_to_test='1', *args):
        """Perform a single LDAP query test based on the parameters given.
        Note that ldaptest will only attempt to connect to the first
        server on the failover list.

        *Parameters:*
        - `query_to_test`: select which LDAP query to test (query number or
        name). Entry names and count depends on particular LDAP profile
        configuration but in general it looks like:
        | 1 | sma19.accept |
        | 2 | sma19.externalauth |
        | 3 | sma19.group |
        | 4 | sma19.isq_alias |
        | 5 | sma19.isq_user_auth |
        | 6 | sma19.masquerade |
        | 7 | sma19.routing |
        | 8 | sma19.smtpauth |
        - `email_addr`: email address to use in query, mandatory
        - `group`: group name to use in query (only for Group query type),
        mandatory
        - `uid`: user identity to use in query (only for isqauth and smtpauth
        query types), mandatory
        - `passwd`: password to use in query, (only for isqauth and smtpauth
        query types), mandatory
        - `bind_passwd`: password for testing LDAP bind, (only for external auth
        and ISQ auth), mandatory

        *Exceptions:*
        - `ConfigError`: if no LDAP queries are configured

        *Return:*
        Raw output - result of ldaptest command output

        *Examples:*
        | ${accept_qres}= | LDAP Test | accept | email_addr=akolodiy@test.com |
        | Should Contain | ${accept_qres} | Action: pass |
        | ${masq_qres}= | LDAP Test | masquerade | email_addr=akolodiy@test.com |
        | Should Contain | ${masq_qres} | Action: masquerade |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.ldaptest(query_to_test=query_to_test, **kwargs)
