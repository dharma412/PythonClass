#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase

class smartaccountinfo(CliKeywordBase):

    def get_keyword_names(self):
        return ['smart_account_details']

    def smart_account_details(self):
        """
        Provides the details of smart account.

        | ${smart_account_info}= | Smart Account Details|
        returns Dictionary
        """
        return self._cli.smartaccountinfo().smart_account_info()
