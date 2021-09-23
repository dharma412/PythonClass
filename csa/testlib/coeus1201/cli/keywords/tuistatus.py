#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/tuistatus.py#1 $

from common.cli.clicommon import CliKeywordBase


class tuistatus(CliKeywordBase):
    """Tuistatus"""

    def get_keyword_names(self):
        return [
            'adagentstatus',
            'listlocalmappings',
        ]

    def adagentstatus(self):
        """adagentstatus listing.

        tuistatus > adagentstatus

        """

        return self._cli.tuistatus().adagentstatus()


    def listlocalmappings(self):

        """listlocalmappings listing.

        tuistatus > listlocalmappings
        """

        return self._cli.tuistatus().listlocalmappings()
