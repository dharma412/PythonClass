#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/howto_update.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

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
