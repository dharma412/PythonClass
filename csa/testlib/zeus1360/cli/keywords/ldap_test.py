#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/ldap_test.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)
from common.cli.cliexceptions import ConfigError


class LDAPTest(CliKeywordBase):

    """Keywords for ldaptest CLI command."""

    def get_keyword_names(self):
        return ['ldap_test_run',]

    def ldap_test_run(self, query_name=DEFAULT, identity=None, password=None,
        email_addr=None, group=None):
        """Perform a single LDAP query test.

        Parameters:
        - `query_name`: name of the query to perform test against.
        - `identity`: user identity to use in query.
        - `password`: password to use in query.
        - `email_addr`: email address to use in query.
        - `group`: group name to use in query.

        Return:
        An output of the ldaptest command execution.

        Examples:
        | LDAP Test Run | LDAP.externalauth | testuser | ironport |
        | LDAP Test Run | LDAP.isqalias | email_addr=testuser@mail.qa |

        Exceptions:
        - `ConfigError`: in case no identity or password was provided when
           testing authentication queries.
        """
        input_dict = {
            'query_to_test': query_name,
        }

        if all((identity, password)):
            input_dict.update({'uid': identity, 'passwd': password})
        elif any((identity, password)):
            raise ConfigError('Both identity and password must be provided')

        if email_addr is not None:
            input_dict.update({'email_addr': email_addr})

        if group is not None:
            input_dict.update({'group': group})

        return self._cli.ldaptest(input_dict)

