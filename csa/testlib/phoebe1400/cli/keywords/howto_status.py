#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/howto_status.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class HowtoStatus(CliKeywordBase):

    def get_keyword_names(self):
        return ['howto_status']

    def howto_status(self):
        """To get the current how to status
        example:
        ${output}=     Howto Status
        """
        return self._cli.howtostatus()
