#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase
import traceback

class DaneVerify(CliKeywordBase):
    """
    cli -> daneverify

    Provides keyword(s) to run daneverify command
    """

    def get_keyword_names(self):
        return ['dane_verify']

    def dane_verify(self, domain):
        """
        *Params*
         domain - Name of the domain to run daneverify

        *Returns*:
         Strint - Output of daneverify command

        *Examples*:
        | ${results}=    | Dane Verify | test-dane.net                  |
        | Should Contain | ${results}  | DANE SUCCESS for test-dane.net |
        """
        try:
            return self._cli.daneverify(domain)
        except Exception,e:
            self._cli.restart()
            traceback.print_exc()
            raise e
