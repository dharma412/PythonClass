#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/test_auth_config.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class TestAuthConfig(CliKeywordBase):
    """If authentication is enabled, this command validates the authentication
    configuration values for a particular realm.
    """

    def get_keyword_names(self):
        return ['test_auth_config']

    def test_auth_config(self, realm_name=DEFAULT):
        """Authentication Configuration Test.

        Parameters:
        - `realm_name` : name of a configured authentication realm.

        Examples:
        | Test Auth Config | realm_name=test |
        | ${output} | Test Auth Config | realm_name=test |
        """
        output = self._cli.testauthconfig(realm_name)
        self._info(output)
        return output