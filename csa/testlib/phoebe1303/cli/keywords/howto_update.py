#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/howto_update.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class HowtoUpdate(CliKeywordBase):

    def get_keyword_names(self):
        return ['howto_update']

    def howto_update(self):
        """To intiate the howto update
        example:
        ${output}=     Howto Update
        """
        return  self._cli.howtoupdate()
