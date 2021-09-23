#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/howto_update.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class HowtoUpdate(CliKeywordBase):

    def get_keyword_names(self):
        return ['howto_update']

    def howto_update(self):
        """To intiate the howto update
        example:
        ${output}=     Howto Update
        """
        return self._cli.howtoupdate()
